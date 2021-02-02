import os

def tosite(ch = 'test'):
	defdi = 'lists/def.txt'
	inp = open(defdi,'r',encoding='utf8')
	t = inp.readlines()
	inp.close()
	defani = 'lists/'+ch
	if not os.path.exists(defani):
		os.makedirs(defani)
	defani+='/list.txt'
	inp = open(defani,'r',encoding='utf8')
	an = inp.readlines()
	inp.close()
	di = '/home/admin/web/kujijiepuk.fun/public_html/lists'
	if os.path.exists(di):
		di+='/'+ch
		if not os.path.exists(di):
			os.makedirs(di)
		di += '/index.html'
	else:
		di = 'lists/'+ch+'/index.html'
	out = open(di,'w',encoding='utf8')
	for line in t:
		out.write(line)
	i = 0
	if len(an)>0:
		for line in an:
			m = '<p><font color="white" face="Arial">'
			if i == 0:
				m+='Cейчас: '
			else:
				m+=str(i)+'. '
			m+=line.replace('\n','')+'</font></p>\n'
			out.write(m)
			i+=1
	else:
		m = '<p><font color="white" face="Arial" size = 5>'
		m+='Заказов сейчас нет'
		m+='</font></p>\n'
		out.write(m)
	out.write('\n</html>\n</body>\n</html>\n')
	out.close()
