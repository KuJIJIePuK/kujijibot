import re
from datetime import datetime
import time
import os
from twitchio.ext import commands
from urllib.request import urlopen, Request

from variables import *

from kuji_http import *
from kuji_defs import *
from kuji_commands import *
from kuji_rewards import *
from kuji_sec import *
#import itertools

bot = commands.Bot(
    irc_token=token,
    client_id=idc,
    nick='kujijibot',
    prefix='k',
    initial_channels=ichan
)

creator = 'kujijiepuk'

dconf = {}
d = {}
dl = {}
last = {}
dmax = 8

list_not_log = ['melharucos','olyashaa','y0nd']

list_bot = ['moobot','nightbot','mikuia','wizebot','kujijibot','nyan_rab','rutonybot','mirrobot','ananonymouscheerer']
list_com = ['botsp','!rename','help','bot','botb','botf','botm','botelo','boti','!anime','!список','!list','!del','!add','!elo','!swap','!мои']

list_ban = []

#for ban in list_banwords_0:
#    a = []
    #print(ban)
#    for ch in ban:
#        a.append(Lett[ch])
#    for l in itertools.product(*a):
#        tban = ''.join(l)
#        if not tban in list_ban:
#            list_ban.append(tban)
list_f_0 = []
for s in list_banwords_0:
    if s[0] in Lett:
        for w in Lett[s[0]]:
            list_f_0.append(w[0])
    else:
        list_f_0.append(s[0])

list_f_1 = []
for s in list_banwords_1:
    if s[0] in Lett:
        for w in Lett[s[0]]:
            list_f_1.append(w[0])
    else:
        list_f_1.append(s[0])

nakrlist = []
nakrlist.append('clck follow')
nakrlist.append('привет хочу предложить тебе накрутку')
nakrlist.append('подними стрим')
nakrlist.append('pleace youtube')
nakrlist.append('plsss open')
nakrlist.append('streаmdеtаilsbot')
nakrlist.append('зайди стрим')
nakrlist.append('зайдите стрим')
nakrlist.append('ez raccattack ezfollow https://tinyurl.com/ezfollow')
nakrlist.append('buy followers')
i = -1
while i<len(nakrlist)-1:
    i+=1
    nakrlist[i]=set(nakrlist[i].split(' '))



dirrew = 'rewards.cfg'
dirconf = 'bot.cfg'

d['tem'] = time.strftime('%Y-%m-%d', time.localtime())
tem = time.strftime('%Y-%m-%d', time.localtime())
#if not os.path.exists('LOG/LOG '+tem+'/'+str(chan)+'/'):
#    os.makedirs('LOG/LOG '+tem+'/'+str(chan)+'/')

dict_rew = {}
dict_rew['_mute'] = 'tempmute'
dict_rew['_sr'] = 'request'
dict_rew['_skip'] = 'skip'
dict_rew['_ladd'] = 'listadd'
dict_rew['_lrem'] = 'listrem'
dict_rew['_lup'] = 'listup'
dict_rew['_ldown'] = 'listdown'
dict_rew['_end'] = 'end'

list_rew = ['_mute','_sr','_skip','_ladd','_lrem','_lup','_ldown','_end']
for t in list_rew:
    dict_rew[dict_rew[t]] = []
#print(dict_rew)

if not os.path.exists(dirrew):
    inp = open(dirrew,'w',encoding='utf8')
    inp.write('tempmute\nrequest\nskip\nlistadd\nlistrem\nlistup\nlistdown\nend')
    inp.close()
if os.path.exists(dirrew):
    inp = open(dirrew,'r',encoding='utf8')
    t = inp.readlines()
    inp.close()
    j = -1
    i = -1
    while j<len(list_rew)-1:
        j+=1
        #print(dict_rew[list_rew[i+1]])
        #print(t[i+1])
        while i<len(t)-2 and not dict_rew[list_rew[j+1]] in t[i+1]:
            i+=1
            t1 = t[i].split(' ')
            t_list = []
            t_list = dict_rew[dict_rew[list_rew[j]]]
            t_list.append(t1[0])
        #print(list_rew[j])

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
        list_init_conf = ['_f','_b','_m','_elo','_spoil']
        for t in list_init_conf:
            ch = chan+t
            if ch not in dconf:
                dconf[ch] = '0'
                confre(dirconf,ch,dconf[ch])
        ch = 'elo_'+chan
        if ch not in dconf:
            dconf[ch] = []
            dconf[ch].append(chan)
            confignore(dirconf,ch,chan)
        ch = chan+'_i'
        if ch not in dconf:
            dconf[ch] = []
            confignore(dirconf,ch,'kujijibot')

        list_init_last = ['elo','sr','sk','fol','bot','help','anim','swap','renam','spoil']
        for t in list_init_last:
            if t+chan not in last:
                last[t+chan] = '00 00 00'


