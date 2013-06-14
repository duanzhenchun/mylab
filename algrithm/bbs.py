#!/usr/bin/env python
# -*- coding: gbk -*-

import re
import telnetlib
import time

RET = "\n"

def loginBBS():
    user = "whille02"
    password = "whille7"
    tn = telnetlib.Telnet("bbs.newsmth.net")
    # tn.set_debuglevel(1)
    tn.read_until("请输入代号:")
    time.sleep(1)
    tn.write(user + RET)
    tn.read_until("请输入密码:")
    time.sleep(1)
    tn.write(password + RET)
    for i in range(3):
        tn.write(RET)
    time.sleep(3)
#     tn.write("eq")
#     print tn.read_very_eager()
    tn.read_until("S) 选择阅读讨论区")
    time.sleep(1)
    return tn
    
def readBoard(tn):
    tn.write("s" + RET)
    tn.read_until("请输入讨论区名称 ")
    time.sleep(1)
    tn.write("ticket" + RET)
    tn.write("$")
    tn.read_until("[一般模式] ")
    tn.read_until("\x1b[m")
    postlist = tn.read_very_eager()
    info = search(postlist)
    if info:
        msg(tn, info)
    # unread = re.search('(\s+\d+ \* .*)', postlist)
    # if unread:
    # print unread.group()
    while re.search(' \* ', postlist):
        tn.write("P")
    postlist = tn.read_very_eager()
    info = search(postlist)
    if info:
        msg(tn, info)
    time.sleep(1)
    tn.write("$")
    tn.read_very_eager()
    time.sleep(1)
    tn.write("c")
    tn.read_very_eager()
    time.sleep(1)
    tn.write("e")
    
def search(string):
    pattern = '想买'
    line = re.search(pattern, string)
    if line:
        print line.group()
    print "\a"
    title = re.search('', line.group())
    # print title.group()
    return title.group()
    return 0
    
def msg(tn, message):
    # tn.set_debuglevel(1)
    tn.write("w")
    tn.read_until("送讯息给:")
    tn.write("" + RET)
    tn.read_until("请输入音信内容，Ctrl+Q 换行:")
    tn.write(message)
    tn.write("" + RET)
    tn.read_until("确定要送出吗")
    tn.write("y" + RET)
    # tn.set_debuglevel(0)
    
def logout(tn):
    tn.read_until("G) 离开水木")
    tn.write("g" + RET)
    tn.read_until("离开本BBS站")
    tn.write("" + RET)
    time.sleep(1)
    tn.write("" + RET)
    tn.read_all
    tn.close()
    
def loop():
    tn = loginBBS()
    while 1:
        readBoard(tn)
        time.sleep(60)
    logout(tn)
    
if __name__ == '__main__':
    loop()
