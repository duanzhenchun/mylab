#!/usr/bin/env python
# coding=utf-8
import os
import filecmp
from conf import *
from utils import *

def douban_cli():
    from douban_client import DoubanClient
    client = DoubanClient(API_KEY, API_SECRET, redirect_uri, SCOPE)
    if not douban_token:
        print client.authorize_url
        # manually get auth code
    client.auth_with_code(douban_token)
    return client

def bestmovie(title, doubancli):
    title = title.split(u'.1080p.')[0]
    dic = doubancli.movie.search(q=title.split('HR-HDTV')[0], count=3)
    best = None
    if dic['total']<1:
        return
    for sub in dic['subjects']:
        score = sub['rating']['average']
        if score < Movie_thold:
            continue
        if not best or best['rating']['average'] < score:
            best = sub
    return best

def getinfo(tr, doubancli):
    td= tr.find('td', {'class':'name magTitle'})
    title = td.find('a').text
    dow=tr.find('td', {'class':'dow'})
    a = dow.find('a', attrs={'class' : re.compile("ed2k.*")})
    if not a:
        return
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

def htmlinfo(lst):
    if not lst:
        return None
    return Movie_head + ''.join(lst) + '</body>'

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
    newfname = CUR_MOVIES+'.new'
    if filecmp.cmp(CUR_MOVIES, newfname):
        os.remove(CUR_MOVIES+'.new')
        return
    os.rename(CUR_MOVIES+'.new', CUR_MOVIES)    
    with open(CUR_MOVIES) as f:
        infos = f.read().decode('utf8')
        if len(infos)>10:
            mailer.send(infos, Tos)
 
def main():
    doubancli = douban_cli()
    urlstr = src_url %Movie_type
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
    send_mail()

if __name__ == '__main__':  
     main()
