import os

def tosite():
	defdi = 'lists/def.txt'
	inp = open(defdi,'r',encoding='utf8')
	t = inp.readlines()
	inp.close()

	defani = 'lists/anime.txt'
	inp = open(defani,'r',encoding='utf8')
	an = inp.readlines()
	inp.close()

	if os.path.exists('/home/admin/web/kujijiepuk.fun/public_html/lists/hubbich/'):
		di = '/home/admin/web/kujijiepuk.fun/public_html/lists/hubbich/index.html'
	else:
		di = 'lists/index.html'
	out = open(di,'w',encoding='utf8')
	for line in t:
		out.write(line)
	i = 0
	for line in an:

		m = '<p><font color="white" face="Arial">'
		if i == 0:
			m+='Смотрим сейчас: '
		else:
			m+=str(i)+'. '
		m+=line.replace('\n','')+'</font></p>\n'
		out.write(m)
		i+=1
	out.write('\n</html>\n</body>\n</html>\n')
	out.close()
