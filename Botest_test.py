import re
from datetime import datetime
import time
import os
from twitchio.ext import commands
from urllib.request import urlopen, Request
from variables import *
bot = commands.Bot(
    irc_token=token,
    client_id=idc,
    nick='kujijibot',
    prefix='k',
    initial_channels=ichan
)
ignorlist = ['inge_moon','oxxyfox_','kujijiepuk','uni_dima']
d = {}
dl = {}
last = {}
tem = time.strftime("%Y-%m-%d", time.localtime())

inp = open('bot.cfg',"r",encoding='utf8')
t = inp.readlines()
inp.close()
for line in t:
    l = []
    line = line.replace('\n','')
    t1 = line.split(' ')
    t2 = t1[0]
    if len(t1)>1:
        if t1[1] == '0' or t1[1] == '1':
            d[t1[0]]=t1[1]
        else:
            exec('global '+t1[0])
            exec(t1[0]+' = []')
            exec('l = '+t1[0])
            for w in t1:
                if w!=t1[0]:
                    l.append(w)
            #print(l)
            d[t2] = '1'
    elif t2[len(t2)-1]=='i':
        exec('global '+t2)
        exec(t2+' = []')
        #exec('print('+t2+')')
        d[t2] = '0'
    #print(l)

#print(hubibichi)
for chan in bot.initial_channels:
    chan = chan.replace('#','')
    if chan+'i' not in d:
        d[str(chan)+'i'] = '1'
        exec('global '+chan+'i')
        exec(chan+'i = []')

        #print(chan+'i')
        #exec('print('+chan+'i)')
    #print(l)

#print(hubbich)




def time0(s):
    return (int(s[0:2])*60*60+int(s[3:5])*60+int(s[6:8]))

def addfile(dir,m):
    inp = open(dir,"a",encoding='utf8')
    inp.write(m)
    inp.close()
    return
def coun(l,s,j):
    i = 0
    for s1 in l:
        if s in s1:
            if not len(s1)>len(s)+j:
                i+=1
    return i
def df(d,s):
    i = 0
    for t in d:
        if d[t]==s:
            i+=1
            del d[t]
    return i
#   followers-only=0
#   followers-only=-1
@bot.event
async def event_raw_data(data):
    if 'followers-only=0' in data:
        time_now = time.strftime("%H:%M:%S", time.localtime())
        last['fol'+chan]=str(time_now)
    elif 'followers-only=-1' in data:
        time_now = time.strftime("%H:%M:%S", time.localtime())
        last['fol'+chan]='00 00 00'




@bot.event
async def event_ready():
    ws = bot._ws  # this is only needed to send messages within event_ready
    #await _websocket.send(f"PRIVMSG #kujijiepuk :.w kujijiepuk hello\r\n")
    #await ws.send_privmsg('kujijiepuk', ".w kujijiepuk has landed!")
    'Called once when the bot goes online.'
    for chan in bot.initial_channels:
        chan = chan.replace('#','')
        print(f"MainBot Подключился к "+chan)
        if chan+'f' not in d:
            d[str(chan)+'f'] = 1
            inp = open('bot.cfg',"a",encoding='utf8')
            inp.write(chan+'f 1\n')
            inp.close()
        last['elo'+chan] = '00 00 00'
        last['sr'+chan] = '00 00 00'
        last['sk'+chan] = '00 00 00'
        last['fol'+chan] = '00 00 00'


    #print(f"MainBot Подключился")

