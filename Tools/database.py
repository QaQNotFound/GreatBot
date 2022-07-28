import sqlite3
from pathlib import Path

db_path = Path() / 'data' / 'GreatBot' / 'user_data' / 'user_data.db'

'''获取个人cookie'''


async def get_private_cookie(value, key='user_id'):
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS private_cookies
        (
            user_id TEXT NOT NULL,
            uid TEXT NOT NULL,
            mys_id TEXT,
            cookie TEXT,
            stoken TEXT,
            PRIMARY KEY (user_id, uid)
        );''')
    cursor.execute(f'SELECT user_id, cookie, uid, mys_id FROM private_cookies WHERE {key}="{value}";')
    cookie = cursor.fetchall()
    connect.close()
    return cookie


'''更新个人cookie'''


async def update_private_cookie(user_id, uid='', mys_id='', cookie='', stoken=''):
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS private_cookies
        (
            user_id TEXT NOT NULL,
            uid TEXT NOT NULL,
            mys_id TEXT,
            cookie TEXT,
            stoken TEXT,
            PRIMARY KEY (user_id, uid)
        );''')
    cursor.execute('REPLACE INTO private_cookies VALUES (?, ?, ?, ?, ?);', (user_id, uid, mys_id, cookie, stoken))
    connect.commit()
    connect.close()


'''删除私人cookie'''


async def delete_private_cookie(user_id):
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS private_cookies
        (
            user_id TEXT NOT NULL,
            uid TEXT NOT NULL,
            mys_id TEXT,
            cookie TEXT,
            stoken TEXT,
            PRIMARY KEY (user_id, uid)
        );''')
    cursor.execute('DELETE FROM private_cookies WHERE user_id=?', (user_id,))
    connect.commit()
    connect.close()


'''获取cookie缓存'''


async def get_cookie_cache(value, key='uid'):
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cookie_cache(
        uid TEXT PRIMARY KEY NOT NULL,
        mys_id TEXT,
        cookie TEXT);''')
    cursor.execute(f'SELECT cookie FROM cookie_cache WHERE {key}="{value}"')
    res = cursor.fetchone()
    if res:
        try:
            cursor.execute('SELECT user_id, uid, mys_id FROM private_cookies WHERE cookie=?;', (res[0],))
            is_in_private = cursor.fetchone()
            if is_in_private:
                return {'type': 'private', 'user_id': is_in_private[0], 'cookie': res[0], 'uid': is_in_private[1],
                        'mys_id': is_in_private[2]}
        except:
            pass
        try:
            cursor.execute('SELECT no FROM public_cookies WHERE cookie=?;', (res[0],))
            is_in_public = cursor.fetchone()
            if is_in_public:
                return {'type': 'public', 'cookie': res[0], 'no': is_in_public[0]}
        except:
            pass
    connect.close()
    return None


'''更新cookie缓存'''


async def update_cookie_cache(cookie, value, key='uid'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cookie_cache(
        uid TEXT PRIMARY KEY NOT NULL,
        mys_id TEXT,
        cookie TEXT);''')
    cursor.execute(f'REPLACE INTO cookie_cache ({key}, cookie) VALUES ("{value}", "{cookie}");')
    conn.commit()
    conn.close()


'''删除cookie缓存'''


async def delete_cookie_cache(value='', key='cookie', all=False):
    try:
        connect = sqlite3.connect(db_path)
        cursor = connect.cursor()
        if all:
            cursor.execute('DROP TABLE cookie_cache;')
        else:
            cursor.execute(f'DELETE FROM cookie_cache WHERE {key}="{value}";')
        connect.commit()
        connect.close()
    except:
        pass


'''删除cookie'''


async def delete_cookie(cookie, type='public'):
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute('DELETE FROM cookie_cache WHERE cookie=?;', (cookie,))
    # cursor.execute(f'DELETE FROM {type}_cookies WHERE cookie="{cookie}";')
    connect.commit()
    connect.close()
