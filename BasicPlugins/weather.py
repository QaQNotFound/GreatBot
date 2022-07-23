from nonebot import on_command
# from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import Arg,CommandArg,ArgPlainText
import requests,urllib
from urllib import parse
from nonebot.plugin import PluginMetadata

__plugin_meta__=PluginMetadata(
    name="当前天气查询",
    description="查询任意城市的当前天气",
    usage=(
        '天气 <你想查询的城市>'
    ),
    extra={
        'type':'实用功能',
        'version':'0.0.1',
        'author':'QaQNotFound'
    }
)


#定义天气查询这个命令
weather = on_command("weather",aliases={"天气","查天气"},priority=5)


@weather.handle()
async def handle_first_receive(matcher:Matcher,args:Message=CommandArg()):
    #提取命令词后的纯文本数据
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("city",args)


@weather.got("city",prompt="你想查询哪个城市的天气?")
async def handle_city(city:Message=Arg(),city_name:str = ArgPlainText("city")):
    #若命令词后没有数据，则进行询问要查询的数据
    try:
        city_weather = await get_weather(city_name)
        await weather.finish(city_weather)
    except Exception as e:
        await weather.send("当前天气插件出现故障，请联系作者")



async def get_weather(city:str):
    #调用免费的天气接口进行简单信息的查询
    cityname = city
    url = "https://yiketianqi.com/api?appid=95811249&appsecret=Tge8lsGs&unescape=1&version=v6&city=%s" % urllib.parse.quote(
        cityname)
    result = requests.get(url=url, timeout=5).json()
    time = "天气更新时间:" + result['update_time']
    wea = "当前天气:" + result['wea']
    city_name = result['city']
    tem = "当前温度:" + result['tem']
    tem_max = "今天最高温度:" + result['tem1']
    tem_min = "最低温度:" + result['tem2']
    win = "风向:" + result['win']
    win_meter = "风速:" + result['win_meter']
    win_speed = "风力等级:" + result['win_speed']
    humidity = "空气湿度:" + result['humidity']
    visibility = "能见度:" + result['visibility']
    hpa = "气压:" + result['pressure'] + 'hPa'
    air = "空气质量:" + result['air_level']
    air_tips = result['air_tips']

    return str(time + '\n' + city_name + '\n' + wea + '\n' + tem + '\n' + tem_max +
              ' ' + tem_min + "\n" + win + ' ' + win_meter + ' ' + win_speed + '\n'
              + humidity + ' ' + visibility + ' ' + hpa + '\n' + air + '\n' + air_tips)