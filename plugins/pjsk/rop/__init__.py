import base64
import time
from io import BytesIO
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, Message
from PIL import Image, ImageFont, ImageDraw
from nonebot.params import CommandArg
from configs.path_config import FONT_PATH
from utils.message_builder import image
from .._autoask import pjsk_update_manager
from .._errors import pjskError
from .._song_utils import jinduChart
from .._utils import get_userid_preprocess
from .._models import UserProfile
from .._config import data_path, NOT_IMAGE_ERROR, suite_path, BUG_ERROR

try:
    import ujson as json
except:
    import json

__plugin_name__ = "烧烤进度/pjsk进度"
__plugin_type__ = "烧烤相关&uni移植"
__plugin_version__ = 0.1
__plugin_usage__ = f"""
usage：
    查询烧烤收歌进度
    移植自unibot(一款功能型烧烤bot)
    若群内已有unibot请勿开启此bot该功能
    私聊可用，限制每人1分钟只能查询2次

    默认难度为master，若带参数ex、expert可以查询expert谱面收歌进度
    指令：
        烧烤进度/pjsk进度/pjskrop       ?[ex,ma]       :查看自己的收歌进度
        烧烤进度/pjsk进度/pjskrop @qq   ?[ex,ma]       :查看艾特用户的收歌进度(对方必须已绑定烧烤账户)
        烧烤进度/pjsk进度/pjskrop 烧烤id ?[ex,ma]       :查看对应烧烤账号的收歌进度
    数据来源：
        pjsekai.moe
        unipjsk.com
""".strip()
__plugin_settings__ = {
    "default_status": False,
    "cmd": ["pjsk进度", "烧烤进度", "烧烤相关"],
}
__plugin_cd_limit__ = {"cd": 60, "count_limit": 2, "rst": "别急，等[cd]秒后再用！", "limit_type": "user"}
__plugin_block_limit__ = {"rst": "别急，还在查！"}

# pjsk进度
pjsk_progress = on_command('pjsk进度', aliases={'pjskrop', "烧烤进度"}, priority=5, block=True)