@bot.event
async def event_message(ctx):
    time_now = time.strftime("%H:%M:%S", time.localtime())
    tim = str(time_now)
    U_m = ctx.author.name + ': ' + ctx.content
    print(U_m)
   # print()
    antf = 1
    antb = 1
    chan = str(ctx.channel)
    mesag = ctx.content.lower()
    autor = str(ctx.author.name.lower())
    if not os.path.exists('LOG/LOG '+tem+'/'+str(ctx.channel)+'/'):
        os.makedirs('LOG/LOG '+tem+'/'+str(ctx.channel)+'/')

    dir_user_log = 'LOG/LOG '+tem+'/'+str(ctx.channel)+'/'+ctx.author.name+'.txt'
    dir_chan_log = 'LOG/LOG '+tem+'/'+str(ctx.channel)+'/'+'LOG '+tem+'.txt'
    mute_log = 'LOG/LOG '+tem+'/'+str(ctx.channel)+'/'+'MUTE_BAN LOG '+tem+'.txt'
    addfile(dir_user_log,time_now+' '+U_m+'\n')
    addfile(dir_chan_log,time_now+' '+U_m+'\n')
    mt = mesag.split(' ')

    #print(mesag)
    if mesag.startswith('!elo'):
        if 'hubibich' in chan or 'hubbich' in chan:
            if time0(time_now)-time0(last['elo'+str(ctx.channel)]) > 5:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
                reg_url = "https://faceitelo.net/player/"
                t2 = []
                t2 = re.findall(r'!elo (\S+)',mesag)
                if t2:
                    t2 = re.findall(r'!elo (\S+)',mesag)
                    reg_url+=t2[0]
                    nik = t2[0]
                else:
                    reg_url+='hubbich'
                    nik = 'hubbich'
                req = Request(url=reg_url, headers=headers)
                try:
                    html = urlopen(req).read()
                    html = str(html)
                    t1 = re.findall(r'<td><strong>(\S+)</strong><br>',html)
                    last['elo'+str(ctx.channel)] = time_now
                    try:
                        await ctx.channel.send(f'@'+ctx.author.name+' Elo '+nik+' = '+str(t1[0]))
                    except:
                        return
                except:
                    last['elo'+str(ctx.channel)] = time_now
                    await ctx.channel.send(f'@'+ctx.author.name+' Ошибка, ник не найден')


    if 'kujijiepuk' in autor:
        if mesag == 'fol':
            if last['fol'+chan]=='00 00 00':
                await ctx.channel.followers()
                last['fol'+chan]=tim
            else:
                await ctx.channel.followersoff()
                last['fol'+chan]='00 00 00'


    if ctx.author.type == 'mod' or 'badges=broadcaster' in ctx.raw_data or 'kujijiepuk' in autor and not 'kujijibot' in autor:
        antf = 0
        #author = ctx.message.author
        
        if mesag == 'bot': #in ctx.content: #and not 'botf' in ctx.content:
            #if d[chan+'f'] == '1':
                #ws = bot._ws  # this is only needed to send messages within event_ready
                #await ws.send_privmsg('kujijiepuk', '.w '+autor+' "botf" чтобы выключить антифлуд, "boti "+ник (можно через @) добавить/удалить ник из списка игнора антифлуда (не будет предупреждений и таймаутов)')
                #await ctx.channel.send('.w '+autor+' "botf" чтобы выключить антифлуд, "boti "+ник (можно через @) добавит/удалит ник из списка игнора антифлуда (не будет предупреждений и таймаутов)')
            if 'hubibich' in chan:
                await ctx.channel.send(f'Команды: "botf" , "botm" , "boti "+ник (можно через @)  @'+ctx.author.name)
            else:
                await ctx.channel.send(f'Команды: "botf" включить/выключить антифлуд @'+ctx.author.name)
                #await ctx.channel.send(f'Напишите "botf" чтобы выключить антифлуд @'+ctx.author.name)
            #elif d[chan+'f'] == '0':
                #await ctx.send_privmsg(autor, '"botf" чтобы выключить антифлуд, "boti "+ник (можно через @) добавить/удалить ник из списка игнора антифлуда (не будет предупреждений и таймаутов)')
                #await client.send_message(ctx.message.author, '"botf" чтобы включить антифлуд, "boti "+ник (можно через @) добавит/удалит ник из списка игнора антифлуда (не будет предупреждений и таймаутов)')
                #await ctx.channel.send(f'Команды: "botf" , "botm" , "boti "+ник (можно через @)  @'+ctx.author.name)
                #await ctx.channel.send(f'Напишите "botf" чтобы включить антифлуд @'+ctx.author.name)
            #await ctx.channel.send(f'Напишите "botf" чтобы переключить режим @'+ctx.author.name)
        if mesag.startswith('boti'):
            temp = str(ctx.content)
            temp = temp.replace('boti','')
            temp = temp.replace('@','')
            if len(temp)>1:
                t1 = temp.split(' ')
                t1.remove('')
                temp = temp.replace(' ','')
            if len(temp)<=1 or len(t1)>1:
                await ctx.channel.send(f'Ошибка, попробуйте ещё раз @'+ctx.author.name)
            else:
                temp = temp.lower()
                if 'hubibich' in chan:
                    templ = hubibichi
                elif 'snivanov' in chan:
                    templ = snivanovi
                elif 'tvoyvladik' in chan:
                    templ = tvoyvladiki
                #print(templ)
                if not temp in templ:
                    templ.append(temp)
                    await ctx.channel.send(temp+' добавлен в список игнора антифлуда @'+ctx.author.name)
                else:
                    templ.remove(temp)
                    await ctx.channel.send(temp+' удалён из списка игнора антифлуда @'+ctx.author.name)
                inp = open('bot.cfg',"r",encoding='utf8')
                t = inp.readlines()
                inp.close()
                inp = open('bot.cfg',"w",encoding='utf8')
                j1 = '-1'
                for line in t:
                    if chan+'i' in line:
                        line = chan+'i'
                        for n in templ:
                            line+=' '+n
                        line+='\n'
                        line = line.lower()
                        j1 = '1'
                    inp.write(line)
                if j1 == '-1':
                    line = chan+'i'
                    if len(templ)>0:
                        for n in templ:
                            line += ' '+n
                    line+='\n'
                    line = line.lower()
                    inp.write(line)
                inp.close()
        if mesag == 'botf':
            #print(d)
            if d[chan+'f'] == '1':
                d[chan+'f'] = '0'
                await ctx.channel.send(f"Антифлуд выключен @"+ctx.author.name)
            elif d[chan+'f'] == '0':
                d[chan+'f'] = '1'
                await ctx.channel.send(f"Антифлуд включен @"+ctx.author.name)
            inp = open('bot.cfg',"r",encoding='utf8')
            t = inp.readlines()
            inp.close()
            inp = open('bot.cfg',"w",encoding='utf8')
            for line in t:
                if chan+'f' in line:
                    #print(line)
                    if '0' in line:
                        line = line.replace('0','1')
                    elif '1' in line:
                        line = line.replace('1','0')
                inp.write(line)
            inp.close()

        if mesag == 'botm':
            #print(d)
            if d[chan+'m'] == '1':
                d[chan+'m'] = '0'
                await ctx.channel.send(f"Заказ/скип музыки выключен @"+ctx.author.name)
            elif d[chan+'m'] == '0':
                d[chan+'m'] = '1'
                await ctx.channel.send(f"Заказ/скип музыки включен @"+ctx.author.name)
            inp = open('bot.cfg',"r",encoding='utf8')
            t = inp.readlines()
            inp.close()
            inp = open('bot.cfg',"w",encoding='utf8')
            for line in t:
                if chan+'m' in line:
                    #print(line)
                    if '0' in line:
                        line = line.replace('0','1')
                    elif '1' in line:
                        line = line.replace('1','0')
                inp.write(line)
            inp.close()
            #print(d)
    #print(ctx.channel)
    #try:
    #    exec('k = '+chan)
    #except NameError:
    #    exec(chan+' = []')
    #    exec('k = '+chan)
    



    if 'hubibichi' in d:        
        if  autor in hubibichi:
            #print('ignor')
            antf = 0
            antb = 0

    if  autor == 'kujijiepuk' or  autor == 'streamelements' or  autor == 'moobot' or  autor == 'nightbot' or autor == 'mikuia':
        antf = 0
    

    

    #re.findall(r'v=([\w-]+)[&?]',t1)

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
        await ctx.channel.timeout(ctx.author.name, 600,"конч?")
        print("Бан "+ctx.author.name+" за запретку в "+time_now)
        addfile(mute_log,"Мут "+ctx.author.name+" за запретку в "+time_now+"\n")        
        addfile(dir_chan_log,"Мут "+ctx.author.name+" за запретку в "+time_now+"\n")
        addfile(dir_user_log,"Мут "+ctx.author.name+" за запретку в "+time_now+"\n")

    #elif 'пидор' in mesag or 'пидар' in mt or 'pidor' in mt or 'yapi_dor' in mesag or 'ya_pidor' in mesag or 'yapid_or' in mesag:
        #await ctx.channel.ban(ctx.author.name, "конч?")
    #    await ctx.channel.timeout(ctx.author.name, 600,"конч?")
    #    print("Бан "+ctx.author.name+" за запретку в "+time_now)
    #    addfile(mute_log,"Мут "+ctx.author.name+" за запретку в "+time_now+"\n")        
    #    addfile(dir_chan_log,"Мут "+ctx.author.name+" за запретку в "+time_now+"\n")
    #    addfile(dir_user_log,"Мут "+ctx.author.name+" за запретку в "+time_now+"\n")
    elif 'даун' in mt or 'нигер' in mt :
        #await ctx.channel.ban(ctx.author.name, "конч?")
        await ctx.channel.timeout(ctx.author.name, 30,"э чо твориш")
        print("Бан "+ctx.author.name+" за запретку в "+time_now)
        addfile(mute_log,"Мут "+ctx.author.name+" за запретку в "+time_now+"\n")        
        addfile(dir_chan_log,"Мут "+ctx.author.name+" за запретку в "+time_now+"\n")
        addfile(dir_user_log,"Мут "+ctx.author.name+" за запретку в "+time_now+"\n")

    if not os.path.isfile(mute_log):
        inp = open(mute_log,"a",encoding='utf8')
        inp.close()

    

    #   pleace youtube anakralı namık çiçeğim gelsene pleaceeee sounddddd baby
    #   https://www.youtube.com/watch?v=vMZ9_uHAGGc plsss open
    

    if antb == 1:
        if 'clck' in mesag and 'follow' in mesag or 'StreаmDеtаilsВot' in mesag:
            await ctx.channel.timeout(ctx.author.name, 600,"Реклама накрутки?")
            #await ctx.channel.ban(ctx.author.name, "Реклама накрутки?")
            print (ctx.author.name+" Получил мут за рекламу накрутки в "+time_now)
            addfile(dir_user_log,"Мут за рекламу накрутки\n")
            addfile(dir_chan_log,autor+"Получил мут за рекламу накрутки в "+time_now+"\n")
    if antb == 1:
        if 'pleace' in mesag and 'youtube' in mesag or 'plsss' in mesag and 'open' in mesag:
            await ctx.channel.timeout(ctx.author.name, 600,"Реклама?")
            #await ctx.channel.ban(ctx.author.name, "Реклама накрутки?")
            print (ctx.author.name+" Получил мут за рекламу в "+time_now)
            addfile(dir_user_log,"Мут за рекламу\n")
            addfile(dir_chan_log,autor+"Получил мут за рекламу в "+time_now+"\n")

    if ctx.author.reward == '2499dbb9-7630-436c-8e0f-98d64b6822ae' and 'hubibich' in str(ctx.channel):
        t0 = re.findall(r'([a-z\d-]+)',mesag)
        muted = 'ошибка'
        try:
            muted = t0[0]
        except:
            return
        await ctx.channel.timeout(muted, 600,"За баллы")
        print (muted+" Получил мут за баллы в "+time_now+' от '+ctx.author.name)
        addfile('LOG/LOG '+tem+'/'+str(ctx.channel)+'/'+muted+'.txt',muted+" Получил мут за баллы в "+time_now+' от '+ctx.author.name+"\n")
        addfile(dir_chan_log,muted+" Получил мут за баллы в "+time_now+' от '+ctx.author.name+"\n")


    if ctx.author.reward == '70e76278-57d5-4989-a2e3-bafc14c3cc73' and 'hubibich' in str(ctx.channel):
        t1 = str(ctx.content)
        if time0(time_now)-time0(last['sr'+str(ctx.channel)]) > 3:
            delay = 0
        else:
            delay = 4
        #if t1.find('&list')!=-1:
        #    t1 = t1[0:t1.find('&list')]
        if 'youtu' in t1:
            #print(t1)
            if "v=" in t1 :
                if not '?v=' in t1:
                    t2 = re.findall(r'v=([\w-]+)[&?]',t1)
                    t1 = t2[0]
                    t0 = 'youtu.be/'+t1
                elif 'v=' in t1:
                    t2 = re.findall(r'v=([\w-]+)',t1)
                    #print(t2)
                    t1 = t2[0]
                    t0 = 'youtu.be/'+t1       
            elif 'youtu.be/' in t1 and '?' in t1 or '&' in t1:
                t2 = re.findall(r'youtu.be/([\w-]+)[?&\s]',t1)
                t1 = t2[0]
                t0 = 'youtu.be/'+t1
            else:
                t0 = t1.replace('https://','')
            time.sleep(delay)
            await ctx.channel.send(f"!sr "+t0)            
            last['sr'+str(ctx.channel)] = time.strftime("%H:%M:%S", time.localtime())
            
        else:
            if '!sr' in ctx.content.lower():
                time.sleep(delay)
                await ctx.channel.send(f""+t1)
                last['sr'+str(ctx.channel)] = time.strftime("%H:%M:%S", time.localtime())
            time.sleep(delay)
            await ctx.channel.send(f"!sr "+t1)
            last['sr'+str(ctx.channel)] = time.strftime("%H:%M:%S", time.localtime())

    if ctx.author.reward == '9972db1c-8d86-4b96-8c23-a490315fb41b' and 'hubibich' in str(ctx.channel):
        t1 = str(ctx.content)
        if time0(time_now)-time0(last['sk'+str(ctx.channel)]) < 2:
            await ctx.channel.send(f"2 скипа сразу, упс")
            return            
        elif time0(time_now)-time0(last['sk'+str(ctx.channel)]) > 3:
            delay = 0
        else:
            delay = 4

        #if t1.find('&list')!=-1:
        #    t1 = t1[0:t1.find('&list')]
        if 'youtu' in t1:
            #print(t1)
            if "v=" in t1 :
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
            await ctx.channel.send(f"!removesong "+t0)
            last['sr'+str(ctx.channel)] = time.strftime("%H:%M:%S", time.localtime())
        else:
            time.sleep(delay)
            await ctx.channel.send(f"!skip")
            last['sr'+str(ctx.channel)] = time.strftime("%H:%M:%S", time.localtime())
        #   "https://www.youtube.com/watch?v=WXt4JB2fSo4"
        #   "https://youtu.be/RByn3on_vW8?list=PLk-PFZMi8NjtCy3jiHtHXYI1h1-JTDkJp"
        #   "https://www.youtube.com/watch?v=RByn3on_vW8&list=RDRByn3on_vW8&start_radio=1"
        #   "https://www.youtube.com/watch?list=PLk-PFZMi8NjtCy3jiHtHXYI1h1-JTDkJp&v=RByn3on_vW8&feature=youtu.be"
        
            #"https://www.youtube.com/watch?v=qQ3ZVmXNgt0&list=PLPwC7kBDPgD8stUQKOnEKOfJCTUG40MSE&index=2"
            #"youtu.be/qQ3ZVmXNgt"

                #if t1.find('&',t1.)
            #if "youtu.be/" in t1:

        #   "youtu.be/RByn3on_vW8"

        #   "youtu.be/lQBtXEAAkLU"
        #if t1.find('?list')!=-1:
        #    t1 = t1[0:t1.find('&list')]

    #   9972db1c-8d86-4b96-8c23-a490315fb41b        СКИП ТРЕКА
    #   70e76278-57d5-4989-a2e3-bafc14c3cc73        МУЗЫКА БЕЗ ОЧЕРЕДИ
    #   2499dbb9-7630-436c-8e0f-98d64b6822ae        МУТ ЛЮБОМУ


    #print(d[chan+'f'])
    #print(antf)
    if not 'fanjqiwehnqugvjklbanjikncvoiuquifo' in mesag:
        #print(d)
        tim = [0,0,0,0,0]
        mess = ['','','','','']
        i = 5
        while i>1:
            i-=1
            if ctx.author.name+str(i-1) in d:
                d[ctx.author.name+str(i)] = d[ctx.author.name+str(i-1)]
        temp = ctx.content.lower()
        d[ctx.author.name+'0'] = time_now+" "+temp
        dl[ctx.author.name] = temp

        if df(d,temp)>=5:
            await ctx.channel.followers()
            last['fol'+chan]=str(tim)

        #print(time_now)
        #print(last['fol'+str(ctx.channel)])
        if last['fol'+str(ctx.channel)]!='00 00 00':
            if time0(time_now)-time0(last['fol'+str(ctx.channel)])>=90:
                await ctx.channel.followersoff()
                last['fol'+chan]='00 00 00'



        i = -1
        while i<4:
            i+=1
            if ctx.author.name+str(i) in d:
                tim[i] = time0(d[ctx.author.name+str(i)])
                t = d[ctx.author.name+str(i)]
                mess[i] = t[9:]

        i = 5
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
            while i<5:
                i+=1
                if ctx.author.name+str(i+1) in d:
                    if len(mess[i])<10 and tim[i]-tim[i+1]<4:
                        if ctx.author.name+str(i+2) in d and tim[i]-tim[i+2]<7:
                            mutef+=1
                    if len(mess[i])<10 and tim[i]-tim[i+1]<5:
                        mutef+=1
            if mutef == 4 and len(mess[0])<10 and tim[0]-tim[1]<=8:
                muteflood = 0
            elif mutef > 4 and len(mess[0])<10 and tim[0]-tim[1]<=8:
                muteflood = 1
            #if mutef<last[chan+'m']:
                
            #last[chan+'mf']=mutef

            #print(mute)
            #print(muteflood)

            
            i = -1
            #print(mess)
            while i<4: #and mess[i]!='':
                #print(i)
                i+=1
                j = i
                if mess[i]!='':
                    ti = mess[i].split(' ')
                    ti1 = len(ti)
                    ti = set(ti)
                while j<4: #and mess[j]!='':
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
                    #print(muter)
            if 'snivanov' in chan:
                tempmuterep = 3
            else:
                tempmuterep = 3

            #print(mute)

            if muter>=2:
                t1 = mess[0].split(' ')
                t3 = list(set(t2) & set(t1))
                if muter==tempmuterep: #and len(t3)>2:
                    muterep = 0
                elif muter > tempmuterep: #and len(t3)>2:
                    muterep = 1
                #elif mute==3 and len(t3)>2:
                #    muterep = 0
                #elif mute > 3 and len(t3)>2:
                #    muterep = 1
            
            #print(muterep)

                #print('mute = '+str(mute))
            #if mute==2 and tempm in mess[0] and len(tempm)>10:
            #    muterep = 0
            #elif mute > 2 and tempm in mess[0] and len(tempm)>10:
            #    muterep = 1
            #elif mute==3 and tempm in mess[0] and len(tempm)<=10:
            #    muterep = 0
            #elif mute > 3 and tempm in mess[0] and len(tempm)<=10:
            #    muterep = 1

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
                



            #print(muterep)
            if time0(time_now)-time0(d[ctx.author.name+'p'])<=300 and muterep == 0:
                muterep = -1
            elif time0(time_now)-time0(d[ctx.author.name+'p'])>60 and muterep == 1:
                muterep = 0
            elif time0(time_now)-time0(d[ctx.author.name+'p'])<=300 and muteflood == 0:
                muteflood = -1
            elif time0(time_now)-time0(d[ctx.author.name+'p'])>60 and muteflood == 1:
                muteflood = 0
            #print(muterep)
            #print(d[ctx.author.name+'p'])
            #print(last)
            #print(muter)
            #print(muterep)

            if muteflood == 1 or muterep == 1:
                inp = open(mute_log,"r",encoding='utf8')
                for line in inp:
                    if ctx.author.name in line:
                        mute_time = mute_time * 2
                inp.close()

            if muteflood == 0:
                if d[chan+'f'] == '1' and antf == 1:
                    await ctx.channel.send(f"Будешь так флудить, отхватишь таймаут @"+ctx.author.name)
                d[ctx.author.name+'p'] = time_now
                print("Предупреждение "+ctx.author.name+" за флуд на "+str(mute_time)+' в '+time_now)
                addfile(dir_chan_log,"Предупреждение "+ctx.author.name+" за флуд на "+str(mute_time)+"\n")
                addfile(dir_user_log,"Предупреждение "+ctx.author.name+" за флуд на "+str(mute_time)+"\n")
            elif muteflood == 1:
                if d[chan+'f'] == '1' and antf == 1:
                    await ctx.channel.timeout(ctx.author.name, mute_time,"Узбагойся (флуд)")
                    addfile(mute_log,ctx.author.name+" в "+time_now+" после : "+ctx.content+"\n")
                print("Мут "+ctx.author.name+" за флуд на "+str(mute_time)+' в '+time_now)
                addfile(dir_chan_log,"Мут "+ctx.author.name+" за флуд на "+str(mute_time)+"\n")
                addfile(dir_user_log,"Мут "+ctx.author.name+" за флуд на "+str(mute_time)+"\n")
                i = 5
                while i>1:
                    i-=1
                    if ctx.author.name+str(i) in d:
                       del d[ctx.author.name+str(i)]
                d[ctx.author.name+'p'] = '00.00.00'
                #print(d[ctx.author.name+str(0)])
                
            elif muterep == 0:
                if d[chan+'f'] == '1' and antf == 1:
                    await ctx.channel.send(f"Ещё раз повторишь, отхватишь таймаут @"+ctx.author.name)
                d[ctx.author.name+'p'] = time_now
                print("Предупреждение "+ctx.author.name+" за повторы на "+str(mute_time)+' в '+time_now)
                addfile(dir_chan_log,"Предупреждение "+ctx.author.name+" за повторы на "+str(mute_time)+"\n")
                addfile(dir_user_log,"Предупреждение "+ctx.author.name+" за повторы на "+str(mute_time)+"\n")
            elif muterep == 1:
                if d[chan+'f'] == '1' and antf == 1:
                    await ctx.channel.timeout(ctx.author.name, mute_time,"Узбагойся (повтор)")
                    addfile(mute_log,ctx.author.name+" в "+time_now+" после : "+ctx.content+"\n")
                print("Мут "+ctx.author.name+" за повторы на "+str(mute_time)+' в '+time_now)
                addfile(dir_chan_log,"Мут "+ctx.author.name+" за повторы на "+str(mute_time)+"\n")
                addfile(dir_user_log,"Мут "+ctx.author.name+" за повторы на "+str(mute_time)+"\n")
                i = 5
                while i>1:
                    i-=1
                    if ctx.author.name+str(i) in d:
                        del d[ctx.author.name+str(i)]
                d[ctx.author.name+'p'] = '00.00.00'
                #print(d[ctx.author.name+str(0)])



#@bot.command(name='test')
#async def test(ctx):
#    await ctx.send('test passed!')

if __name__ == "__main__":
    bot.run()