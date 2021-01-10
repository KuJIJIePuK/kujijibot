import re
from datetime import datetime
import time
import os
from twitchio.ext import commands
from urllib.request import urlopen, Request
from variables import *
from kujdef import *
#from defnew import *

bot = commands.Bot(
    irc_token=token,
    client_id=idc,
    nick='kujijibot',
    prefix='k',
    initial_channels=ichan
)
botlist = ['streamelements','moobot','nightbot','mikuia','kujijibot']
dconf = {}
d = {}
dl = {}
last = {}
dmax = 8

dirconf = 'bot1.cfg'

d['tem'] = time.strftime('%Y-%m-%d', time.localtime())
tem = time.strftime('%Y-%m-%d', time.localtime())
#if not os.path.exists('LOG/LOG '+tem+'/'+str(chan)+'/'):
#    os.makedirs('LOG/LOG '+tem+'/'+str(chan)+'/')

if not os.path.exists(dirconf):
    inp = open(dirconf,'a',encoding='utf8')
    inp.close()

inp = open(dirconf,'r',encoding='utf8')
t = inp.readlines()
inp.close()

for line in t:
    if not line == '\n':
        line = line.replace('\n','')
        line = line.split(' ')
        if not '_i' in line[0]:
            if len(line)>1:
                dconf[line[0]]=line[1]
            else:
                d[line[0]]='0'
        elif '_i' in line[0]:
            dconf[line[0]]=[]
            for t1 in line:
                if not t1 == line[0]:
                    dconf[line[0]].append(t1)
#print(dconf)

@bot.event
async def event_raw_data(data):
    if 'followers-only=' in data:
        time_now = time.strftime('%H:%M:%S', time.localtime())
        t0 = re.findall(r'followers-only=([0-9]+)',data)
        if t0:
            t1 = re.findall(r'#(\S+)',data)
            if t0[0] == '0':
                last['fol'+chan]=str(time_now)
                addfile('LOG/LOG '+d['tem']+'/'+chan+'/'+'LOG '+'.txt','Фолловмод включен''\n')
            elif t0[0] == '-1':
                last['fol'+chan]='00 00 00'
                addfile('LOG/LOG '+d['tem']+'/'+chan+'/'+'LOG '+'.txt','Фолловмод выключен''\n')


@bot.event
async def event_ready():
    time_now = time.strftime('%H:%M:%S', time.localtime())
    addfile('START_LOG.txt',tem+' '+time_now+'\n')
    ws = bot._ws  # this is only needed to send messages within event_ready
    #await _websocket.send(f'PRIVMSG #kujijiepuk :.w kujijiepuk hello\r\n')
    #await ws.send_privmsg('kujijiepuk', '.w kujijiepuk has landed!')
    'Called once when the bot goes online.'
    for chan in bot.initial_channels:
        chan = chan.replace('#','')
        print(f'MainBot Подключился к '+chan)
        ch = chan+'_f'
        if ch not in dconf:
            dconf[ch] = '0'
            confre(dirconf,ch,dconf[ch])
        ch = chan+'_b'
        if ch not in dconf:
            dconf[ch] = '0'
            confre(dirconf,ch,dconf[ch])
        ch = chan+'_m'
        if ch not in dconf:
            dconf[ch] = '0'
            confre(dirconf,ch,dconf[ch])
        ch = chan+'_i'
        if ch not in dconf:
            dconf[ch] = []
            confignore(dirconf,ch,'kujijibot')

        #if chan+'f' not in d:
        #    d[str(chan)+'f'] = 1
        #    inp = open('bot.cfg','a',encoding='utf8')
        #    inp.write(chan+'f 1\n')
        #    inp.close()
        last['elo'+chan] = '00 00 00'
        last['sr'+chan] = '00 00 00'
        last['sk'+chan] = '00 00 00'
        last['fol'+chan] = '00 00 00'

