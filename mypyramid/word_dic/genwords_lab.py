#encoding:utf-8
strTotal = u'_all'

import sys,logging
from tools import * 

def test_incr2():
    dic,rdic={},{}
    incr2(u'葡萄',dic)
    incr2(u'萄葡',rdic)
    print dic,rdic

# 2 char    
def incr2(w,d):
    d.setdefault(w[:-1],{})
    d[w[:-1]][w[-1]]=d[w[:-1]].setdefault(w[-1],0)+1
    d[w[:-1]][strTotal]=d[w[:-1]].setdefault(strTotal,0)+1   # we can use float as possibility, but n/sum is efficient      
                
def gen_w2(sens,dic,rdic):
    for sen in sens:
        for i in xrange(len(sen)-1):
            incr2(sen[i:i+2],dic)
            incr2(sen[i+1]+sen[i],rdic)
    
"""
- 葡萄
symmetry:
- forward： one direction does not interfear other 
- backward: 谁的
high level：
1 to 2, 2 to 3, 3 to all
- 艾莉亚： 艾莉|莉亚
- 自己人： 自己|人
- 布兰登： 布兰
- 布莱克|布莱美
- 布鲁克斯
- 蒙大拿
"""
def test_word():
    f=open('sample/3cs.txt','r')
    dic = gen_singlef2(f)
    print 'wdict len', len(dic)
    for k,v in dic.iteritems():print k,v,
    for i in (u'琼恩', u'艾莉亚', u'唐纳', u'梅里', u'克里冈', u'唐纳尔',u'培提尔',u'卡丽熙'):
        assert i in dic
    for i in (u'熊的', u'的男'):
        assert i not in dic

def gen_singlef2(f, high=9 ):
    sents = getsents(f)
    dic,rdic={},{}
    gen_w2(sents,dic,rdic)
    fsize=getfsize(f)   
    print 'fize:',fsize
    # assume 10**5 file has 1 count on average 
    thold=0.01 # fsize * 10**(-5)
    #find possible w
    wdic={}
    for w in dic:
        wcount = dic[w][strTotal]
        for w1,count in dic[w].iteritems():
            if strTotal == w1: continue
            if w+w1 == u'梅里':
                print count,wcount,rdic[w1][w],rdic[w1][strTotal],1.0* count /wcount * rdic[w1][w]/rdic[w1][strTotal]
            if thold < 1.0* count /wcount * rdic[w1][w]/rdic[w1][strTotal]:
                wdic[w+w1]=count   
              
#    for l in range(2,high):
#        hdic = gen_whigh(sents,wdic,l)
#        gen_wtrue(hdic,wdic,rdic,thold) 
    return wdic                        
    
def gen_whigh(sents,wdic,lowlen):
    hdic={}
    for sen in sents:
        for i in xrange(len(sen)-lowlen):
            if sen[i:i+lowlen] in wdic and sen[i+lowlen-1:i+lowlen+1] in wdic:
                incr2(sen[i:i+lowlen+1],hdic)
    return hdic
#    trim_low(dic_l,dic_h)
#    cut_tail(dic_h)    
#    return dic_h
        
def gen_wtrue(hdic,wdic,rdic,thold):
    for w in hdic:   #艾莉
        for w1,count in hdic[w].iteritems(): #亚
            if strTotal == w1: continue
            if thold < count *1.0* rdic[w1][w[-1]]/rdic[w1][strTotal]:
                wdic[w+w1]=count   #艾莉亚
                # trim low
                if w in wdic:
                    wdic[w]-=count
                    if thold > wdic[w] *1.0* rdic[w[-1]][w[-2]]/rdic[w[-1]][strTotal]:
                        del wdic[w]
                if w[-1]+w1 in wdic:    #莉亚
                    wdic[w[-1]+w1]-=count
                    if thold > wdic[w[-1]+w1] *1.0* rdic[w1][w[-1]]/rdic[w1][strTotal]:
                        del wdic[w[-1]+w1]
                            
if __name__ == "__main__":
    test_word()
