import aiohttp
from setting import tg_setting


async def sendMessage(name, perm, text, server, session):
    data = {'name': name, 'perm': perm, 'text': text, 'server': server}
    session.post(tg_setting['url'], data=data, timeout=60)