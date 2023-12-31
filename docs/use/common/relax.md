---
title: 娱乐功能
date: 2023-4-5
---
## 语句抽象化
* 冷却限制 - `5秒/1次/每人`  
* 次数限制 - `10次/1天/每人`  
* 阻塞限制 - `开启`  
* 说明  
    使用抽象表情替换消息中的文字  
* 指令  
    `语句抽象化`/`抽象化`/`抽象`+`[要抽象的语句]`  
## 疯狂星期四
* 冷却限制 - `8秒/1次/每群`  
* 次数限制 - `10次/1天/每人`  
* 说明  
    随机KFC疯狂星期四文案  
* 指令  
    `疯狂星期X`/`狂乱X曜日`  
## 今天吃什么
* 冷却限制 - `5秒/1次/每人`  
* 说明  
    选择恐惧症？让Bot建议你今天吃什么！  
* 指令  
    `@bot`+`今天吃什么` ：问bot恰什么  
    `@bot`+`菜单` ：查看群自定义菜单，管理菜单需要bot群管权限  
* 示例  
    奏宝，今天吃什么  
    小奏，早上吃啥  
    knd，夜宵造点啥  
## 点歌
* 冷却限制 - `10秒/1次/每人`  
* 次数限制 - `30次/1天/每人`  
* 说明  
    在线点歌  
    默认为网易云点歌  
* 指令  
    `点歌`/`qq点歌`/`网易点歌`/`b站点歌`+`[歌名]`  
## 昵称系统
* 说明  
    个人昵称系统，使用违禁昵称会被bot短暂拉黑作为惩罚()  
    每个群每个用户的昵称都互相独立  
* 指令  
    `@bot`+`以后叫我`+`[昵称]`  
    `@bot`+`我是谁`/`我叫什么`  
    `取消昵称`  
## 互动
* 阻塞限制 - `开启`  
* 说明  
    Kanadebot可以对一些关键词做出各种反应，而且说不定有时还会索求你作出一些特定回复的样子噢？  
    这里列出一些常见的关键词(需要艾特)：  
    戳一戳、夸可爱、叫laopo、嗦面、奏门、骂人、今日运势(幸运曲)、一些和奏有关系的sekai角色的名字  
    除此之外，还有一些整活向关键词等等就需要你日常使用时慢慢发掘啦，虽然很少也很难被触发(ˉ▽ˉ；)...  
* 指令  
    `奏宝可爱`/`奏宝骂人`/`奏宝老婆`/`奏宝嗦面`/`奏门`  
* 注意  
    - 部分回复的文案内容与好感度相关, 详见签到功能  
    文案语料库在以极其缓慢的速度更新中  
    - 功能存在的时间已久，部分旧文案可能已经ooc (ﾉω･､)  
    但语料库本身十！分！缺！文！案！而且维护语料库比较麻烦，姑且不修改or删除(*￣3￣)  
    - 有好玩的需要特定回复的词条可以联系管理添加，哦内该 ヾ\(_ _。)  
    master属性all奏all杂食，无需担心会被文案雷到(但会被ooc的文案创到)  
    - 文案内容偏向于还原可爱(目前是占压倒性的主要成分)、亚萨西、怕生、呆萌、容易害羞（下接）  
    体力差、自我谴责、阴郁、作曲脑、音乐宅、完全夜行性、偶尔又会突然很帅气高冷等等等的奏  
    没错，定了个基本完全还原奏的目标，但对于master的水平而言感觉是在挑战不可能  
    所以还请不要太期待master一个人的力量能把奏宝从游戏里带出来(画大饼ing)  
## roll
* 说明  
    随机数字 或 随机选择事件  
* 指令  
    `roll` ：随机 0-100 的数字  
    `roll`+`*[文本]` ：随机从选项中选取一个进行答复  
    `@bot`+`[选项]`+`还是`+`[选项]` ：同上，较人性化的触发方式     
* 示例  
    roll 吃饭 睡觉 打游戏  
    小奏，肝榜还是开摆  
## 签到
* 说明  
    每日签到(不同群好感度数据不共享)  
    不是很懂有多大意义，但和小奏的 随机文本回复 功能有一定关联   
    至少你还可以视好感度增长多少为今日人品的一种体现（嗯！OvO  
* 指令  
    `签到`+`?[all]` ：all代表签到所有群，但不显示签到结果  
    `补签`+`?[all]` ：all代表补签所有群，默认使用全部拥有的补签卡  
    `我的签到/好感度` ：查看群内自己的好感度  
    `好感度排行` ：查看群内好感度排行  
    `好感度总排行`+`?[屏蔽我/显示我]` ：不带参数时，查看所有群好感度排行  
    `设置好感度`+`[数字]` ：将好感度等级固定为某等级(必须低于原等级，设为-1时恢复原等级)(用于触发低等级随机回复文案)  
    `转移好感度数据`/`转移好感`+`[群id]` ：不带群id时，将自己好感度最高的群数据与当前群进行交换; 有参数时，交换指定群号的数据  
* 注意  
    签到时默认有 3% 概率 ×2  
    本功能的金币目前仅能在 '商店' 内使用  
## VITS
* 冷却限制 - `30秒/3次/每群`  
* 阻塞限制 - `开启`  
* 群权限 - `6`  
* 说明  
    使用VITS生成角色语音，因为服务器性能极其有限，故仅有部分开放高权限的群才可以使用  
* 指令  
    `[角色名]`+`说`+`?[中文/日文]`+`[文字]`  
* 举例  
    knd说こんニーゴ ：输出日语语音  
    kanade说日文よくわからない ：输出日语语音  
    小奏说日文我不是很懂 ：会先翻译为日文，再输出日语语音  
    奏宝说中文你好，我是宵崎奏 ：输出协和语语音  
    宵崎奏说中文ども、宵崎奏です ：会先翻译为中文，再输出协和语语音  
* 注意  
    可识别的\[角色名]为目前收录的烧烤原创角色(包括来自\[角色昵称]功能中保存的角色别名)  
    输出语音的语种仅支持中日双语，但无论你输入的\[文字]本身是什么语种，最终生成的语音都会采用你选择的语言，默认为日文  
    （意思就是会预先翻译你输入的文字为你所选择的语言）  
    若语音生成失败，可以检查\[文字]中的符号是否符合对应语种  
    语音模型来自圈内大佬们，详请可参阅：https://github.com/Kanade-nya/PJSK-MultiGUI  
    个人测评，感觉ws全员的效果可能不太好，然后志步的效果基本还挺好的(?)  
    最后，请勿生成以及传播可能导致他人对角色产生严重误解的奇怪语音！  
## 缩写查询/梗百科
* 冷却限制 - `8秒/1次/每人`  
* 说明  
    可以查询缩写话或者梗的原意，小众词汇可能查不到  
    数据来自小鸡词典(已经寄了，所以现在功能只有查缩写)  
* 指令  
    `百科`+`[文本]`   
    `[文本]`+`是什么`/`是啥`/`是谁`  
    `缩写`/`缩写查询`+`[文本]`  