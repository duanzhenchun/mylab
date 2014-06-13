#coding=utf8
import re
from db import Mem
import ast

#http://people.umass.edu/nconstan/CMU-IPA/
#https://gist.github.com/srubin/5139432
#also:
#http://www.speech.cs.cmu.edu/cgi-bin/cmudict
#http://en.wikipedia.org/wiki/Arpabet

K_IPA = 'onion_en_IPA'

def phonetic(w):
    res = Mem.hget(name, w)
    if res:
        res = ast.literal_eval(res)
    return res

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
    Mem = redis.Redis()
    for w, lst in Dic.iteritems():
        Mem.hset(name, w, lst)
    
