#encoding:utf-8
import os,re,sys,logging,math
#import mmap
from tools import *

len_thold=0.15
    
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
    
def find_allmatch(path):
    enfname=os.sep.join((path, 'en', 'en_out'))

    fnames=('en/en.txt','cs/cs.txt')
    endata=open(path+os.sep+fnames[0],'r').read()
    csdata=open(path+os.sep+fnames[1],'r').read()
    posdic_cs={} 
    csfname=os.sep.join((path, 'cs', 'cs_out'))
    enfile = open(enfname ,'r')  
    csfile = open(csfname,'r')
    res=''
    return words_match(posdic_cs,endata,csdata,enfile,csfile)

def find_dicmatch(endic,csdic,enf,csf):
    enf.seek(0)
    csf.seek(0)
    endata=to_unicode(enf.read())
    csdata = to_unicode(csf.read())
#    wratio = len(csdata)*1.0/len(endata)   #cs2en ratio
    posdic_cs={} 
    return words_match(posdic_cs,endata,csdata,endic,csdic)
    
def words_match(posdic_cs,endata,csdata,enfile,csfile):
    res=''
    iter_fn=get_iterfn(enfile)
    for en,count in iter_fn(enfile):
#        if en !='Eto': continue
        #find start,end pos in en
#        en_range=(endata.find(en), endata.rfind(en))
#        cs_range=(max(int(en_range[0]*wratio)-50,0), min(int(en_range[1]*wratio)+50,len(endata)))
#        
#        from genwords import gen_singlef
#        csfile=gen_singlef(csdata[cs_range[0]:cs_range[1]]) 
        if aimed_en(en,count):
            for info in encs_match(posdic_cs,endata,csdata,csfile,en,count):
                res += '%s\n' %info
    return res
    
def get_iterfn(data):
    def iter_f(f):
        f.seek(0)
        for line in data:
            yield decode_line(line)    
    if dict == type(data):
        return lambda data: iter(sorted(data.iteritems())) # data.iteritems()
    elif file == type(data):
        return iter_f
    else:
        raise Exception('data type not supported')     
    
def encs_match(posdic_cs,endata,csdata, csfile,en_w,en_count):
    scale = 1.0*len(csdata)/len(endata)
    poslst_en = allpos(en_w,endata)
    cs_range=[int(i*en_count) for i in (1-len_thold, 1.0/(1-len_thold))]
    cs_range[1]+=1
    candidates={}
    iter_fn=get_iterfn(csfile)
    for cs_w,cs_count in iter_fn(csfile):
#        if cs_w != u'伊图': continue
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
    distance = cal_diff(scale,x,y)/len(cs_w)
    if distance < 500:
        candidates[cs_w] = distance 
            
def cal_diff(scale,x,y):
#    torture=2**abs(len(y)-len(x))
    adjust_miss1(x,y)
    residuals = 0
    #y=kx+c     k=scale,  c is tolarated  for certain amount
    c=sum(y)/len(x) - sum(x)/len(x)*scale 
    for i in range(len(x)):
        residuals += (x[i]*scale +c - y[i])**2
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
                  
