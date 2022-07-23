from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import Arg,CommandArg,ArgPlainText
import requests
import json
from nonebot.plugin import PluginMetadata

__plugin_meta__=PluginMetadata(
    name="随机一句",
    description="随机一句",
    usage=(
        '一言/一句话'
    ),
    extra={
        'type':'实用功能',
        'version':'0.0.1',
        'author':'QaQNotFound'
    }
)


oneWord = on_command("oneWord",aliases={"一言","一句话"},priority=6)

@oneWord.handle()
async def handle():
    try:
        word = await get_oneWord()
        await oneWord.finish(word)
    except Exception as e:
        await oneWord.send("一言插件出现故障，请联系作者")

async def get_oneWord():
    #调用一言接口获取数据
    url = 'https://v1.hitokoto.cn?encode=json&charset=utf-8'
    result = requests.get(url)
    res_json = result.text
    res_dict = json.loads(res_json)
    res=res_dict['hitokoto']
    word_from = res_dict['from']
    return res+'(出自'+' '+word_from+')'