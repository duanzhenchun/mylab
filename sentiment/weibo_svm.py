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


POS, NEG=1, -1
DATA_FOLDER='./data/ccf_nlp'
F_CHIPROB = 'chi_prob.txt'

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
        obs = []
        for k in cc:
            obs.append([wc[w][k], cc[k] - wc[w][k]])
        res[w] = chi2_contingency(obs)[0]
    fout=codecs.open('%s/%s' %(DATA_FOLDER, F_CHIPROB), 'w', encoding='utf8')
    x,y=[],[]
    for k,v in sortv_iter(res, True):
        fout.write(u'%s: %s\n' %(k,v))
        y.append(v)
    fout.close()
    plt.plot(y)
#    plt.show()
    return res

@benchmark
def build_lexicon(docs):
    N = len(docs) 
    wc, cc = wcount(docs)
    print "class count:\t %s" %cc
    res = chi2(N, wc, cc)


def tf_idf(m, N, wfreq):
    return m * math.log(N/wfreq)

def test_data():
    docs=[[u'abc ded', POS],
          [u'ffe afe', NEG],
          [u'l wfe', POS]]
    return docs

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
            is_pos = f.name.split('/')[1] == "pos" and POS or NEG
            txt = tar.extractfile(f).read()
            txt = txt.decode('gbk', 'ignore')
            yield txt.strip(), is_pos


def rm_tag(txt):
    for i in txt.split('#')[::2]:
        if i:
            yield i

def ccf_nlp_data():
    import xml.etree.ElementTree as et
    import os
    fol = u"./data/ccf_nlp/2012/微博情感分析评测/测试数据/"
    for fname in os.listdir(fol):
        if not fname.endswith('.xml'):
            continue
        for wb in et.parse(fol + fname).findall('weibo'):
            for sent in wb.findall('sentence'):
                txt = ' '.join(rm_tag(sent.text))
                op = sent.attrib['opinionated']
                is_pos = 0
                if op == 'Y':
                    is_pos = (sent.attrib['polarity'] == repr(POS)) and POS or NEG
                yield txt, is_pos

def top_lex(K):
    lex = {}
    with codecs.open('%s/%s' %(DATA_FOLDER, F_CHIPROB), encoding='utf8') as f:
        for _ in range(K):
            l = f.next()
            res = l.split(':')
            if len(res)<2:
                continue
            lex[res[0]] = res[1]
    return lex

def vec_doc(docs, lex, K):
    N=len(docs)
    wc, cc = wcount(docs)
#    print 'wc keys len=', len(wc.keys())
    vec=[0.0,]*len(lex)
    dic= dict(zip(lex.keys(), range(len(lex))))
    fout=codecs.open('%s/vec_%s_index.txt' %(DATA_FOLDER, K), 'w', encoding='utf8')
    for k in lex:
        fout.write(u'%s\n' %k)
    fout.close()
    fout=codecs.open('%s/vec_%s_doc.txt' %(DATA_FOLDER, K), 'w', encoding='utf8')
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


def gen_rows(K, simple_c = False):
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
                    v[w] = simple_c and 1.0 or c
        yield [v, is_pos, i]


def experiment(docs, K, ntrain):
    print "%d\t%d" %(K, ntrain),
    cls = classify.SVMer()
    rows = list(gen_rows(K))
    random.shuffle(rows)
    for row in rows[:ntrain]:
        cls.add(*row)
    cls.fit()
    for row in rows[ntrain:]:
        cls.add(*row)
    f1s=cls.stats()
    print "\t%.2f\t%.2f" %(f1s[0], f1s[1])
 
def main():
    doc_fn = {'hotel': hotel_data, 
              'prod': prod_data,
              'ccf_nlp': ccf_nlp_data,
              }
    docs = list(doc_fn.get(DATA_FOLDER.split('/')[-1])())
    print DATA_FOLDER
    print 'len(docs)=%d' %len(docs)
    build_lexicon(docs)
    print 'K\tntrain\tf1_micro\tf1_macro'
    for K in (50, 100, 500):
        vec_doc(docs, top_lex(K), K)
        for ntrain in (500, 1000, 2000):
            experiment(docs, K, ntrain)

   
if __name__ == "__main__":
    main()
