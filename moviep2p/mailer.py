#!/usr/bin/env python
# coding=utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from conf import *

html = """\
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head></head>
<body>
%s
</body>
</html>
"""

Subject = "高分电影P2P"
From = ME + "@gmail.com"
Server = 'smtp.gmail.com:587'
password = PASSWORD

def send(infos, tolist, sub=Subject):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = sub
    msg['From'] = From
    msg['To'] = ','.join(tolist)

    part2 = MIMEText(html % infos, 'html', _charset='utf-8')
    msg.attach(part2)

    svr = smtplib.SMTP(Server)
    svr.starttls()
    if '' != password > 0:
        svr.login(From[:From.index('@')], password)
    svr.sendmail(From, tolist, msg.as_string())
    svr.quit()
