#encoding:utf-8
    
def incr(dic,w):
    dic[w]=dic.setdefault(w,0)+1
    
def is_cs(word):
    return  u'\u4e00' < word < u'\u9fa5'
    
def sortk_iter(dic):
    return sorted(dic.iteritems())

def sortk_iter_bylen(dic,decrease=True):
    return sorted(dic.iteritems(),key=lambda (k,v):(len(k),v),reverse=decrease)
            
def sortv_iter(dic):
    for key, value in sorted(dic.iteritems(), reverse=True, key=lambda (k,v): (v,k)):
        yield key,value

def dic_out(dic,fname, iter_fn=sortk_iter, overide=False):
    if not overide:
        fname=fname+ '_out'
    f=open(fname,'w')
    for k,v in iter_fn(dic):  
        out_line="%s:%s\r\n" %(k,v)
        if type(out_line)==unicode:
            out_line=out_line.encode('utf-8')
        f.write(out_line)       
    f.close()  

g_char = u'[\+\-a-zA-Z0-9\u4e00-\u9fa5]'
g_div = u'[^(\+\-a-zA-Z0-9\u4e00-\u9fa5)]+'
g_noncsdiv = u'[^(\u4e00-\u9fa5)]+'

import re
def split_sens(txt):
  txt = to_unicode(txt.strip())
  lst = re.split(g_noncsdiv, txt)
  lst=filter(None,lst)
  if lst and is_cs(txt[-1]):
    return lst[:-1],lst[-1]
  else:
    return lst, u''
    
def iter_block(ppath,wc_threshold, target='.txt'):
    """neglect tail < threshold
    """
    blk_lst,wc=[],0
    for fname in iter_fname(ppath,target):
        remain=u''
        for line in open(fname,'r'):
            line = line.replace(' ','').replace('　','')
            wc+=len(line)
            sens,tail = split_sens(line)
            if sens:
                sens[0]=remain+sens[0]
                blk_lst += sens
            remain=tail
        if remain:
            blk_lst.append(remain)
        if wc >= wc_threshold:
            yield blk_lst
            blk_lst,wc=[],0    

def count_cs(ppath):
    count=0
    for line in iter_lines(ppath):
        for w in line:
            if is_cs(w):
                count+=1
    return count            
        
not_end = u'[a-zA-Z0-9，\u4e00-\u9fa5]'
u_space=u'[ 　]+'

import re
def repairline(fname):
    """repaire broken line"""
    txt=to_unicode(open(fname,'r').read())
    pattern, repl = '('+not_end + u')\r\n'+u_space + '('+not_end+')', r'\1\2'
    txt = re.sub(pattern, repl, txt)   # all are replaced
    wfile = open(fname, 'w')
    wfile.write(txt.encode('utf-8'))
    wfile.close()
            
import pickle
def savepkl(dic,dname):
    f = file(dname+'.pkl', 'wb')
    pickle.dump(dic, f)
    f.close()

def loadpkl(dname):
    f = file(dname+'.pkl', 'rb')
    dic= pickle.load(f)
    f.close()
    return dic

def iter_dics(out, high):
    for i in xrange(1,high):
        dname=out + os.sep + 'dic_%dw' %(i+1)
        yield loadpkl(dname), dname

def to_unicode(s):
    if type(s) !=unicode:
        s = s.decode('utf-8','ignore')
    return s
        
import os
from dbmgr import dbmanager

def saveall(dic,out):
    db=dbmanager(to_unicode(out))
    db.saveall(dic)
    del db
    
def load_dic(out):
    db=dbmanager(to_unicode(out))
    return db.getall()
    del db

import pylab
def plot_w(dic,name):
    X=pylab.frange(0,len(dic)-1)
    Y=list(sorted(dic.values(),reverse=True))
    Y=map(lambda y:pylab.log(y), Y)
    pylab.plot(X,Y)
    #show()
    pylab.savefig(name+'.png')  

def plot_dic_cmp(dic,imgname,firstnum):
    X=pylab.frange(0,len(dic)-1)
    Ys=list(sorted(dic.values(),key=lambda lis:sum(lis), reverse=True))
    for i in xrange(len(Ys[0])):
        Y=[y[i] for y in Ys]
        pylab.plot(X[:firstnum],Y[:firstnum])
    pylab.savefig(imgname+'_%d.png' %firstnum)  

def merged(dics):
    dic_sum={}
    for d in dics:
        dic_sum.update(d)
    return dic_sum
            
def cmp_dics(dics):
    dic_cmp=merged(dics)
    for k in dic_cmp:
        for d in dics:
            if k not in d:
                d[k]=0
    for k in dic_cmp: 
        dic_cmp[k]=[d[k] for d in dics]
    return dic_cmp
         
def weight_ave(v_ws):
    total,w_sum = 0,0
    for i in v_ws:
        total += i[0]*i[1]
        w_sum += i[1]
    average=0
    if w_sum >0:
        average= (float)(total)/w_sum
    return average  
       
def rela_name(fname):
    return fname[fname.rfind(os.sep)+1:]

import hashlib
def filemd5(fname):
    txt=open(fname,'rb').read()
    m=hashlib.md5()
    m.update(txt)    
    return m.hexdigest()

def get_dulps():
    return g_dulps

import os        
def _is_dulp(fname,rec,md5rec,dulps):
    """rec possible dulplicate file in files, and output them in folder
       dulplic condition: same fname or md5sum
       return: is dulplic or not
    """
    rela=rela_name(fname)
    if rela in rec:
        dulps[rela]=fname
    elif os.path.exists(fname):     #tolerate none exist file
        digest = filemd5(fname)
        if digest in md5rec:
            print 'dulp file', fname
            dulps[rela]=fname
            return True
        else:
            md5rec[digest]=fname
    else:
        rec[rela]=fname    
    return False    

def is_dulp(fnames):
    rec,md5rec,dulps={},{},{}
    for fname in fnames:
        _is_dulp(fname,rec,md5rec,dulps)
    return dulps             
    
g_rec,g_md5rec,g_dulps={},{},{}

def dulp_dec(iter_f):
    global g_rec,g_md5rec,g_dulps
    def _(*a, **kw):         # func args
        for fname in iter_f(*a, **kw):
            if not _is_dulp(fname,g_rec,g_md5rec,g_dulps):
                yield fname
    return _
    
@dulp_dec
def iter_fname(ppath,target):
    if ppath.find(os.sep)<0:
        yield ppath
        return
    for path, dirs, files in os.walk(ppath):
        for filename in files:
            fullpath = os.path.join(path, filename)
            suffix=filename[filename.rfind('.'):].lower()
            if suffix == target.lower():
                print fullpath
                yield fullpath     
                
def allsub(ws):
    for i in range(len(ws)):
        head,remain = ws[:i+1],ws[i+1:]
        if len(remain)<=0:
            yield head
        for p in allsub(remain):
            yield head +'|'+ p
                            
class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance


