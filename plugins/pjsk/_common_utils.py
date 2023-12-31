import Levenshtein as lev
from datetime import datetime
from typing import Optional, Tuple, Dict, Any
import requests
from PIL import Image, ImageDraw, ImageFont
from configs.path_config import FONT_PATH
from utils.http_utils import AsyncHttpx
from ._config import data_path, ONLY_TOP100_ERROR, suite_path
from utils.imageutils import union
import urllib.parse

from ._errors import apiCallError, QueryBanned, maintenanceIn, userIdBan

try:
    import ujson as json
except:
    import json


# 通用api查询
async def callapi(
        url: str,
        param: Optional[Dict] = None,
        query_type: str = 'unknown',
        is_force_update: bool = False
) -> Dict[str, Any]:
    if param is not None:
        q = urllib.parse.urlencode(param)
        url = url + '?' + q
    # 处理sk和rk的api
    json_path = None
    if r'/event/' in url:
        json_path = data_path / 'sktop100.json'
    elif r'/rank-match-season/' in url:
        json_path = data_path / 'rktop100.json'
    if 'targetRank' in url and json_path:
        targetRank = int(url[url.find('targetRank=') + len('targetRank='):])
        with open(json_path, 'r', encoding='utf-8') as f:
            top100 = json.load(f)
        updatetime = json_path.stat().st_mtime
        for single in top100["rankings"]:
            if single["rank"] == targetRank:
                return {
                    "rankings": [single],
                    'updateTime': datetime.fromtimestamp(updatetime).strftime("%m-%d %H:%M:%S")
                }
        else:
            raise apiCallError(ONLY_TOP100_ERROR)
    elif 'targetUserId' in url and json_path:
        targetUserId = int(url[url.find('targetUserId=') + len('targetUserId='):])
        with open(json_path, 'r', encoding='utf-8') as f:
            jptop100 = json.load(f)
        updatetime = json_path.stat().st_mtime
        for single in jptop100["rankings"]:
            if single["userId"] == targetUserId:
                return {
                    "rankings": [single],
                    'updateTime': datetime.fromtimestamp(updatetime).strftime("%m-%d %H:%M:%S")
                }
        else:
            raise apiCallError(ONLY_TOP100_ERROR)
    # 处理逮捕、b30、profile、进度
    # 逮捕仍然实时查询
    if '/profile' in url and query_type != 'arrest' and not is_force_update:
        userid = url[url.find('user/') + 5:url.find('/profile')]
        # 先尝试取本地结果
        user_suite_file = suite_path / f'{userid}.json'
        if user_suite_file.exists():
            with open(user_suite_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        # 拿不到再访问uni提供的接口
        else:
            api_url = fr'https://suite.unipjsk.com/api/user/{userid}/profile'
            resp = await AsyncHttpx.get(api_url, timeout=4)
            if resp.status_code == 200:
                return resp.json()
            # 两个方式都拿不到数据，并且要查询的数据用于b30、rop、难度排行时
            # 因为没有详细信息所以无法使用
            elif query_type in ['b30', 'rop', 'rank']:
                raise QueryBanned("无法查询到用户信息，可能是没有上传")
    # 处理其他api（profile、逮捕）
    try:
        data = (await AsyncHttpx.get(url, timeout=4)).json()
    except:
        data = requests.get(url).json()
    try:
        if data == {'status': 'maintenance_in'}:
            raise maintenanceIn
        elif data == {'status': 'user_id_ban'}:
            raise userIdBan
        return data
    except:
        raise apiCallError

# 时间戳格式化
def timeremain(time):
    if time < 60:
        return f'{int(time)}秒'
    elif time < 60*60:
        return f'{int(time / 60)}分{int(time % 60)}秒'
    elif time < 60*60*24:
        hours = int(time / 60 / 60)
        remain = time - 3600 * hours
        return f'{int(time / 60 / 60)}小时{int(remain / 60)}分{int(remain % 60)}秒'
    else:
        days = int(time / 3600 / 24)
        remain = time - 3600 * 24 * days
        return f'{int(days)}天{timeremain(remain)}'


# 获取字符串相似度
def string_similar(s1, s2):
    # 使用Levenshtein库计算两个字符串之间的距离
    distance = lev.distance(s1, s2)
    # 计算最大可能的距离
    max_len = max(len(s1), len(s2))
    # 计算相似度，并返回。距离越小，相似度越高，所以我们用1减去它们的比值
    return 1 - (distance / max_len)


# 文字生成图片
def t2i(
    text: str,
    font_size: int = 40,
    font_color: str = "black",
    padding: Optional[Tuple[int, int, int, int]] = (0, 0, 0, 0),
    max_width: Optional[int] = None,
    wrap_type: str = "left",
    line_interval: Optional[int] = None,
) -> Image:
    """
    根据文字生成图片，仅使用思源字体，支持\n换行符的输入
    :param text: 文字内容
    :param font_size: 文字大小
    :param font_color: 文字颜色
    :param padding: 文字边距，参数顺序为上下左右
    :param max_width: 限制的文字宽度，文字超出此宽度自动换行
    :param wrap_type: 换行后文字的对齐方式（左对齐left，居中对齐center，右对齐right）
    :param line_interval: 文字有多行时的行间距，默认为字体大小的1/4
    """
    # 仿照meetwq佬的PIL工具插件imageutils的text2image方法制作的简易版
    # 工具地址(https://github.com/noneplugin/nonebot-plugin-imageutils)
    if wrap_type not in ['left', 'center', 'right']:
        raise TypeError('对齐方式参数错误！')
    lines = text.split('\n')
    if max_width is not None:
        def wrap(line, max_width):
            font = ImageFont.truetype(str(FONT_PATH / 'SourceHanSansCN-Medium.otf'), font_size)
            (_w, _), (_, _) = font.font.getsize(line)
            last_idx = 0
            for idx in range(len(line)):
                (_tmp_w, _), (_, _) = font.font.getsize(line[last_idx: idx+1])
                if _tmp_w > max_width:
                    yield line[last_idx:idx]
                    last_idx = idx
            yield line[last_idx:]
        new_lines = []
        for line in lines:
            l = wrap(line, max_width)
            new_lines.extend(l)
        lines = new_lines
    imgs = []
    width = 0
    height = 0
    line_interval = line_interval if line_interval is not None else font_size//4
    for line in lines:
        font = ImageFont.truetype(str(FONT_PATH / 'SourceHanSansCN-Medium.otf'), font_size)
        (_width, _height), (offset_x, offset_y) = font.font.getsize(line)
        img = Image.new('RGBA', (_width, _height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.text((-offset_x + padding[2], -offset_y + padding[0]), line, font_color, font)
        width = _width if width < _width else width
        height += _height + line_interval
        imgs.append(img)
    height -= line_interval
    size = (width + padding[2] + padding[3], height + padding[0] + padding[1])
    pic = Image.new('RGBA', size, (255, 255, 255, 0))
    _h = 0
    for img in imgs:
        if wrap_type == 'left':
            _w = 0
        elif wrap_type == 'center':
            _w = (width - img.width) // 2
        else:
            _w = width - img.width
        pic.paste(img, (_w, _h), mask=img.split()[-1])
        _h += line_interval + img.height
    return pic


