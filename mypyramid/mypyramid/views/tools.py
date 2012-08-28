#encoding:utf-8

import re
import logging
import os

pagesize=20000
ahead = 1000
            
def to_unicode(s):
    if type(s) !=unicode:
        s = s.decode('utf-8','ignore')
    return s
    
def txt2html(txt):
    #for python2.6 
    return re.sub(re.compile('(^.*?$)', re.MULTILINE), '<p>\\1</p>', txt)
#    return re.sub('(^.*?$)', '<p>\\1</p>', txt, flags=re.MULTILINE)
        
    
def find_key(dic, val):
    res=None
    lst = [k for k, v in dic.iteritems() if v == val]
    if lst: 
        res = lst[0]
    return res
    
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
    
def sortk_iter_byklen(dic,decrease=True):
    return sorted(dic.iteritems(),key=lambda (k,v):(len(k),v),reverse=decrease)

def sortk_iter_byvlen(dic,decrease=True):
    return sorted(dic.iteritems(),key=lambda (k,v):(len(v),k),reverse=decrease)
    
                        
def dicsub(dic, txt, dicref):
    # trans en already
    for en,cs in sortk_iter_byklen(dic):
        txt = re.sub(en, hint(en,cs,dicref), txt)
    # trans cs
    for en,cs in sortk_iter_byvlen(dic):    
        #negtive lookbehind & lookahead
        txt = re.sub('((?<!title=\'))%s((?!\'))' %cs, '\\1%s\\2' %hint(en,cs,dicref), txt)
        
    return txt
    
def hint(k,v, dicref):
    return "<a title='%s' class=edit-word href=# >%s</a>"  %(v,k)


import posixpath

_os_alt_seps = list(sep for sep in [os.path.sep, os.path.altsep]
                    if sep not in (None, '/'))
                    
def safe_join(directory, filename):
    """Safely join `directory` and `filename`.  If this cannot be done,
    this function returns ``None``.
    """
    filename = posixpath.normpath(filename)
    for sep in _os_alt_seps:
        if sep in filename:
            return None
    if os.path.isabs(filename) or filename.startswith('../'):
        return None
    return os.path.join(directory, filename)
