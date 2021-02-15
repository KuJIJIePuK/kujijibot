import time
import os
from kuji_defs import *
from kuji_http import *

def bot_com(mes,aut,chan,is_mod,is_str,last,dir_list,dir_list_log,dirconf,dconf,time_now):
    mesag = mes.lower()
    au = aut.lower()
    intime_now = time0(time.strftime('%H:%M:%S', time.localtime()))
    m1 = 'Ошибка'
    if is_mod == 1:
        if mesag == 'bot':
            m1 = 'Команды: "help", "botsp", "botf" , "botm" , "botb", "botelo", "boti "+ник'
            if is_str == 1:
                m1 = 'Команды: "!rename", "!up", "!add", "!del", "!swap", "help", "botsp", "botf" , "botm" , "botb", "botelo", "boti "+ник'
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
                m1 = 'Ошибка, попробуйте ещё раз'+' @'+au
                return m1
            else:
                templ = dconf[chan+'_i']
                if not nick in templ:
                    templ.append(nick)
                    m1 = nick+' добавлен в список игнора антифлуда'+' @'+au
                else:
                    templ.remove(nick)
                    m1 = nick+' удалён из списка игнора антифлуда'+' @'+au
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
                m1 = 'Ошибка, попробуйте ещё раз'+' @'+au
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
                    m1 = nick+' добавлен как стандарт в !elo'+' @'+au
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
        elif mesag == 'botsp':
            ch = chan+'_spoil'
            m1 = 'Антиспойлер '
            doc = 1

        if doc==1:
            if dconf[ch] == '1':
                dconf[ch] = '0'
                stat = 'выключен'
            elif dconf[ch] == '0':
                dconf[ch] = '1'
                stat = 'включен'
            confre(dirconf,ch,dconf[ch])
            m1+=stat+' @'+au
            return m1

    else:
        if mesag == 'bot':
            las = intime_now-time0(last['bot'+chan])
            if las > 25 or las < 0:
                m1 = 'Команды:'
                if dconf[chan+'_elo']=='1':
                    m1 += ' !elo'
                if os.path.isfile(dir_list):
                    m1+=' !список, "!мои", !swap, !rename'
                if m1 == 'Команды:':
                    m1 = 'Доступных на канале команд, нет'
                last['bot'+chan] = time.strftime('%H:%M:%S', time.localtime())
            m1+=' @'+au
            return m1


    if mesag.startswith('!add '):
        if is_str==1:
            if not os.path.exists(dir_list.replace('/list.txt','')):
                os.makedirs(dir_list.replace('/list.txt',''))
            if not os.path.isfile(dir_list):
                inp = open(dir_list,'w',encoding='utf8')
                inp.close()
            mes = mes.replace('!add ','')
            if not aut in mes:
                mes+=' ('+aut+')'
            li = listedit(dir_list,mes,'добавить')
            tosite(chan)
            addfile(dir_list_log,time_now+' '+aut+': '+mes+' ('+'добавить'+')\n')
            addfile(dir_list_log,mes+' '+'добавлено'+'\n')
            m1 = ' '+mes.replace('\n','')+' добавлено'+' @'+au
            return m1
        else:
            m1 = 'Команда доступна только стримеру @'+au
    #if os.path.isfile(dir_list):
    if is_str==1:
        if mesag.startswith('!del '):
            li = listedit(dir_list,mesag.replace('!del ',''),'удалить')
            tosite(chan)
            addfile(dir_list_log,time_now+' '+aut+': '+mesag+' ('+'удалить'+')\n')
            li = str(li)
            if li!='-1':
                m1 = ' '+li+' удалено'
                addfile(dir_list_log,li+' '+'удалено\n')
            else:
                m1 = 'В списке не найдено!'
                addfile(dir_list_log,'Не найдено\n')
            m1+=' @'+au
            return m1
        if mesag.startswith('!up '):
            li = listedit(dir_list,mesag.replace('!up ',''),'поднять')
            tosite(chan)
            inp = open(dir_list,'r',encoding='utf8')
            t = inp.readlines()
            inp.close()
            addfile(dir_list_log,time_now+' '+aut+': '+mesag+' ('+'поднять'+')\n')
            if li!='-1':
                na = t[li].replace('\n','')
                m1 = ' '+na+' поднято'
                addfile(dir_list_log,na+' '+'поднято\n')
            else:
                m1 = 'В списке не найдено!'
                addfile(dir_list_log,'Не найдено\n')
            m1+=' @'+au
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
                m1 = 'Ошибка'+' @'+au
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
                    #if is_serv==0:
                    #    print(au)
                    #    print(t[ti])
                    #    print(t[tj])
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
    if mesag.startswith('!rename'):
        m1 = 'Ошибка'
        doren = 0
        nome = -3
        las = intime_now-time0(last['renam'+chan])
        mes = mes.replace('!rename','')
        if len(mes)<=1:
            m1 = 'Чтобы изменить название: !rename + номер или ОДНО слово из названия'+' @'+au
            last['renam'+chan] = time_now
            addfile(dir_list_log,'Ошибка\n')
            return m1
        else:
            nom = mes.split(' ')
            nom.remove('')
            try:
                nome = nom[0]
            except:
                m1 = 'Чтобы изменить название: !rename + номер или ОДНО слово из названия'+' @'+au
                last['renam'+chan] = time_now
                addfile(dir_list_log,'Ошибка\n')
                return m1
            if nome != -3:
                mes = mes.replace(' '+str(nome)+' ','')
                addfile(dir_list_log,time_now+' '+aut+': '+mesag+' (rename)\n')
                if is_str == 1:
                    doren = 1
                if las > 10 or las < 0:
                    doren = 1
                if doren == 1:
                    try:
                        inp = open(dir_list,'r',encoding='utf8')
                        t = inp.readlines()
                        inp.close()
                    except:
                        m1 = 'Ошибка'+' @'+au
                        return m1
                    li = -3
                    try:
                        li = int(nome)
                    except:
                        li = listedit(dir_list,str(nome),'найти')
                        li = li[0]
                    addfile(dir_list_log,mes+'\n')
                    if li == -3:
                        m1 = 'Чтобы изменить название: !rename + номер или ОДНО слово из названия'+' @'+au
                        last['renam'+chan] = time_now
                        addfile(dir_list_log,'Ошибка\n')
                        return m1
                    else:
                        addfile(dir_list_log,t[li])
                        print(t[li].lower())
                        print(au)
                        if au in t[li].lower() or is_str==1:
                            doren = 0
                            if li>0:
                                doren = 1
                            elif is_str==1:
                                doren = 1
                            if doren == 1:
                                if not aut in mes:
                                    mes+=' ('+aut+')'
                                if 'фильм' in t[li].lower() and not 'фильм' in mes.lower():
                                    mes = 'Фильм '+mes
                                mes+='\n'
                                t[li]=mes
                                inp = open(dir_list,'w',encoding='utf8')
                                for s in t:
                                    inp.write(s)
                                inp.close()
                                tosite(chan)
                                m1 = 'Готово'+' @'+au
                                addfile(dir_list_log,t[li])
                                addfile(dir_list_log,'Готово\n')
                            elif doren == 0:
                                m1 = 'Нельзя менять текущий заказ'+' @'+au
                                addfile(dir_list_log,'Ошибка\n')
                            last['renam'+chan] = time_now
                        elif not au in t[li].lower():
                            m1 = 'Нельзя менять чужой заказ'+' @'+au
                            addfile(dir_list_log,'Чужой заказ\n')
                return m1

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
                        #if is_serv==0:
                        #    print(nom)
                        nom = ' ('+str(t1)+'/'+str(len(t)-1)+')'
                        t2 += t[t1].replace('\n','')+' '+nom+'; '
                    m1 = t2+' @'+au
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
                        m1 = ''
                        for t1 in li:
                            nom = ' ('+str(t1)+'/'+str(len(t)-1)+')'
                            m1 += t[t1].replace('\n','')+' '+nom+'; '
                        #m1 = ' '+t[int(li[0])]+' Сейчас под номером ('+str(int(li[0]))+'/'+str(len(t)-1)+')'
                        #m1 = m1+' @'+au
                    else:
                        m1 = ' Такое название не найдено'
                elif t2<0:
                    m1 = ' Попробуйте ввести номер больше -_-'                    
            last['anim'+chan] = time_now
            m1+=' @'+au
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
                r_url = 'https://faceitelo.net/player/'+nik
                html = html_finder(r_url)
                t1 = []
                if html!=-1:
                    t1 = re.findall(r'<td><strong>(\S+)</strong><br>',html)
                if len(t1)>0:
                    m1 = ' Elo '+nik+' = '+str(t1[0])
                else:
                    m1 = ' Ошибка, ник не найден'
                last['elo'+chan] = time_now
                m1+=' @'+au
                return m1

    return m1