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
    res = [m.start() for m in re.finditer('(?<=\W)%s(?=\W)' %pattern, data,re.IGNORECASE)]
    return res
    
def notgood(lst1,lst2):
    if len(lst1)<2 or len(lst2)<2:
        return True
    return  False
            
def decode_line(line):
    word,v=line.split(':')
    return word, eval(v)
      
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
    endic = dict(iter_f(enfile))
    filter_en(endic)
    csdic = dict(iter_f(csfile))
    logging.info('endic len:%d, csdic len:%d' %(len(endic),len(csdic)))
    return words_match(posdic_cs,endata,csdata,endic,csdic)

def filter_en(endic):
    for en,v in endic.items():
        count=int(v[0])
        if not aimed_en(en,count):
            endic.pop(en)
        
def iter_f(f):
    f.seek(0)
    for line in f:
        yield decode_line(line)  
            
def find_dicmatch(endic,csdic,enf,csf):
    enf.seek(0)
    csf.seek(0)
    endata=to_unicode(enf.read())
    csdata = to_unicode(csf.read())
#    wratio = len(csdata)*1.0/len(endata)   #cs2en ratio
    posdic_en={} 
    return words_match(posdic_en,endata,csdata,endic,csdic)

def sub_lst(ls1,ls2):
    remv=0
    for i in ls1:
        for j in ls2:
            if abs(j-i) < 4:    #near position
                ls1.remove(i)
                remv+=1
    return remv
def less_pos(w,pos,dic, data):
    remv=0
    if debug:
        print 'before less', len(pos)
    #remove sub word, like Bran, Brandon; Stark, Karstark
    for k,v in dic.iteritems():
        if w!=k and w in k:
            pos1 = allpos(k,data)
            if debug: 
                print w, k
            remv+=sub_lst(pos,pos1)
    if debug:
        print remv, len(pos)
    return remv
    
def words_match(posdic_en,endata,csdata,endic,csdic):
    scale = 1.0*len(csdata)/len(endata)
    res=''
    en_res={}
    for cs,v in sortk_iter_bylen(csdic,False):
        if debug and cs != t_cs: continue
        count=int(v[0])
        poslst_cs = allpos(cs,csdata)
#        remv=less_pos(cs,poslst_cs,csdic,csdata)
#        count -=remv 
#        if debug:
#            print 'remv', cs, remv
        csen_match(poslst_cs,en_res, scale, posdic_en,endata,csdata,endic,cs,count)
    for en, cs_candi in iter(sorted(en_res.iteritems())):
        info = '%s:%d,   %s:distance:%d' %(en,endic[en][0],cs_candi[1], cs_candi[0])
        print info
        res +=info+'\n'
    return res
        
def csen_match(poslst_cs,en_res, scale, posdic_en,endata,csdata, endic, cs_w,cs_count):
    en_range=[int(i*cs_count) for i in (1-len_thold, 1.0/(1-len_thold))]
    en_range[1]+=1
    candidates={}   #en candidates with distance
    for en_w,v in endic.iteritems():
        en_count=int(v[0])
        if debug:
            print en_w,en_count,en_range,cs_w, cs_count
        if en_count in range(*en_range):
            if en_w not in posdic_en: 
                if debug: print en_w
                posdic_en[en_w] = allpos(en_w,endata)
            y=poslst_cs[:]
            update_candi(scale,en_w,cs_w,posdic_en[en_w],y,candidates)
    match_res(en_res,candidates,cs_w,cs_count)
            
def match_res(en_res, candidates, cs_w,cs_count, num=1):  
    if not candidates:
        return
    out={}
    res = dict_nmin(candidates,num)
    for k in res:
        en_res.setdefault(k,[candidates[k],cs_w])
        if candidates[k] < en_res[k][0]:
            en_res[k][:2] = candidates[k],cs_w
        
def update_candi(scale,en_w,cs_w,x,y,candidates):
    if notgood(x,y):
        return
    if debug and t_cs == cs_w:
        print x,'\n', y
    distance = cal_diff(scale,x,y)/(2**len(cs_w))
    if distance < 250:
        candidates[en_w] = distance 
            
def cal_diff(scale,x,y):
#    torture=2**abs(len(y)-len(x))
    adjust_miss(x,y)
    if debug:   plotxy(x,y)
    residuals = 0
    #y=kx+c     k=scale,  c is tolarated  for certain amount
    c=sum(y)/len(x) - sum(x)/len(x)*scale 
    for i in range(len(x)):
        residuals += (x[i]*scale +c - y[i])**2
    return (residuals/len(x))**0.5/len(x)    
            
def adjust_miss(X,Y):
    if len(X)==len(Y):
        return
    newlen=min(len(X),len(Y))  
    for aim in (X,Y):
        for i in range(newlen,len(aim)):
            aim.pop(-1)
    return
        
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
                  
