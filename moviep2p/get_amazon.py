#!/usr/bin/env python
# encoding: utf-8

import re
import BeautifulSoup
import mailer
from utils import getpage

THRESHOLD = 22.0
tolist = ['whille@163.com', ]
url = "http://www.amazon.co.uk/gp/product/B00BSNL77I"
URL_ADDR = '<a href="%s" >%s</a></br>' % ((url, ) * 2)
SUBJECT = 'clear clue < %s' % THRESHOLD


def main():
    res = getpage(url)
    soup = BeautifulSoup.BeautifulSoup(res)
    sp = soup.find('span', id='priceblock_ourprice')
    price = float(sp.text[1:])
    div = soup.find('div', id='clippedCouponSns')
    cu = div.findChild('span', {'class': 'a-size-small a-color-state'})
    ret = re.search('&pound;(.*) extra saving', cu.text)
    realprice = price * .85 - float(ret.group(1))

    if realprice < THRESHOLD:
        mailer.send(URL_ADDR, tolist, sub=SUBJECT)


if __name__ == '__main__':
    main()
