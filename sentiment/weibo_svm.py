# coding=utf-8
from collections import defaultdict
import jieba
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2_contingency
import math
import codecs
from utils import *


POS,NEG=1, 0
DATA_FOLDER='./data/hotel'

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


def chi2(N, wc, cc):
    res = {} 
    for w in wc:
        a = [[wc[w][POS], wc[w][NEG]], [cc[POS]-wc[w][POS], cc[NEG]-wc[w][NEG]]]
        res[w] = chi2_contingency(a)[0]
    fout=codecs.open('%s/out.txt' %DATA_FOLDER, 'w')
    x,y=[],[]
    for k,v in sortv_iter(res):
        fout.write(u'%s: %s\n' %(k,v))
        y.append(v)
    fout.close()
    plt.plot(y)
    plt.show()
    return res


def build_lexicon(docs):
    N = len(docs) 
    wc, cc = wcount(docs)
    print "class count: %s" %cc
    res = chi2(N, wc, cc)


def tf_idf(m, N, wfreq):
    return m * math.log(N/wfreq)

def prod_data():
    for fname in ('IntegratedCons.txt', 'IntegratedPros.txt'):
        f= open('%s/%s' %(DATA_FOLDER, fname))
        dic = {'<Cons>': NEG, '<Pros>': POS}
        for line in f:
            line = line.strip()
            for k in dic:
                if line.startswith(k):
                   n=len(k)
                   txt=line[n:-(n+1)]
                   yield txt, dic[k]
                   continue
                
def hotel_data():
    import tarfile
    tar = tarfile.open('%s/Ctrip_htl_ba_4000.tar.gz' %DATA_FOLDER)
    for f in tar.getmembers():
        if f.isfile():
            is_pos = f.name.split('/')[1] == "pos" and 1 or 0
            txt = tar.extractfile(f).read()
            txt = txt.decode('gbk', 'ignore')
            yield txt.strip(), is_pos

def test_data():
    docs=[
        [u'abc ded', POS],
        [u'ffe afe', NEG],
        [u'l wfe', POS],
    ]

def vectorize(K):
    lex = {}
    for l in open('%s/out.txt' %DATA_FOLDER):
        res = l.split(':')
        lex[res[0]] = res[1]
        K-=1
        if K<1:
            break
    return lex

def vec_doc(docs, lex, K):
    N=len(docs)
    wc, cc = wcount(docs)
    vec=[0.0,]*len(lex)
    dic= dict(zip(lex.keys(), range(len(lex))))
    fout=codecs.open('%s/vec_%s_index.txt' %(DATA_FOLDER, K), 'w')
    for k in lex:
        fout.write('%s\n' %k)
    fout.close()
    fout=codecs.open('%s/vec_%s_doc.txt' %(DATA_FOLDER, K), 'w')
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


def gen_rows(K):
    divi=": "
    f = codecs.open('%s/vec_%s_doc.txt' %(DATA_FOLDER, K))
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
                    v[w] = c
        yield [v, is_pos, i]


def training_f1(K, ntrain):
    import classify
    cls = classify.SVMer()
    rows = list(gen_rows(K))
    np.random.shuffle(rows)
    for row in rows[:ntrain]:
        cls.add(*row)
    cls.fit()
    for row in rows[ntrain:]:
        cls.add(*row)
    cls.stats()

def experiment(docs, K, ntrain):
    doc_fn = {'hotel': hotel_data, 'prod': prod_data}
    print "K=%d, ntrain=%d" %(K, ntrain)
#    build_lexicon(docs)
    training_f1(K, ntrain)
 
def main():
    print DATA_FOLDER
    docs = list(doc_fn.get(DATA_FOLDER.split('/')[-1])())
    print 'len(docs)=%d' %len(docs)
    for K in (50, 100, 1000):
        vec_doc(docs, vectorize(K), K)
        for ntrain in (500, 1000, 2000 ):
            experiment(docs, K, ntrain)

   
if __name__ == "__main__":
    main()
