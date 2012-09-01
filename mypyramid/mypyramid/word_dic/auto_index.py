#encoding:utf-8
import os,re,sys,logging,math
#import mmap
import matplotlib.pyplot as plt
from tools import *

len_thold=0.15
slope_thold=1.1
    
def getfsize(f):
    f.seek(0,2)
    size=f.tell()
    f.seek(0)
    return size    
        
def allpos(pattern, data):
#    data = f.read() #mmap.mmap(f.fileno(), size, access=mmap.ACCESS_READ)
    res=None
    res = [m.start() for m in re.finditer(pattern, data)]
    return res


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
            
def decode_line(line):
    word,count=line.split(':')
    count=int(count)
    return word, count
      
def dict_nmin(dic,n):
    import heapq
    return heapq.nsmallest(n ,dic, key = lambda k: dic[k])
    
def aimed_en(en,count,count_thold):
    return count >count_thold and en[0].isupper() and len(en)>1 and (is_peoplename(en) or not iseng(en))
    
def find_allmatch(path):
    enfname=os.sep.join((path, 'en', 'en_out'))

    fnames=('en/en.txt','cs/cs.txt')
    endata=open(path+os.sep+fnames[0],'r').read()
    csdata=open(path+os.sep+fnames[1],'r').read()
    posdic_cs={} 
    csfname=os.sep.join((path, 'cs', 'cs_out'))
    enfile = open(enfname ,'r')  
    csfile = open(csfname,'r')
    res={}
    count_thold = 5# max(os.stat(enfname).st_size/80000,10)
    for line in enfile:   
        en,count=decode_line(line)  
        if aimed_en(en,count,count_thold):
            for info in encs_match(posdic_cs,endata,csdata,csfile,en,count):
                res[en]= info    
    return res

def find_dicmatch(endic,csdic,enf,csf):
    enf.seek(0)
    csf.seek(0)
    csdata = to_unicode(csf.read())
    endata=enf.read()
    posdic_cs={} 
    res={}
    count_thold = max(getfsize(enf)/40000,10)
    for en, count in iter(sorted(endic.iteritems())):
        if aimed_en(en,count,count_thold):
            for info in encs_match(posdic_cs,endata,csdata,csdic,en,count):
                res[en]=info
    return res
    
def get_iterfn(data):
    def iter_f(f):
        f.seek(0)
        for line in data:
            yield decode_line(line)    
    if dict == type(data):
        return lambda data: data.iteritems()
    elif file == type(data):
        return iter_f
    else:
        raise Exception('data type not supported')     
    
def encs_match(posdic_cs,endata,csdata, csfile,en_w,en_count):
    scale = 1.0*len(csdata)/len(endata)
    poslst_en = allpos(en_w,endata)
    cs_range=[int(i*en_count) for i in (1-len_thold, 1.0/(1-len_thold))]
    candidates={}
    iter_fn=get_iterfn(csfile)
    for cs_w,cs_count in iter_fn(csfile):
        if cs_count in range(*cs_range):
            if cs_w not in posdic_cs: 
                posdic_cs[cs_w] = allpos(cs_w,csdata)
            x=poslst_en[:]
            update_candi(scale,en_w,cs_w,x,posdic_cs[cs_w], candidates)
    for info in match_res(candidates,en_w,en_count):
        yield info

        
def update_candi(scale,en_w,cs_w,x,y,candidates):
    if notgood(x,y):
        return
#    show =False
#    label=to_unicode('%s_%s' %(en_w,cs_w))
    # longer the cs word, more precious, so divide the length for distance
    distance = cal_diff1(scale,x,y)/len(cs_w)**0.5
#    distance = cal_diff(x,y)*abs(count_vowel(en_w)-len(to_unicode(cs_w)))
    if distance < 55:
        candidates[cs_w] = distance 
            
def cal_diff1(scale,x,y):
#    torture=2**abs(len(y)-len(x))
    adjust_miss1(x,y)
    residuals = 0
    for i in range(len(x)):
        residuals += (x[i]*scale - y[i])**2
    return (residuals/len(x))**0.5/len(x)    
            
def adjust_miss1(X,Y):
    if len(X)==len(Y):
        return
    newlen=min(len(X),len(Y))  
    for aim in (X,Y):
        for i in range(newlen,len(aim)):
            aim.pop(-1)
    return


def match_res(candidates, en_w,en_count, num=3):  
    if not candidates:
        return
    res = dict_nmin(candidates,num)
    info = "%s:%d:   " %(en_w, en_count)
    for k in res:
        info += "%s:%d" %(k,candidates[k])
    print info
    yield info
        
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
          
def rehearsal():
    from genwords import gen_whole_merge_save, gen_eng

    path = 'Foundation'
    gen_whole_merge_save(path+os.sep+'cs', 10**5)
    gen_eng(path+os.sep+'en')
    find_allmatch(path)
    for i in ('en','cs'):
        clean_dic(i)
                
def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: %s PATH' % sys.argv[0])
    path = sys.argv[1]
    logging.basicConfig(level=logging.DEBUG, filename=path+'.log')

    rehearsal()

if __name__ == "__main__":
    sys.exit(main())  
                  
