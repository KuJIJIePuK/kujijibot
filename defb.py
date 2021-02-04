import time
import os
from kujdef import *
from hht import *

def bot_com(mesag,aut,chan,is_mod,is_str,last,dir_list,dir_list_log,dirconf,dconf,time_now):
    au = aut.lower()
    intime_now = time0(time.strftime('%H:%M:%S', time.localtime()))
    m1 = 'Ошибка'
    if is_mod == 1:
        if mesag == 'bot':
            m1 = 'Команды: "help", "botf" , "botm" , "botb", "botelo", "boti "+ник'
            if is_str == 1:
                m1 = 'Команды: "!add", "!del", "!swap", "help", "botf" , "botm" , "botb", "botelo", "boti "+ник'
            return m1
        if mesag.startswith('help'):
            las = intime_now-time0(last['help'+chan])
            if las > 3 or las < 0:
                last['help'+chan] = time.strftime('%H:%M:%S', time.localtime())
                if mesag == 'help':
                    m1 = 'https://kujijiepuk.fun/bot'
                elif 'botf' in mesag:
                    m1 = 'Это режим антифлуда. Если недавно (от одного пользователя) было отправленно много коротких сообщений или много одинаковых, то после предупреждения выдастся мут (если есть модерка)'
                elif 'botb' in mesag:
                    m1 = 'Это режим антиботов. Если набирается несколько одинаковых сообщений от разных пользователей, ставится режим только для фолловеров, так же выключает его через 90 секунд (если есть сообщения в чате) нужна модерка'
                elif 'boti' in mesag:
                    m1 = 'Добавляет пользователя в список игнора, тоесть при включенном режиме антифлуда ему не будет выдаваться предупреждения и мут'
                elif 'botm' in mesag:
                    m1 = 'Переключает режим заказа и скипа музыки для ручного добавления (на всякий случай)'
                elif 'botelo' in mesag:
                    m1 = 'Включает/Выключает команду !elo, так же если написать "botelo "+ник на faceit, он установится как стандартный'
                elif 'anime' in mesag:
                    m1 = '!anime + <название/номер> Выводит актуальную информацию об аниме (номер в списке)'
                elif 'rew' in mesag:
                    m1 = 'Для инициализации наград за баллы (например мут на 10 минут, заказ/скип музыки (через !sr)) нужно в сообщении с заказом награды написать bot_init_sr'
                else:
                    mr = 'ошибка'
                return m1
        if mesag.startswith('boti'):
            temp = mesag
            temp = temp.replace('boti','')
            temp = temp.replace('@','')
            if len(temp)>1:
                t1 = temp.split(' ')
                t1.remove('')
                temp = temp.replace(' ','')
            nick = temp.lower()
            if len(nick)<=1 or len(t1)>1:
                m1 = 'Ошибка, попробуйте ещё раз'
                return m1
            else:
                templ = dconf[chan+'_i']
                if not nick in templ:
                    templ.append(nick)
                    m1 = nick+' добавлен в список игнора антифлуда'
                else:
                    templ.remove(nick)
                    m1 = nick+' удалён из списка игнора антифлуда'
                ch = chan+'_i'
                confignore(dirconf,ch,nick)
                return m1
        doc = 0
        if mesag == 'botelo':
            ch = chan+'_elo'            
            m1 = '!elo '
            doc = 1

        elif mesag.startswith('botelo'):
            temp = mesag
            temp = temp.replace('botelo','')
            temp = temp.replace('@','')
            if len(temp)>1:
                t1 = temp.split(' ')
                t1.remove('')
                temp = temp.replace(' ','')
            nick = temp.lower()
            if len(nick)<=1 or len(t1)>1:
                m1 = 'Ошибка, попробуйте ещё раз'
                return m1
            else:
                ch = 'elo_'+chan
                templ = dconf['elo_'+chan]
                if not nick in templ:
                    if nick not in dconf['elo_'+chan]:
                        t1 = dconf['elo_'+chan]
                        confignore(dirconf,ch,t1[0])
                        templ.remove(t1[0])
                    dconf['elo_'+chan].append(nick)
                    confignore(dirconf,ch,nick)
                    m1 = nick+' добавлен как стандарт в !elo'
                    return m1
        if mesag == 'botf':
            ch = chan+'_f'
            m1 = 'Антифлуд '
            doc = 1
        elif mesag == 'botb':
            ch = chan+'_b'
            m1 = 'Антиботфлуд '
            doc = 1
        elif mesag == 'botm':
            ch = chan+'_m'
            m1 = 'Заказ/скип музыки '
            doc = 1

        if doc==1:
            if dconf[ch] == '1':
                dconf[ch] = '0'
                stat = 'выключен'
            elif dconf[ch] == '0':
                dconf[ch] = '1'
                stat = 'включен'
            confre(dirconf,ch,dconf[ch])
            m1+=stat
            return m1

    else:
        if mesag == 'bot':
            las = intime_now-time0(last['bot'+chan])
            if las > 25 or las < 0:
                m1 = 'Команды:'
                if dconf[chan+'_elo']=='1':
                    m1 += ' !elo'
                if os.path.isfile(dir_list):
                    m1+=' !список, !swap, "!мои"'
                if m1 == 'Команды:':
                    m1 = 'Доступных на канале команд, нет'
                last['bot'+chan] = time.strftime('%H:%M:%S', time.localtime())
            return m1

    if os.path.isfile(dir_list):
        if is_str==1:
            if mesag.startswith('!del '):
                li = listedit(dir_list,mesag.replace('!del ',''),'удалить')
                tosite(chan)                
                addfile(dir_list_log,time_now+' '+aut+': '+mesag+' ('+'удалить'+')\n')
                addfile(dir_list_log,li+' '+'удалено'+'\n')
                if li!='-1':
                    m1 = ' '+li+' удалено'
                else:
                    m1 = 'В списке не найдено!'

                return m1
            if mesag.startswith('!add '):
                li = listedit(dir_list,mesag.replace('!add ',''),'добавить')
                tosite(chan)                
                addfile(dir_list_log,time_now+' '+aut+': '+mesag+' ('+'добавить'+')\n')
                addfile(dir_list_log,mesag.replace('!add ','')+' '+'добавлено'+'\n')
                m1 = ' '+mesag.replace('!add ','')+' добавлено'
                return m1

        if mesag.startswith('!swap'):
            doswap = 0
            las = intime_now-time0(last['swap'+chan])
            if is_str == 1:
                doswap = 1
            elif las > 10 or las < 0:
                doswap = 1
            if doswap == 1:
                try:
                    inp = open(dir_list,'r',encoding='utf8')
                    t = inp.readlines()
                    inp.close()
                except:
                    m1 = 'Ошибка'
                    return m1
                er = 0
                t1 = mesag.replace('!swap ','')
                t1 = t1.split(' ')
                if len(t1)!=2:
                    er = 1
                else:
                    try:
                        ti = int(t1[0])
                        tj = int(t1[1])
                        if ti>0 and ti<len(t)-1 and tj>0 and tj<=len(t)-1:
                            er = 0
                        else:
                            er = 1
                    except:
                        er = 1
                        pass
                if er!=1:
                    if au in t[ti].lower() and au in t[tj].lower():
                        tif = 1
                    else:
                        tif = -1
                    if tif == 1 or is_str == 1:
                        t[ti],t[tj]=t[tj],t[ti]

                        inp = open(dir_list,'w',encoding='utf8')
                        for l in t:
                            inp.write(l)
                        inp.close()
                        tosite(chan)                        
                        addfile(dir_list_log,time_now+' '+aut+': '+mesag+' (swap)\n')
                        addfile(dir_list_log,'Готово\n')
                        m1 = 'Готово @'+au
                        return m1
                    else:
                        if is_serv==0:
                            print(au)
                            print(t[ti])
                            print(t[tj])                        
                        addfile(dir_list_log,time_now+' '+aut+': '+mesag+' (swap)\n')
                        addfile(dir_list_log,'чужой заказ\n')
                        m1 = 'Менять местами можно только свои заказы @'+au
                        return m1
                if er == 1:                    
                    addfile(dir_list_log,time_now+' '+aut+': '+mesag+' (swap)\n')
                    addfile(dir_list_log,'Ошибка запроса\n')
                    m1 = 'Пример: "!swap 1 2" @'+au
                    return m1
                last['swap'+chan] = time_now

        if mesag.startswith('!list') or mesag.startswith('!список') or mesag.startswith('!anime') or mesag == '!мои' :
            las = intime_now-time0(last['anim'+chan])
            doanim = -1
            if is_mod:
                doanim = 1
            elif las > 5 or las < 0:
                doanim = 1
            if doanim == 1:
                try:
                    inp = open(dir_list,'r',encoding='utf8')
                    t = inp.readlines()
                    inp.close()
                except:
                    m1 = 'Ошибка, список не найден, свяжитесь с KuJIJIePuK @'+au
                    return m1
                if mesag == '!мои':
                    li = listedit(dir_list,str(au),'найти')
                    if len(li)>0:
                        t2 = ''
                        nom = ''
                        for t1 in li:
                            if is_serv==0:
                                print(nom)
                            nom = ' ('+str(t1)+'/'+str(len(t)-1)+')'
                            t2 += t[t1].replace('\n','')+' '+nom+'; '
                        m1 = t2
                        return m1
                    else:
                        m1 = 'Сейчас нет ваших заказов @'+au
                        return m1
                if mesag == '!anime' or mesag == '!list' or mesag == '!список':
                    m1 = ' Полный список: https://kujijiepuk.fun/lists/'+chan+'/'
                elif mesag.startswith('!anime') or mesag.startswith('!список') or mesag.startswith('!list'):
                    nom = ''
                    last['anim'+chan] = time_now
                    t2 = -2
                    t1 = mesag.replace('!anime ','')
                    t1 = t1.replace('!list ','')
                    t1 = t1.replace('!список ','')
                    try:
                        t2 = int(t1)
                        if t2 == 0:
                            nom = 'Сейчас: '
                        else:
                            nom = 'Под номером '+str(t2)+' сейчас: '
                    except:
                        pass
                    if t2>len(t)-1:
                        nom = 'В списке сейчас '+str(len(t)-1)+', попробуйте ещё раз.'
                        m1 = ' '+nom
                    elif t2!=-2 and t2>=0:
                        m1 = ' '+nom+t[t2]
                    elif t2 == -2:
                        li = listedit(dir_list,t1,'найти')
                        if li!='-1':
                            m1 = ' '+t[int(li[0])]+' Сейчас под номером ('+str(int(li[0]))+'/'+str(len(t)-1)+')'
                        else:
                            m1 = ' Такое название не найдено'
                    elif t2<0:
                        m1 = ' Попробуйте ввести номер больше -_-'                    
                last['anim'+chan] = time_now
                return m1

    if mesag.startswith('!elo'):
        if dconf[chan+'_elo']=='1':
            doelo = -1
            las = intime_now-time0(last['elo'+chan])
            if is_mod == 1:
                doelo = 1
            elif las > 5 or las < 0:
                doelo = 1
            if doelo == 1:
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
                    m1 = ' Elo '+nik+' = '+str(delo)
                else:
                    m1 = ' Ошибка, ник не найден'
                last['elo'+chan] = time_now
                return m1

    return m1