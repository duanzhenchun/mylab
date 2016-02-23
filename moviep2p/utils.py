import zlib
import urllib2


def getpage(urlstr, data=None):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0'),
                         ('Accept-Encoding', 'gzip')]
    page = opener.open(urlstr, data)
    if page.headers.get('Content-Encoding', '') == 'gzip':
        data = zlib.decompress(page.read(), 16 + zlib.MAX_WBITS)
    else:
        data = page.read()
    return data
