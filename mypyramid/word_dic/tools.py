#encoding:utf-8
import logging

# v: [count,start,end]
def incr(dic,w,curpos):
    if len(w)>1 and w in dic:   # e.g.: 嘶嘶,阿朵阿多
        if curpos - dic[w][2]+1 <6: # neglect too near
            return
    dic.setdefault(w,[0,curpos,curpos])
    dic[w][0] += 1
    dic[w][2] = curpos
    
    
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
g_noncsdiv = u'[^\u4e00-\u9fa5]+'
g_nonendiv = u'[^\w]+'

def is_cs(word):
    return  u'\u4e00' < word < u'\u9fa5'
    
def is_en(word):
    return word.isalpha()
        
import re
def split_sens(txt ):
  txt = to_unicode(txt.strip())
  lst = re.split(g_noncsdiv, txt)
  lst=filter(None,lst)
  if lst and is_cs(txt[-1]):
    return lst[:-1],lst[-1]
  else:
    return lst, u''
    
def iter_block(ppath,wc_threshold, target='.txt'):
    """neglect tail < threshold"""
    blk_lst,wc=[],0
    for fname in iter_fname(ppath,target):
        logging.info(fname)
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

def get_singlefile(f):
    blk_lst = []
    remain=u''
    for line in f:
        line = line.replace(' ','').replace('　','')
        sens,tail = split_sens(line)
        if sens:
            sens[0]=remain+sens[0]
            blk_lst += sens
        remain=tail
    if remain:
        blk_lst.append(remain)
    return blk_lst

def split_sens_en(txt ):
  txt = to_unicode(txt.strip())
  lst = re.split(g_nonendiv, txt)
  lst=filter(None,lst)
  return lst
    
def iter_en_sens(ppath, target='.txt'):
    for fname in iter_fname(ppath,target):
        logging.info(fname)
        sens = []
        for sen in iter_single_en(open(fname,'r')):
            yield sen

 
def iter_single_en(f):
    for line in f:
        line = line.replace('　','') #chinese space
        sens = split_sens_en(line)
        if sens:
            yield sens
            
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

def clean_dic(out):
    db=dbmanager(to_unicode(out))
    return db.clean()
    
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
                logging.info(fullpath)
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

import enchant

def endicmaker(lang):
    dic=enchant.Dict(lang)
    def wrapper(word):
        return dic.check(word)
    return wrapper
iseng=endicmaker('en_US')

def pnamemaker(fname):
    f=open(fname,'r')
    pname=set()
    for line in f:
        pname.add(line.strip('\n'))
    def wrapper(word):
        return word.upper() in pname
    return  wrapper
is_peoplename=pnamemaker(os.path.join(os.path.dirname(__file__), 'people.name'))
              
def aimed_en(en,count):
#    max(os.stat(enfname).st_size/80000,10)
    count_thold = 8 
    return count >count_thold and en[0].isupper() and len(en)>1 and (is_peoplename(en) or not iseng(en))
    
    
def singularmaker():
    import inflect
    p = inflect.engine()
    def wrapper(word):
        return p.singular_noun(word)
    return wrapper
singular_teller = singularmaker()    

def merge_pluralname(en_dic):
    for k,v in en_dic.items():
        sig = singular_teller(k)
        if sig and sig != k and sig in en_dic:
            logging.info('plural name: %s -> %s' %(k,sig))
            v1=en_dic[sig]
            #merge
            en_dic[sig]=[v[0]+ v1[0], min(v[1],v1[1]), max(v[2],v1[2])]
            en_dic.pop(k) 
    
import matplotlib.pyplot as plt

def plotxy(x,y):
    import numpy as np
    x=np.array(x)
    y=np.array(y)
    A = np.vstack([x, np.ones(len(x))]).T
    (m,c), residuals = np.linalg.lstsq(A, y)[:2]
    plt.plot(x, y, 'o')
    plt.plot(x, m*x + c, 'r', label='Fitted line')
    plt.legend()
    plt.show()     
    return residuals[0]     

def plot_diff(X,Y):
    plt.plot(range(len(X)),map(lambda x:x-X[0],X),'g-',
             range(len(Y)),map(lambda y:y-Y[0],Y),'b+'
            )
    plt.show()
    
debug = True  
t_en=u'Tywin'
t_cs=u'泰温'


"""
x=[1855, 3703, 3753, 27889, 29522, 46153, 75929, 77632, 133482, 150157, 162140]
y=[7, 710, 1356, 1385, 10563, 11138, 16986, 28180, 28754, 50055, 56744, 61520]

y=kx+c  k~=0.38
for i in range(1,len(x)):
    if abs((y[i]-y[i-1] ) -2.6*(x[i]-x[i-1])) < 10:
                        
for i in range(1,len(y)-1):
    print plotxy(x,y[:i]+y[i+1:])
    
    
巴 [401, 54, 599356]
利 [1757, 185, 597768]
斯 [3044, 963, 598806]
坦 [411, 21412, 595323]
巴利斯坦 [35, 88810, 547425] 458615 3.17336455192e+11  4 1.69662466791e+11

"""    
