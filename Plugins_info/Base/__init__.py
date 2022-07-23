import sqlite3
from pathlib import Path

db = Path()

async def get_public_cookie():
    connect = sqlite3.connect(db)
    cursor = connect.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS public_cookie'''
    )