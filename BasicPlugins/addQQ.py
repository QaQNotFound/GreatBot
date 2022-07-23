from nonebot import on_request
from nonebot import on_notice
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11 import FriendRequestEvent,FriendAddNoticeEvent,GroupRequestEvent

#加好友
add_friend = on_request()

@add_friend.handle()
async def add_friend___(bot:Bot,event:FriendRequestEvent):
    await event.approve(bot)

#加群
add_group = on_request()
@add_group.handle()
async def add_group___(bot:Bot,event:GroupRequestEvent):
    await event.approve(bot)


#加好友后发送消息
friend_added = on_notice()
@friend_added.handle()
async def friend_added__(bot:Bot,event:FriendAddNoticeEvent):
    await bot.send(
        event=event,
        message='一起来玩吧！'
    )


#加群后发送消息
group_added = on_notice()
@group_added.handle()
async def group_added__(bot:Bot,event:GroupRequestEvent):
    await bot.send(
        event=event,
        message='一起来玩吧！'
    )