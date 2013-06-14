#!/usr/bin/env python
#coding=utf-8

import zlib
import json
import re
import urllib2, urllib
from BeautifulSoup import BeautifulSoup
import mailer
from conf import *


def getpage(urlstr):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Accept-Encoding', 'gzip,deflate')]
    page = opener.open(urlstr)
    data = zlib.decompress(page.read(), 16 + zlib.MAX_WBITS)
    return data


def bestmovie(title, thold=7):
    dic = {'q':title.split(u'-人')[0].encode('utf8'), 'count':3}
    qstr = urllib.urlencode(dic)
    urlstr = "http://api.douban.com/v2/movie/search?%s" % qstr
    page = urllib2.urlopen(urlstr)
    res = urllib.urlopen(urlstr).read()
    dic = json.loads(res)
    best = None
    for sub in dic['subjects']:
        score = sub['rating']['average']
        if score < thold:
            continue
        if not best or best['rating']['average'] < score:
            best = sub
    return best

def getinfo(red):
    dic = {}
    best = bestmovie(red.text)
    if not best:
        return None
    dic['text'] = red.text
    dic['score'] = best['rating']['average']
    for i in ('title', 'original_title', 'year', 'alt'):
        dic[i] = best[i]
    dic['img'] = best['images']['large']
    dow = red.findParent('tbody').findAll('td', {'class':'dow'})
    ed2k = dow[0](ed2k=re.compile("ed2k"))
    dic['ed2k'] = ed2k[0].get('ed2k') 
    return dic
    
def main():
    urlstr = 'http://oabt.org/?cid=6'
    data = getpage(urlstr)
    soup = BeautifulSoup(data)
    #print soup.prettify()
    toplist = soup.findAll('div', {"class" : "toplist"})
    reds = toplist[0].findAll('a', {'class':'red'})
    
    infos = '<ul>'
    for red in reds:
        infos += movieinfo(getinfo(red))
    infos += '</ul>'
    
    with open(CUR_MOVIES, 'w') as f:
        f.write(infos.encode('utf8'))
        f.close()
#    mailer.send(infos)    

MOVIE_FMT = """<li>
<a href="%s" target="_blank"><img src="%s" width="150px"></a>
<p>score: %s</p>
<p>title: %s</p>
<p>original_title: %s</p>
<p>year: %s</p>
<a href="%s">%s</a>
</li>
"""

def movieinfo(dic):
    if not dic:
        return ''
    return MOVIE_FMT % (dic['alt'], dic['img'], dic['score'], dic['title'], dic['original_title'], dic['year'], dic['ed2k'], dic['text'])
    
if __name__ == '__main__':  
     main()

"""
{
count: 3,
start: 0,
total: 1,
subjects: [
{
rating: {
max: 10,
average: 8.1,
stars: "40",
min: 0
},
title: "冲浪英豪",
original_title: "Chasing Mavericks",
subtype: "movie",
year: "2012",
images: {
small: "http://img3.douban.com/spic/s11139149.jpg",
large: "http://img3.douban.com/lpic/s11139149.jpg",
medium: "http://img3.douban.com/mpic/s11139149.jpg"
},
alt: "http://movie.douban.com/subject/5153883/",
id: "5153883"
}
],
title: "搜索 "Chasing.Mavericks.2012.冲浪英豪.双语字幕.HR-HDTV.AC3.1024X576.x264" 的结果"
}

score: 7.5
title: 派对恐龙
original_title: Partysaurus Rex
year: 2012
alt: http://movie.douban.com/subject/11599090/
ed2k://|file|Partysaurus.Rex.2012.%E6%B4%BE%E5%AF%B9%E6%81%90%E9%BE%99.%E5%8F%8C%E8%AF%AD%E5%AD%97%E5%B9%95.HR-HDTV.AC3.1024X576.x264-%E4%BA%BA%E4%BA%BA%E5%BD%B1%E8%A7%86%E5%88%B6%E4%BD%9C.mkv|107660838|f962951c476e04593ef6f18be144d2e2|h=etn26u55g67q3ycmwcgbnk6bwd47jc24|/
score: 8.1
title: 霍比特人1：意外之旅
original_title: The Hobbit: An Unexpected Journey
year: 2012
alt: http://movie.douban.com/subject/1966182/
ed2k://|file|The.Hobbit.An.Unexpected.Journey.2012.%E9%9C%8D%E6%AF%94%E7%89%B9%E4%BA%BA%EF%BC%9A%E6%84%8F%E5%A4%96%E6%97%85%E7%A8%8B.%E5%8F%8C%E8%AF%AD%E5%AD%97%E5%B9%95.HR-HDTV.AC3.1024X576.x264-%E4%BA%BA%E4%BA%BA%E5%BD%B1%E8%A7%86%E5%88%B6%E4%BD%9CV3.mkv|2780244159|277143a94c8a20446c90b30d8bea5ef1|h=o7oujkwbhncwwd4ncr2y6hmlmz7g6qsv|/

"""
