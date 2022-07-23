import psutil
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot,Event
from nonebot.adapters.onebot.v11 import GROUP_OWNER,GROUP_ADMIN
from nonebot.plugin import PluginMetadata

__plugin_meta__=PluginMetadata(
    name="获取当前系统状态",
    description="获取当前系统状态",
    usage=(
        'status/系统状态'
    ),
    extra={
        'type':'实用功能',
        'version':'0.0.1',
        'author':'QaQNotFound'
    }
)



#获取cpu状态
def get_cpu_status() -> float:
    return psutil.cpu_percent(interval=1)

#获取内存状态
def get_memory_status() ->float:
    return psutil.virtual_memory().percent


#获取状态指令
status = on_command("状态",aliases={'系统状态','status','state'},priority=3,block=True)
@status.handle()
async def status_(bot:Bot,event:Event):
    #设置权限分类
    if event.get_user_id != str(event.self_id):
        try:
            message = 'CPU占用率:'+str(get_cpu_status())+'%\n'+'内存占用率'+str(get_memory_status())+'%\n'
            if await GROUP_ADMIN(bot,event):
                await bot.send(
                    event=event,
                    message=message
                )
            elif await GROUP_OWNER(bot,event):
                await bot.send(
                    event=event,
                    message=message
                )
            else:
                await bot.send(
                    event=event,
                    message='瞅啥瞅，你没权限查看'
                )
        except Exception as e:
            await bot.send(
                event=event,
                message='系统状态插件出现故障，请联系作者'
            )