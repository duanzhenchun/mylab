#encoding:utf-8
import os,re,sys,logging,math
#import mmap
from tools import *

len_thold=0.15

def allpos(pattern, data):
#    data = f.read() #mmap.mmap(f.fileno(), size, access=mmap.ACCESS_READ)
    res=None
    res = [m.start() for m in re.finditer('(?<=\W)%s(?=\W)' %pattern, data,re.IGNORECASE)]
    
    #short it to faster
#    if len(res)>100:
#        res=res[:100]
    return res
    
def notgood(ls1,ls2):
    if len(ls1)<2 or len(ls2)<2:
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
    posdic_en={} 
    csfname=os.sep.join((path, 'cs', 'cs_out'))
    enfile = open(enfname ,'r')  
    csfile = open(csfname,'r')
    endic = dict(iter_f(enfile))
    filter_en(endic)
    csdic = dict(iter_f(csfile))
    logging.info('endic len:%d, csdic len:%d' %(len(endic),len(csdic)))
    return words_match(posdic_en,endata,csdata,endic,csdic)

def filter_en(endic):
    for en,v in endic.items():
        count=int(v[0])
        if not aimed_en(en,count):
            endic.pop(en)
        
def iter_f(f):
    f.seek(0)
    for line in f:
        yield decode_line(line)  
            
def find_dicmatch(endic,modi_ens, csdic,enf,csf):
    enf.seek(0)
    csf.seek(0)
    endata=to_unicode(enf.read())
    csdata = to_unicode(csf.read())
#    wratio = len(csdata)*1.0/len(endata)   #cs2en ratio
    posdic_en={} 
    return words_match(posdic_en,endata,csdata,endic,modi_ens,csdic)

def sub_lst(ls1,ls2):
    remv=0
    i,j = len(ls1)-1,len(ls2)-1
    while i >=0 and j >=0:
        if abs(ls1[i] - ls2[j])<6:
            ls1.pop(i)
            i-=1    
            remv+=1
        if i>=0 and ls1[i]>ls2[j]:
            i-=1
        else:
            j-=1
    print '%d removed' %remv
    
def words_match(posdic_en,endata,csdata,endic,modi_ens,csdic):
    scale = 1.0*len(csdata)/len(endata)
    res=''
    en_res={}
    for cs,v in sortk_iter_bylen(csdic):        # long cs word first
#        if debug and cs not in t_cs: continue
        count=int(v[0])
        poslst_cs = allpos(cs,csdata)
        csen_match(poslst_cs,en_res, scale, posdic_en,endata,csdata,endic,modi_ens,cs,count)
                
    #ajust sub str candidates: Brandon, Bran
    pair=[]
    for en in en_res:
        for suben in en_res:
            if suben != en and suben !=en and suben.lower() in en.lower() and en_res[en][0]<100:
                pair.append([en,suben])    
    for en,suben in pair:
        for subcs in csdic:
            if subcs in en_res[en][1]:
                print '$'*10, en,suben, en_res[en][1], subcs
                poslst_cs = allpos(en_res[en][1],csdata)   
                poslst_subcs = allpos(subcs,csdata)   
                sub_lst(poslst_subcs,poslst_cs)     
                # rm dulp pos
                csen_match(poslst_subcs,en_res, scale, posdic_en,endata,csdata,endic,modi_ens,subcs,int(csdic[subcs][0]))        
                
    for en, cs_candi in iter(sorted(en_res.iteritems())):
        info = '%s:%d,   %s:distance:%d' %(en,endic[en][0],cs_candi[1], cs_candi[0])
        res +=info+'\n'
    res +='\n\ntotoal words: %d' %len(en_res)
    return res
        
def csen_match(poslst_cs,en_res, scale, posdic_en,endata,csdata, endic, modi_ens,cs_w,cs_count):
    en_range=[int(i*cs_count) for i in (1-len_thold, 1.0/(1-len_thold))]
    en_range[1]+=1
    candidates={}   #en candidates with distance
    for en_w,v in endic.iteritems():
        en_count=int(v[0])
        if en_count in range(*en_range):
            if en_w not in posdic_en: 
                if debug: print en_w
                posdic_en[en_w] = allpos(en_w,endata)
                if en_w in modi_ens:
                    for i in modi_ens[en_w]:
                        posdic_en[en_w] += allpos(i,endata)
                    posdic_en[en_w] = sorted(posdic_en[en_w])    
                    print len(posdic_en[en_w])
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
        if candidates[k] < en_res[k][0]:    #update candi with short distance
            en_res[k][:2] = candidates[k],cs_w
        
def update_candi(scale,en_w,cs_w,x,y,candidates):
    if notgood(x,y):
        return
    if debug and cs_w in t_cs:
        print x,'\n', y
    distance = cal_diff(scale,x,y)/(len(cs_w))
    if distance < 250:
        candidates[en_w] = distance 
            
def cal_diff(scale,x,y):
#    torture=2**abs(len(y)-len(x))
    adjust_miss(x,y)
#    if debug:   plotxy(x,y)
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
                  
