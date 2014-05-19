#coding=utf8
from nltk.corpus import wordnet
import re
from stemming.porter2 import stem
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import marshal
import logging
import tempfile
import sys
import os
import random
from utils import *


log_console = logging.StreamHandler(sys.stderr)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_console)

WDict=None
Dic_uk=None
initialized=False
Word_pat = re.compile(r"[\w’']+|\W+")
ST = PorterStemmer()
Wnl= WordNetLemmatizer()

def word_lem(w):
    w = w.lower()
    if w in Dic_uk:
        w=Dic_uk[w]
    return ST.stem(Wnl.lemmatize(w))

def init_dict(fname='all.num'):
    f=open(fname)
    lst=f.readlines()
    dic={}
    for l in lst[-1:0:-1]:
        t = l.strip().split(' ')
        w = word_lem(t[1])
        dic[w] = max(dic.get(w,0), int(t[0]))
    return dic


def uk_us():
    #http://www.tysto.com/uk-us-spelling-list.html
    uk_f = open('uk.txt')
    us_f = open('us.txt')
    dic={}
    for uk, us in zip(uk_f, us_f):
        dic[uk.strip()]=us.strip()
    return dic

@benchmark
def gen_paras(dic, txt, k):
    for line in txt.split('\n'):
        yield '<p>'
        for w0 in Word_pat.findall(line):
            if not w0.isalpha():
                yield w0
            else:
                w = word_lem(w0)
                if w in dic and dic[w]<= k:      
                    yield word_def(w0)
                else:
                    yield w0
        yield '</p>'


def word_def(w):
    ss = wordnet.synsets(w)
    if not ss:
        return w
    else:
        definition = '%s:\n%s' %(ss[0].name, ss[0].definition)
        return '<span title="%s" >%s</span>' %(definition, w)


def init():
    global WDict, Dic_uk, initialized
    if initialized:
        return
    cache_file = os.path.join(tempfile.gettempdir(),"en_word_freq.cache")
    load_fail = True 
    if os.path.exists(cache_file):
        logger.debug("loading model from cache %s" % cache_file)
        try:
            WDict, Dic_uk = marshal.load(open(cache_file,'rb'))
            logger.debug('english dict len: %d' %len(WDict))
            load_fail = False
        except Exception, e:
            print e
    if load_fail:
        Dic_uk = uk_us()
        WDict = init_dict()
        logger.debug("dumping model to file cache %s" % cache_file)
        try:
            tmp_suffix = "."+str(random.random())
            with open(cache_file+tmp_suffix,'wb') as temp_cache_file:
                marshal.dump((WDict, Dic_uk), temp_cache_file)
            if os.name=='nt':
                import shutil
                replace_file = shutil.move
            else:
                replace_file = os.rename
            replace_file(cache_file+tmp_suffix,cache_file)
        except:
            logger.error("dump cache file failed.")
            logger.exception("")
    initialized = True

@benchmark
def api(txt):
    k=WDict.get(word_lem('freak'))
    print 'k:%d' %k
    return ''.join(gen_paras(WDict, txt, k))


def test(fname):
    print fname
    txt=open(fname).read()
    k=WDict.get(word_lem('freak'))
    print 'k:%d' %k
    f=open('%s.html' %fname, 'w')
    f.write(to_html(''.join(gen_paras(WDict, txt, k)), 'onion'))
    f.close()

init()

if __name__ == '__main__':
    test('razors.edge.txt')