@bot.event
async def event_message(ctx):
    time_now = time.strftime('%H:%M:%S', time.localtime())

    #tim = str(time_now)
    U_m = ctx.author.name + ': ' + ctx.content
    print(U_m)
    antf = 1
    antb = 1
    chan = str(ctx.channel)
    mesag = ctx.content.lower()
    autor = str(ctx.author.name.lower())

    tem = d['tem']
    if not d['tem'] == time.strftime('%Y-%m-%d', time.localtime()):
        d['tem'] = time.strftime('%Y-%m-%d', time.localtime())
        tem = d['tem']
        for chan in bot.initial_channels:
            chan = chan.replace('#','')
    if not os.path.exists('LOG/LOG '+tem+'/'+str(chan)+'/'):
        os.makedirs('LOG/LOG '+tem+'/'+str(chan)+'/')

    
    
    dir_user_log = 'LOG/LOG '+tem+'/'+str(ctx.channel)+'/'+ctx.author.name+'.txt'
    dir_chan_log = 'LOG/LOG '+tem+'/'+str(ctx.channel)+'/'+'LOG '+tem+'.txt'
    mute_log = 'LOG/LOG '+tem+'/'+str(ctx.channel)+'/'+'MUTE_BAN LOG '+tem+'.txt'
    
    addfile(dir_user_log,time_now+' '+U_m+'\n')
    addfile(dir_chan_log,time_now+' '+U_m+'\n')
    mt = mesag.split(' ')

    if mesag.startswith('!elo'):
        if 'hubibich' in chan or 'hubbich' in chan or 'kujijiepuk' in chan:
            doelo = -1
            las = time0(time_now)-time0(last['elo'+str(ctx.channel)])
            if ctx.author.type == 'mod' or 'badges=broadcaster' in ctx.raw_data:
                doelo = 1
            elif las > 5 or las < 0:
                doelo = 1
            if doelo == 1:
                nik = 'hubbich'
                t2 = []
                t2 = re.findall(r'!elo (\S+)',mesag)
                try:
                    nik = t2[0]
                except:
                    pass
                delo = defelo(mesag,nik)
                if delo!=-1:
                    await ctx.channel.send(f'@'+ctx.author.name+' Elo '+nik+' = '+str(delo))
                else:
                    await ctx.channel.send(f'@'+ctx.author.name+' Ошибка, ник не найден')
                last['elo'+str(ctx.channel)] = time_now


    if 'kujijiepuk' in autor:
        if mesag == 'fol':
            if last['fol'+chan]=='00 00 00':
                await ctx.channel.followers()
                last['fol'+chan]=time_now
                addfile(dir_chan_log,'Фолловмод включен''\n')
            else:
                await ctx.channel.followersoff()
                last['fol'+chan]='00 00 00'
                addfile(dir_chan_log,'Фолловмод выключен''\n')


    if ctx.author.type == 'mod' or 'badges=broadcaster' in ctx.raw_data or 'kujijiepuk' in autor and not 'kujijibot' in autor:
        antf = 0

        if mesag == 'bot':
            if 'hubibich' in chan:                
                m1 = 'help + команда выдаст подробности. Команды: "botf" , "botm" , "botb", "boti "+ник (можно через @)'
                await ctx.channel.send(f''+m1+' @'+ctx.author.name)
            elif chan+'_i' in dconf:
                m1 = 'help + команда выдаст подробности. Команды: "botf", "botb", "boti "+ник (можно через @)'
                await ctx.channel.send(f''+m1+' @'+ctx.author.name)
            else:
                m1 = 'help + команда выдаст подробности. Команды: "botb" антиботфлуд, "botf" антифлуд'
                await ctx.channel.send(f''+m1+' @'+ctx.author.name)
        if mesag.startswith('help '):
            if 'botf' in mesag:
                m1 = 'Это режим антифлуда. Если недавно (от одного пользователя) было отправленно много коротких сообщений или много одинаковых, то после предупреждения выдастся мут (если есть модерка)'
                await ctx.channel.send(f''+m1+' @'+ctx.author.name)
            if 'botb' in mesag:
                m1 = 'Это режим антиботов. Если набирается несколько одинаковых сообщений от разных пользователей, ставится режим только для фолловеров, так же выключает его через 90 секунд (если есть сообщения в чате) нужна модерка'
                await ctx.channel.send(f''+m1+' @'+ctx.author.name)
            if 'boti' in mesag:
                m1 = 'Добавляет пользователя в список игнора, тоесть при включенном режиме антифлуда ему не будет выдаваться предупреждения и мут'
                await ctx.channel.send(f''+m1+' @'+ctx.author.name)
            if 'botm' in mesag:
                m1 = 'Переключает режим заказа и скипа музыки для ручного добавления (на всякий случай)'
                await ctx.channel.send(f''+m1+' @'+ctx.author.name)


        if mesag.startswith('boti'):
            temp = str(ctx.content)
            temp = temp.replace('boti','')
            temp = temp.replace('@','')
            if len(temp)>1:
                t1 = temp.split(' ')
                t1.remove('')
                temp = temp.replace(' ','')
            nick = temp.lower()
            if len(nick)<=1 or len(t1)>1:
                await ctx.channel.send(f'Ошибка, попробуйте ещё раз @'+ctx.author.name)
            else:
                templ = dconf[chan+'_i']
                if not nick in templ:
                    templ.append(nick)
                    await ctx.channel.send(nick+' добавлен в список игнора антифлуда @'+ctx.author.name)
                else:
                    templ.remove(nick)
                    await ctx.channel.send(nick+' удалён из списка игнора антифлуда @'+ctx.author.name)
                ch = chan+'_i'
                confignore(dirconf,ch,nick)

        if mesag == 'botf':
            ch = chan+'_f'
            if not ch in dconf:
                dconf[ch] = '1'
            if dconf[ch] == '1':
                dconf[ch] = '0'
                stat = 'выключен'
            elif dconf[ch] == '0':
                dconf[ch] = '1'
                stat = 'включен'
            await ctx.channel.send(f'Антифлуд '+stat+' @'+ctx.author.name)
            confre(dirconf,ch,dconf[ch])
            

        if mesag == 'botb':
            ch = chan+'_b'
            if not ch in dconf:
                dconf[ch] = '0'
            if dconf[ch] == '1':
                dconf[ch] = '0'
                stat = 'выключен'
            elif dconf[ch] == '0':
                dconf[ch] = '1'
                stat = 'включен'
            await ctx.channel.send(f'Антиботфлуд '+stat+' @'+ctx.author.name)
            confre(dirconf,ch,dconf[ch])

        if mesag == 'botm' and 'hubibich' in chan:
            ch = chan+'_m'
            if not ch in dconf:
                dconf[ch] = '0'
            if dconf[ch] == '1':
                dconf[ch] = '0'
                stat = 'выключен'
            elif dconf[ch] == '0':
                dconf[ch] = '1'
                stat = 'включен'
            await ctx.channel.send(f'Заказ/скип музыки '+stat+' @'+ctx.author.name)
            confre(dirconf,ch,dconf[ch])

    else:
        if mesag == 'bot':
            m1 = 'Команды: !elo'
            await ctx.channel.send(f''+m1+' @'+ctx.author.name)

    if  autor in dconf[chan+'_i']:
        antf = 0
        antb = 0

    if  autor in botlist:
        antf = 0


    t2 = re.findall(r'([пидорpidor][^абвгдеёжзклмнстуфхцчшщъыьэюяabcefjhklmnqstvwxyz_\W]+)',mesag)
    t0 = ''.join(map(str, t2))
    i = -1
    while i<len(t0)-1:
        i+=1
        while i+1<len(t0) and t0[i]==t0[i+1]:
            t3 = t0[i]
            t3+=t3
            t0 = t0.replace(t3,t0[i])

    if t0 == 'пидор' or t0 == 'pidor':
        await ctx.channel.timeout(ctx.author.name, 600,'гц')
        act = ' Мут '
        res = ' за запретку в '
        print(act+ctx.author.name+res+time_now)
        addfile(mute_log,act+ctx.author.name+res+time_now+'\n')
        addfile(dir_chan_log,act+ctx.author.name+res+time_now+'\n')
        addfile(dir_user_log,act+ctx.author.name+res+time_now+'\n')

    elif 'даун' in mt or 'нигер' in mt :
        await ctx.channel.timeout(ctx.author.name, 30,'э чо твориш')
        act = ' Мут '
        res = ' за запретку в '
        print(act+ctx.author.name+res+time_now)
        addfile(mute_log,act+ctx.author.name+res+time_now+'\n')
        addfile(dir_chan_log,act+ctx.author.name+res+time_now+'\n')
        addfile(dir_user_log,act+ctx.author.name+res+time_now+'\n')


    if 'зайдите' in mt and 'на' in mt and 'стрим' in mt:
        await ctx.channel.timeout(ctx.author.name, 600,'гц')
        act = ' Мут '
        res = ' за рекламу в '
        print(act+ctx.author.name+res+time_now)
        addfile(mute_log,act+ctx.author.name+res+time_now+'\n')
        addfile(dir_chan_log,act+ctx.author.name+res+time_now+'\n')
        addfile(dir_user_log,act+ctx.author.name+res+time_now+'\n')


    if not os.path.isfile(mute_log):
        inp = open(mute_log,'a',encoding='utf8')
        inp.close()

    if antb == 1:
        if 'clck' in mesag and 'follow' in mesag or 'StreаmDеtаilsВot' in mesag:
            await ctx.channel.timeout(ctx.author.name, 600,'Реклама накрутки?')
            act = ' Мут '
            res = ' за рекламу накрутки в '
            print(ctx.author.name+act+res+time_now)
            addfile(dir_chan_log,act+ctx.author.name+res+time_now+'\n')
            addfile(dir_user_log,act+ctx.author.name+res+time_now+'\n')

    if antb == 1:
        if 'pleace' in mesag and 'youtube' in mesag or 'plsss' in mesag and 'open' in mesag:
            await ctx.channel.timeout(ctx.author.name, 600,'Реклама?')
            act = ' Мут '
            res = ' за рекламу в '
            print(ctx.author.name+act+res+time_now)
            addfile(dir_chan_log,act+ctx.author.name+res+time_now+'\n')
            addfile(dir_user_log,act+ctx.author.name+res+time_now+'\n')

    if ctx.author.reward == '2499dbb9-7630-436c-8e0f-98d64b6822ae' and 'hubibich' in str(ctx.channel):
        t0 = re.findall(r'([a-z\d-]+)',mesag)
        muted = 'ошибка'
        try:
            muted = t0[0]
        except:
            return
        await ctx.channel.timeout(muted, 600,'За баллы')
        print (muted+' Получил мут за баллы в '+time_now+' от '+ctx.author.name)
        addfile('LOG/LOG '+tem+'/'+str(ctx.channel)+'/'+muted+'.txt',muted+' Получил мут за баллы в '+time_now+' от '+ctx.author.name+'\n')
        addfile(dir_chan_log,muted+' Получил мут за баллы в '+time_now+' от '+ctx.author.name+'\n')

    if ctx.author.reward == '70e76278-57d5-4989-a2e3-bafc14c3cc73' and 'hubibich' in str(ctx.channel):
        t1 = str(ctx.content)
        if time0(time_now)-time0(last['sr'+str(ctx.channel)]) > 3 or time0(time_now)-time0(last['sr'+str(ctx.channel)]) < 0:
            delay = 0
        else:
            delay = 4
        if 'youtu' in t1:
            if 'v=' in t1 :
                if not '?v=' in t1:
                    t2 = re.findall(r'v=([\w-]+)[&?]',t1)
                    t1 = t2[0]
                    t0 = 'youtu.be/'+t1
                elif 'v=' in t1:
                    t2 = re.findall(r'v=([\w-]+)',t1)
                    t1 = t2[0]
                    t0 = 'youtu.be/'+t1
            elif 'youtu.be/' in t1 and '?' in t1 or '&' in t1:
                t2 = re.findall(r'youtu.be/([\w-]+)[?&\s]',t1)
                t1 = t2[0]
                t0 = 'youtu.be/'+t1
            else:
                t0 = t1.replace('https://','')
            time.sleep(delay)
            await ctx.channel.send(f'!sr '+t0)
            last['sr'+str(ctx.channel)] = time.strftime('%H:%M:%S', time.localtime())
            
        else:
            if '!sr' in ctx.content.lower():
                time.sleep(delay)
                await ctx.channel.send(f''+t1)
                last['sr'+str(ctx.channel)] = time.strftime('%H:%M:%S', time.localtime())
            time.sleep(delay)
            await ctx.channel.send(f'!sr '+t1)
            last['sr'+str(ctx.channel)] = time.strftime('%H:%M:%S', time.localtime())

    if ctx.author.reward == '9972db1c-8d86-4b96-8c23-a490315fb41b' and 'hubibich' in str(ctx.channel):
        t1 = str(ctx.content)
        if time0(time_now)-time0(last['sk'+str(ctx.channel)]) < 2:
            await ctx.channel.send(f'2 скипа сразу, упс')
            return
        elif time0(time_now)-time0(last['sk'+str(ctx.channel)]) > 3:
            delay = 0
        else:
            delay = 4
        if 'youtu' in t1:
            if 'v=' in t1 :
                if not '?v=' in t1:
                    t2 = re.findall(r'v=(\S+)[&?]',t1)
                    t1 = t2[0]
                    t0 = 'youtu.be/'+t1
                else:
                    t2 = re.findall(r'v=(\S+)',t1)
                    t1 = t2[0]
                    t0 = 'youtu.be/'+t1
            elif 'youtu.be/' in t1 and '?' in t1 or '&' in t1:
                t2 = re.findall(r'youtu.be/(\S+)[?&\s]',t1)
                t1 = t2[0]
                t0 = 'youtu.be/'+t1
            else:
                t0 = t1.replace('https://','')
            time.sleep(delay)
            await ctx.channel.send(f'!removesong '+t0)
            last['sk'+str(ctx.channel)] = time.strftime('%H:%M:%S', time.localtime())
        else:
            time.sleep(delay)
            await ctx.channel.send(f'!skip')
            last['sk'+str(ctx.channel)] = time.strftime('%H:%M:%S', time.localtime())

    #   Запись всех сообщений в дневник (dmax = кол-во последних сообщений пользователя)
    if not 'fanjqiwehnqugvjklbanjikncvoiuquifo' in mesag:
        tim = []
        mess = []
        i = -1
        while i < dmax:
            i+=1
            tim.append(0)
        i = -1
        while i < dmax:
            i+=1
            mess.append('')

        i = dmax
        while i>1:
            i-=1
            if ctx.author.name+str(i-1) in d:
                d[ctx.author.name+str(i)] = d[ctx.author.name+str(i-1)]
        temp = ctx.content.lower()
        d[ctx.author.name+'0'] = time_now+' '+temp
        dl[ctx.author.name] = temp

        if df(dl,temp)>=5 and dconf[chan+'_b'] == '1':
            await ctx.channel.followers()
            addfile(dir_chan_log,'Фолловмод включен''\n')
            last['fol'+chan]=str(time_now)
            for key, value in dict(dl).items():
                if value == temp:
                    del dl[key]

        if last['fol'+chan]!='00 00 00' and dconf[chan+'_b'] == '1':
            if time0(time_now)-time0(last['fol'+chan])>=90:
                await ctx.channel.followersoff()
                addfile(dir_chan_log,'Фолловмод выключен''\n')
                last['fol'+chan]='00 00 00'

        i = -1
        while i<dmax-1:
            i+=1
            if ctx.author.name+str(i) in d:
                tim[i] = time0(d[ctx.author.name+str(i)])
                t = d[ctx.author.name+str(i)]
                mess[i] = t[9:]

        i = dmax
        while i>1:
            i-=1
            if tim[0]-tim[i] >=300 and tim[i]!=0:
                if ctx.author.name+str(i) in d:
                    del d[ctx.author.name+str(i)]
                    tim[i] = 0
                    mess[i] = ''

        if ctx.author.name+str(1) in d:
            mute_time = 15
            mutef = 0
            muter = 0
            muterep = -1
            muteflood = -1
            maxcount = 0
            counts = {}
            tempm = '-19489×56'

            i = -1
            while i<dmax-1:
                i+=1
                if ctx.author.name+str(i+1) in d:
                    if len(mess[i])<10 and tim[i]-tim[i+1]<4:
                        if ctx.author.name+str(i+2) in d and tim[i]-tim[i+2]<7:
                            mutef+=1
                    if len(mess[i])<10 and tim[i]-tim[i+1]<5:
                        mutef+=1
            if mutef == 7 and len(mess[0])<10 and tim[0]-tim[1]<=8:
                muteflood = 0
            elif mutef > 7 and len(mess[0])<10 and tim[0]-tim[1]<=8:
                muteflood = 1

            i = -1
            while i<dmax-1:
                i+=1
                j = i
                if mess[i]!='':
                    ti = mess[i].split(' ')
                    ti1 = len(ti)
                    ti = set(ti)
                while j<dmax-1:
                    j+=1
                    if mess[j]!='':
                        tj = mess[j].split(' ')
                        tj1 = len(tj)
                        tj = set(tj)
                        t2 = list(set(ti) & set(tj))
                        tt = max(tj1,ti1)
                        if max(len(tj),len(ti))/min(tj1,ti1)<0.3:
                            if tim[i]-tim[j]<=60:
                                muter+=1
                        if len(t2)/tt>=0.65 and len(tj)>=1:
                            if tim[i]-tim[j]<=20:
                                muter+=2
                            elif tim[i]-tim[j]<=60:
                                muter+=1

            if mess[0]!='':
                ti = mess[0].split(' ')
                ti1 = len(ti)
                ti = set(ti)
            j = 0
            while j<dmax-1:
                j+=1
                if mess[j]!='':
                    tj = mess[j].split(' ')
                    tj1 = len(tj)
                    tj = set(tj)
                    t2 = list(set(ti) & set(tj))
                    tt = max(tj1,ti1)
                    if max(len(tj),len(ti))/min(tj1,ti1)<0.3:
                        if tim[i]-tim[j]<=60:
                            muter+=1
                    if len(t2)/tt>=0.65 and len(tj)>=1:
                        if tim[i]-tim[j]<=5:
                            muter+=3
                        elif tim[i]-tim[j]<=25:
                            muter+=2
                        elif tim[i]-tim[j]<=60:
                            muter+=1

            if 'snivanov' in chan:
                tempmuterep = 8
            else:
                tempmuterep = 6

            if muter>=2:
                t1 = mess[0].split(' ')
                t3 = list(set(t2) & set(t1))
                if muter==tempmuterep:
                    muterep = 0
                elif muter > tempmuterep:
                    muterep = 1

            if not ctx.author.name+'mf' in last:
                last[ctx.author.name+'mf'] = 0

            if mutef>last[ctx.author.name+'mf']:
                last[ctx.author.name+'mf']=mutef
            else:
                last[ctx.author.name+'mf']=mutef
                if muteflood == 1:
                    muteflood = 0

            if not ctx.author.name+'mr' in last:
                last[ctx.author.name+'mr'] = 0

            if muter>last[ctx.author.name+'mr']:
                last[ctx.author.name+'mr']=muter
            else:
                last[ctx.author.name+'mr']=muter
                if muterep == 1:
                    muterep = 0

            if not ctx.author.name+'p' in d:
                d[ctx.author.name+'p'] = '00.00.00'

            #print(d[ctx.author.name+'p'])
            if time0(time_now)-time0(d[ctx.author.name+'p'])<=300 and muterep == 0:
                muterep = -1
            elif time0(time_now)-time0(d[ctx.author.name+'p'])>60 and muterep == 1:
                muterep = 0
            elif time0(time_now)-time0(d[ctx.author.name+'p'])<=300 and muteflood == 0:
                muteflood = -1
            elif time0(time_now)-time0(d[ctx.author.name+'p'])>60 and muteflood == 1:
                muteflood = 0

            if muteflood == 1 or muterep == 1:
                inp = open(mute_log,'r',encoding='utf8')
                for line in inp:
                    if ctx.author.name in line:
                        mute_time = mute_time * 2
                inp.close()

            if muteflood == 0 or muterep == 0:
                if muteflood == 0:
                    mess = 'Будешь так флудить, отхватишь таймаут @'
                    res = 'флуд'
                elif muterep == 0:
                    mess = 'Ещё раз повторишь, отхватишь таймаут @'      
                    res = 'повторы'          
                if dconf[chan+'_f'] == '1' and antf == 1:
                    await ctx.channel.send(f''+mess+ctx.author.name)
                d[ctx.author.name+'p'] = time_now
                print('Предупреждение '+ctx.author.name+' за '+res+' в '+time_now)
                addfile(dir_chan_log,'Предупреждение '+ctx.author.name+' за '+res+' на '+str(mute_time)+'\n')
                addfile(dir_user_log,'Предупреждение '+ctx.author.name+' за '+res+' на '+str(mute_time)+'\n')

            if muteflood == 1 or muterep == 1:
                if muteflood == 1:
                    res = 'флуд'
                elif muterep == 1:
                    res = 'повторы'          
                if dconf[chan+'_f'] == '1' and antf == 1:
                    await ctx.channel.timeout(ctx.author.name, mute_time,'Узбагойся ('+res+')')
                    d[ctx.author.name+'p'] = time_now
                    i = dmax
                while i>1:
                    i-=1
                    if ctx.author.name+str(i) in d:
                        del d[ctx.author.name+str(i)]
                d[ctx.author.name+'p'] = '00.00.00'
                print('Мут '+ctx.author.name+' за флуд на '+str(mute_time)+' в '+time_now)
                addfile(dir_chan_log,'Мут '+ctx.author.name+' за '+res+' на '+str(mute_time)+'\n')
                addfile(dir_user_log,'Мут '+ctx.author.name+' за '+res+' на '+str(mute_time)+'\n')

#@bot.command(name='test')
#async def test(ctx):
#    await ctx.send('test passed!')

if __name__ == '__main__':
    bot.run()