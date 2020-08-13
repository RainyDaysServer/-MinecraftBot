import aiohttp
from setting import tg_setting


async def sendMessage(name, perm, text, server):
    data = {'name': name, 'perm': perm, 'text': text, 'server': server}
    timeout = aiohttp.ClientTimeout(total=1)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(tg_setting['url'], data=data):
            pass
