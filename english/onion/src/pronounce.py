#coding=utf8
import re
import ast
from db import *
from utils import *

#http://people.umass.edu/nconstan/CMU-IPA/
#https://gist.github.com/srubin/5139432
#also:
#http://www.speech.cs.cmu.edu/cgi-bin/cmudict
#http://en.wikipedia.org/wiki/Arpabet


def show(w):
    res = Mem.hget(K_IPA, w)
    return res and tounicode(res, 'utf8') or ''

# abandoned, used cmudict instead
def prepare():
    import zipfile
    from collections import defaultdict

    Dic=defaultdict(list)
    Match = re.compile(r'(\w+)(\((\d+)\))?[ \t,]+(\w+)', re.U)
    f=zipfile.ZipFile('../data/CMU-in-IPA.zip','r')
    fname=f.namelist()[0]
    print fname
    txt=f.read(fname).decode('utf8')
    Sep=re.compile(u'[\s\t,]+')
    for line in txt.split('\n'):
        res = Match.search(line)
        if res:
            w, alp =(res.group(i) for i in (1, 4))
            Dic[w].append(alp)
    Mem = redis.Redis(db=1)
    for w, lst in Dic.iteritems():
        Mem.hset(K_IPA, w, lst)
    
