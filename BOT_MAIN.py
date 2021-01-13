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
botlist = ['streamelements','moobot','nightbot','mikuia','wizebot','kujijibot']
dconf = {}
d = {}
dl = {}
last = {}
dmax = 8

dirconf = 'bot.cfg'
dirlist = 'anime.txt'
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
        if '_i' in line[0]:
            dconf[line[0]]=[]
            for t1 in line:
                if not t1 == line[0]:
                    dconf[line[0]].append(t1)
        elif 'elo_' in line[0]:
            dconf[line[0]]=[]
            for t1 in line:
                if not t1 == line[0]:
                    dconf[line[0]].append(t1)
        else:# not '_i' in line[0]:
            if len(line)>1:
                dconf[line[0]]=line[1]
            else:
                d[line[0]]='0'


@bot.event
async def event_ready():
    time_now = time.strftime('%H:%M:%S', time.localtime())
    if int(time_now[0:2])+4>=24:
        t1 = str(int(time_now[0:2])-20)
    else:        
        t1 = str(int(time_now[0:2])+4)
    time4 = t1+':'+time_now[3:]
    addfile('START_LOG.txt',tem+' '+time_now+' ('+time4+')'+'\n')
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
        ch = 'elo_'+chan
        if ch not in dconf:
            dconf[ch] = []
            dconf[ch].append(chan)
            confignore(dirconf,ch,chan)
        ch = chan+'_elo'
        if ch not in dconf:
            dconf[ch] = '0'
            confre(dirconf,ch,dconf[ch])
        ch = chan+'_i'
        if ch not in dconf:
            dconf[ch] = []
            confignore(dirconf,ch,'kujijibot')
        if 'elo'+chan not in last:
            last['elo'+chan] = '00 00 00'
        if 'sr'+chan not in last:
            last['sr'+chan] = '00 00 00'
        if 'sk'+chan not in last:
            last['sk'+chan] = '00 00 00'
        if 'fol'+chan not in last:
            last['fol'+chan] = '00 00 00'
        if 'bot'+chan not in last:
            last['bot'+chan] = '00 00 00'
        if 'help'+chan not in last:
            last['help'+chan] = '00 00 00'
        if 'anim'+chan not in last:
            last['anim'+chan] = '00 00 00'


@bot.event
async def event_raw_data(data):
    if 'custom-reward-id=' in data:
        time_now = time.strftime('%H:%M:%S', time.localtime())
        addfile('LOG/LOG '+d['tem']+'/'+'REWARD LOG'+'.txt',time_now+': '+data+'\n')
    if 'followers-only=' in data:
        time_now = time.strftime('%H:%M:%S', time.localtime())
        t0 = re.findall(r'followers-only=([-0-9]+)',data)
        if t0:
            t1 = re.findall(r'ROOMSTATE #([\w_-]+)[\b]*',data)
            if not os.path.exists('LOG/LOG '+d['tem']+'/'+t1[0]):
                os.makedirs('LOG/LOG '+d['tem']+'/'+t1[0])
            if t0[0] == '0':
                last['fol'+t1[0]]=str(time_now)
                addfile('LOG/LOG '+d['tem']+'/'+t1[0]+'/'+'LOG '+d['tem']+'.txt',time_now+' Фолловмод включен\n')

            elif t0[0] == '-1':
                last['fol'+t1[0]]='00 00 00'
                addfile('LOG/LOG '+d['tem']+'/'+t1[0]+'/'+'LOG '+d['tem']+'.txt',time_now+' Фолловмод выключен\n')

