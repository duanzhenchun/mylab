#!/usr/bin/env python
# coding=utf-8

import poplib
from email import parser
import mailer
from email.header import decode_header
from conf import *
import os

HOTWORD = 'hotword'
SAE_DOMAIN = 'hotupload'
ipY = '. ~/my_env/bin/activate'
SAE_STORAGEUPLOAD = '%s && swift -A https://auth.sinas3.com/v1.0 -U y54xynw0yn -K 1x2jx3l2xj4ww1lhmm2jx5zxx5m225ljmlk3h4zm upload %s text.txt' % (ipY, SAE_DOMAIN)
HOTWORD_RESULT = '<a href="http://2.weiboexposure.sinaapp.com/hotresult">result</a>'
ERROR_UPLOAD = 'error upload'


def check_new(user, password):
    pop_conn = poplib.POP3_SSL('pop.gmail.com')
    pop_conn.user(user)
    pop_conn.pass_(password)

    # Get messages from server:
    messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
    # Concat message pieces:
    messages = ["\n".join(mssg[1]) for mssg in messages]
    # Parse message into an email object:
    messages = [parser.Parser().parsestr(mssg) for mssg in messages]
    for message in messages:
        subj = message['subject']
        try:
            subj = decode_header(subj)[0][0]
            From = message.get('from', '')
            if subj.find(SUBSCRIBE_MOVIE) == 0:
                yield From
            elif subj.find(HOTWORD) == 0:
                attachment = message.get_payload()[1]
#                 attachment.get_content_type()
                open('text.txt', 'wb').write(attachment.get_payload(decode=True))
                res = os.system(SAE_STORAGEUPLOAD)
                retmsg = res == 0 and HOTWORD_RESULT or ERROR_UPLOAD
                mailer.send(retmsg, (From,), sub='hotresult')
        except:
            pass
    pop_conn.quit()

def main():
    Tos = []
    for To in check_new(ME, PASSWORD):
        print To
        Tos.append(To)
    if Tos:
        with open(CUR_MOVIES) as f:
            infos = f.read().decode('utf8')
            mailer.send(infos, Tos)

if __name__ == '__main__':
    main()

