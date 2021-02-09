# -*- coding: utf-8 -*-
import os
import sys
from kuji_defs import addfile

if __name__ == "__main__":
    
    if os.path.exists('/home/admin/web/kujijiepuk.fun/public_html/'):
        addfile('/root/kujijibot/START_LOG.txt','Ручной перезапуск!\n')
        os.system("killall python3")
    else:
        addfile('START_LOG.txt','Ручной перезапуск!\n')
    print('Перезапущено!')