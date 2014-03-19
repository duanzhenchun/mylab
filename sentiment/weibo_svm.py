# coding=utf-8
from collections import defaultdict
import jieba
import matplotlib.pyplot as plt
import random
from scipy.stats import chi2_contingency
import math
import codecs
import classify
from utils import *
import sys


DATA_FOLDER='./data/'
F_CHIPROB = 'chi_prob.2.txt'

def word_seg(doc):
    wc = defaultdict(int)
    for w in jieba.cut(doc):
        if w:
            wc[w]+=1
    return wc


def wcount(docs):
    wc = defaultdict(lambda: defaultdict(int))
    cc = defaultdict(int)
    for (doc, is_pos) in docs:
        cc[is_pos] += 1
        for w in word_seg(doc):
            wc[w][is_pos] += 1
    return wc, cc


def chi2(N, wc, cc, folder):
    res = {} 
    for w in wc:
        obs = []
        for k in cc:
            obs.append([wc[w][k], cc[k] - wc[w][k]])
        res[w] = chi2_contingency(obs)[1]
    fout=codecs.open('%s/%s' %(folder, F_CHIPROB), 'w', encoding='utf8')
    x,y=[],[]
    for k,v in sortv_iter(res, False):
        fout.write(u'%s: %s\n' %(k,v))
        y.append(v)
    fout.close()
    plt.plot(y)
#    plt.show()
    return res

@benchmark
def build_lexicon(docs, folder):
    N = len(docs) 
    wc, cc = wcount(docs)
    print "class count:\t %s" %cc
    res = chi2(N, wc, cc, folder)


def tf_idf(m, N, wfreq):
    return m * math.log(N/wfreq)


def top_lex(K, folder):
    lex = {}
    with codecs.open('%s/%s' %(folder, F_CHIPROB), encoding='utf8') as f:
        for _ in range(K):
            l = f.next()
            res = l.split(':')
            if len(res)<2:
                continue
            lex[res[0]] = res[1]
    return lex

def vec_doc(docs, lex, K, folder):
    N=len(docs)
    wc, cc = wcount(docs)
#    print 'wc keys len=', len(wc.keys())
    vec=[0.0,]*len(lex)
    dic= dict(zip(lex.keys(), range(len(lex))))
    fout=codecs.open('%s/vec_%s_index.txt' %(folder, K), 'w', encoding='utf8')
    for k in lex:
        fout.write(u'%s\n' %k)
    fout.close()
    fout=codecs.open('%s/vec_%s_doc.txt' %(folder, K), 'w', encoding='utf8')
    for i, (doc, is_pos) in enumerate(docs):
        fout.write('%s: %s, ' %(i, is_pos))
        for w, c in word_seg(doc).iteritems():
            if w in lex:
                weight = tf_idf(c, N, sum(wc[w].values()))
                vec[dic[w]]=weight
                fout.write('%s: %.2f, ' %(dic[w], weight))
        fout.write('\n')
    fout.close()
    return vec


def gen_rows(K, folder, simple_c = False):
    divi=": "
    f = codecs.open('%s/vec_%s_doc.txt' %(folder, K))
    for l in f:
        h,t = l.split(', ',1)
        i, is_pos=[int(j) for j in h.split(divi)]
        v = [0.0,] * K
        for j in t.split(', '):
            j = j.strip()
            if j:
                res = j.split(divi)
                w, c = int(res[0]), float(res[1])
                if w<K:
                    v[w] = simple_c and 1.0 or c
        yield [v, is_pos, i]

#@benchmark
def experiment(docs, K, ntrain, folder):
    print "%d\t%d" %(K, ntrain),
    cls = classify.SVMer()
    rows = list(gen_rows(K, folder))
    random.shuffle(rows)
    for row in rows[:ntrain]:
        cls.add(*row)
    cls.fit()
    for row in rows[ntrain:]:
        cls.add(*row)
    f1s=cls.stats()
    print "\t%.2f\t%.2f\t%s" %(f1s[0], f1s[1], f1s[2])
 

def main():
    folder, data_fn = get_data_f_fn()
    docs = list(data_fn(folder))
    print 'len(docs)=%d' %len(docs)
#    build_lexicon(docs, folder)
    print 'K\tntrain\tf1_micro\tf1_macro\tf1_seperate'
    for K in (50, 100, 500, ):#1000, 2000,):
        vec_doc(docs, top_lex(K, folder), K, folder)
        for ntrain in (500, 1000, 2000):
            experiment(docs, K, ntrain, folder)

   
if __name__ == "__main__":
    main()
