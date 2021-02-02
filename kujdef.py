import os
import re
from urllib.request import urlopen, Request

def time0(s):
    return (int(s[0:2])*60*60+int(s[3:5])*60+int(s[6:8]))

def addfile(di,m):
    if not os.path.isfile(di):
        inp = open(di,'w',encoding='utf8')
        inp.close()
    inp = open(di,'a',encoding='utf8')
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
def df(d,s,tim,ch):
    i = 0
    for t in d:
        #print(ch)
        #print(t)
        if ch in t:
            te = d[t]
            te = te[9:]
            #print(te+'  '+s)
            if te==s:
                t1 = time0(tim)
                t2 = time0(d[t])
                #print(str(t1-t2))
                if t1-t2<=5 and t1-t2>=0:
                    i+=1
    #print(i)
    return i

def confre(di,ch,r):
    inp = open(di,'r',encoding='utf8')
    t = inp.readlines()
    inp.close()
    
    rr = -1
    inp = open(di,'w',encoding='utf8')
    for line in t:
        if ch in line:
            line = ch+' '+str(r)+'\n'
            rr = 1
        inp.write(line)
    if rr == -1:
        line = ch+' '+str(r)+'\n'
        inp.write(line)
    inp.close()

def confignore(di,ch,nick):
    inp = open(di,'r',encoding='utf8')
    t = inp.readlines()
    inp.close()
    inp = open(di,'w',encoding='utf8')
    rr = -1
    for line in t:
        test1 = line
        if ch in line:
            line = line.replace('\n','')
            rr = 1
            t1 = line.split(' ')
            for n in t1:
                if n == nick:
                    t1.remove(n)
                    rr = 2
            if rr == 1:
                t1.append(nick)
            test1 = ' '.join(t1)
            test1+='\n'
        inp.write(test1)
    if rr == -1:
        line = ch+' '+nick+'\n'
        inp.write(line)
    inp.close()

def defelo(mesag,nik):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    reg_url = 'https://faceitelo.net/player/'
    reg_url+=nik
    req = Request(url=reg_url, headers=headers)
    try:
        html = urlopen(req).read()
        html = str(html)
        t1 = re.findall(r'<td><strong>(\S+)</strong><br>',html)
        return t1[0]
    except:
        return -1

def mreq(t1):
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
        return('!sr '+t0)        
    else:
        if not t1.startswith('!sr'):
            return('!sr '+t1)
        else:
            return(t1)

def listedit(di,mes,com,nick = '-1859489484564'):
    j = '-1'
    if com!='добавить':
        if len(mes.split(' '))==1:
            tint = -1
            try:
                tint = int(mes)
            except:
                pass

        mes=mes.lower()
        mes = re.sub('[!@#$%^&*,.?()<>]','',mes)
    ti = mes.split(' ')
    inp = open(di,'r',encoding='utf8')
    t = inp.readlines()
    inp.close()
    l = []
    sk = -1
    for line in t:
        l.append(line)

    if com == 'найти':
        sk = 1
        i = -1
        rr = -1
        j = []
        while i<len(l)-1:
            i+=1
            t2 = re.sub('[!@#$%^&*,.?()<>]','',l[i])
            t2 = t2.lower()
            t2 = t2.replace('\n','')
            tj = t2.split(' ')
            t3 = list(set(ti) & set(tj))
            if set(ti)==set(t3):
                j.append(i)
                #print(j)

    elif com == 'поднять':
        if tint>1 and tint<=len(l)-1:
            l[tint],l[tint-1]=l[tint-1],l[tint]
            j = tint-1
        else:
            i = -1
            rr = -1
            while i<len(l)-1 and rr!=1:
                i+=1
                t2 = re.sub('[!@#$%^&*,.?()<>]','',l[i])
                t2 = t2.lower()
                t2 = t2.replace('\n','')
                tj = t2.split(' ')            
                t3 = list(set(ti) & set(tj))
                #print(set(ti))
                #print(set(tj))
                if set(ti)==set(t3) and i>=2:
                    j = i-1
                    l[i],l[i-1]=l[i-1],l[i]
                    rr = 1
                elif set(ti)==set(t3) and i<=2 and i>=0:
                    j = -3
    elif com == 'опустить':
        if tint>1 and tint<=len(l)-1:
            l[tint],l[tint+1]=l[tint+1],l[tint]
            j = tint+1
        else:
            i = -1
            rr = -1
            while i<len(l)-1 and rr!=1:
                i+=1
                t2 = re.sub('[!@#$%^&*,.()?<>]','',l[i])
                t2 = t2.lower()
                t2 = t2.replace('\n','')
                tj = t2.split(' ')
                t3 = list(set(ti) & set(tj))
                if set(ti)==set(t3) and not i==len(l)-1:
                    j = i+1
                    l[i],l[i+1]=l[i+1],l[i]
                    rr = 1
    elif com == 'удалить':
        if tint>-1 and tint<=len(l)-1:
            j = l[tint].replace('\n','')
            l.remove(l[tint])
        else:
            i = -1
            rr = -1
            while i<len(l)-1 and rr!=1:
                i+=1
                t2 = re.sub('[!@#$%^&*,().?<>]','',l[i])
                t2 = t2.lower()
                t2 = t2.replace('\n','')
                tj = t2.split(' ')
                t3 = list(set(ti) & set(tj))
                if set(ti)==set(t3):
                    j = l[i].replace('\n','')
                    l.remove(l[i])
                    rr = 1
    elif com == 'добавить':
        l.append(mes+'\n')
        j = len(l)-1

    
    if not sk == 1:
        inp = open(di,'w',encoding='utf8')
        for s in l:
            inp.write(s)
        inp.close()
    return j

def rew_conf(di,te,rew):
    inp = open(di,'r',encoding='utf8')
    t = inp.readlines()
    inp.close()
    #print(t)
    inp = open(di,'w',encoding='utf8')
    if rew+'\n' in t:
        ret = 0
        t.remove(rew+'\n')
        i = -1
        while i<len(t)-1:
            i+=1
            inp.write(t[i])
    elif not rew in t:     
        e = 0   
        ret = 1
        i = -1
        while not te in t[i]:
            i+=1
            inp.write(t[i])
        inp.write(rew+'\n')
        while i<len(t)-1:
            i+=1
            inp.write(t[i])
    inp.close()
    return ret