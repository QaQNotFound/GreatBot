# -*- coding: utf-8 -*-
# @Time    : 2022/5/4 18:42
# @Author  : Felix
# @FileName: poke.py
import random
from nonebot import on_notice
from nonebot.adapters.onebot.v11 import GroupMessageEvent,PrivateMessageEvent,\
    FriendRecallNoticeEvent,GroupRecallNoticeEvent,Message,PokeNotifyEvent,\
    LuckyKingNotifyEvent,Bot,Event,MessageSegment
from nonebot.matcher import Matcher
from nonebot.rule import to_me
from random import choice
import re
from nonebot.plugin import PluginMetadata

__plugin_meta__=PluginMetadata(
    name="戳一戳",
    description="戳一戳机器人",
    usage=(
        '双击机器人头像'
    ),
    extra={
        'type':'实用功能',
        'version':'0.0.1',
        'author':'QaQNotFound'
    }
)

poke = on_notice()


@poke.handle()
async def poke_event(match:Matcher,event:PokeNotifyEvent):
    id = str(event.get_user_id)
    pattern = re.compile('user_id=(\d*)')

    # 提取目标qq号
    target_qqnum_str = re.search(pattern,id).group(1)

    #发送戳一戳
    msg = Message('[CQ:poke,qq=%s]' % target_qqnum_str)

    #发送语句
    msg1 = choice([
        "你再戳！",
        "发送命令-帮助 以获取详细功能",
        "别戳啦别戳啦",
        "有什么事吗？",
        "那...那里...那里不能戳...绝对...",
        "(。´・ω・)ん?",
        "?",
        "差不多得了😅",
        "给你一拳",
        "代码写完了没？",
        "项目做完了没？",
        "爬去学习"
    ])

    #使用Random随机抽取数值进行判断
    # try:
    while (poke):
        t = random.random()
        if (t > 0.5):
            await poke.finish(msg)
        else:
            await poke.finish(msg1)
    # except Exception as e:
        # await poke.send("戳一戳插件出现故障，请联系作者")

withdraw = on_notice()
@withdraw.handle()
async def withdraw__(bot:Bot,event:GroupRecallNoticeEvent):
    try:
        if event.operator_id == event.user_id:
            await bot.send(
                event=event,
                message= '我可都看到了哦',
            )
    except Exception as e:
        await withdraw.send('撤回插件出现故障，请联系作者')

redbag = on_notice()
@redbag.handle()
async def redbag__(bot:Bot,event:LuckyKingNotifyEvent):
    try:
        atmessage = MessageSegment.at(event.target_id)
        await bot.send(
            event=event,
            message=atmessage+'恭喜这个比成为运气王，赶紧接力红包'
        )

    except Exception as e:
        await redbag.send("红包插件出现故障，请联系作者")