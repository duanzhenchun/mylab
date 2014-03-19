# encoding:utf-8
import time
import logging
import sys
import os


POS, NEG, NEU = 1, 0, 2
Sen_dic={POS:'POS', NEG:'NEG', NEU:'NEU'}


def sortk_iter(dic):
    return sorted(dic.iteritems())


def sortk_iter_bylen(dic, decrease=True):
    return sorted(dic.iteritems(), key=lambda (k, v):(len(k), v), reverse=decrease)


def sortv_iter(dic, reverse=False):
    for key, value in sorted(dic.iteritems(), reverse=reverse, key=lambda (k, v): (v, k)):
        yield key, value

def decode_line(l):
    if not (type(l) is unicode):
        try:
            l = l.decode('utf-8')
        except:
            l = l.decode('gbk', 'ignore')
    return l
    
def benchmark(f):
    def wrapper(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print '%s %f %s' % (f.__name__, time.time() - t, 'sec')
        return res
    return wrapper


def rm_tag(txt):
    for i in txt.split('#')[::2]:
        if i:
            yield i
            

def test_data():
    docs=[[u'abc ded', POS],
          [u'ffe afe', NEG],
          [u'l wfe', POS]]
    return docs

def prod_data(folder):
    for fname in ('IntegratedCons.txt', 'IntegratedPros.txt'):
        f= open('%s/%s' %(folder, fname))
        dic = {'<Cons>': NEG, '<Pros>': POS}
        for line in f:
            line = line.strip()
            for k in dic:
                if line.startswith(k):
                   n=len(k)
                   txt=line[n:-(n+1)]
                   yield txt, dic[k]
                   continue
                
def hotel_data(folder):
    import tarfile
    tar = tarfile.open('%s/Ctrip_htl_ba_4000.tar.gz' %folder)
    for f in tar.getmembers():
        if f.isfile():
            is_pos = f.name.split('/')[1] == "pos" and POS or NEG
            txt = tar.extractfile(f).read()
            txt = txt.decode('gbk', 'ignore')
            yield txt.strip(), is_pos


def ccf_nlp_data(folder):
    import xml.etree.ElementTree as et
    import os
    fol = u"%s/2012/微博情感分析评测/测试数据/" %folder
    for fname in os.listdir(fol):
        if not fname.endswith('.xml'):
            continue
        for wb in et.parse(fol + fname).findall('weibo'):
            for sent in wb.findall('sentence'):
                txt = ' '.join(rm_tag(sent.text))
                op = sent.attrib['opinionated']
                is_pos = NEU 
                if op == 'Y':
                    is_pos = (sent.attrib['polarity'] == 'POS') and POS or NEG
                yield txt, is_pos


def get_data_f_fn(dfolder = './data/'):
    data_t = 'ccf_nlp'
    doc_fn = {'hotel': hotel_data, 
              'prod': prod_data,
              'ccf_nlp': ccf_nlp_data,
              }
    if len(sys.argv)>1 and sys.argv[1] in doc_fn:
        data_t = sys.argv[1]
    return dfolder + data_t, doc_fn.get(data_t)


