#encoding:utf-8
import sys, logging
from tools import *
import math


BLOCK_UNIT = 10 ** 5
WCOUNT_MIN = 5
MAX_WORD_LEN = 7
ENTROPY_Thold = 0.75
ENTROPY_Thold2 = 3


def cut_tail(dic):
    """cut word freq less than threshold"""
    for k, v in dic.items():
        if v[0] < WCOUNT_MIN:
            dic.pop(k)


def allwords(sents, maxwlen=MAX_WORD_LEN):
    dic_1w, dic_h = {}, {}
    curpos = 0
    for sen in sents:
        for i in xrange(len(sen)):
            dic_1w.setdefault(sen[i], 0)
            dic_1w[sen[i]] += 1
            for wlen in range(2, maxwlen + 1):
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
    return findword(dic_1w, dic_h)


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
        if res < ENTROPY_Thold2:
            return False
    return True


def findword(dic_1w, dic_h):
    dic_true = {}
    for k, v in dic_h.iteritems():
        product = float(1)
        for i in k:
            product *= (float(dic_1w[i]) / BLOCK_UNIT)
        if product * 100 > float(v[0]) / BLOCK_UNIT:
            continue
        if not isfree(k, v):
            continue
        dic_true[k] = v[0]     #find a word
    return dic_1w, dic_true


def reduce_low(dic):
    keys = sorted(dic.keys(), key=lambda x:len(x), reverse=True)
    for k in keys:
        #find substr of k
        if k in dic:
            pass


def gen_whole(ppath, maxwlen=MAX_WORD_LEN):
    if ppath.endswith(os.sep):
        ppath = ppath[:-1]
    out = rela_name(ppath)
    logging.info(out)
    dic_sum = {}
    dic_1w = {}
    for sents in iter_block(ppath, BLOCK_UNIT):
        ls_merge = [{}] * maxwlen
        res_1w, res = allwords(sents, maxwlen)
        for k, v in res.iteritems():
            dic_sum[k] = (dic_sum.get(k, 0) + float(v) / BLOCK_UNIT) / 2
        for k, v in res_1w.iteritems():
            dic_1w[k] = (dic_1w.get(k, 0) + float(v) / BLOCK_UNIT) / 2
#    print len(dic_sum)
#    head_n(dic_sum, 100)
    save_wdic(dic_sum, ppath + os.sep + str(BLOCK_UNIT) + '_' + str(ENTROPY_Thold2), sortv_iter)
    save_wdic(dic_1w, ppath + os.sep + '1w' + str(BLOCK_UNIT), sortv_iter)


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
#    global BLOCK_UNIT, ENTROPY_Thold2
#    for i in (10 ** 4, 10 ** 5, 10 ** 6):
#        for j in (2.5, 3, 3.5):
#            BLOCK_UNIT = i
#            ENTROPY_Thold2 = j
    gen_whole(targpath)

if __name__ == "__main__":
    sys.exit(main())
#    test_out()
