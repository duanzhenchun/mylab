# -*- coding: gbk -*-

import re
import telnetlib
import time
import codecs
import sys
import logging
sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout)

target = u'(\d+) .+?(\S*[转出].+卡.*)\n'
RECEIVERS = ('meng3r@qq.com', 'whille@163.com')
# RECEIVERS = ('whille@163.com',)
RET = "\r"
PAGEUP = '\x1b[5~'
LISTS_TIMEBREAK = 30
LASTFILE = './last.log'
LINE_END = u'\x1b[K'

logger = logging.getLogger('bbs')

def init_log():
    hdlr = logging.FileHandler('./bbs.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)

def loginBBS(passwd):
    user = "whille"
    tn = telnetlib.Telnet("bbs.newsmth.net")
    tn.read_until("请输入代号:")
    tn.write(user + RET)
    tn.read_until("请输入密码:")
    tn.write(passwd + RET)
    for i in range(4):  # according to login parameter set i (I)
        tn.write(RET)
    time.sleep(3)
    tn.read_until("S) 选择阅读讨论区")
    return tn

def readBoard(tn, last, first, board='SecondMarket'):
    tn.write('s')
    if first:
        tn.read_lazy()
        tn.write(RET)  # select discussion
    tn.read_until("讨论区")
    tn.write(board + RET)
    tn.write("$")
    tn.read_until("一般模式] ")
    tn.read_until("\x1b[m")
    tn.write('\007')
    tn.read_until("积分变更")
    tn.write('4\r')
    time.sleep(3)
    postlist = tn.read_very_eager().decode('gbk')
    tn.write(PAGEUP)
    postlist = tn.read_very_eager().decode('gbk') + postlist
    lst = list(search(postlist))
    if not lst:
        return None
    newlast = lst[-1][-1]
    for (n, title) in reversed(lst):
        if title == last:
            break
        tn.write(str(n) + '\r')
        tn.read_very_eager()
        logger.info("%s, %s" %( n, title))
        mail2(tn)
    return newlast

def search(txt):
    for i in re.findall(target, txt):
        yield i[0], i[1].strip(LINE_END)

def mail2(tn):
    for rec in RECEIVERS:
        tn.write("F")
        tn.read_until("转寄给:")
        tn.write(rec)
        tn.write(RET)
        for i in range(8):
            tmp = tn.read_eager()
            time.sleep(3)
            tn.write(RET)
            if '转寄完成' in tmp:
                break
        tn.read_eager()

def logout(tn):
    for i in range(3):
        tn.write("e")
    tn.read_until("G) 离开水木")
    tn.write("g" + RET)
    tn.read_until("离开本BBS站")
    tn.write("" + RET)
    tn.write("" + RET)
    tn.read_all
    tn.close()

def loop(passwd, maxIter=2):
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
    tn = loginBBS(passwd)
    first = True
    for _ in range(maxIter):
        newlast = readBoard(tn, last, first)
        first = False
        tn.read_very_eager()
        if newlast and newlast != last:
            with codecs.open(LASTFILE, 'a', encoding='utf-8') as f:
                logging.info('newlast: '+newlast)
                if last != newlast:
                    f.write((newlast + u'\r\n'))
                    f.close()
            last = newlast
        time.sleep(LISTS_TIMEBREAK)
    logout(tn)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("""
Usage:
    %s bbs_pwd  """ % sys.argv[0])
    init_log()
    loop(sys.argv[1])
