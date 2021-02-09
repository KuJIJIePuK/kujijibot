import time
import os
from kuji_defs import *
from kuji_http import *

def bot_rewards(mes,author_disp,chan,time_now,m_reward,is_mod,is_str,dict_rew,last,intime_now,dir_list,dir_list_log):
    m1 = 'Ошибка'    
    mesag = mes.lower()
    author = author_disp.lower()
    t_list = dict_rew[dict_rew['_sr']]
    if m_reward in t_list:
        t1 = mes
        if intime_now-time0(last['sr'+chan]) > 3 or intime_now-time0(last['sr'+chan]) < 0:
            delay = 0
        else:
            delay = 4
        t0 = mreq(t1)
        time.sleep(delay)
        last['sr'+chan] = time.strftime('%H:%M:%S', time.localtime())
        m1 = ''+t0
        return m1
    t_list = dict_rew[dict_rew['_skip']]
    if m_reward in t_list:
        t1 = mes
        if intime_now-time0(last['sk'+chan]) < 2:
            m1 = '2 скипа сразу, упс'
            return m1
        elif intime_now-time0(last['sk'+chan]) > 3:
            delay = 0
        else:
            delay = 4
        t0 = mreq(t1)
        t0=t0.replace('!sr ','')
        if 'youtu' in t0:
            time.sleep(delay)
            m1 = '!removesong '+t0
            return m1
        else:
            time.sleep(delay)
            m1 = '!skip'
            return m1
        last['sk'+chan] = time.strftime('%H:%M:%S', time.localtime())

    doli = -1
    t1 = ''

    t_list = dict_rew[dict_rew['_ladd']]
    if m_reward in t_list:
        if chan=='hubibich':
            chan = 'hubbich'
        comment = 'добавить'
        editn = 'Добавлено'
        doli = 1
    t_list = dict_rew[dict_rew['_lup']]
    if m_reward in t_list:
        comment = 'поднять'
        editn = 'Поднято'
        doli = 1
    if m_reward == '303c8930-6972-4649-8129-012bf2ec396e':
        if not 'фильм' in mes.lower():
            t1 = 'Фильм '
        comment = 'добавить'
        editn = 'Добавлен'
        doli = 1
    t_list = dict_rew[dict_rew['_ldown']]
    if m_reward in t_list:
        comment = 'опустить'
        editn = 'Опущено'
        doli = 1
    t_list = dict_rew[dict_rew['_lrem']]
    if m_reward in t_list:
        comment = 'удалить'
        editn = 'Удалено'
        doli = 1
    if doli == 1:
        dir_list = 'lists/'+chan
        if not os.path.exists(dir_list):
            os.makedirs(dir_list)
        dir_list+='/list.txt'
        try:
            inp = open(dir_list,'a',encoding='utf8')
            inp.close()
        except:
            m1 = 'Ошибка, свяжитесь с KuJIJIePuK @'+author
            return m1
        t2 = -2
        spis = ''
        
        if comment == 'добавить':
            li = listedit(dir_list,t1+mes+' ('+author_disp+')',comment)
            inp = open(dir_list,'r',encoding='utf8')
            t = inp.readlines()
            inp.close()
            nom = ' ('+str(int(li))+'/'+str(len(t)-1)+')'
            t1 = t1+mes+' ('+author_disp+')'
            addfile(dir_list_log,time_now+' '+author_disp+': '+mes+' ('+comment+')\n')
            addfile(dir_list_log,t1+' '+editn+nom+'\n')
            m1 = ''+t1+' '+editn+nom+' @'+author+spis
        elif comment == 'удалить':
            li = listedit(dir_list,mes,comment)
            if not 'фильм' in li:
                m1 = ''+li+' '+editn+' @'+author+spis
            else:
                m1 = ''+li+' '+'Удалён'+' @'+author+spis
            addfile(dir_list_log,time_now+' '+author_disp+': '+mes+' ('+comment+')\n')
            addfile(dir_list_log,li+' '+editn+'\n')
        else:
            li = listedit(dir_list,mes,comment)
            try:
                t2 = int(li)
            except:
                pass
            inp = open(dir_list,'r',encoding='utf8')
            t = inp.readlines()
            inp.close()
            if t2>=0:
                if comment == 'поднять':
                    nom = ' ('+str(t2)+'/'+str(len(t)-1)+')'
                    m1 = ''+t[t2]+' '+editn+nom+' @'+author+spis
                elif comment == 'опустить':
                    nom = ' ('+str(t2)+'/'+str(len(t)-1)+')'
                    m1 = ''+t[t2]+' '+editn+nom+' @'+author+spis
                addfile(dir_list_log,time_now+' '+author_disp+': '+mes+' ('+comment+')\n')
                addfile(dir_list_log,t[t2].replace('\n','')+' '+editn+nom+'\n')
            elif t2==-3:
                m1 = 'Выше некуда!'+' @'+author
                addfile(dir_list_log,time_now+' '+author_disp+': '+mes+' ('+comment+')\n')
                addfile(dir_list_log,'Слишком высоко\n')
                for line in t:
                    addfile(dir_list_log,line)
                addfile(dir_list_log,'\n')
            else:
                m1 = 'Ошибка, свяжитесь с @KuJIJIePuK'+' @'+author
                addfile(dir_list_log,time_now+' '+author_disp+': '+mes+' ('+comment+')\n')
                addfile(dir_list_log,'ОШИБКА\n')
                for line in t:
                    addfile(dir_list_log,line)
                addfile(dir_list_log,'\n')
        tosite(chan)
        return m1
    return m1