@bot.event
async def event_raw_data(data):
    if 'custom-reward-id=' in data:
        time_now = time.strftime('%H:%M:%S', time.localtime())
        di = 'LOG/LOG '+d['tem']+'/'+'REWARD LOG'+'.txt'
        if os.path.isfile(di):
            addfile(di,time_now+': '+data+'\n')
    if 'followers-only=' in data:
        time_now = time.strftime('%H:%M:%S', time.localtime())
        t0 = re.findall(r'followers-only=([-0-9]+)',data)
        if t0:
            t1 = re.findall(r'ROOMSTATE #([\w_-]+)[\b]*',data)
            if os.path.exists('LOG/LOG '+d['tem']+'/'+t1[0]):
                #os.makedirs('LOG/LOG '+d['tem']+'/'+t1[0])
                if t0[0] == '0':
                    last['fol'+t1[0]]=str(time_now)
                    addfile('LOG/LOG '+d['tem']+'/'+t1[0]+'/'+'LOG '+d['tem']+'.txt',time_now+' Фолловмод включен\n')

                elif t0[0] == '-1':
                    last['fol'+t1[0]]='00 00 00'
                    addfile('LOG/LOG '+d['tem']+'/'+t1[0]+'/'+'LOG '+d['tem']+'.txt',time_now+' Фолловмод выключен\n')

