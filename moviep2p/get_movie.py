#!/usr/bin/env python
# coding=utf-8
from conf import *
from utils import *

douban_token = '26813bd953cdac9e'


def douban_cli():
    from douban_client import DoubanClient
    API_KEY = '09e7e2ad76917ac81db7a80863b47058'
    API_SECRET = '42764a7149130882'
    redirect_uri = 'http://54.250.166.126/spam/auth'
    SCOPE = 'douban_basic_common,movie_basic_r'
    client = DoubanClient(API_KEY, API_SECRET, redirect_uri, SCOPE)
    if not douban_token:
        print client.authorize_url
        # manually get auth code
    client.auth_with_code(douban_token)
    return client

def bestmovie(title, doubancli, thold=7):
    title = title.split(u'.1080p.')[0]
#     dic = {'q':title.encode('utf8'), 'count':3}
#     qstr = urllib.urlencode(dic)
#     urlstr = "http://api.douban.com/v2/movie/search?%s" % qstr
#     page = urllib2.urlopen(urlstr)
#     res = urllib.urlopen(urlstr).read()
#     dic = json.loads(res)
    dic = doubancli.movie.search(q=title, count=3)
    best = None
    for sub in dic['subjects']:
        score = sub['rating']['average']
        if score < thold:
            continue
        if not best or best['rating']['average'] < score:
            best = sub
    return best

def getinfo(red, doubancli):
    dic = {}
    best = bestmovie(red.text, doubancli)
    if not best:
        return None
    dic['text'] = red.text
    dic['score'] = best['rating']['average']
    for i in ('title', 'original_title', 'year', 'alt'):
        dic[i] = best[i]
    dic['img'] = best['images']['large']
    dow = red.findParent('tbody').findAll('td', {'class':'dow'})
    ed2k = dow[0].findAll('a', attrs={'class' : re.compile("ed2k.*")})
    dic['ed2k'] = ed2k[0].get('ed2k') 
    return dic
    
def main():
    doubancli = douban_cli()
    urlstr = 'http://oabt.org/?cid=11'  # 1080P
    data = getpage(urlstr)
    soup = BeautifulSoup(data)
    # print soup.prettify()
    aims = []
    for toplist in soup.findAll('div', {"class" : "toplist"}):
        aims += toplist.findAll('a', href=re.compile(u'show\.php\?tid=\d+?'))
    lst = [movieinfo(getinfo(aim, doubancli)) for aim in aims]
    infos = htmlinfo(lst)
        
    with open(CUR_MOVIES, 'w') as f:
        f.write(infos.encode('utf8'))
        f.close()

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
