#!/usr/bin/env python
# encoding: utf-8

import re
import BeautifulSoup
from utils import *

url = "http://www.amazon.co.uk/gp/product/B00BSNL77I"
res = getpage(url)
soup = BeautifulSoup.BeautifulSoup(res)
sp = soup.find('span', id='priceblock_ourprice')
price = float(sp.text[1:])
div = soup.find('div', id='clippedCouponSns')
coup = div.findChild('span', {'class': 'a-size-small a-color-state'})
ret = re.search('&pound;(.*) extra saving', cu)
float(ret.group(1))
price - float(ret.group(1))
price * .85 - float(ret.group(1))
