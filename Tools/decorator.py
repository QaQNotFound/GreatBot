import datetime
import datetime
import functools
import inspect
import re
from json import JSONDecodeError

from nonebot import get_bot, logger
from nonebot.adapters.onebot.v11 import ActionFailed
from nonebot.exception import FinishedException


# 异常处理装饰器
def exception_handler():
    def wrapper(func):

        @functools.wraps(func)
        async def wrapped(**kwargs):
            event = kwargs['event']
            try:
                await func(**kwargs)
            except FinishedException:
                raise
            except ActionFailed:
                logger.exception('账号可能被风控，消息发送失败')
                await get_bot().send(event, f'账号可能被风控，消息发送失败')
            except JSONDecodeError:
                await get_bot().send(event, '获取信息失败，重试一下吧')
            except FileNotFoundError as e:
                file_name = re.search(r'\'(.*)\'', str(e)).group(1)
                file_name = file_name.replace('\\\\', '/').split('/')
                file_name = file_name[-2] + '\\' + file_name[-1]
                await get_bot().send(event, f"缺少{file_name}资源，请联系开发者补充")
            except Exception as e:
                await get_bot().send(event, f'好像出了点问题，{e}')

        return wrapped

    return wrapper


# 缓存装饰器 ttl为过期时间 参数use_cache决定是否使用缓存，默认为True
def cache(ttl=datetime.timedelta(hours=1)):
    def wrap(func):
        cache_data = {}

        @functools.wraps(func)
        async def wrapped(*args, **kw):
            nonlocal cache_data
            bound = inspect.signature(func).bind(*args, **kw)
            bound.apply_defaults()
            ins_key = '|'.join(['%s_%s' % (k, v) for k, v in bound.arguments.items()])
            default_data = {"time": None, "value": None}
            data = cache_data.get(ins_key, default_data)
            now = datetime.datetime.now()
            if 'use_cache' not in kw:
                kw['use_cache'] = True
            if not kw['use_cache'] or not data['time'] or now - data['time'] > ttl:
                try:
                    data['value'] = await func(*args, **kw)
                    data['time'] = now
                    cache_data[ins_key] = data
                except Exception as e:
                    raise e
            return data['value']

        return wrapped

    return wrap
