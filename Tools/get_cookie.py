import hashlib
import json
import random
import string
import time

from nonebot import logger

from database import get_private_cookie, delete_cookie, delete_cookie_cache, update_cookie_cache


async def get_own_cookie(uid='', mys_id='', action=''):
    if uid:
        cookie = (await get_private_cookie(uid, 'uid'))
    elif mys_id:
        cookie = (await get_private_cookie(mys_id, 'mys_id'))
    else:
        cookie = None
    if not cookie:
        return None
    else:
        cookie = cookie[0]
        logger.info(f'---派蒙调用用户{cookie[0]}的uid{cookie[2]}私人cookie执行{action}操作---')
        return {'type': 'private', 'user_id': cookie[0], 'cookie': cookie[1], 'uid': cookie[2], 'mys_id': cookie[3]}


'''md5加密'''


def md5(content: str) -> str:
    md5 = hashlib.md5()
    md5.update(content.encode())
    return md5.hexdigest()


'''生成随机字符串'''


def random_hex(length):
    result = hex(random.randint(0, 16 ** length)).replace('0x', '').upper()
    if len(result) < length:
        result = '0' * (length - len(result)) + result
    return result


# 米游社headers的ds_token，对应版本2.11.1
def get_ds(q="", b=None) -> str:
    if b:
        br = json.dumps(b)
    else:
        br = ""
    s = "xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs"
    t = str(int(time()))
    r = str(random.randint(100000, 200000))
    c = md5("salt=" + s + "&t=" + t + "&r=" + r + "&b=" + br + "&q=" + q)
    return f"{t},{r},{c}"


# 米游社爬虫headers
def get_headers(cookie, q='', b=None):
    headers = {
        'DS': get_ds(q, b),
        'Origin': 'https://webstatic.mihoyo.com',
        'Cookie': cookie,
        'x-rpc-app_version': "2.11.1",
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS '
                      'X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.11.1',
        'x-rpc-client_type': '5',
        'Referer': 'https://webstatic.mihoyo.com/'
    }
    return headers


def get_oldversion_ds() -> str:
    s = 'h8w582wxwgqvahcdkpvdhbh2w9casgfl'
    t = str(int(time()))
    r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
    c = md5("salt=" + s + "&t=" + t + "&r=" + r)
    return f"{t},{r},{c}"



def get_sign_headers(cookie):
    headers = {
        'User_Agent':        'Mozilla/5.0 (Linux; Android 10; MIX 2 Build/QKQ1.190825.002; wv) AppleWebKit/537.36 ('
                             'KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36 '
                             'miHoYoBBS/2.3.0',
        'Cookie':            cookie,
        'x-rpc-device_id':   random_hex(32),
        'Origin':            'https://webstatic.mihoyo.com',
        'X_Requested_With':  'com.mihoyo.hyperion',
        'DS':                get_oldversion_ds(),
        'x-rpc-client_type': '5',
        'Referer':           'https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?bbs_auth_required=true&act_id'
                             '=e202009291139501&utm_source=bbs&utm_medium=mys&utm_campaign=icon',
        'x-rpc-app_version': '2.3.0'
    }
    return headers

''' 检查数据返回状态，
    10001为ck过期了，
    10101为达到每日30次上线了
'''
async def check_retcode(data, cookie, uid):
    if data['retcode'] == 10001 or data['retcode'] == -100:
        await delete_cookie(cookie['cookie'], cookie['type'])
        # await send_cookie_delete_msg(cookie)
        return False
    elif data['retcode'] == 10101:
        if cookie['type'] == 'public':
            logger.info(f'{cookie["no"]}号公共cookie达到了每日30次查询上限')
            # await limit_public_cookie(cookie['cookie'])
            await delete_cookie_cache(cookie['cookie'], key='cookie')
        elif cookie['type'] == 'private':
            logger.info(f'用户{cookie["user_id"]}的uid{cookie["uid"]}私人cookie达到了每日30次查询上限')
            return '私人cookie达到了每日30次查询上限'
        return False
    else:
        await update_cookie_cache(cookie['cookie'], uid, 'uid')
        return True