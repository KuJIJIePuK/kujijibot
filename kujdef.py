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
def df(d,s,tim):
    i = 0
    for t in d:
        te = d[t]
        te = te[9:]
        if te==s:
            t1 = time0(tim)
            t2 = time0(d[t])
            if t1-t2<=5:
                i+=1
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