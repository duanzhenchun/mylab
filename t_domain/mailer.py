#!/usr/bin/env python
# encoding: utf-8

import smtplib
from email.mime.text import MIMEText


def send(sender, receivers, subject, txt):
    msg = MIMEText(txt)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ','.join(receivers)

    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(sender, [receivers], msg.as_string())
    s.quit()


if __name__ == "__main__":
    send('hello', 'test', 'xx', 'yy')
