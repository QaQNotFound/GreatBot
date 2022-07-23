from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import Arg,CommandArg,ArgPlainText
import requests
import json
from nonebot.plugin import PluginMetadata

__plugin_meta__=PluginMetadata(
    name="翻译",
    description="翻译你想翻译的内容，默认中翻英，英翻中",
    usage=(
        '翻译 <你想翻译的内容>'
    ),
    extra={
        'type':'实用功能',
        'version':'0.0.1',
        'author':'QaQNotFound'
    }
)


#定义翻译这个命令
translate = on_command("translate",aliases={"翻译"},priority=4)

@translate.handle()
async def handle_first_receive(matcher:Matcher,args:Message=CommandArg()):
    #提取翻译命令之后要进行翻译的纯文本内容
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("content",args)


@translate.got("content",prompt="请输入你想翻译的内容：")
async def handle_content(content:str=ArgPlainText("content")):
    #若翻译命令后没有内容则进行进一步询问要查询的内容
    try:
        trans_res = await get_trans(content)
        await translate.finish(trans_res)
    except Exception as e:
        await translate.send("翻译插件出现故障，请联系作者")


async def get_trans(content:str):
    #使用翻译接口发送数据并接受返回值发送给查询者
    post_content = content
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    form = {
        'i': post_content,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': '16530356643702',
        'sign': 'c358160babfb203dd4bd5b557c7431c4',
        'lts': '1653035664370',
        'bv': '1744f6d1b31aab2b4895998c6078a934',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }
    result = requests.post(url, data=form)
    result.encoding = "utf-8"
    res_json = result.text
    res_dict = json.loads(res_json)
    trans_res = res_dict[ 'translateResult'][0][0]['tgt']
    return trans_res