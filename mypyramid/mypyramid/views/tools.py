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
    logging.info(abspath)
    return abspath
    
def getdic(fpath):
    path=getabspath(fpath)
    return dict(gendic(path))  
    
def sortk_iter_bylen(dic,decrease=True):
    return sorted(dic.iteritems(),key=lambda (k,v):(len(k),v),reverse=decrease)
                    
def dicsub(dic, txt, iter_fn=sortk_iter_bylen):
    for k,v in iter_fn(dic):
        txt = re.sub(k, '%s(%s)' %(v,k), txt)
    return txt
    
