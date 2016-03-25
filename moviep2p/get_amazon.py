#!/usr/bin/env python
# encoding: utf-8

import os
import re
import BeautifulSoup
import mailer
from utils import getpage

# url, THRESHOLD, product_name
Targets = (
    ("http://www.amazon.co.uk/gp/product/B00BSNL77I", 22.0, 'clearblue'),
    ("http://www.amazon.co.uk/gp/product/B004GHALRK", 10.2,
     'conceive_plus_8pac'), )

tolist = ['whille@163.com', 'meng3r@qq.com']


def cur_fname(fname):
    return os.path.dirname(os.path.realpath(__file__)) + '/' + fname


def get_price(fname):
    price = 0
    if os.path.isfile(fname):
        with open(fname) as fold:
            price = fold.read()
            price = price and float(price) or 0.0
    return round(price, 2)


def replace_file(filename, content):
    import tempfile
    with tempfile.NamedTemporaryFile('w',
                                     dir=os.path.dirname(filename),
                                     delete=False) as tf:
        tf.write(content)
        tempname = tf.name
        os.rename(tempname, filename)


def get_coupon(soup):
    ret = 0.0
    div = soup.find('div', id='clippedCouponSns')
    if not div:
        return ret
    cu = div.findChild('span', {'class': 'a-size-small a-color-state'})
    if not cu:
        return ret
    res = re.search('&pound;(.*) extra saving', cu.text)
    if not res:
        return ret
    ret = float(res.group(1))
    return ret


def main():
    for (url, threshold, product_name) in Targets:
        fprice = product_name + '.old'
        fullname = cur_fname(fprice)
        old_price = get_price(fullname)

        res = getpage(url)
        soup = BeautifulSoup.BeautifulSoup(res)
        sp = soup.find('span', id='priceblock_ourprice')
        price = float(sp.text[1:])
        realprice = price * .85 - get_coupon(soup)

        if old_price != realprice:
            replace_file(fullname, str(realprice))

        if old_price == 0 or (realprice < threshold and realprice < old_price):
            url_addr = '<a href="%s" >%s</a></br>' % ((url, ) * 2)
            subject = '%s < %s' % (product_name, threshold)
            mailer.send(url_addr + 'realprice: %s\n old_price: %s' %
                        (realprice, old_price),
                        tolist,
                        sub=subject)


if __name__ == '__main__':
    main()
