#!/usr/bin/env python
# encoding: utf-8

import os
import re
import BeautifulSoup
import mailer
from utils import getpage 

THRESHOLD = 22.0
tolist = ['whille@163.com', 'meng3r@qq.com' ]
url = "http://www.amazon.co.uk/gp/product/B00BSNL77I"
URL_ADDR = '<a href="%s" >%s</a></br>' % ((url, ) * 2)
SUBJECT = 'clear blue < %s' % THRESHOLD

def cur_fname(fname):
    return os.path.dirname(os.path.realpath(__file__))+'/'+fname

def get_price(fname):
    price = 0
    if os.path.isfile(fname): 
        with open(fname) as fold:
            price = fold.read()    
            price = price and float(price) or 0.0
    return price

def replace_file(filename, content):
    import tempfile
    with tempfile.NamedTemporaryFile(
          'w', dir=os.path.dirname(filename), delete=False) as tf:
       tf.write(content)
       tempname = tf.name
       os.rename(tempname, filename)


def main():
    fprice='clearblue.old'
    fullname = cur_fname(fprice)
    old_price = get_price(fullname)

    res = getpage(url)
    soup = BeautifulSoup.BeautifulSoup(res)
    sp = soup.find('span', id='priceblock_ourprice')
    price = float(sp.text[1:])
    div = soup.find('div', id='clippedCouponSns')
    cu = div.findChild('span', {'class': 'a-size-small a-color-state'})
    ret = re.search('&pound;(.*) extra saving', cu.text)
    realprice = price * .85 - float(ret.group(1))

#    print old_price, realprice
    if old_price != realprice:
        replace_file(fullname, str(realprice))

#    print old_price, realprice
    if old_price == 0 or (realprice < THRESHOLD and realprice < old_price):
#        print 'send_mail'
        mailer.send(URL_ADDR + 'realprice: %s' %realprice, tolist, sub=SUBJECT)


if __name__ == '__main__':
    main()
