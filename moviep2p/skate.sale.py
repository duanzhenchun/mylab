from utils import *
import mailer

AIM_SIZE = (' 285 ', ' 260 ')   #size 42.5, 39
tolist = ['whille@163.com',]
saleurl = 'http://www.skatermate.co.uk/skateshop/cat_284313-Clearance-Items-up-to-50-off-clearance-items.html'
SALE_FMT='<a href="%s" >%s</a></br>' %((saleurl,)*2)

def main():
    data = getpage(saleurl)
    soup = BeautifulSoup(data)
    res = soup.findAll('h2', {"class" : "wdk_shopproduct-title"})


    lst=[]
    for i in res:
        for aim in AIM_SIZE:
            if i.string.find(aim)>=0:
                lst.append("<li>%s</li>" %i.string)
    infos = htmlinfo(lst)
    if infos:
        mailer.send(SALE_FMT+infos, tolist, sub='skate sale')

if __name__ == '__main__':
     main()
