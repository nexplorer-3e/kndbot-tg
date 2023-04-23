---
title: 关于Bot
date: 2023-4-5
---
## 关于功能来源
KanadeBot许多已实现的功能魔改自网络上获取的插件，master负责后续的维护更新，插件无法再使用欢迎找master询问，与插件原作者已经无关  
有部分功能完全是master凭兴趣开发并提供使用的，这些插件包括但不限于以下功能
* [烧烤同人图库](/use/common/pjsk.md#烧烤同人图库)
* [互动](/use/common/relax.md#互动)
* roll点、ycm等等...
欢迎对这些功能的改进提出自己的看法
::: tip 提示
如果你对Bot的插件库感兴趣，可以了解一下这些宝藏项目
* [绪山真寻Bot](https://github.com/HibiKier/zhenxun_bot)
* [Nonebot](https://github.com/nonebot/nonebot2)
* [Unibot](https://github.com/watagashi-uni/Unibot)
:::
---
## 关于使用文档中出现的符号、字段说明
+ 在功能的说明文档中，可能会出现以下符号  
`\`或者`/`代表前后两种指令格式均可以识别，效果相同
`+`代表指令后需要接上某些关键参数  
`[ ]`中的说明文字是指令所需要的参数类型  
`[ ]`前面的 `?` 符号，代表此参数可以携带也可以不携带，一般不携带的时候会取参数的默认值  
`[ ]`前面的 `*` 符号，代表此参数可以携带多次，使用空格隔开，一般会在生成带有多段文字的表情包的指令下使用到  
**这些符号出现在指令中只是为了方便作特殊性说明，因此在实际触发指令时你并不需要携带这些符号**
+ 在功能的说明文档中，还可能会出现以下字段，如果没出现，说明字段取默认值  

| 字段   | 说明 | 参数范围 | 默认值 |
|:------:|:--------|:-:|:---:|
| `功能优先级` | 当用户的消息有可能触发多个功能时，优先级越高(数字越小越高)的功能会优先触发  | 1~100 | 5 |
| `群权限` | 功能要求群具备的群聊等级，所有群默认为level 5，更高权限需要找master提升 | -1~6 | 5 |
| `默认开关` | 机器人进到新群时，或者机器人安装了新的功能时，此功能默认的开关状态 | 开启/关闭 | 开启 |
| `用户权限` | 功能要求用户权限具备的权限等级，群聊环境下生效，群管/群主默认为level 5，成员默认为level 0 | 0~7 | 5 |
| `功能类型` | 功能可以触发的聊天环境 | 私聊/群聊/无限制 | 群聊 |
| `冷却限制` | 功能在规定时间内可以使用的次数 | - | 无 |
| `次数限制` | 功能在一天内可以使用的次数  | - |无 |
| `阻塞限制` | 功能在每次使用后陷入阻塞，功能处理完毕后才会再次恢复使用 | - | 无 |

::: tip 提示
如果需要明白各字段在机器人处理消息时的具体流程，可以接着往下阅读
:::
---
## 关于机器人处理消息的流程
KanadeBot在每次处理用户的指令，会按顺序经过以下的判定，任一判定环节不通过，指令便无法触发  
1. 功能可以在当前聊天类型下使用 (聊天类型指：群聊/私聊)
2. 群聊类型下，群不在群黑名单内(群权限高于-1)
3. 群聊类型下，机器人处于`工作`状态(群内可以设置机器人为`工作`/`沉睡`状态)
4. 群聊类型下，用户具有高于使用此功能要求的`用户权限`
5. 群聊类型下，群具有高于使用此功能要求的`群权限`(权限不够会提醒)
6. 群聊类型下，此功能处于`开启`状态(功能没有被群管理或master关闭)
7. 触发命令的用户不在用户黑名单内
8. 对于设置了次数上限机制的功能，功能未到使用次数的上限
9. 对于设置了冷却机制的功能，功能未进入冷却状态
10. 对于设置了阻塞机制的功能，上一次使用此功能时的流程已经完全结束(一般指已经成功返回了消息，否则说明上次功能仍在处理中)
---
## 关于邀请机器人入群
凭借长期以来处理各种拉群事项的经验，邀请入群需要遵守的条款经过了多次更新，目前变成了这个样子 **(看图)**  
<img :src="$withBase('/image/group_invite.png')" alt="拉群条件">

::: tip 提示
这张图你也可以在加机器人好友后发送`入群条件`、`拉群条件`获取
:::
> 目前在活动的KanadeBot
>* 一号机 **2953928559** (自动同意好友申请，但不再处理新群邀请)
>* 二号机 **2488024911** (自动同意好友申请，但不再处理新群邀请)
>* 三号机 **878536923** (自动同意好友申请，但不再处理新群邀请)
>* 四号机 **3630133726** (好友验证填`拉群`会自动同意好友申请，可以处理pjsk群邀请)
::: warning 注意
一、二、三号机暂停加群是因为群过多容易寄 (会被腾讯制裁) ，不过当有群踢出机器人或者群被master清理掉时，自然会再腾出加群的名额
:::
::: danger 警告
如果不符合这张图的规定而进行的拉群行为一般会被master默认忽略，  
master不想解释为什么会有图中这样的规定，因为机器人实际上偏私用，    
并不乐意去加各种各样的群，如果你有能力，可以考虑自行搭建一只类似的机器人
:::
---
## 关于master
- 如果需要联系master，请确保话题与KanadeBot相关，并通过KanadeBot的`滴滴滴`指令联系master，如果是其它话题大概率不会作出回应  
- 被master发现辱骂KanadeBot甚至奏宝本人的人会被永久拉黑，master会不定期统计日志中关于奏的话题(起初只是为了收集奏宝的互动文案)
- 承载Bot的服务器性能很低，如果Bot寄了 **(账号风控不算)**，master会视具体情况处理，可能会主动联系到弄崩溃的人   
**特别对于刷Bot指令做压测、乱发指令拿Bot测Bug的用户，如果不事先联系master取得同意让master可以预防风险的话，master发现后会血压MAX，自然不会对这类用户予以尊重，不要期待master会像平时的 _客服模式_ 一样好声好气地待人**