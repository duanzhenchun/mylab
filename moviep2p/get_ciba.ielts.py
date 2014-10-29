from utils import *
import BeautifulSoup

url='http://web.iciba.com/ciku/list.php?mod=IELTS_1'
res = getpage(url)
soup = BeautifulSoup.BeautifulSoup(res)
ws = soup.find('div', id='word_list')
res=ws.findAll('div',{'class':'wl_char_list'})
f=open('./ielts.words.all.txt','w')
for i in res:
    # except phrases
    f.write('%s\n\n' %(' '.join(i.findAll('a',text=re.compile('^[^\s]+$')))))
f.close()

