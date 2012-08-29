#encoding:utf-8
import os,re,sys,logging
import mmap
import matplotlib.pyplot as plt

len_thold=0.2

def allpos(pattern, fname):
    size = os.stat(fname).st_size
    f = open(fname,'r')
    data = mmap.mmap(f.fileno(), size, access=mmap.ACCESS_READ)
    res=None
    res = [m.start() for m in re.finditer(pattern, data)]
    return res


def cal_diff(x,y, show=False, label=''):
    """return average of residuals"""
    adjust_miss(x,y)
    import numpy as np
    x=np.array(x)
    y=np.array(y)
    A = np.vstack([x, np.ones(len(x))]).T
    (m,c), residuals = np.linalg.lstsq(A, y)[:2]
    if len(residuals)<1:
        logging.error('residuals is None')
        return 999999
    if show:
        plt.plot(x, y, 'o', label=label)
        plt.plot(x, m*x + c, 'r', label='Fitted line')
        plt.legend()
        plt.show()          
    return (residuals[0]/len(x))**0.5/len(x)

def plot_diff(lsts):
    plt.plot(range(len(lsts[0])),map(lambda x:x-lsts[0][0],lsts[0]),'g-',
             range(len(lsts[1])),map(lambda x:x-lsts[1][0],lsts[1]),'b+'
             )
    plt.show()
    

def sim_distance(X, Y):
  si = {}
  for item in prefs[person1]:
    if item in prefs[person2]: si[item] = 1
  # if they have no ratings in common, return 0
  if len(si) == 0: return 0
  # Add up the squares of all the differences
  sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                      for item in prefs[person1] if item in prefs[person2]])
  return 1 / (1 + sum_of_squares)
 
 
def slope(X,Y,i):
    res = (Y[i]-Y[0])*1.0/(X[i]-X[0])
    return res
    
def notgood(lst1,lst2):
    if len(lst1)<2 or len(lst2)<2:
        return True
    return  False
            
def adjust_miss(X,Y):
    slope_thold=1.1
    if len(X)==len(Y):
        return
    newlen=min(len(X),len(Y))  
    if len(Y)-len(X)<0:
        aim=X
    else:
        aim=Y
    difflen=abs(len(Y)-len(X))
    roughk=slope(X,Y,newlen-1)
    for i in xrange(1,newlen):
        if difflen==0:
            break
        k=slope(X,Y,i)
        if (len(Y)<len(X) and k>slope_thold*roughk) or (len(Y)>len(X) and k<1.0/(slope_thold*roughk)):
            aim.pop(i)
            difflen-=1
    if difflen>0:
        for i in xrange(difflen):
            aim.pop(-1) 
    assert len(X) == len(Y)

def test_adjust():
    X=range(10)
    Y=range(10)
    Y.pop(3)
    adjust_miss(X,Y)
    print X,Y
    
def decode_line(line):
    word,count=line.split(':')
    count=int(count)
    return word, count
      
def dict_nmin(dic,n):
    import heapq
    return heapq.nsmallest(n ,dic, key = lambda k: dic[k])
    
     
def encs_match(path,en_w,en_count):
    fnames=('en/en.txt','cs/cs.txt')
    cs_range=[int(i*en_count) for i in (1-len_thold, 1.0/(1-len_thold))]

    lst_en=allpos(en_w,path+os.sep+fnames[0])   
    candidates={}
    csfname=os.sep.join((path, 'cs', 'cs_out'))
    csfile = open(csfname,'r')
    for line in csfile:
        cs_w,cs_count=decode_line(line)
        if cs_count in range(*cs_range):
            x=lst_en[:]
            y=allpos(cs_w,path+os.sep+fnames[1])   
            if notgood(x,y):
                continue
            show =False
            label=to_unicode('%s_%s' %(en_w,cs_w))
            # longer the cs word, more precious, so divide the length for distance
            candidates[cs_w] = cal_diff(x,y,show, label)/len(cs_w)
    res = dict_nmin(candidates,3)
    info = "%s:%d:   " %(en_w, en_count)
    for k in res:
        info += "%s:%d" %(k,candidates[k])
    print info
    

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
is_peoplename=pnamemaker('people.name')

def find_allmatch(path):
    enfname=os.sep.join((path, 'en', 'en_out'))
    f = open( enfname ,'r')    
    for line in f:   
        w,count=decode_line(line)  
        if count >8 and w[0].isupper() and len(w)>1 and (not iseng(w)):
            encs_match(path,w,count)    

from genwords import *
def rehearsal():
    path = './Foundation'
    gen_whole_merge_save(path+os.sep+'cs', 10**5)
    gen_eng(path+os.sep+'en')
    find_allmatch(path)
                
def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: %s PATH' % sys.argv[0])
    path = sys.argv[1]
    logging.basicConfig(level=logging.DEBUG, filename=path+'.log')
#    find_allmatch(path)
    rehearsal()

if __name__ == "__main__":
    sys.exit(main())  
                  
