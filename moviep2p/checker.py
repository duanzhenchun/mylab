#!/usr/bin/env python
#coding=utf-8

import poplib
from email import parser
import mailer
from email.header import decode_header
from conf import *

def check_new(user, password):
    pop_conn = poplib.POP3_SSL('pop.gmail.com')
    pop_conn.user(user)
    pop_conn.pass_(password)

    #Get messages from server:
    messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
    # Concat message pieces:
    messages = ["\n".join(mssg[1]) for mssg in messages]
    #Parse message intom an email object:
    messages = [parser.Parser().parsestr(mssg) for mssg in messages]
    for message in messages:
        subj = message['subject']
        try:
            subj = decode_header(subj)[0][0]
            if subj.find(SUBSCRIBE_MOVIE) == 0:
                From = message.get('from', '')
                yield From
#            print message.get_payload()
        except:
            pass
    pop_conn.quit()
    
def main():
    Tos=[]
    for To in check_new(ME, PASSWORD):
        print To
        Tos.append(To)
    if Tos:
        with open(CUR_MOVIES) as f:
            infos=f.read().decode('utf8')
            mailer.send(infos, Tos)
        
if __name__ == '__main__':  
    main()

