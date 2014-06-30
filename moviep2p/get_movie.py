#!/usr/bin/env python
# coding=utf-8
import os
import filecmp
from conf import *
from utils import *

douban_token = '26813bd953cdac9e'
src_url = 'http://oabt.org/?cid=%d'
movie_type = 7 #720p
movie_thold = 7


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

def bestmovie(title, doubancli):
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
        if score < movie_thold:
            continue
        if not best or best['rating']['average'] < score:
            best = sub
    return best

def getinfo(tr, doubancli):
    td= tr.find('td', {'class':'name magTitle'})
    title = td.find('a').text
    dow=tr.find('td', {'class':'dow'})
    a = dow.find('a', attrs={'class' : re.compile("ed2k.*")})
    ed2k = a.get('ed2k') 
    #print title, ed2k
    dic = {}
    best = bestmovie(title, doubancli)
    if not best:
        return None
    dic['text'] = title
    dic['score'] = best['rating']['average']
    for i in ('title', 'original_title', 'year', 'alt'):
        dic[i] = best[i]
    dic['img'] = best['images']['large']
    dic['ed2k'] = ed2k
    return dic
   
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
    return MOVIE_FMT % (dic['alt'], dic['img'], dic['score'], dic['title'], dic['original_title'], dic['year'], dic['ed2k'], dic['text'])
    

def insanity():
    soup=BeautifulSoup(data)
    d=soup.find('div', {'class':'file_src file_list liebiao'})
    lis=d.findAll('li')
    f=open('/home/whille/Desktop/out.txt', 'w')
    for li in lis:
        a=li.find('a', {'class':re.compile('file_name .*')})
        if a:
            f.write('%s, %s\n' %(a.get('title'), a.get('href')))
    f.close()


def send_mail():
    import mailer 
    if filecmp.cmp(CUR_MOVIES, CUR_MOVIES+'.new'):
        os.remove(CUR_MOVIES+'.new')
        return
    os.rename(CUR_MOVIES+'.new', CUR_MOVIES)    
    Tos=['whille@163.com',]
    with open(CUR_MOVIES) as f:
        infos = f.read().decode('utf8')
        if len(infos)>10:
            mailer.send(infos, Tos)
 
def main():
    doubancli = douban_cli()
    urlstr = src_url %movie_type
    print urlstr
    data = getpage(urlstr)
    soup = BeautifulSoup(data)
    toplist =soup.find('div', {"class" : "toplist"})
    trs=toplist.findAll('tr')
    trs=trs[1:] #cut table head
    print len(trs)
    lst=[]
    for tr in trs:
        dic = getinfo(tr, doubancli)
        if dic:
            lst.append(movieinfo(dic))
    if not lst:
        return
    infos = htmlinfo(lst)
    with open(CUR_MOVIES+'.new', 'w') as f:
        f.write(infos.encode('utf8'))
        f.close()
        

if __name__ == '__main__':  
     main()
     send_mail()