@bot.event
async def event_message(ctx):
    time_now = time.strftime('%H:%M:%S', time.localtime())
    intime_now = time0(time_now)
    
    chan = str(ctx.channel)
    
    author_disp = str(ctx.author.display_name)
    author = author_disp.lower()
    mes = ctx.content
    mesag = ctx.content.lower()



    U_m = author + ': ' + ctx.content

    is_serv = 0
    is_mod = 0
    is_str = 0
    if ctx.author.type == 'mod':
        is_mod = 1
    if author == chan or author == creator:
        is_str = 1
        is_mod = 1

    if os.path.exists('/home/admin/web/kujijiepuk.fun/public_html/'):
        is_serv = 1
    if is_serv==0:
        print(U_m)
    antf = 1
    antb = 1


    tem = d['tem']
    if not d['tem'] == time.strftime('%Y-%m-%d', time.localtime()):
        d['tem'] = time.strftime('%Y-%m-%d', time.localtime())
        tem = d['tem']
    

    dir_chan = 'LOG/LOG '+tem+'/'+str(chan)+'/'
    if not os.path.exists(dir_chan):
        os.makedirs(dir_chan)

    dir_list = 'lists/'+chan+'/list.txt'
    dir_list_log = 'lists/'+chan+'/list_LOG.txt'
    
    dir_user_log = dir_chan+'/'+author+'.txt'
    dir_chan_log = dir_chan+'LOG '+tem+'.txt'
    mute_log = dir_chan+'MUTE_BAN LOG '+tem+'.txt'
    dir_bug_log = dir_chan+'MUTE BUG LOG '+tem+'.txt'

    if chan not in list_not_log:
        addfile(dir_user_log,time_now+' '+U_m+'\n')
    elif author == 'kujijibot':
        addfile(dir_user_log,time_now+' '+U_m+'\n')
    addfile(dir_chan_log,time_now+' '+U_m+'\n')

    



    if author == creator:
        if mesag == 'fol':
            if last['fol'+chan]=='00 00 00':
                await ctx.channel.followers()
                last['fol'+chan]=time_now
                addfile(dir_chan_log,'Фолловмод включен''\n')
            else:
                await ctx.channel.followersoff()
                last['fol'+chan]='00 00 00'
                addfile(dir_chan_log,'Фолловмод выключен''\n')
        if mesag == 'upd':
            tosite(chan)
            await ctx.channel.send(f'@'+author+' Готово')
        if mesag.startswith('мут '):
            t1 = mesag.replace('мут ','')
            t2 = t1.split(' ')
            if '@' in t2[0]:
                t2[0] = t2[0].replace('@','')
            nik = t2[0]
            t3 = t1.replace(nik+' ','')
            t2 = t3.split(' ')            
            if t3.startswith(' '):
                t3 = t3.replace(' ','')
            try:
                mtime = int(t2[0])
                t3 = t3.replace(t2[0],'')
            except:
                mtime = 600
            await ctx.channel.timeout(nik, mtime,t3)

    i = -1
    r = 0
    while i<len(list_com)-1 and r == 0:
        i+=1
        com = list_com[i]
        if com in mesag:
            if author not in list_bot:
                m1 = bot_com(mes,author_disp,chan,is_mod,is_str,last,dir_list,dir_list_log,dirconf,dconf,time_now)
                if m1!='Ошибка':
                    await ctx.channel.send(f''+m1)
                    r = 1

    if is_mod == 1 or author in list_bot:
        antf = 0
    if  author in dconf[chan+'_i']:
        antf = 0
    act = ''

    #result = re.sub('[%&,.<>()?]','',mes)
    result = re.sub('[%&,.<>()?⠀⌜-]','',mes)
    result = result.split(' ')
    while '' in result:
        result.remove('')
    #t = ''.join(result)
    #res = [t]

    
    spoil = 0
    j = 0
    list_spoiler = ['сезон','сери']
    temp = rasp_full(result,list_spoiler,Lett)
    if temp != 0:
        spoil = 1

    list_spoiler = ['съедят','съест','умрёт','выживет','убьёт','получит','выиграет','убьют','станет','станут','дохнет','сдела','будет']
    for t in list_spoiler:
        list_temp = [t]
        temp = rasp_full(result,list_temp,Lett)
        if temp != 0:
            j+=1

    if spoil == 1 and j>=1:
        if dconf[chan+'_spoil'] == '1':
            if chan!='kujijiepuk':
                m_time = 600
            else:
                m_time = 3
            act = 'Мут '
            res = ' за спойлер в '
            comm = 'спойлер?'
            if ctx.author.reward != 'Empty':
                ctx.author.reward = 'Empty'
        addfile('Rasp.txt','СПОЙЛЕР: '+mes+'\n\n')


    temp = raspoz_word(result,list_banwords_0,list_f_0,Lett)
    if temp!= 0:
        addfile('Rasp.txt',temp+'\n\n')

    
    temp_w = rasp_full(result,list_banwords_0,Lett)
    temp_white = rasp_full(result,list_white_0,Lett)
    if temp_w!=0 and temp_white==0:
        if chan!='kujijiepuk':
            m_time = 600
        else:
            m_time = 3
        act = 'Мут '
        res = ' за запретку в '
        comm = 'гц'
        if ctx.author.reward != 'Empty':
            ctx.author.reward = 'Empty'
        stop = 1

    if temp_white==0 and temp_w!=0:
        for w in temp_w:
            addfile('Rasp.txt',w+' ')
        addfile('Rasp.txt','\n\n')

    neban = 0

    
    if temp != 0 and neban == 0:
        for wor in list_white_0:
            if wor in temp:
                neban = 1
        if chan!='kujijiepuk':
            m_time = 600
        else:
            m_time = 3
        act = 'Мут '
        res = ' за запретку в '
        comm = 'гц'
        if ctx.author.reward != 'Empty':
            ctx.author.reward = 'Empty'
        stop = 1
        #except:
        #    pass
    temp = raspoz_word(result,list_banwords_1,list_f_1,Lett)
    if temp!= 0:
        addfile('Rasp.txt',temp+'\n\n')
    temp_w = rasp_full(result,list_banwords_1,Lett)
    temp_white = rasp_full(result,list_white_1,Lett)
    if temp_w!=0 and temp_white==0:
        if chan!='kujijiepuk':
            m_time = 600
        else:
            m_time = 3
        act = 'Мут '
        res = ' за запретку в '
        comm = 'гц'
        if ctx.author.reward != 'Empty':
            ctx.author.reward = 'Empty'
        stop = 1
    if temp_white==0 and temp_w!=0:
        for w in temp_w:
            addfile('Rasp.txt',w+' ')
        addfile('Rasp.txt','\n')
    if act == '':
        neban = 0    
        if temp != 0 and neban == 0:
            for wor in list_white_1:
                if wor in temp:
                    neban = 1
            if chan!='kujijiepuk':
                m_time = 30
            else:
                m_time = 2
            comm = 'э чо твориш'
            act = 'Мут '
            res = ' за запретку в '
            stop = 1
            if ctx.author.reward != 'Empty':
                ctx.author.reward = 'Empty'

    
    #mt = re.sub('[!@#$%^&*,.?()<>]','',mesag)
    #mt = mt.split(' ')
    mt = result
    #if 'пидор' in mt or 'pidor' in mt or 'пидар' in mt or 'pidar' in mt or 'пидарас' in mt or 'педик' in mt or 'Пiдо₽@с' in mt:
    #    await ctx.channel.timeout(author, 600,'гц')
    #    act = ' Мут '
    #    res = ' за запретку в '
        
    #if 'даун' in mt or 'нигер' in mt or 'дауны' in mt or 'даунов' in mt or 'нигир' in mt:
    #    await ctx.channel.timeout(author, 60,'э чо твориш')
    #    act = 'Мут '
    #    res = ' за запретку в '


    if not 'классные зpители' in mesag and not 'веди диалог' in mesag:
        setmes = mesag.lower()
        setmes = re.sub('[!@#$%^&*,.?()<>]','',setmes)
        setmes = set(setmes.split(' '))
        for t in nakrlist:
            t2 = list(t & set(setmes))
            if len(t2)/len(t)>0.65:
                act = 'Мут '
                res = ' за рекламу в '
                m_time = 600
                comm = 'Реклама?'
    if act =='':
        if 'clck' in mesag and 'follow' in mesag:
            print(mesag)
            act = 'Мут '
            res = ' за рекламу в '
            m_time = 600
            comm = 'Реклама?'

    if act != '':
        if is_serv == 0:
            print(author+' '+act+res+time_now)
        addfile(dir_chan_log,act+author+res+time_now+'\n')
        addfile(dir_user_log,act+author+res+time_now+'\n')
        addfile(dir_bug_log,act+author+res+time_now+'\n')
        addfile(dir_bug_log,time_now+' '+U_m+'\n\n')
    
    if act == 'Мут ':
        await ctx.channel.timeout(author, m_time,comm)

    if 'bot_init' in mesag:
        if is_mod:
            if ctx.author.reward == 'Empty':
                m1 = ' Нужно прописать это при заказе награды'
                await ctx.channel.send(f'@'+author+m1)
            else:
                dorew = 1
                temp = 'end'
                inp = open(dirrew,'r',encoding='utf8')
                t = inp.readlines()
                inp.close()
                t_mesag = mesag.replace('bot_init','')
                if t_mesag in dict_rew:
                    dorew = 1
                    t_list = []
                    t_list = dict_rew[dict_rew[t_mesag]]
                    temp = dict_rew[t_mesag]
                    if not ctx.author.reward in t_list:
                        t_list.append(ctx.author.reward)
                    else:
                        t_list.remove(ctx.author.reward)
                else:
                    dorew = -1
                    await ctx.channel.send(f'@'+author+' Ошибка. Нет такой инициализации')
                if dorew == 1:
                    t = rew_conf(dirrew,temp,ctx.author.reward,chan,author)
                    if t == 1:
                        await ctx.channel.send(f'@'+author+' Награда добавлена в конфиг')
                    elif t == 0:
                        await ctx.channel.send(f'@'+author+' Награда удалена из конфига')

    #   БЛОК ВСЕХ НАГРАД
    m_reward = ctx.author.reward
    if m_reward != 'Empty':
        if not 'bot_init' in mesag:
            t_list = dict_rew[dict_rew['_mute']]
            if ctx.author.reward in t_list:
                t0 = re.findall(r'\t*([a-z\d_-]+)\t*',mesag)
                muted = 'ошибка'
                temp = mesag.split(' ')
                for t1 in temp:
                    if '@' in t1:
                        t0[0]=t1.replace('@','')
                try:
                    muted = t0[0]
                except:
                    return
                await ctx.channel.timeout(muted, 600,'За баллы')
                if is_serv==0:
                    print (muted+' Получил мут за баллы в '+time_now+' от '+author)
                addfile('LOG/LOG '+tem+'/'+str(ctx.channel)+'/'+muted+'.txt',muted+' Получил мут за баллы в '+time_now+' от '+author+'\n')
                addfile(dir_chan_log,muted+' Получил мут за баллы в '+time_now+' от '+author+'\n')
            else:
                m1 = bot_rewards(mes,author_disp,chan,time_now,m_reward,is_mod,is_str,dict_rew,last,intime_now,dir_list,dir_list_log)
                if m1!='Ошибка':
                    await ctx.channel.send(f''+m1)
    chan = str(ctx.channel)


        #   abfb912f-0502-4c67-a7da-5afacbddd7ee    заказ аниме на основе
        #   68490923-e11a-4a88-8731-b74811e831ea    заказ аниме на втором
        #   1225ec90-a7c3-413a-8120-b8bcd210c45e    перенос вверх
        #   f24a0b06-53be-4d35-a753-3609e3943da7    перенос вниз
        #   7257f8f9-f9d7-46b6-87bb-0be8feb5850e    скип аниме/игры
        #   303c8930-6972-4649-8129-012bf2ec396e    Заказ фильма/аниме фильма
    #   Запись всех сообщений в дневник (dmax = кол-во последних сообщений пользователя)
    mesag = ctx.content.lower()
    if not 'fanjqiwehnqugvjklbanjikncvoiuquifo' in mesag:
        user = chan+'_'+author
        if not user in d:
            d[user] = []

        intime_now = time0(time_now)
        mesw = re.sub('[!@#$%^&*(),.?<>]','',mesag)

        dl[user] = time_now+' '+mesw

        mess = d[user]
        if len(mess)<dmax:
            mess.append(time_now+' '+mesag)
        elif len(mess)>=dmax:
            mess.remove(mess[0])
            mess.append(time_now+' '+mesag)
        tim = []
        i = -1
        while i<len(mess)-1:
            i+=1
            tim.append(time0(mess[i]))
        end = -1
        i = len(mess)
        while i>0 and end==-1:
            i-=1
            t1 = intime_now-tim[i]
            if t1<0:
                t1 = 301
            if t1>=300:
                j = i+1
                while j>0:
                    j-=1
                    mess.remove(mess[j])
                end = 1

        if df(dl,mesw,time_now,chan+'_')>=6 and mesag!= '!play':
            if dconf[chan+'_b'] == '1':
                await ctx.channel.followers()
                last['fol'+chan]=str(time_now)
            if not os.path.exists('/home/admin/web/kujijiepuk.fun/public_html/lists/hubbich/'):
                print('Включен фоловмод')
            addfile(dir_chan_log,str(time_now)+'Фолловмод включен''\n')
            for key, value in dict(dl).items():
                if mesag in value:
                    del dl[key]

        if last['fol'+chan]!='00 00 00':
            ti = intime_now-time0(last['fol'+chan])
            if ti>=90 or ti<0:
                if dconf[chan+'_b'] == '1':
                    await ctx.channel.followersoff()
                    last['fol'+chan]='00 00 00'
                    addfile(dir_chan_log,str(time_now)+'Фолловмод выключен''\n')

        mute_time = 15
        mutef = 0
        muter = 0
        muteflood = -1
        muterep = -1

        i = len(mess)
        while i>0:
            i-=1
            if tim[len(mess)-1]-tim[i]<=30:
                temp = mess[i]
                temp = temp[9:]
                if tim[i]-tim[i-1]>=0:
                    if len(temp)<10 and tim[i]-tim[i-1]<4:
                        mutef+=1
                        if i>=2 and tim[i]-tim[i-2]<7 and tim[i]-tim[i-2]>=0:
                            mutef+=1
                    if len(temp)<10 and tim[i]-tim[i-1]<5:
                        mutef+=1

        #if 'snivanov' in chan:
        #    tempmuterep = 13
        #else:
        tempmuterep = 10
        temp = mess[0]
        temp = temp[9:]
        if mutef == tempmuterep and len(temp)<10 and tim[0]-tim[1]<=8:
            muteflood = 0
        elif mutef > tempmuterep and len(temp)<10 and tim[0]-tim[1]<=8:
            muteflood = 1


        i = len(mess)-1
        j = i
        ti0 = mess[i].split(' ')
        ti0.remove(ti0[0])
        ti0l = len(ti0)
        ti0 = set(ti0)

        while i>0:
            i-=1

            ti = mess[i].split(' ')
            ti.remove(ti[0])
            til = len(ti)
            ti = set(ti)

            t2 = list(set(ti) & set(ti0))
            tt = max(ti0l,til)

            tim_ij = tim[j]-tim[i]

            if max(len(ti0),len(ti))/min(ti0l,til)<0.3:
                if tim_ij<=60:
                    muter+=1
            if len(t2)/tt>=0.65 and len(ti0)>=1:
                if tim_ij<=5:
                    muter+=3
                elif tim_ij<=30:
                    muter+=2
                elif tim_ij<=60:
                    muter+=1
                j = i

        #if 'snivanov' in chan:
        #    tempmuterep = 8
        #else:
        tempmuterep = 6
        if len(t2)<=3:
            tempmuterep+=3
        #print('muter = '+str(muter))
        if muter>=2:
            t1 = mess[0].split(' ')
            t3 = list(set(t2) & set(t1))
            if muter==tempmuterep:
                muterep = 0
            elif muter > tempmuterep:
                muterep = 1
        if not author+'mf' in last:
            last[author+'mf'] = 0

        if mutef>last[author+'mf']:
            last[author+'mf']=mutef
        else:
            last[author+'mf']=mutef
            if muteflood == 1:
                muteflood = 0

        if not author+'mr' in last:
            last[author+'mr'] = 0

        if muter>last[author+'mr']:
            last[author+'mr']=muter
        else:
            last[author+'mr']=muter
            if muterep == 1:
                muterep = 0

        #print(d)
        #print(mutef)
        #print(muter)
        if not author+'p' in d:
            d[author+'p'] = '00.00.00'

        #print(d[author+'p'])
        if intime_now-time0(d[author+'p']+chan)<=300 and muterep == 0:
            muterep = -1
        elif intime_now-time0(d[author+'p']+chan)>60 and muterep == 1:
            muterep = 0
        elif intime_now-time0(d[author+'p']+chan)<=300 and muteflood == 0:
            muteflood = -1
        elif intime_now-time0(d[author+'p']+chan)>60 and muteflood == 1:
            muteflood = 0

        if muteflood == 1 or muterep == 1:
            if os.path.isfile(mute_log):
                inp = open(mute_log,'r',encoding='utf8')
                for line in inp:
                    if author in line:
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
                await ctx.channel.send(f''+mess+author)
            d[author+'p'] = time_now
            if is_serv==0:
                print('Предупреждение '+author+' за '+res+' в '+time_now)
            addfile(dir_chan_log,'Предупреждение '+author+' за '+res+' на '+str(mute_time)+'\n')
            addfile(dir_user_log,'Предупреждение '+author+' за '+res+' на '+str(mute_time)+'\n')
            addfile(dir_bug_log,'Предупреждение '+author+' за '+res+' на '+str(mute_time)+'\n'+'mutef = '+str(mutef)+'  muter = '+str(muter)+'\n')
            mesl = d[user]
            i = -1
            while i < len(mesl)-1:
                i+=1
                addfile(dir_bug_log,mesl[i]+'\n')
            addfile(dir_bug_log,'\n')



        if muteflood == 1 or muterep == 1:
            if muteflood == 1:
                res = 'флуд'
            elif muterep == 1:
                res = 'повторы'          
            if dconf[chan+'_f'] == '1' and antf == 1:
                await ctx.channel.timeout(author, mute_time,'Узбагойся ('+res+')')
                d[author+'p'+chan] = time_now
                i = dmax
            #while i>1:
            #    i-=1
            #    if author+str(i)+chan in d:
            #        del d[author+str(i)+chan]
            d[author+'p'+chan] = '00.00.00'
            if is_serv==0:
                print('Мут '+author+' за '+res+' на '+str(mute_time)+' в '+time_now)
            addfile(dir_chan_log,'Мут '+author+' за '+res+' на '+str(mute_time)+'\n')
            addfile(dir_user_log,'Мут '+author+' за '+res+' на '+str(mute_time)+'\n')
            addfile(dir_bug_log,'Мут '+author+' за '+res+' на '+str(mute_time)+'\n'+'mutef = '+str(mutef)+'  muter = '+str(muter)+'\n')
            mesl = d[user]
            i = -1
            while i < len(mesl)-1:
                i+=1
                addfile(dir_bug_log,mesl[i]+'\n')
            addfile(dir_bug_log,'\n')
            del d[user]

#@bot.command(name='test')
#async def test(ctx):
#    await ctx.send('test passed!')

if __name__ == '__main__':
    bot.run()