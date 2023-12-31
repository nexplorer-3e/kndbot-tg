---
title: 群管插件
date: 2023-4-5
---
## 刷屏禁言/拉黑
* 说明  
    刷屏禁言/拉黑相关操作，需要 Bot 有群管理员权限  
    Bot无管理员权限时仅能使用 "限制触发指令频率" 的刷屏拉黑功能  
* 指令  
    设置刷屏禁言参数 \[X] \[T] \[N] \[M] ：一次性设置完所有参数  
    设置刷屏检测类型 \[X] ： 见注意事项, 默认为限制复读频率  
    设置刷屏检测时间 \[T] ： 见注意事项, 默认为60秒  
    设置刷屏检测次数 \[N] ： 见注意事项, 默认为3次  
    设置刷屏禁言时长 \[M] ： 见注意事项, 默认为0分钟(关闭状态)  
    查看刷屏禁言参数 ： 查看当前的刷屏检测设置  
* 效果  
    T 秒内满足刷屏条件 N 次，禁言 M 分钟  
* 注意  
    X的取值有3种：0,1,2  
    \* X=0代表限制复读频率(规定时间内仅记入 '用户同一句话' 的发送次数)  
    \* X=1代表限制群员发言频率(规定时间内计入 '用户任何发言' 的发送次数)  
    \* X=2代表限制触发指令频率(规定时间内计入 '用户任何触发bot指令' 的次数)  
    T的取值范围限制为1~120(秒)  
    N的取值范围限制为2~30(次数)  
    M的取值范围限制为0~43200(分钟)(0为关闭)  
* 示例  
    设置刷屏禁言参数 0 60 3 1 ：群内有人一分钟重复发送同一消息3次，禁言拉黑1分钟  
    设置刷屏禁言参数 1 5 3 1 ：群内有人5秒发消息3次，禁言拉黑1分钟  
    设置刷屏禁言参数 2 30 3 1 ：群内有人30秒触发3次bot的指令，禁言拉黑1分钟  

## 设置群欢迎消息
* 说明  
    能自定义群欢迎消息的功能  
* 指令  
    设置群欢迎消息 ?\[文本] ?\[图片]  
    删除群欢迎消息 ：使群欢迎消息恢复默认  
* 示例  
    设置群欢迎消息 欢迎你\[at]  
* 注意  
    可以通过\[at]来确认是否艾特新成员  

## 群功能开关
* 说明  
    群内通用功能与被动功能开关  
* 指令  
    群被动状态 ：查看群被动状态  
    开启/关闭\[功能名] ：插件开关  
    开启/关闭全部被动 ：群被动功能总开关  
    开启/关闭全部功能 ：群通用功能总开关  
    @bot 起来工作/唤醒 ：让Kanadebot工作  
    @bot 去休息吧/休眠 ：让Kanadebot睡大觉 (此时通用功能与被动功能全部无法使用)  

## 本地图库
* 说明  
    包含删除图片、移动图片的功能
### 删除图片
* 指令  
    删除图片 \[图库] \[id]
* 示例  
    删除图片 美图 666
* 注意  
    中途发送 `取消` 或者 `算了` 可以结束指令
### 移动图片
* 指令  
    移动图片 \[源图库] \[目标图库] \[id]
* 示例  
    移动图片 壁纸 美图 234
* 注意  
    中途发送 `取消` 或者 `算了` 可以结束指令

## 今天吃什么
* 说明  
    管理群菜单
* 指令  
    菜单 ：查看群菜单
    添加菜品 \[菜名] ：添加菜品至群自定义菜单
    移除菜品 \[菜名] ：从菜单移除菜品

## 拉黑用户
* 说明  
    将用户拉入或拉出黑名单
* 指令  
    .ban \[at] ?\[小时] ?\[分钟] ：拉黑某用户
    .unban \[at] ?\[小时] ?\[分钟] ：解禁某用户
* 示例  
    .ban @某用户 ：将用户永久拉黑
    .ban @某用户 6 ：将用户拉黑6小时
    .ban @某用户 2 10 ：将用户拉黑2小时10分钟
    .unban @某用户 ：将用户解禁
## 词条管理
* 说明  
    管理群词条，可以让Bot按自己的想法对特定消息作出回复  
* 注意  
    对指定问题的随机回答，对相同问题可以设置多个不同回答  
    自定义词条优先级低于随机消息回复功能，这可能会导致有些词条无响应  
    自定义词条如果非必要请尽量不要含图片，容易被风控，尤其动图  
    自定义词条含有图片、艾特、qq黄豆表情时，查看、删除词条的指令只能使用下标方式代替问句！  
    删除词条后每个词条的id可能会变化，请查看后再删除  
* 指令  
    添加词条 ?\[模糊/正则]问...答...            :添加问答词条，可重复添加相同问题的不同回答  
    删除词条 \[问题/下标] ?\[下标] ：删除指定问句的指定下标回答或全部回答  
    查看词条 ?\[问题/下标]       ：查看全部词条或对应词条的答句   
* 示例  
    添加词条问谁是奏宝答是我 ：向"谁是奏宝"此问句添加新的答句"是我"  
    添加词条模糊问谁是奏宝答是我 ：同上，但匹配模式为消息中一旦含有此问句都会触发  
    添加词条正则问谁是奏宝答是我 ：同上，但匹配模式为满足正则条件则触发，不懂什么是正则不要去用  
    删除词条 谁是奏宝 ：删除"谁是奏宝"问句的所有答句  
    删除词条 谁是奏宝 0 ：删除"谁是奏宝"问句中下标为0的答句  
    删除词条 id:0 ：删除下标为0的问句的所有答句  
    查看词条 ：查看此群所有的问句以及由bot主设置的全局问句  
    查看词条 谁是奏宝 ：查看问句"谁是奏宝"的所有答句  
    查看词条 id:0 ：查看下标为0的问句的所有答句  
## 更新群组成员列表
* 说明  
    更新群组成员的基本信息  
* 指令  
    更新群组成员列表/更新群组成员/更新群成员  
* 效果  
    让bot更新变化的群成员信息，用于bot没有检测到群员人数变化、权限变化等的情况下  
    比如说bot掉线or关机的情况下群成员发生变化时  
    一般不需要使用，总之会自己更新