import urllib2
import logging  
import json

json_fmt='alt=json'
apikey='apikey=0cc65c265ad25ea12653147310771be3'

def init_log(lvl=logging.INFO):
    import logging,sys
    selflogfile = "./%s.log" % (sys.argv[0].split('/')[-1][:-3])
    logging.basicConfig(filename=selflogfile,level=lvl, format='[%(asctime)s] [%(levelname)s] %(message)s')

simbol = '='
max_pos=50

def progressbar(n,pos):
    pos=pos*max_pos/n
    s='\r[%s>%s]' %(simbol*pos,' '*(max_pos-pos))
    print s,

import time    
def waitmaker(sleeptime):
    l_c=[40,0]
    def clo():
        l_c[1]+=1
        if l_c[1] %l_c[0] == 0:
            print 'wait'
            time.sleep(sleeptime)
    return clo
waitnot=waitmaker(60)

from random import randint

def randselect(length):
    return [randint(1*10**6,9*10**6) for i in range(length)]

def get_ret(urlstr,kv=None):
    waitnot()
    try:
        urlstr +='?'
        if kv:
            for k,v in kv.iteritems():
                urlstr +='%s=%s&' %(k, str(v))
        urlstr +=json_fmt + '&' + apikey
        logging.info(urlstr)
        data=urllib2.urlopen(urlstr).read()
        return json.loads(data)
    except urllib2.HTTPError, e:
        if e.code in(403,404):
            logging.error(urlstr)
            logging.error(e)
            return None
    except Exception, e2:
            logging.error(urlstr)
            logging.error(e2)            
            return None
            #raise e
