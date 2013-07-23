import zlib
import json
import re
import urllib2, urllib
from BeautifulSoup import BeautifulSoup

def getpage(urlstr):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Accept-Encoding', 'gzip')]
    page = opener.open(urlstr)
    if page.headers.get('Content-Encoding', '') == 'gzip':
        data = zlib.decompress(page.read(), 16 + zlib.MAX_WBITS)
    else:
        data = page.read()
    return data
    
def htmlinfo(lst):
    if not lst:
        return None
    infos = '<ul>'
    for i in lst:
        infos += i
    infos += '</ul>'
    return infos
