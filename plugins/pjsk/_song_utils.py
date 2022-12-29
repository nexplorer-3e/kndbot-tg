import re
import datetime
import time
import pytz
import yaml
from typing import Tuple
from mutagen.mp3 import MP3
from PIL import Image, ImageDraw, ImageFont
from services import logger
from utils.http_utils import AsyncHttpx
from utils.imageutils import pic2b64
from configs.path_config import FONT_PATH
from ._autoask import pjsk_update_manager
from ._common_utils import string_similar
from ._config import data_path
from ._models import MusicInfo, PjskSongsAlias

try:
    import ujson as json
except:
    import json
import os




# 更新从uniapi获取的歌曲alias
async def save_songs_data(song_id: int):
    url = f'https://api.unipjsk.com/getalias2/{song_id}'
    song_list = (await AsyncHttpx.get(url)).json()
    for song in song_list:
        if await PjskSongsAlias.add_alias(
            song_id, song['alias'], 114514, 114514, datetime.datetime.now(), True
        ):
            logger.info(f"更新歌曲id:{song_id}别称({song['alias']})成功")

    
# 模糊搜索曲名的具体函数
def _matchname(alias):
    match = {'match': 0, 'musicId': 0, 'status': 'false', 'title': '', 'translate': ''}
    with open(data_path / 'realtime/musics.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(data_path / 'translate.yaml', encoding='utf-8') as f:
        trans = yaml.load(f, Loader=yaml.FullLoader)['music_titles']

    for musics in data:
        name = musics['title']
        similar = string_similar(alias.lower(), name.lower())
        if similar > match['match']:
            match['match'] = similar
            match['musicId'] = musics['id']
            match['title'] = musics['title']
        try:
            translate = trans[musics['id']]
            if '/' in translate:
                alltrans = translate.split('/')
                for i in alltrans:
                    similar = string_similar(alias.lower(), i.lower())
                    if similar > match['match']:
                        match['match'] = similar
                        match['musicId'] = musics['id']
                        match['title'] = musics['title']
            else:
                similar = string_similar(alias.lower(), translate.lower())
                if similar > match['match']:
                    match['match'] = similar
                    match['musicId'] = musics['id']
                    match['title'] = musics['title']
        except KeyError:
            pass
    try:
        match['translate'] = trans[match['musicId']]
        if match['translate'] == match['title']:
            match['translate'] = ''
    except KeyError:
        match['translate'] = ''
    if match['match'] > 0:
        match['status'] = 'success'
    return match


# 准确/模糊搜索曲名
async def get_songs_data(alias: str, isfuzzy: bool = False):
    sid = await PjskSongsAlias.query_sid(alias)
    if sid:
        with open(data_path / 'realtime/musics.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        for musics in data:
            if musics['id'] == sid:
                name = musics['title']
                break
        else:
            name = ''
        with open(data_path / 'translate.yaml', encoding='utf-8') as f:
            trans = yaml.load(f, Loader=yaml.FullLoader)['music_titles']
        try:
            translate = trans[sid]
            if translate == name:
                translate = ''
        except KeyError:
            translate = ''
        return {'match': 1, 'musicId': sid, 'status': 'success', 'title': name, 'translate': translate}
    elif isfuzzy:
        return _matchname(alias)
    else:
        return {"match": 0, "musicId": 0, "status": "false", "title": "", "translate": ""}


# 获取歌曲演奏者信息
def _vocalimg(musicid):
    with open(data_path / 'musicVocals.json', 'r', encoding='utf-8') as f:
        musicVocals = json.load(f)
    with open(data_path / 'outsideCharacters.json', 'r', encoding='utf-8') as f:
        outsideCharacters = json.load(f)
    pos = 20
    row = 0
    height = [20, 92, 164, 236, 308]
    cut = [0, 0]
    vs = 0
    sekai = 0
    noan = True

    for vocal in musicVocals:
        if vocal['musicId'] == musicid:
            if vocal['musicVocalType'] == "original_song":
                vs += 1
            elif vocal['musicVocalType'] == "sekai":
                sekai += 1
            elif vocal['musicVocalType'] == "virtual_singer":
                vs += 1
            elif vocal['musicVocalType'] == "instrumental":
                img = Image.open(data_path / 'pics/inst.png')
                return img
            else:
                noan = False
                break
    if vs > 1:
        noan = False

    if noan:
        font_style = ImageFont.truetype(str(FONT_PATH / r"SourceHanSansCN-Bold.otf"), 35)
        img = Image.open(data_path / 'pics/vocal.png')
        if vs == 0:
            draw = ImageDraw.Draw(img)
            draw.text((220, 102), 'SEKAI Ver. ONLY', fill=(227, 246, 251), font=font_style)
        if sekai == 0:
            draw = ImageDraw.Draw(img)
            draw.text((165, 257), 'Virtual Singer Ver. ONLY', fill=(227, 246, 251), font=font_style)
        for vocal in musicVocals:
            if vocal['musicId'] == musicid:
                vocalimg = Image.new('RGBA', (750, 85), color=(0, 0, 0, 0))
                draw = ImageDraw.Draw(vocalimg)
                innerpos = 0
                for chara in vocal['characters']:
                    if chara['characterType'] == 'game_character':
                        chara = Image.open(
                            data_path / f'chara/chr_ts_{chara["characterId"]}.png'
                        ).resize((70, 70))
                        r, g, b, mask = chara.split()
                        vocalimg.paste(chara, (innerpos + 5, 8), mask)
                        innerpos += 80
                    else:
                        try:
                            chara = Image.open(
                                data_path / f'chara/outsideCharacters/{chara["characterId"]}.png'
                            ).resize((70, 70))
                            r, g, b, mask = chara.split()
                            vocalimg.paste(chara, (innerpos + 5, 8), mask)
                            innerpos += 80
                        except:
                            for i in outsideCharacters:
                                if i['id'] == chara['characterId']:
                                    draw.text((innerpos + 8, 20), i['name'], fill=(67, 70, 101), font=font_style)
                                    innerpos += 8 + font_style.getsize(str(i['name']))[0]
                vocalimg = vocalimg.crop((0, 0, innerpos + 15, 150))
                r, g, b, mask = vocalimg.split()
                if vocal['musicVocalType'] == "original_song" or vocal['musicVocalType'] == "virtual_singer":
                    img.paste(vocalimg, (370 - int(vocalimg.size[0] / 2), 162 - int(vocalimg.size[1] / 2)), mask)
                elif vocal['musicVocalType'] == "sekai":
                    img.paste(vocalimg, (370 - int(vocalimg.size[0] / 2), 317 - int(vocalimg.size[1] / 2)), mask)
    else:
        font_style = ImageFont.truetype(str(FONT_PATH / r"SourceHanSansCN-Bold.otf"), 27)
        img = Image.new('RGBA', (720, 380), color=(0, 0, 0, 0))
        for vocal in musicVocals:
            if vocal['musicId'] == musicid:
                vocalimg = Image.new('RGBA', (700, 70), color=(0, 0, 0, 0))
                draw = ImageDraw.Draw(vocalimg)
                if vocal['musicVocalType'] == "original_song":
                    text = '原曲版'
                elif vocal['musicVocalType'] == "sekai":
                    text = 'SEKAI版'
                elif vocal['musicVocalType'] == "virtual_singer":
                    text = 'V版'
                elif vocal['musicVocalType'] == "april_fool_2022":
                    text = '2022愚人节版'
                elif vocal['musicVocalType'] == "another_vocal":
                    text = '其他'
                elif vocal['musicVocalType'] == "instrumental":
                    text = '无人声伴奏'
                else:
                    text = vocal['musicVocalType']
                innerpos = 25 + font_style.getsize(str(text))[0]
                draw.text((20, 20), text, fill=(67, 70, 101), font=font_style)
                for chara in vocal['characters']:
                    if chara['characterType'] == 'game_character':
                        chara = Image.open(data_path / f'chara/chr_ts_{chara["characterId"]}.png').resize((60, 60))
                        r, g, b, mask = chara.split()
                        vocalimg.paste(chara, (innerpos + 5, 8), mask)
                        innerpos += 65
                    else:
                        try:
                            chara = Image.open(data_path / f'chara/outsideCharacters/{chara["characterId"]}.png').resize((60, 60))
                            r, g, b, mask = chara.split()
                            vocalimg.paste(chara, (innerpos + 5, 8), mask)
                            innerpos += 65
                        except:
                            for i in outsideCharacters:
                                if i['id'] == chara['characterId']:
                                    draw.text((innerpos + 8, 20), i['name'], fill=(67, 70, 101), font=font_style)
                                    innerpos += 8 + font_style.getsize(str(i['name']))[0]
                vocalimg = vocalimg.crop((0, 0, innerpos + 15, 72))
                r, g, b, mask = vocalimg.split()

                if pos + vocalimg.size[0] > 720:
                    pos = 20
                    row += 1
                img.paste(vocalimg, (pos, height[row]), mask)
                if pos + vocalimg.size[0] > cut[0]:
                    cut[0] = pos + vocalimg.size[0]
                pos += vocalimg.size[0]
                if (vocal['musicVocalType'] == "sekai" or vocal['musicVocalType'] == "original_song"
                    or vocal['musicVocalType'] == "virtual_singer") and pos != 20:
                    pos = 20
                    row += 1
        if pos == 20:
            row -= 1
        cut[1] = height[row] + 65
        img = img.crop((0, 0, cut[0] + 10, cut[1] + 10))
    return img


# 获取歌曲长度，调用mutagen
async def _musiclength(musicid, fillerSec=0):
    try:
        # print('开始获取歌曲长度')
        with open(data_path / r'musicVocals.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        # print('开始读取歌曲长度')
        for vocal in data:
            if vocal['musicId'] == musicid:
                path = f'ondemand/music/long/{vocal["assetbundleName"]}'
                file = f'{vocal["assetbundleName"]}.mp3'
                await pjsk_update_manager.update_jp_assets(path, file, True)
                # print('下载资源完毕')
                audio = MP3(rf'{data_path / path / file}')
                # print('歌曲信息：', audio.info)
                # print(f'得到歌曲长度：{audio.info.length - fillerSec}')
                return audio.info.length - fillerSec
        return 0
    except Exception as e:
        logger.warning(f'获取歌曲长度失败，Error：{e}')
        return 0


# 获取歌曲pjskinfo的具体函数
async def _drawpjskinfo(musicid: int) -> Tuple[bool, str]:
    info = MusicInfo()
    with open(data_path / r'realtime/musics.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for music in data:
        if music['id'] == musicid:
            info.title = music['title']
            info.lyricist = music['lyricist']
            info.composer = music['composer']
            info.arranger = music['arranger']
            info.publishedAt = music['publishedAt']
            info.fillerSec = music['fillerSec']
            try:
                info.hot = music['hot']
                info.hotAdjust = music['hotAdjust']
            except KeyError:
                pass
            break

    with open(data_path / r'realtime/musicDifficulties.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for i in range(0, len(data)):
        if data[i]['musicId'] == musicid:
            info.playLevel = [data[i]['playLevel'], data[i + 1]['playLevel'],
                              data[i + 2]['playLevel'], data[i + 3]['playLevel'], data[i + 4]['playLevel']]
            info.noteCount = [data[i]['totalNoteCount'], data[i + 1]['totalNoteCount'],
                              data[i + 2]['totalNoteCount'], data[i + 3]['totalNoteCount'], data[i + 4]['totalNoteCount']]
            try:
                info.playLevelAdjust = [data[i]['playLevelAdjust'], data[i + 1]['playLevelAdjust'],
                                        data[i + 2]['playLevelAdjust'], data[i + 3]['playLevelAdjust'],
                                        data[i + 4]['playLevelAdjust']]
                info.fullComboAdjust = [data[i]['fullComboAdjust'], data[i + 1]['fullComboAdjust'],
                                        data[i + 2]['fullComboAdjust'], data[i + 3]['fullComboAdjust'],
                                        data[i + 4]['fullComboAdjust']]
                info.fullPerfectAdjust = [data[i]['fullPerfectAdjust'], data[i + 1]['fullPerfectAdjust'],
                                          data[i + 2]['fullPerfectAdjust'], data[i + 3]['fullPerfectAdjust'],
                                          data[i + 4]['fullPerfectAdjust']]
            except KeyError:
                pass
            break
    now = int(time.time() * 1000)
    leak = False
    if now < info.publishedAt:
        img = Image.open(data_path / r'pics/leak.png')
        leak = True
    else:
        if info.playLevelAdjust[0] == 0:
            img = Image.open(data_path / r'pics/pjskinfonew.png')
        else:
            img = Image.open(data_path / r'pics/pjskinfo.png')
    try:
        jacket = await pjsk_update_manager.get_asset(
            fr'startapp/music/jacket/jacket_s_{str(musicid).zfill(3)}',
            f'jacket_s_{str(musicid).zfill(3)}.png'
        )
        jacket = jacket.resize((650, 650))
        img.paste(jacket, (80, 47))
    except FileNotFoundError:
        pass

    if len(info.title) < 12:
        size = 90
        font_style = ImageFont.truetype(str(FONT_PATH / r"KOZGOPRO-BOLD.OTF"), size)
        highplus = 0
    else:
        size = int(90 - (len(info.title) - 12) * 4.5)
        font_style = ImageFont.truetype(str(FONT_PATH / r"KOZGOPRO-BOLD.OTF"), size)
        text_width = font_style.getsize(info.title)
        if text_width[1] != 90:
            highplus = (90 - text_width[1]) / 2
        else:
            highplus = 0
    draw = ImageDraw.Draw(img)
    # 标题
    draw.text((760, 100 + highplus), info.title, fill=(1, 255, 221), font=font_style)
    # 作词作曲编曲
    font_style = ImageFont.truetype(str(FONT_PATH / r"KOZGOPRO-BOLD.OTF"), 40)
    draw.text((930, 268), info.lyricist, fill=(255, 255, 255), font=font_style)
    draw.text((930, 350), info.composer, fill=(255, 255, 255), font=font_style)
    draw.text((930, 430), info.arranger, fill=(255, 255, 255), font=font_style)
    # 长度(需要mutagen.mp3)
    info.length = await _musiclength(musicid, info.fillerSec)
    if info.length:
        length = f'{round(info.length, 1)}秒 ({int(info.length / 60)}分{round(info.length - int(info.length / 60) * 60, 1)}秒)'
    else:
        length = 'No data'
    draw.text((928, 514), length, fill=(255, 255, 255), font=font_style)
    # 上线时间
    if info.publishedAt < 1601438400000:
        info.publishedAt = 1601438400000
    uptime = datetime.datetime.fromtimestamp(
        info.publishedAt / 1000, pytz.timezone('Asia/Shanghai')
    ).strftime('%Y/%m/%d %H:%M:%S (UTC+8)')
    draw.text((930, 593), uptime, fill=(255, 255, 255), font=font_style)

    # 难度
    font_style = ImageFont.truetype(str(FONT_PATH / r"SourceHanSansCN-Bold.otf"), 60)
    for i in range(0, 5):
        text_width = font_style.getsize(str(info.playLevel[i]))
        text_coordinate = (int((132 + 138 * i) - text_width[0] / 2), int(873 - text_width[1] / 2))
        draw.text(text_coordinate, str(info.playLevel[i]), fill=(1, 255, 221), font=font_style)
    font_style = ImageFont.truetype(str(FONT_PATH / r"SourceHanSansCN-Bold.otf"), 45)
    for i in range(0, 5):
        text_width = font_style.getsize(str(info.noteCount[i]))
        text_coordinate = (int((132 + 138 * i) - text_width[0] / 2), int(960 - text_width[1] / 2))
        draw.text(text_coordinate, str(info.noteCount[i]), fill=(67, 70, 101), font=font_style)

    if info.playLevelAdjust[0] != 0:

        if info.hotAdjust > 0.5:
            hotpic = Image.open(data_path / r'pics/hot.png')
        elif info.hotAdjust > 0:
            hotpic = Image.open(data_path / r'pics/hot3.png')
        elif info.hotAdjust > -1:
            hotpic = Image.open(data_path / r'pics/hot2.png')
        elif info.hotAdjust > -2:
            hotpic = Image.open(data_path / r'pics/hot1.png')
        else:
            hotpic = Image.open(data_path / r'pics/hot0.png')

        if info.hot == 0:
            hot = '最新最热'
            hotpic = Image.open(data_path / r'pics/new.png')
        else:
            hot = str(round(info.hot))

        hotpic = hotpic.resize((48, 48))
        r, g, b, mask = hotpic.split()
        font_style = ImageFont.truetype(str(FONT_PATH / r"SourceHanSansCN-Bold.otf"), 28)
        text_width = font_style.getsize(str(hot))
        text_coordinate = (int(1760 - text_width[0]), int(805 - text_width[1] / 2))
        draw.text(text_coordinate, hot, fill=(67, 70, 101), font=font_style)
        if info.hotAdjust > 0.5:
            if info.hotAdjust > 2:
                text_coordinate = (int(1720 + text_width[0] / 2), int(802 - text_width[1] / 2))
                img.paste(hotpic, text_coordinate, mask)
                text_coordinate = (int(1755 + text_width[0] / 2), int(802 - text_width[1] / 2))
                img.paste(hotpic, text_coordinate, mask)
                text_coordinate = (int(1790 + text_width[0] / 2), int(802 - text_width[1] / 2))
                img.paste(hotpic, text_coordinate, mask)
            elif info.hotAdjust > 1:
                text_coordinate = (int(1745 + text_width[0] / 2), int(802 - text_width[1] / 2))
                img.paste(hotpic, text_coordinate, mask)
                text_coordinate = (int(1785 + text_width[0] / 2), int(802 - text_width[1] / 2))
                img.paste(hotpic, text_coordinate, mask)
            else:
                text_coordinate = (int(1755 + text_width[0] / 2), int(802 - text_width[1] / 2))
                img.paste(hotpic, text_coordinate, mask)
        else:
            text_coordinate = (int(1755 + text_width[0] / 2), int(802 - text_width[1] / 2))
            img.paste(hotpic, text_coordinate, mask)

        for i in range(3, 5):
            levelplus = str(round(info.playLevel[i] + info.playLevelAdjust[i], 1))
            fclevelplus = str(round(info.playLevel[i] + info.fullComboAdjust[i], 1))
            aplevelplus = str(round(info.playLevel[i] + info.fullPerfectAdjust[i], 1))

            text_width = font_style.getsize(str(levelplus))
            text_coordinate = (int(1363 + 116 * i - text_width[0] / 2), int(864 - text_width[1] / 2))
            draw.text(text_coordinate, levelplus, fill=(67, 70, 101), font=font_style)

            text_width = font_style.getsize(str(fclevelplus))
            text_coordinate = (int(1363 + 116 * i - text_width[0] / 2), int(922 - text_width[1] / 2))
            draw.text(text_coordinate, fclevelplus, fill=(67, 70, 101), font=font_style)

            text_width = font_style.getsize(str(aplevelplus))
            text_coordinate = (int(1363 + 116 * i - text_width[0] / 2), int(980 - text_width[1] / 2))
            draw.text(text_coordinate, aplevelplus, fill=(67, 70, 101), font=font_style)

        font_style = ImageFont.truetype(str(FONT_PATH / r"SourceHanSansCN-Bold.otf"), 20)
        for i in range(0, 5):
            if info.playLevelAdjust[i] > 1.5:
                adjust = "++"
            elif info.playLevelAdjust[i] > 0.5:
                adjust = "+"
            elif info.playLevelAdjust[i] < -1.5:
                adjust = "--"
            elif info.playLevelAdjust[i] < -0.5:
                adjust = "-"
            else:
                adjust = ""
            if adjust != "":
                text_width = font_style.getsize(str(adjust))
                text_coordinate = (int((132 + 138 * i) - text_width[0] / 2), int(915 - text_width[1] / 2))
                draw.text(text_coordinate, str(adjust), fill=(1, 255, 221), font=font_style)
    vocals = _vocalimg(musicid)
    r, g, b, mask = vocals.split()
    if vocals.size[1] < 320:
        img.paste(vocals, (758, 710), mask)
    else:
        img.paste(vocals, (758, 670), mask)
    save_path = data_path / f'pjskinfo'
    if not save_path.exists():
        save_path.mkdir(parents=True, exist_ok=True)
    img.save(save_path / f'pjskinfo_{musicid}.png')
    return leak, pic2b64(img)


# 获取歌曲pjskinfo
async def info(musicid) -> Tuple[bool, str]:
    path = data_path / f'pjskinfo/pjskinfo_{musicid}.png'
    if path.exists():
        pjskinfotime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        playdatatime = datetime.datetime.fromtimestamp(os.path.getmtime(data_path / 'realtime/musics.json'))
        with open(data_path / 'realtime/musics.json', 'r', encoding='utf-8') as f:
            musics = json.load(f)
        for i in musics:
            if i['id'] == musicid:
                publishedAt = i['publishedAt'] / 1000
                break
        else:
            raise IndexError('找不到对应曲目')
        if pjskinfotime > playdatatime:  # 缓存后数据未变化
            if time.time() < publishedAt:  # 偷跑
                return True, ""
            else:  # 已上线
                if pjskinfotime.timestamp() < publishedAt:  # 缓存是上线前的
                    return await _drawpjskinfo(musicid)
                return False, ""
        else:
            return await _drawpjskinfo(musicid)
    else:
        return await _drawpjskinfo(musicid)


# 获取歌曲bpm
async def parse_bpm(music_id):
    try:
        await pjsk_update_manager.update_jp_assets(rf'startapp/music/music_score/{music_id:04d}_01', 'expert')

        with open(
            data_path / rf'startapp/music/music_score/{music_id:04d}_01/expert', encoding='utf-8'
        ) as f:
            r = f.read()
    except FileNotFoundError:
        return 0, [{'time': 0.0, 'bpm': '无数据'}], 0

    score = {}
    max_time = 0
    for line in r.split('\n'):
        match: re.Match = re.match(r'#(...)(...?)\s*\:\s*(\S*)', line)
        if match:
            time, key, value = match.groups()
            score[(time, key)] = value
            if time.isdigit():
                max_time = max(max_time, int(time) + 1)

    bpm_palette = {}
    for time, key in score:
        if time == 'BPM':
            bpm_palette[key] = float(score[(time, key)])

    bpm_events = {}
    for time, key in score:
        if time.isdigit() and key == '08':
            value = score[(time, key)]
            length = len(value) // 2

            for i in range(length):
                bpm_key = value[i * 2:(i + 1) * 2]
                if bpm_key == '00':
                    continue
                bpm = bpm_palette[bpm_key]
                t = int(time) + i / length
                bpm_events[t] = bpm

    bpm_sequence = [{
        'time': time,
        'bpm': bpm,
    } for time, bpm in sorted(bpm_events.items())]

    for i in range(len(bpm_sequence)):
        if i > 0 and bpm_sequence[i]['bpm'] == bpm_sequence[i - 1]['bpm']:
            bpm_sequence[i]['deleted'] = True

    bpm_sequence = [bpm_event for bpm_event in bpm_sequence if bpm_event.get('deleted') != True]

    bpms = {}
    for i in range(len(bpm_sequence)):
        bpm = bpm_sequence[i]['bpm']
        if bpm not in bpms:
            bpms[bpm] = 0.0

        if i + 1 < len(bpm_sequence):
            bpms[bpm] += (bpm_sequence[i + 1]['time'] - bpm_sequence[i]['time']) / bpm
        else:
            bpms[bpm] += (max_time - bpm_sequence[i]['time']) / bpm

    sorted_bpms = sorted([(bpms[bpm], bpm) for bpm in bpms], reverse=True)
    mean_bpm = sorted_bpms[0][1]

    return mean_bpm, bpm_sequence, max_time


# 获取歌曲标题
def idtoname(musicid):
    with open(data_path / 'realtime/musics.json', 'r', encoding='utf-8') as f:
        musics = json.load(f)
    for i in musics:
        if i['id'] == musicid:
            return i['title']
    return ""
