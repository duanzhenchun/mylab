#encoding:utf-8

from tools import *
    
import os
def test_dulplicate():
    assert not is_dulp([])   
    assert not is_dulp(['tmp'])
    assert is_dulp(['tmp']*2)
    fnames=['ff.txt','fefe', './ave fe/ff.txt',]
    assert is_dulp(fnames) 
    assert is_dulp(['~/mydoc/yum.txt']*2)   
    assert is_dulp(['./sample/titles','./sample/copy of titles',])

def test_allsub():
    ws=u'谢文东笑'
    lst = list(allsub(ws))
    assert len(lst) == 8
    for i in lst:    
        print i
        
def test_singleton():
    s1=Singleton()
    s2=Singleton()
    assert id(s1)==id(s2)
    
