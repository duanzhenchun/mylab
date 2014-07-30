#encoding=utf8
import os
import logging
import gzip
import struct
import re
from db import *
from utils import *


Vocut = re.compile('\[.+?\]|/.+?/ ')
Egcut = re.compile(u':.+?(?=\n)')
Origin = ('adj ', 'adv ')

def dict_info(ifoloc):
    logging.info("parse stardict info file %s" % ifoloc)
    try:
        ifo = open(ifoloc, 'r')
    except IOError:
        logging.warn("failed to open %s" % ifoloc)
        return False
    ifodata = {}
    for line in ifo.readlines():
        if line.find('=')<0:
            continue

        if line[-1] == '\n':
            line = line[:-1]
        k, v = line.split('=')
        ifodata[k] = v
    return ifodata

def get_dict(folder, fname):
    ifoloc = '%s/%s.ifo' %(folder, fname)
    ifodata = dict_info(ifoloc)
    wordcount, bookname  = [ifodata.get(i) for i in ('wordcount', 'bookname')]
    wordcount=int(wordcount)
    print wordcount, bookname
    idx=open('%s/%s.idx' %(folder, fname),'rb')
    idxdata=idx.read()
    f=gzip.open('%s/%s.dict.dz' %(folder, fname),'rb')

    encoding=get_encoding(f.read(200))
    print encoding
    f.seek(0)
    start = 0
    Wdict={}
    last=('','')
    for i in range(wordcount):
        pos = idxdata.find('\0', start, -1)
        fmt = "%ds" % (pos-start)
        w = struct.unpack_from(fmt, idxdata, start)[0]
        start += struct.calcsize(fmt) + 1
        (off, size) = struct.unpack_from(">LL",idxdata, start)
        start += struct.calcsize(">LL")
        f.seek(off,0)
        v = f.read(size)
        if w.find(' ')>=0:    #exclude phrase
            continue
        v = Egcut.sub('', v+'\n').strip()
        if len(Vocut.sub('', v))<5:
            v += '\n%s:\n%s' %last
            #Wdict[w]= v 
            #Mem.hset(K_encs, w, v)
        else:
            last = (w,v)
        Wdict[w] = v 
    return Wdict


def oxford_dict():
    folder='%s/.stardict/dic/%s' %(os.path.expanduser('~'),'stardict-oxford-gb-2.4.2')
    fname='oxford-gb'
    Wdict=get_dict(folder, fname)

def add2langdao(Wdict):
    for w in Wdict:
        if Vocut.sub('', v)[:4] in Origin:
            w1=w
        else:
            w1=word_lem(w)
        if not Mem.hexists(K_encs, w1):
            Mem.hset(K_encs, w1, Wdict[w])

def langdao_ec_dict():
    folder='%s/.stardict/dic/%s' %(os.path.expanduser('~'),'stardict-langdao-ec-gb-2.4.2')
    fname='langdao-ec-gb'
    Wdict=get_dict(folder, fname)

def cmu():
    folder = '../data/stardict-cmudict-2.4.2'
    fname='cmudict'
    Wdict=get_dict(folder, fname)
    dump_pronounce(Wdict)

def dump_pronounce(Wdict):
    Mem.delete(K_IPA)
    for w,v in Wdict.iteritems():
        Mem.hset(K_IPA, w, v)