@bot.event
async def event_message(ctx):
    time_now = time.strftime('%H:%M:%S', time.localtime())

    #tim = str(time_now)
    U_m = ctx.author.name + ': ' + ctx.content
    print(U_m)
    antf = 1
    antb = 1
    
    mesag = ctx.content.lower()
    autor = str(ctx.author.name.lower())

    tem = d['tem']
    if not d['tem'] == time.strftime('%Y-%m-%d', time.localtime()):
        d['tem'] = time.strftime('%Y-%m-%d', time.localtime())
        tem = d['tem']
        for chan in bot.initial_channels:
            chan = chan.replace('#','')

    chan = str(ctx.channel)

    dir_chan = 'LOG/LOG '+tem+'/'+str(chan)+'/'
    if not os.path.exists(dir_chan):
        os.makedirs(dir_chan)


    dir_user_log = dir_chan+'/'+ctx.author.name+'.txt'
    dir_chan_log = dir_chan+'LOG '+tem+'.txt'
    mute_log = dir_chan+'MUTE_BAN LOG '+tem+'.txt'
    
    addfile(dir_user_log,time_now+' '+U_m+'\n')
    addfile(dir_chan_log,time_now+' '+U_m+'\n')
    mt = mesag.split(' ')

    if mesag.startswith('!anime') :
        las = time0(time_now)-time0(last['anim'+str(ctx.channel)])
        doanim = -1
        if ctx.author.type == 'mod' or 'badges=broadcaster' in ctx.raw_data:
            doanim = 1
        elif las > 5 or las < 0:
            doanim = 1
        if doanim == 1:
            nom = ''
            last['anim'+str(ctx.channel)] = time_now
            t2 = -2
            t1 = mesag.replace('!anime ','')
            try:
                t2 = int(t1)
                nom = 'Под номером '+str(t2)+' сейчас: '
            except:
                pass
            inp = open(dirlist,'r',encoding='utf8')
            t = inp.readlines()
            inp.close()
            #print(t2!=-2 and t2>0 and t2<=len(t))
            #print(t2 == -2)
            #print(t2<=0)
            #print(t2>len(t))
            #print(len(t))
            if t2>len(t):
                nom = 'В списке сейчас '+str(len(t))+', попробуйте ещё раз.'
                await ctx.channel.send(f'@'+ctx.author.name+' '+nom)
            elif t2!=-2 and t2>0:
                await ctx.channel.send(f'@'+ctx.author.name+' '+nom+t[t2-1])
            elif t2 == -2:
                li = listedit(dirlist,mesag.replace('!anime ',''),'найти')
                if li!='-1':
                    await ctx.channel.send(f'@'+ctx.author.name+' '+t[int(li)]+' Сейчас под номером ('+str(int(li)+1)+'/'+str(len(t))+')')
                else:
                    await ctx.channel.send(f'@'+ctx.author.name+' Такое название не найдено')
            elif t2<=0:
                await ctx.channel.send(f'@'+ctx.author.name+' Попробуйте ввести номер больше нуля -_-')
            
            last['anim'+str(ctx.channel)] = time_now

    if mesag.startswith('!elo'):
        if dconf[chan+'_elo']=='1':
        #if 'hubibich' in chan or 'hubbich' in chan or 'kujijiepuk' in chan:

            doelo = -1
            las = time0(time_now)-time0(last['elo'+str(ctx.channel)])
            if ctx.author.type == 'mod' or 'badges=broadcaster' in ctx.raw_data:
                doelo = 1
            elif las > 5 or las < 0:
                doelo = 1
            if doelo == 1:
                #print(dconf['elo_'+chan])
                
                #nik = 'hubbich'
                t2 = []
                t2 = dconf['elo_'+chan]
                nik = t2[0]
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
            if 'hubbich' in chan:
                m1 = 'help + команда выдаст подробности. Команды: !anime+название "help", "botf" , "botm" , "botb", "botelo", "boti "+ник'
                await ctx.channel.send(f''+m1+' @'+ctx.author.name)
            if 'hubibich' in chan:
                m1 = 'help + команда выдаст подробности. Команды: "help", "botf" , "botm" , "botb", "botelo", "boti "+ник'
                await ctx.channel.send(f''+m1+' @'+ctx.author.name)
            elif chan+'_i' in dconf:
                m1 = 'help + команда выдаст подробности. Команды: "help", "botf", "botb", "botelo", "boti "+ник'
                await ctx.channel.send(f''+m1+' @'+ctx.author.name)
            else:
                m1 = 'help + команда выдаст подробности. Команды: "help", "botelo", "botb" антиботфлуд, "botf" антифлуд'
                await ctx.channel.send(f''+m1+' @'+ctx.author.name)
        if mesag.startswith('help'):
            las = time0(time_now)-time0(last['help'+str(ctx.channel)])
            if las > 3 or las < 0:
                last['help'+str(ctx.channel)] = time.strftime('%H:%M:%S', time.localtime())
                if 'botf' in mesag:
                    m1 = 'Это режим антифлуда. Если недавно (от одного пользователя) было отправленно много коротких сообщений или много одинаковых, то после предупреждения выдастся мут (если есть модерка)'
                    await ctx.channel.send(f''+m1+' @'+ctx.author.name)
                elif 'botb' in mesag:
                    m1 = 'Это режим антиботов. Если набирается несколько одинаковых сообщений от разных пользователей, ставится режим только для фолловеров, так же выключает его через 90 секунд (если есть сообщения в чате) нужна модерка'
                    await ctx.channel.send(f''+m1+' @'+ctx.author.name)
                elif 'boti' in mesag:
                    m1 = 'Добавляет пользователя в список игнора, тоесть при включенном режиме антифлуда ему не будет выдаваться предупреждения и мут'
                    await ctx.channel.send(f''+m1+' @'+ctx.author.name)
                elif 'botm' in mesag:
                    m1 = 'Переключает режим заказа и скипа музыки для ручного добавления (на всякий случай)'
                    await ctx.channel.send(f''+m1+' @'+ctx.author.name)
                elif 'botelo' in mesag:
                    m1 = 'Включает/Выключает команду !elo, так же если написать "botelo "+ник на faceit, он установится как стандартный'
                    await ctx.channel.send(f''+m1+' @'+ctx.author.name)
                elif 'anime' in mesag:
                    m1 = '!anime + <название> Выводит актуальную информацию об аниме (номер в списке)'
                    await ctx.channel.send(f''+m1+' @'+ctx.author.name)
                else:
                    m1 = 'Основные (невыключаемые) функции это муты: за рекламу накрутки (стандартную), за запретные на твиче слова (п,н,д), за что-то типа "зайдите на стрим" (требуется модерка)'
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
        if mesag == 'botelo':
            ch = chan+'_elo'
            if not ch in dconf:
                dconf[ch] = '1'
            if dconf[ch] == '1':
                dconf[ch] = '0'
                stat = 'выключен'
            elif dconf[ch] == '0':
                dconf[ch] = '1'
                stat = 'включен'
            await ctx.channel.send(f'!elo '+stat+' @'+ctx.author.name)
            confre(dirconf,ch,dconf[ch])

        elif mesag.startswith('botelo'):
            temp = str(ctx.content)
            temp = temp.replace('botelo','')
            temp = temp.replace('@','')
            if len(temp)>1:
                t1 = temp.split(' ')
                t1.remove('')
                temp = temp.replace(' ','')
            nick = temp.lower()
            if len(nick)<=1 or len(t1)>1:
                await ctx.channel.send(f'Ошибка, попробуйте ещё раз @'+ctx.author.name)
            else:
                ch = 'elo_'+chan
                templ = dconf['elo_'+chan]
                #print(dconf['elo_'+chan])
                if not nick in templ:
                    #print(nick)
                    if nick not in dconf['elo_'+chan]:
                        t1 = dconf['elo_'+chan]
                        confignore(dirconf,ch,t1[0])
                        templ.remove(t1[0])
                    #templ = nick
                    await ctx.channel.send(nick+' добавлен как стандарт в !elo @'+ctx.author.name)  
                    dconf['elo_'+chan].append(nick)
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
            las = time0(time_now)-time0(last['bot'+str(ctx.channel)])
            if las > 25 or las < 0:
                m1 = 'Команды:'
                if dconf[chan+'_elo']=='1':
                    m1 = ' !elo'
                if 'hubbich' in chan:
                    m1+=' !anime + название'
                if m1 != 'Команды:':
                    await ctx.channel.send(f''+m1+' @'+ctx.author.name)
                else:
                    m1 = 'Доступных на канале команд, нет'
                    await ctx.channel.send(f''+m1+' @'+ctx.author.name)
                last['bot'+str(ctx.channel)] = time.strftime('%H:%M:%S', time.localtime())


    if  autor in dconf[chan+'_i']:
        antf = 0

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

    elif 'даун' in mt or 'нигер' in mt or 'дауны' in mt or 'даунов' in mt:
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


    #   БЛОК ВСЕХ НАГРАД
    if ctx.author.reward != 'Empty':
        if ctx.author.reward == '2499dbb9-7630-436c-8e0f-98d64b6822ae' and 'hubibich' in str(ctx.channel):
            t0 = re.findall(r'\s*([a-z\d_-]+)\s*',mesag)
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
            t0 = mreq(t1)
            time.sleep(delay)
            await ctx.channel.send(f''+t0)
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
            t0 = mreq(t1)
            t0=t0.replace('!sr ','')
            if 'youtu' in t0:
                time.sleep(delay)
                await ctx.channel.send(f'!removesong '+t0)
            else:
                time.sleep(delay)
                await ctx.channel.send(f'!skip')
            last['sk'+str(ctx.channel)] = time.strftime('%H:%M:%S', time.localtime())

        doli = -1
        t1 = ''
        if ctx.author.reward == 'abfb912f-0502-4c67-a7da-5afacbddd7ee' or ctx.author.reward == '68490923-e11a-4a88-8731-b74811e831ea':
            comment = 'добавить'
            editn = 'Добавлено'
            doli = 1
        if ctx.author.reward == '1225ec90-a7c3-413a-8120-b8bcd210c45e':
            comment = 'поднять'
            editn = 'Поднято'
            doli = 1
        if ctx.author.reward == '303c8930-6972-4649-8129-012bf2ec396e':
            if not 'фильм' in str(ctx.content).lower():
                t1 = 'Фильм '
            comment = 'добавить'
            editn = 'Добавлен'
            doli = 1
        if ctx.author.reward == 'f24a0b06-53be-4d35-a753-3609e3943da7':
            comment = 'опустить'
            editn = 'Опущено'
            doli = 1
        if ctx.author.reward == '7257f8f9-f9d7-46b6-87bb-0be8feb5850e':
            comment = 'удалить'
            editn = 'Удалено'
            doli = 1
        if doli == 1:
            t2 = -2
            spis = ' Текущий список уточняйте у @KuJIJIePuK, или через !anime'
            if comment == 'добавить':                
                li = listedit(dirlist,t1+str(ctx.content)+' ('+str(ctx.author.display_name)+')',comment)
                inp = open(dirlist,'r',encoding='utf8')
                t = inp.readlines()
                inp.close()
                nom = ' ('+str(int(li)+1)+'/'+str(len(t))+')'
                t1 = t1+str(ctx.content)+' ('+str(ctx.author.display_name)+')'
                await ctx.channel.send(f''+t1+' '+editn+nom+' @'+ctx.author.name+spis)
            elif comment == 'удалить':
                li = listedit(dirlist,str(ctx.content),comment)
                if not 'фильм' in li:
                    await ctx.channel.send(f''+li+' '+editn+' @'+ctx.author.name+spis)
                else:
                    await ctx.channel.send(f''+li+' '+'Удалён'+' @'+ctx.author.name+spis)
            else:
                li = listedit(dirlist,str(ctx.content),comment)
                try:
                    t2 = int(li)
                except:
                    await ctx.channel.send(f'Ошибка, свяжитесь с @KuJIJIePuK'+' @'+ctx.author.name)
                if t2!=-2 and t2!=-1:
                    inp = open(dirlist,'r',encoding='utf8')
                    t = inp.readlines()
                    inp.close()
                    nom = ' ('+str(t2+1)+'/'+len(t)+')'
                    await ctx.channel.send(f''+t[t2]+' '+editn+nom+' @'+ctx.author.name+spis)

        #   abfb912f-0502-4c67-a7da-5afacbddd7ee    заказ аниме на основе
        #   68490923-e11a-4a88-8731-b74811e831ea    заказ аниме на втором
        #   1225ec90-a7c3-413a-8120-b8bcd210c45e    перенос вверх
        #   f24a0b06-53be-4d35-a753-3609e3943da7    перенос вниз
        #   7257f8f9-f9d7-46b6-87bb-0be8feb5850e    скип аниме/игры
        #   303c8930-6972-4649-8129-012bf2ec396e    Заказ фильма/аниме фильма
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
        t1 = re.sub('[!@#$%^&*(),.?<>]','',temp)
        d[ctx.author.name+'0'] = time_now+' '+temp
        dl[ctx.author.name] = time_now+' '+t1
        #print(dl)
        if df(dl,t1,time_now)>=5 and dconf[chan+'_b'] == '1' and temp!= '!play':
            await ctx.channel.followers()
            addfile(dir_chan_log,'Фолловмод включен''\n')
            last['fol'+chan]=str(time_now)
            for key, value in dict(dl).items():
                if value == temp:
                    del dl[key]

        if last['fol'+chan]!='00 00 00' and dconf[chan+'_b'] == '1':
            ti = time0(time_now)-time0(last['fol'+chan])
            if ti>=90 or ti<0:
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
            if 'snivanov' in chan:
                tempmuterep = 9
            else:
                tempmuterep = 7

            if mutef == tempmuterep and len(mess[0])<10 and tim[0]-tim[1]<=8:
                muteflood = 0
            elif mutef > tempmuterep and len(mess[0])<10 and tim[0]-tim[1]<=8:
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
            if len(t2)<=3:
                tempmuterep+=3

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
                print('Мут '+ctx.author.name+' за '+res+' на '+str(mute_time)+' в '+time_now)
                addfile(dir_chan_log,'Мут '+ctx.author.name+' за '+res+' на '+str(mute_time)+'\n')
                addfile(dir_user_log,'Мут '+ctx.author.name+' за '+res+' на '+str(mute_time)+'\n')

#@bot.command(name='test')
#async def test(ctx):
#    await ctx.send('test passed!')

if __name__ == '__main__':
    bot.run()