@pjsk_progress.handle()
async def _(event: MessageEvent, msg: Message = CommandArg()):
    # 参数解析
    arg = msg.extract_plain_text().strip()
    if 'ex' in arg.lower() or 'expert' in arg.lower():
        diff = 'expert'
    else:
        diff = 'master'
    state = await get_userid_preprocess(event, msg)
    if reply := state['error']:
        await pjsk_progress.finish(reply, at_sender=True)
    userid = state['userid']
    isprivate = state['private']
    # 用户信息
    profile = UserProfile()
    try:
        await profile.getprofile(userid, 'rop')
    except pjskError as e :
        await pjsk_progress.finish(str(e))
    except:
        await pjsk_progress.finish(BUG_ERROR)
    await pjsk_progress.send("收到", at_sender=True)
    # 生成图片
    id = '保密' if isprivate else userid
    if diff == 'master':
        img = Image.open(data_path / 'pics/bgmaster.png')
    else:
        img = Image.open(data_path / 'pics/bgexpert.png')
    with open(data_path / 'cards.json', 'r', encoding='utf-8') as f:
        cards = json.load(f)
    try:
        assetbundleName = ''
        for i in cards:
            if i['id'] == profile.userDecks[0]:
                assetbundleName = i['assetbundleName']
        if profile.special_training[0]:
            cardimg = await pjsk_update_manager.get_asset(
                r'startapp/thumbnail/chara', rf'{assetbundleName}_after_training.png'
            )
        else:
            cardimg = await pjsk_update_manager.get_asset(
                r'startapp/thumbnail/chara', rf'{assetbundleName}_normal.png'
            )
        cardimg = cardimg.resize((117, 117))
        r, g, b, mask = cardimg.split()
        img.paste(cardimg, (67, 57), mask)
    except FileNotFoundError:
        pass
    except AttributeError:
        await pjsk_progress.send(NOT_IMAGE_ERROR)
    draw = ImageDraw.Draw(img)
    font_style = ImageFont.truetype(str(FONT_PATH / "SourceHanSansCN-Bold.otf"), 31)
    draw.text((216, 55), profile.name, fill=(0, 0, 0), font=font_style)
    font_style = ImageFont.truetype(str(FONT_PATH / "FOT-RodinNTLGPro-DB.ttf"), 15)
    draw.text((216, 105), f'id:{id}', fill=(0, 0, 0), font=font_style)
    font_style = ImageFont.truetype(str(FONT_PATH / "FOT-RodinNTLGPro-DB.ttf"), 26)
    draw.text((314, 138), str(profile.rank), fill=(255, 255, 255), font=font_style)
    font_style = ImageFont.truetype(str(FONT_PATH / "SourceHanSansCN-Bold.otf"), 35)
    if diff == 'master':
        levelmin = 26
    else:
        levelmin = 21
        profile.masterscore = profile.expertscore
    for i in range(0, 5):
        text_width = font_style.getsize(str(profile.masterscore[i + levelmin][0]))
        text_coordinate = (int(183 - text_width[0] / 2), int(295 + 97 * i - text_width[1] / 2))
        draw.text(text_coordinate, str(profile.masterscore[i + levelmin][0]), fill=(228, 159, 251), font=font_style)

        text_width = font_style.getsize(str(profile.masterscore[i + levelmin][1]))
        text_coordinate = (int(183 + 78 - text_width[0] / 2), int(295 + 97 * i - text_width[1] / 2))
        draw.text(text_coordinate, str(profile.masterscore[i + levelmin][1]), fill=(254, 143, 249), font=font_style)

        text_width = font_style.getsize(str(profile.masterscore[i + levelmin][2]))
        text_coordinate = (int(183 + 2 * 78 - text_width[0] / 2), int(295 + 97 * i - text_width[1] / 2))
        draw.text(text_coordinate, str(profile.masterscore[i + levelmin][2]), fill=(255, 227, 113), font=font_style)

        text_width = font_style.getsize(str(profile.masterscore[i + levelmin][3]))
        text_coordinate = (int(183 + 3 * 78 - text_width[0] / 2), int(295 + 97 * i - text_width[1] / 2))
        draw.text(text_coordinate, str(profile.masterscore[i + levelmin][3]), fill=(108, 237, 226), font=font_style)

    if diff == 'master':
        secondRawCount = 7
    else:
        secondRawCount = 6
    for i in range(0, secondRawCount):
        text_width = font_style.getsize(str(profile.masterscore[i + levelmin + 5][0]))
        text_coordinate = (int(683 - text_width[0] / 2), int(300 + 96.4 * i - text_width[1] / 2))
        draw.text(text_coordinate, str(profile.masterscore[i + levelmin + 5][0]), fill=(228, 159, 251), font=font_style)

        text_width = font_style.getsize(str(profile.masterscore[i + levelmin + 5][1]))
        text_coordinate = (int(683 + 78 - text_width[0] / 2), int(300 + 96.4 * i - text_width[1] / 2))
        draw.text(text_coordinate, str(profile.masterscore[i + levelmin + 5][1]), fill=(254, 143, 249), font=font_style)

        text_width = font_style.getsize(str(profile.masterscore[i + levelmin + 5][2]))
        text_coordinate = (int(683 + 2 * 78 - text_width[0] / 2), int(300 + 96.4 * i - text_width[1] / 2))
        draw.text(text_coordinate, str(profile.masterscore[i + levelmin + 5][2]), fill=(255, 227, 113), font=font_style)

        text_width = font_style.getsize(str(profile.masterscore[i + levelmin + 5][3]))
        text_coordinate = (int(683 + 3 * 78 - text_width[0] / 2), int(300 + 96.4 * i - text_width[1] / 2))
        draw.text(text_coordinate, str(profile.masterscore[i + levelmin + 5][3]), fill=(108, 237, 226), font=font_style)
    chart = jinduChart(profile.masterscore)
    img.paste(chart, (15, 732), chart.split()[-1])
    # 上传时间
    if not profile.isNewData:
        font_style = ImageFont.truetype(str(FONT_PATH / "SourceHanSansCN-Bold.otf"), 25)
        updatetime = time.localtime(profile.updatedAt // 1000)
        draw.text(
            (68, 10), '数据更新于：' + time.strftime("%Y-%m-%d %H:%M:%S", updatetime),
            fill=(100, 100, 100), font=font_style
        )
    # 发送图片
    buf = BytesIO()
    img.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getvalue()).decode()
    await pjsk_progress.finish(image(b64=base64_str))
