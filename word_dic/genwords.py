#encoding:utf-8

Fwc_threshold = 10**7
Word_threshold=6    #0~10

import sys,logging
from tools import * 

def gen_1_2w(blk_lst):
    """gen 1w,2w dic""" 
    dic_1w,dic_2w={},{} 
    for sen in blk_lst:
        for i in xrange(len(sen)):
            incr(dic_1w,sen[i])
            if i <len(sen)-1:
                incr(dic_2w,sen[i:i+2])
    return dic_1w,dic_2w            

import math
            
def gen_true(dic_lows,dic_i):
    dic_true={}
    for k,v in dic_i.iteritems():
        for sub in allsub(k):
            sub_ls=sub.split('|')
            if len(sub_ls)<2:
                continue
            product =1
            for i in sub_ls:
                if not i in dic_lows[len(i)-1]:
                    break
                product *=dic_lows[len(i)-1][i]
            else:
                if v**(len(sub_ls)*10/Word_threshold) < product:
                    break
        else:
            dic_true[k]=v
            
            
    return dic_true                      
                
def trim_low(dic_l,dic_h):
    rmdic={}
    for hk in dic_h.iterkeys():
        for k in (hk[:-1],hk[1:]):
            if k in dic_l:
                #almost same freqence
                if dic_h[hk] >= dic_l[k] or (dic_l[k]-dic_h[hk])*1.0/dic_l[k]<0.1: 
                    rmdic[k]=dic_l[k]
    for k in rmdic:
        dic_l.pop(k)          
    
def cut_tail(dic):
    """cut word appear only once"""
    for k,v in dic.items():
        if v==1:dic.pop(k)

def gen_high(dic_l,blk_lst):
    dic_h={}
    if len(dic_l)<=0:
        return dic_h
        
    wlen=len(dic_l.keys()[0])
    for sen in blk_lst:
        for i in xrange(len(sen)-wlen):
            if sen[i:i+wlen] in dic_l:
                incr(dic_h,sen[i:i+wlen+1])
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
    
def stats(out, iter_fn=sortk_iter_bylen):
    sum_len,sum_freq=0,0
    dic=load_dic(out)
    dic_out(dic,out, iter_fn )
    plot_w(dic,out)    
    print '%s words length: %d, sum feqence: %d' %(out, len(dic),sum(dic.values()))

def load_dics(out,high):
    return load_dic(out)

def ave_pre(pre_dic,dic):
    for k,v in pre_dic.iteritems():
        if k in dic:
            pre_dic[k] = v+dic[k]
    for k,v in dic.iteritems():
        if k not in pre_dic:
            pre_dic[k]=v
            
def save_ws(dic_ls, out):
    pre_dic = load_dic(out)
    logging.info('dic len:%s' %dic_ls)
    for i in xrange(len(dic_ls)):
        if i > 0:
            dic_ls[i] = gen_true(dic_ls[:i],dic_ls[i])
        ave_pre(pre_dic,dic_ls[i])    
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
        stats(out)

def gen_eng(ppath,wcthold):
    if ppath.endswith(os.sep):
        ppath=ppath[:-1]
    out = rela_name(ppath) +'_en'
    logging.info(out)
    pre_dic = load_dic(out)
    logging.info('existed dic len:%s' %len(pre_dic))
    raw_input()
    for sens in iter_en_sens(ppath):
        for w in sens:
            incr(pre_dic,w)
    saveall(pre_dic, out)
    stats(out, sortv_iter)

def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: %s *.har' % sys.argv[0])
    targpath = sys.argv[1]
    logging.basicConfig(level=logging.DEBUG, filename=targpath+'.log')
    
    gen_whole_merge_save(targpath, 10**5)
#    gen_eng(targpath,10**5)

    print get_dulps()

if __name__ == "__main__":
    sys.exit(main())
    
