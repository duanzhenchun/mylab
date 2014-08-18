import math
import json
import urllib
from utils import *


def outf(lst, fname):
    import codecs
    fw = codecs.open(fname, 'w', encoding='utf-8')
    for i in lst:
        fw.write(u'\t'.join(i) + u'\n')
    fw.close()


def gen_comments(videoid):
    pages = 10**4
    for page in range(1,pages+1):
        ap = {"videoid":videoid, "page":page}
        qstr = urllib.urlencode({"__ap":ap})
        url = 'http://comments.youku.com/comments/~ajax/vpcommentContent.html?__ap=' + '%7B%22videoid%22%3A%22' + videoid +'%22%2C%22page%22%3A' + str(page) +'%7D'
        data=getpage(url)
        dic=json.loads(data)
        con=dic['con']
        soup2=BeautifulSoup(con)
        res=soup2.findAll('div',{'class':'comment'})
        if page==1:
            total = int(dic['totalSize'])
            page_size = len(res)
            pages = page_size and int(math.ceil(total*1.0/page_size)) or 1
            print total, page_size, pages
        print 'page:', page
        for t in res:
            username =t.find('a',id=re.compile('comment_name')).text
            comment =t.find('div',{'class':'text'}).text
            yield (username, comment)

if __name__ == '__main__':
    videoid='XNzU0MDg1MjA4'
    outf(gen_comments(videoid), 'out.txt')
    
