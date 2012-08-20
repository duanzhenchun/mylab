#encoding:utf-8

import re
import logging

def to_unicode(s):
    if type(s) !=unicode:
        s = s.decode('utf-8','ignore')
    return s
    
def txt2html(txt):
    return re.sub('(^.*?$)', '<p>\\1</p>', txt, flags=re.MULTILINE)
        
def txt2html2(txt):
    return re.sub('(^.*?$)', '\\1<br/>', txt, flags=re.MULTILINE)
    
def find_key(dic, val):
    res=None
    lst = [k for k, v in dic.iteritems() if v == val]
    if lst: 
        res = lst[0]
    return res
    
pagesize=20000
ahead = 1000

import os
def getlastpage(fname):
    print fname
    size = os.path.getsize(fname)
    return size/pagesize

class OutpageException(Exception):
    def __init__(self, pagenum):
        self.pagenum = pagenum
                            
def getpage(fname, pageindex=0):
    """read page roughly by byte size"""
    size = os.path.getsize(fname)
    pagenum = size/pagesize
    if pageindex > pagenum:
        raise OutpageException(pagenum)
    
    f=open(fname,'r')
    pos=pageindex * pagesize
    #ahead some line
    pos -= ahead
    if pos <= 0: 
       f.seek(0)   
    else:
        f.seek(pos)
        f.readline()
    txt = f.read(pagesize)
    txt += f.readline()    
    return txt

def getpage2(fname, pageindex=0, pagelines=100):
    f=open(fname,'r')
    startline=pageindex * pagelines
    txt=''
    i = 0
    for line in f:
        i+=1
        if i <startline:
            continue
        if i > startline + pagelines:
            break
        txt += line
    else:
        if i < startline:
            raise Exception('out of page!')   
    return txt
        
def gendic(fpath):
    f=open(fpath,'r')
    for line in f.readlines():
        if len(line)<2:continue
        ch,en = map(str.strip, line.strip('\n').replace('：',':').split(':'))
        if len(ch)<1 or len(en) <1: continue
        yield(to_unicode(ch),to_unicode(en))    
                
def getabspath(fpath):
    from pyramid.path import AssetResolver
    a = AssetResolver('mypyramid')
    resolver = a.resolve(fpath)
    abspath = resolver.abspath()
    logging.debug(abspath)
    return abspath
    
def getdic(fpath):
    path=getabspath(fpath)
    return dict(gendic(path))  
    
def sortk_iter_bylen(dic,decrease=True):
    return sorted(dic.iteritems(),key=lambda (k,v):(len(k),v),reverse=decrease)

def sortk_iter_byvlen(dic,decrease=True):
    return sorted(dic.iteritems(),key=lambda (k,v):(len(v),k),reverse=decrease)
    
                        
def dicsub(dic, txt, dicref, iter_fn=sortk_iter_byvlen):
    for en,cs in iter_fn(dic):
        txt = re.sub(en, hint(en,cs,dicref), txt)
        #negtive lookbehind
        txt = re.sub('((?<!title=\'))%s((?!\'))' %cs, '\\1%s\\2' %hint(en,cs,dicref), txt)
    return txt
    
def popup(txt):
    txt= """<div class="bodynav"><li class="bodynavli"> %s <ul><li class="bodynavli"><a href="/">Edit</a></li><li class="bodynavli"><a href="/">Delete</a></li></ul></li></div>""" %txt
    return txt
        
def hint(k,v, dicref):
#    return "<a title='%s'  class=edit-word href=%s>%s </a>"  %(v,dicref,k )
    return "<a title='%s' class=edit-word href=# >%s</a>"  %(v,k)

