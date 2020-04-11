from aiohttp import web
import MCBot
import datetime
from setting import web_server_setting
from SendChatToQQGroup import report_data
routes = web.RouteTableDef()

@routes.get('/')
async def get_handler(request):
    return web.Response(text='Python Robot Server is running')

@routes.post('/post')
async def post_handler(request):
    data = await request.post()
    try:
        name = data['name']
    except Exception:
        return web.Response(text='No_Name')
    try:
        perm = data['perm']
    except Exception:
        return web.Response(text='No_Perm')
    try:
        text = data['text']
    except Exception:
        text = ''
    print('[' + str(datetime.datetime.now().strftime('%H:%M:%S.%f'))[:-3] + ' INFO]: ' + '[' + perm + '] ' + name + ': ' + text)
    await MCBot.main(perm, name, text)
    await report_data(name, text)
    return web.Response(text='OK')
        

if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host=web_server_setting['host'], port=web_server_setting['port'])