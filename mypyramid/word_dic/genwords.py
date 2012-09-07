#encoding:utf-8

Fwc_threshold = 10**7
Word_Thold=2.14

import sys,logging
from tools import * 

def gen_1_2w(blk_lst):
    """gen 1w,2w dic""" 
    dic_1w,dic_2w={},{} 
    curpos=0
    for sen in blk_lst:
        for i in xrange(len(sen)):
            incr(dic_1w,sen[i],curpos)
            if i <len(sen)-1:       # gen 2w
                incr(dic_2w,sen[i:i+2],curpos)
            curpos+=1
    for k,v in dic_2w.items():
        if v[0]<2:
            dic_2w.pop(k)
    return dic_1w,dic_2w            

import math
            
# low word to high word generation, filtered by threshold            
def gen_true(dic_lows,dic_i):
    dic_true={}
    for k,v in dic_i.iteritems():
        vrange = max((v[2]-v[1]),1)
        for sub in allsub(k):
            sub_ls=sub.split('|')
            if len(sub_ls)<2:
                continue
            product =1
            for i in sub_ls:
                if not i in dic_lows[len(i)-1]:
                    break
                subv=dic_lows[len(i)-1][i]
                if debug and t_cs==k:
                    print i, subv
                product *=subv[0]*vrange*1.0/max((subv[2]-subv[1]),1)
            else:
                if debug and t_cs==k:
                    print k,v,vrange, product, v[0]**(len(sub_ls)*Word_Thold)
                if v[0]**(len(sub_ls)*Word_Thold) < product:
                    break
        else:
            dic_true[k]=v
    return dic_true                      
             
#probability diff <0.1 
def trim_low(dic_l,dic_h):
    rmdic={}
    for hk in dic_h.iterkeys():
        for k in (hk[:-1],hk[1:]):
            if k in dic_l:
                if dic_h[hk][0] >= dic_l[k][0] or (dic_l[k][0]-dic_h[hk][0])*1.0/dic_l[k][0]<0.1: 
                    rmdic[k]=dic_l[k]
    for k in rmdic:
        dic_l.pop(k)          
    
def cut_tail(dic):
    """cut word appear only once"""
    for k,v in dic.items():
        if v[0]<2:dic.pop(k)

def gen_high(dic_l,blk_lst):
    dic_h={}
    if len(dic_l)<=0:
        return dic_h
        
    wlen=len(dic_l.keys()[0])
    curpos = 0
    for sen in blk_lst:
        for i in xrange(len(sen)-wlen):
            if sen[i:i+wlen] in dic_l:
                incr(dic_h,sen[i:i+wlen+1],curpos)
            curpos+=1
        curpos += wlen
    trim_low(dic_l,dic_h)
    cut_tail(dic_h)    
    return dic_h
                
def gen_whole(blk_lst, high):
    dic_ls=[{}]*high
    dic_ls[:2] = gen_1_2w(blk_lst)
    cut_tail(dic_ls[1])
    for i in xrange(2,high):
        dic_ls[i]=gen_high(dic_ls[i-1], blk_lst)
    return dic_ls  
    
def stats(path,out, iter_fn=sortk_iter_bylen):
    sum_len,sum_freq=0,0
    dic=load_dic(out)
    dic_out(dic,path+os.sep+out, iter_fn )
#    plot_w(dic,out)    
#    print '%s words length: %d, sum feqence: %d' %(out, len(dic),sum(dic.values()))

def load_dics(out,high):
    return load_dic(out)

# average word count of all dicts
def ave_pre(pre_dic,dic):
    for k,v in pre_dic.iteritems():
        if k in dic:
            pre_dic[k][0] = v[0]+dic[k][0]
            pre_dic[k][1] = min(v[1],dic[k][1])
            pre_dic[k][2] = max(v[2],dic[k][2])
    for k,v in dic.iteritems():
        if k not in pre_dic:
            pre_dic[k]=v
            

def gen_cs(dic_ls,pre_dic):
    for i in xrange(len(dic_ls)):
        if i > 0:
            dic_ls[i] = gen_true(dic_ls[:i],dic_ls[i])
        ave_pre(pre_dic,dic_ls[i])    
    return pre_dic
                            
def save_ws(dic_ls, out):
    pre_dic = load_dic(out)
    gen_cs(dic_ls,pre_dic)
    saveall(pre_dic, out)  
        
def gen_whole_merge_save(ppath, wcthold = Fwc_threshold, high=9 ):
    if ppath.endswith(os.sep):
        ppath=ppath[:-1]
    out = rela_name(ppath)
    logging.info(out)
    for blk_lst in iter_block(ppath,wcthold):
        ls_merge=[{}]*high
        dic_ls = gen_whole(blk_lst,high)
        for i in xrange(high):
            ls_merge[i]= merged((ls_merge[i],dic_ls[i]))    
        save_ws(ls_merge, out)
        stats(ppath, out, sortv_iter)

def gen_singlef(f, high=9 ):
    blk_lst = get_singlefile(f)
    ls_merge=[{}]*high
    dic_ls = gen_whole(blk_lst,high)
    for i in xrange(high):
        ls_merge[i]= merged((ls_merge[i],dic_ls[i]))    
    dic = {}
    gen_cs(dic_ls,dic)
    logging.info('cs dict len:%d' %len(dic))
    if debug:
        print t_cs in dic
    
    return dic
            
def gen_single_enf(f):
    pre_dic={}
    curpos=0
    for sen in iter_single_en(f):
        for w in sen:
            incr(pre_dic,w,curpos)
            curpos+=1    
    en_dic={}
    for en,v in pre_dic.iteritems():
        if debug and t_en not in en: continue
        if aimed_en(en,v[0]):
            en_dic[en]=v
    merge_pluralname(en_dic) 
    logging.info('aimed en dic len:%d' %len(en_dic))                          
    return en_dic

def gen_eng(ppath):
    if ppath.endswith(os.sep):
        ppath=ppath[:-1]
    out = rela_name(ppath)
    pre_dic = {}
    curpos=0
    for sens in iter_en_sens(ppath):
        for w in sens:
            incr(pre_dic,w,curpos)
            curpos+=1
    dic_out(pre_dic,ppath+os.sep+out, sortv_iter )    

def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: %s PATH' % sys.argv[0])
    targpath = sys.argv[1]
    logging.basicConfig(level=logging.DEBUG, filename=targpath+'.log')
    
    gen_whole_merge_save(targpath, 10**5)
    gen_eng(targpath)
    print get_dulps()

if __name__ == "__main__":
    sys.exit(main())
    
