#!/usr/bin/env python
# -*- coding: gbk -*-

import re
import telnetlib
import time
import codecs
import sys
sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout)

RECEIVERS = ('meng3r@qq.com', 'whille@163.com')
# RECEIVERS = ('whille@163.com',)
RET = "\r"
PAGEUP = '\x1b[5~'
LISTS_TIMEBREAK = 60
LASTFILE = './last.log'


def loginBBS():
    user = "whille02"
    password = "whille7"
    tn = telnetlib.Telnet("bbs.newsmth.net")
    # tn.set_debuglevel(1)
    tn.read_until("请输入代号:")
    tn.write(user + RET)
    tn.read_until("请输入密码:")
    tn.write(password + RET)
    for i in range(3):
        tn.write(RET)
    time.sleep(3)
#     tn.write("eq")
#     print tn.read_very_eager()
    tn.read_until("S) 选择阅读讨论区")
    return tn
    
def readBoard(tn, last, first, board='SecondMarket'):
    tn.write('s')
    if first:
        tn.write(RET)  # select discussion
    tn.read_until("讨论区")
    tn.write(board + RET)
    tn.write("$")
    tn.read_until("一般模式] ")
    tn.read_until("\x1b[m")
    tn.write('\007')
    tn.read_until("积分变更")
    tn.write('4\r')
    time.sleep(1)
    postlist = tn.read_very_eager().decode('gbk')
    tn.write(PAGEUP)
    postlist = tn.read_very_eager().decode('gbk') + postlist
    lst = list(search(postlist))
    if not lst:
        return None
#     lst.reverse()
    newlast = lst[-1][-1]
    with codecs.open(LASTFILE, 'a', encoding='utf-8') as f: 
        if last != newlast:
            f.write((newlast + u'\r\n'))
            f.close()
    for (n, title) in reversed(lst):
        if title == last:
            return
        tn.write(str(n) + '\r')
        tn.read_very_eager()
        mail2(tn)
#     time.sleep(1)
#     tn.write("e")
#     tn.read_very_eager()
#     tn.write("e")
#     tn.read_until('个人工具箱')
    return newlast
    
def search(txt):
    target = u'(\d+).*\u25cf(.*[转出].*卡.*)\\x1b\[K\n'
    for i in re.findall(target, txt):
        print i[0], i[1]
        yield i
    
def mail2(tn):
    for rec in RECEIVERS:
        tn.write("F")
        tn.read_until("转寄给:")
        tn.write(rec + RET)
    #     tn.read_until("(Y/N):")
        for i in range(5):
            tn.write("" + RET)
            tn.read_eager()
    # tn.set_debuglevel(0)
    
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
    
def loop():
    last = None
    try:
        with codecs.open(LASTFILE, encoding='utf-8') as f:
            f.seek(0, 2)
            leng = f.tell()
            start = leng > 1024 and 1024 or leng
            f.seek(-start, 2)
            last = f.readlines()[-1]
    except IOError:
        pass
    tn = loginBBS()
    first = True
    for i in range(2):
        new = readBoard(tn, last, first)
        first = False
        print tn.read_very_eager()
        time.sleep(LISTS_TIMEBREAK)
        last = new
    logout(tn)
    
if __name__ == '__main__':
    loop()
