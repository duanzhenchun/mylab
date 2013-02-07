#encoding:utf-8

Fwc_Thold = 1 * 10 ** 5
WC_Thold = 5
MAX_W = 7
ENTROPY_Thold = 0.75    
ENTROPY_Thold2 = 3

import sys, logging
from tools import * 
import math
            
            
def cut_tail(dic):
    """cut word freq less than threshold"""
    for k, v in dic.items():
        if v[0] < WC_Thold:
            dic.pop(k)

def gen_all(blk_lst, high):
    dic_1w, dic_h = {}, {}
    curpos = 0
    for sen in blk_lst:
        for i in xrange(len(sen)):
            dic_1w.setdefault(sen[i], 0)
            dic_1w[sen[i]] += 1
            for wlen in range(2, high + 1):
                if i + wlen > len(sen):
                    break
                w = sen[i:i + wlen]
                incr(dic_h, w, curpos)
                if i > 0:                  # left_1w
                    dic_h[w][3].setdefault(sen[i - 1], 0)
                    dic_h[w][3][sen[i - 1]] += 1
                if i < len(sen) - wlen:    # right_1w
                    dic_h[w][4].setdefault(sen[i + wlen], 0)
                    dic_h[w][4][sen[i + wlen]] += 1
            curpos += 1
        curpos += 1
    cut_tail(dic_h)    
    return dic_1w, gen_true(dic_1w, dic_h)

def max_entropy(n):
    tmp = float(1) / n
    return - tmp * math.log(tmp) * n
            
def isfree(k, V):
    n = V[0]
    threshold = max_entropy(n) * ENTROPY_Thold
    for dic in (V[3], V[4]):
        res = 0
        total = 0
        for v in dic.itervalues():
            total += v
            tmp = float(v) / n
            res -= tmp * math.log(tmp, 2)
        if total < n:
            tmp = float(1) / n
            res -= tmp * math.log(tmp, 2) * (n - total)
#        if res < threshold:
        if k in (u'产品', u'决定', u'商品', u'预付'):
            print k
        if res < ENTROPY_Thold2:
            return False
    return True

def gen_true(dic_1w, dic_h):
    dic_true = {}
    for k, v in dic_h.iteritems():
        product = float(1)
        for i in k:
            product *= (float(dic_1w[i]) / Fwc_Thold)
        if product * 100 > float(v[0]) / Fwc_Thold:
            continue
        if not isfree(k, v):
            continue
        dic_true[k] = v[0]     #find a word
    return dic_true    
    
def load_dics(out, high):
    return load_dic(out)

def head_n(dic, n):
    i = 0
    for k, v in sortv_iter(dic):
        i += 1
        print k, v
        if i > n:
            return
                        
def gen_whole(ppath, high=MAX_W):
    if ppath.endswith(os.sep):
        ppath = ppath[:-1]
    out = rela_name(ppath)
    logging.info(out)
    dic_sum = {}
    dic_1w = {}
    for sents in iter_block(ppath, Fwc_Thold):
        ls_merge = [{}] * high
        res_1w, res = gen_all(sents, high)
        for k, v in res.iteritems():
            dic_sum[k] = (dic_sum.get(k, 0) + float(v) / Fwc_Thold) / 2
        for k, v in res_1w.iteritems():
            dic_1w[k] = (dic_1w.get(k, 0) + float(v) / Fwc_Thold) / 2            
    print len(dic_sum)
#    head_n(dic_sum, 100)
    dic_out(dic_sum, ppath + os.sep + str(Fwc_Thold) + '_' + str(ENTROPY_Thold2), sortv_iter)
    dic_out(dic_1w, ppath + os.sep + '1w' + str(Fwc_Thold), sortv_iter)


def show_result(path):
    out = rela_name(path)
    stats(path, out, sortv_iter)

def test_out(ppath='./data2/'):
    g_dic = set([unicode(x.rstrip(), 'utf-8') for x in file("/home/whille/my_env/src/mywordsegment/worddic/main.dic") ])
    print len(g_dic)
    for fname in iter_fname_end(ppath, '_out'):
        print fname
        i = 0
        wrong = 0
        for line in open(fname, 'r'):
            i += 1
            if i == 1:
                continue
            if line.split(':')[0].decode('utf-8') not in g_dic:
                wrong += 1
        print i - wrong, float(i - wrong) / i
                        
            
def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: %s PATH' % sys.argv[0])
    targpath = sys.argv[1]
    logging.basicConfig(level=logging.DEBUG, filename=targpath + '.log')
#    global Fwc_Thold, ENTROPY_Thold2
#    for i in (10 ** 4, 10 ** 5, 10 ** 6):
#        for j in (2.5, 3, 3.5):
#            Fwc_Thold = i
#            ENTROPY_Thold2 = j
    gen_whole(targpath)

if __name__ == "__main__":
    sys.exit(main())
#    test_out()
