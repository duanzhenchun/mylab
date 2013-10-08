# -*- coding: gbk -*-

import telnetlib
import time
import codecs
import sys
import logging
sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout)

RET = "\r"
LISTS_TIMEBREAK = 120
LASTFILE = './last.log'
LINE_END = u'\x1b[K'

logger = logging.getLogger('bbs')

def init_log():
    hdlr = logging.FileHandler('./bbs.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)

def loginBBS(uname, passwd):
    tn = telnetlib.Telnet("bbs.newsmth.net")
    tn.read_until("请输入代号:")
    tn.write(uname + RET)
    tn.read_until("请输入密码:")
    tn.write(passwd + RET)
    for _ in range(4):  # according to login parameter set i (I)
        tn.write(RET)
    time.sleep(3)
    tn.read_until("S) 选择阅读讨论区")
    return tn

def logout(tn):
    for _ in range(3):
        tn.write("e")
    tn.read_until("G) 离开水木")
    tn.write("g" + RET)
    tn.read_until("离开本BBS站")
    tn.write("" + RET)
    tn.write("" + RET)
    tn.read_all
    tn.close()

def loop(uname, passwd):
    last = None
    try:
        with codecs.open(LASTFILE) as f:
            f.seek(-1024, 2)
            txt=f.readlines()[-1].decode('utf-8')
            last = txt.strip()
            logging.info('last: '+last)
            f.close()
    except IOError:
        pass
    tn = loginBBS(uname, passwd)
    while True:
        tn.write('s')
        tn.read_lazy()
        tn.write(RET)
        time.sleep(LISTS_TIMEBREAK)
    logout(tn)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("""
Usage:
    %s user, pwd  """ % sys.argv[0])
    init_log()
    loop(sys.argv[1],sys.argv[2])
