import sys, os, time, re, json, requests, random
import asyncio
from mcrcon import MCRcon
from setting import rcon_setting

is_enable_ip_check = 1
is_enable_ip_check_public = 0
is_enable_luckdraw = 0
is_can_say = 1
who_luckdraw = ''
luckdraw_list = []

async def getip(text):
    try:
        ip = re.search("((?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]))", text).group(1)
    except Exception:
        ip = ''
    return ip

async def send_message(text):
    with MCRcon(rcon_setting['address'], rcon_setting['password'], rcon_setting['port']) as mcr:
        r = mcr.command('tellraw @a {"extra":[{"text":"[","bold":true,"color":"gold"},{"text":"BOT","color":"dark_green"},{"text":"] ","bold":true,"color":"gold"},{text:"' + text + '"}],"text":""}')

async def PrintIPLoc(ip):
    a, b, c, d = map(int,ip.split('.'))
    if a <= 255 and b <= 255 and c <= 255 and d <= 255:
        r = json.loads(requests.get('http://whois.pconline.com.cn/ipJson.jsp?ip=' + ip).text.replace('if(window.IPCallBack) {IPCallBack(','').replace(');}',''))
        await send_message(str(ip + ': ' + r['addr'].strip()).replace('&',' & '))
    else:
        await send_message(str(ip + ': ' + '不是一个标准IPV4地址'))

async def luckdraw_setting(perm, who_said, what_said):
    global is_enable_ip_check, is_enable_ip_check_public, is_enable_luckdraw, is_can_say, who_luckdraw, luckdraw_list
    if (what_said.find('enable') != -1) and (perm == 'ADMIN'):
        is_enable_luckdraw = 1
        await send_message('已启用抽奖')
    elif (what_said.find('disable') != -1) and (perm == 'ADMIN'):
        is_enable_luckdraw = 0
        await send_message('已关闭抽奖')
    elif (what_said.find('help') != -1):
        await send_message('抽奖功能帮助:\\n#hankbot 抽奖 enable/disable/check/help\\n!开始抽奖 奖品名称\\n!cj !结束抽奖 !强制结束抽奖')
    elif (what_said.find('check') != -1):
        if (is_enable_luckdraw == 1):
            await send_message('抽奖功能: 开启状态')
        else:
            await send_message('抽奖功能: 关闭状态')
    else:
        if (is_enable_luckdraw == 1):
            await send_message('抽奖功能: 开启状态')
        else:
            await send_message('抽奖功能: 关闭状态')

async def ip_check_setting(perm, who_said, what_said):
    global is_enable_ip_check, is_enable_ip_check_public, is_enable_luckdraw, is_can_say, who_luckdraw, luckdraw_list
    if (what_said.find('enable') != -1) and (perm == 'ADMIN'):
        is_enable_ip_check = 1
        await send_message('已启用IP查询')
    elif (what_said.find('disable') != -1) and (perm == 'ADMIN'):
        is_enable_ip_check = 0
        await send_message('已关闭IP查询')
    elif (what_said.find('dispublic') != -1) and (perm == 'ADMIN'):
        is_enable_ip_check_public = 0
        await send_message('已关闭公开IP查询')
    elif (what_said.find('public') != -1) and (perm == 'ADMIN'):
        is_enable_ip_check_public = 1
        await send_message('已启用公开IP查询')
    elif (what_said.find('help') != -1):
        await send_message('IP查询功能帮助:\\n#hankbot ip-check enable/disable/dispublic/public/check/help')
    elif (what_said.find('check') != -1):
        if (is_enable_ip_check == 1 and is_enable_ip_check_public == 1):
            await send_message('IP查询功能: 开启 公开')
        elif (is_enable_ip_check == 1 and is_enable_ip_check_public == 0):
            await send_message('IP查询功能: 开启 不公开')
        else:
            await send_message('IP查询功能: 关闭')

async def with_hankbot(perm, who_said, what_said):
    global is_enable_ip_check, is_enable_ip_check_public, is_enable_luckdraw, is_can_say, who_luckdraw, luckdraw_list
    if is_can_say == 0:
        if (what_said.find('取消禁言')) != -1 and (perm == 'ADMIN'):
            is_can_say = 1
            await send_message('取消禁言')
    else:
        if (what_said.find('禁言') != -1 and (perm == 'ADMIN')):
            is_can_say = 0
            await send_message('已禁言')
        elif what_said.find('test') != -1:
            await send_message('运行正常')
        elif what_said.find('ip-check') != -1:
            await ip_check_setting(perm, who_said, what_said)
        elif what_said.find('抽奖') != -1:
            await luckdraw_setting(perm, who_said, what_said)
        elif what_said.find('help') != -1:
            await send_message('总帮助:\\n#hankbot test/help/禁言/取消禁言\\n#hankbot ip-check/抽奖 help')
        else:
            await send_message('输入#hankbot help获取帮助')

async def luckdraw(perm, who_said, what_said):
    global is_enable_ip_check, is_enable_ip_check_public, is_enable_luckdraw, is_can_say, who_luckdraw, luckdraw_list
    if (what_said.find('!开始抽奖') != -1) and (is_enable_luckdraw == 1) and (who_said != '') and (is_can_say == 1):
        item = what_said.replace('!开始抽奖','').strip().replace('§', '&')
        if item != '':
            if who_luckdraw == '':
                luckdraw_list = []
                who_luckdraw = who_said
                await send_message(who_said + '发起了抽奖! 抽取 ' + item + '\\n发送 !cj 参加')
            else:
                await send_message('对不起' + who_said + ', ' + who_luckdraw+ '发起的抽奖未结束, 无法发起新的抽奖!')
        else:
            await send_message('请补全奖品名称后重新发送')
    elif (what_said.find('!cj') != -1) and (who_luckdraw != '') and (is_enable_luckdraw == 1) and (who_said != '') and (is_can_say == 1):
        luckdraw_list.append(str(who_said))
    elif (what_said.find('!结束抽奖') != -1) and (who_said == who_luckdraw) and (is_enable_luckdraw == 1) and (who_said != '') and (is_can_say == 1):
        luckdraw_list = list(set(luckdraw_list))
        if luckdraw_list == []:
            await send_message('抽奖结束! 无中奖者')
        else:
            await send_message('抽奖结束! 中奖者是 &6&l' + str(random.choice(luckdraw_list)))
        who_luckdraw = ''
        luckdraw_list = []
    elif (what_said.find('!强制结束抽奖') != -1) and (is_enable_luckdraw == 1) and (who_said != '') and (is_can_say == 1) and (perm == 'ADMIN'):
        await send_message('抽奖已被强制结束!')
        who_luckdraw = ''
        luckdraw_list = []

async def chat_manage(perm, who_said, what_said):
    global is_enable_ip_check, is_enable_ip_check_public, is_enable_luckdraw, is_can_say, who_luckdraw, luckdraw_list
    ip = await getip(what_said)
    if what_said.find('#hankbot') != -1:
        await with_hankbot(perm, who_said, what_said)
    elif (what_said.find('!') != -1):
        await luckdraw(perm, who_said, what_said)
    elif (is_can_say == 1) and (ip != '') and (perm == 'ADMIN') and (is_enable_ip_check == 1):
        await PrintIPLoc(ip)
    elif (is_can_say == 1) and (ip != '') and (is_enable_ip_check_public == 1) and (is_enable_ip_check == 1):
        await PrintIPLoc(ip)

async def main(perm, who_said, what_said):
    await chat_manage(perm, who_said, what_said)