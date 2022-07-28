import datetime

from ..Tools import asynchttp
from ..Tools.decorator import cache
from ..Tools.get_cookie import get_own_cookie, get_sign_headers, check_retcode, update_cookie_cache, get_headers


# 获取签到信息
async def get_daily_sign_info(uid):
    server_id = 'cn_qd01' if uid[0] == '5' else 'cn_gf01'

    url = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/info'
    cookie = await get_own_cookie()

    if not cookie:
        return f'你的uid{uid}没有绑定对应cookie,必须先绑定cookie才能签到哦'

    '''
        设置请求头
    '''

    headers = {
        'x-rpc-app_version': '2.11.1',
        'x-rpc-client_type': '5',
        'Origin': 'https://webstatic.mihoyo.com',
        'Referer': 'https://webstatic.mihoyo.com/',
        'Cookie': cookie['cookie'],
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS '
                      'X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.11.1',

    }

    '''
        设置请求参数
    '''
    params = {
        'act_id': 'e202009291139501',
        'region': server_id,
        'uid': uid
    }

    response = await asynchttp.get(url=url,headers=headers,params=params)
    data = response.json()
    if await check_retcode(data, cookie, uid):
        return data
    else:
        return f'你的uid{uid}的cookie已过期,需要重新绑定哦!'


# 执行签到操作
async def sign(uid):

    server_id = 'cn_qd01' if uid[0]=='5' else 'cn_gf01'

    url = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/sign'
    cookie = await get_own_cookie()

    if not cookie:
        return f'你的uid{uid}没有绑定对应cookie,必须先绑定cookie才能签到哦'

    '''
        设置请求头
    '''

    headers = get_sign_headers(cookie['cookie'])

    json_data = {
        'act_id': 'e202009291139501',
        'uid': uid,
        'region': server_id
    }

    response = await asynchttp.post(url=url,headers=headers,json=json_data)
    try:
        data = response.json()
    except:
        return response.read()
    if await check_retcode(data, cookie, uid):
        return data
    else:
        return f'你的uid{uid}的cookie已过期,需要重新绑定哦!'


# 查询签到奖励
async def get_sign_list():
    url = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/home'
    headers = {
        'x-rpc-app_version': '2.11.1',
        'User-Agent':        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 ('
                             'KHTML, like Gecko) miHoYoBBS/2.11.1',
        'x-rpc-client_type': '5',
        'Referer':           'https://webstatic.mihoyo.com/'
    }
    params = {
        'act_id': 'e202009291139501'
    }
    resp = await asynchttp.get(url=url, headers=headers, params=params)
    data = resp.json()
    return data


@cache(ttl=datetime.timedelta(hours=1))
async def get_monthinfo_data(uid, month, use_cache=True):
    server_id = "cn_qd01" if uid[0] == '5' else "cn_gf01"
    url = 'https://hk4e-api.mihoyo.com/event/ys_ledger/monthInfo'
    cookie = await get_own_cookie(uid, action='查询每月札记')
    if not cookie:
        return f'你的uid{uid}没有绑定对应的cookie,使用ysb绑定才能用每月札记哦!'
    await update_cookie_cache(cookie['cookie'], uid, 'uid')
    headers = get_headers(q=f'month={month}&bind_uid={uid}&bind_region={server_id}', cookie=cookie['cookie'])
    params = {
        "month": int(month),
        "bind_uid": uid,
        "bind_region": server_id
    }
    resp = await asynchttp.get(url=url, headers=headers, params=params)
    data = resp.json()
    if await check_retcode(data, cookie, uid):
        return data
    else:
        return f'你的uid{uid}的cookie已过期,需要重新绑定哦!'
