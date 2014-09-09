#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import random
import m1
import statist
from utils import *
import sys
import codecs
import jieba
import re
from multiprocessing import Pool
    
    
sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout)

procnum = 8
P_THRESHOLD = 1e-3
DT_ratio = 5
data_folder = '../../data/'
DOC_NAME, TITLE_NAME = (data_folder + i for i in ('doc', 'title'))
hanse, hansf, enf, csf = (data_folder + i for i in (
                        'hansards.e', 'hansards.f', 'pp_en.txt', 'pp_cs.txt'))
 
@benchmark()
def save_diction(trans, table):
    cursor = get_connect()
    print 'doc_w len:', len(trans)
    for w in trans:
        if not w:
            continue
        # clear previous translation
        cursor.execute('delete from %s where doc_w="%s"' % (table, w)) 
        for t, p in trans[w].iteritems():
            if p < P_THRESHOLD:
                continue
            dic = {'doc_w':w, 'title_w':t, 'p':p}
            statist.insertDB(cursor, table, dic, update=True, privatekeys=('doc_w', 'title_w'))
    cursor.connection.close()
    
@benchmark()
def guess(trans, doc, idf, max_idf, n=None):
    lst = doc.split()
    tf = get_tf(lst, idf, max_idf)
    dic = {}
    for w in lst:
        if w not in trans:
            continue
        for t, p in trans[w].iteritems():
            dic.setdefault(t, 0.0)
            dic[t] += p * tf[w]
    if not n:
        n = title_len(lst)
    return list(sortv_iter(dic))[:n]
    
@benchmark()    
def get_idf(docs):
    # http://en.wikipedia.org/wiki/Tf-idf
    log_ndoc = math.log(len(docs))
    idf = {}
    for doc in docs:
        for w in set(doc.split()):
            idf.setdefault(w, 0)
            idf[w] += 1
    for k in idf:
        idf[k] = log_ndoc - math.log(idf[k])
    return idf


def get_tf(lst, idf, max_idf):
    tf = {}
    for w in lst:
        tf.setdefault(w, 0)
        tf[w] += 1
    for w in tf:
        tf[w] *= idf.get(w, max_idf)
    return tf

@benchmark()  
def gen_doc_title(docs, idf):
    max_idf = max(idf.values())
    for doc in docs:
        tf = {}
        lst = doc.split()
        n = title_len(lst)
        tf = get_tf(lst, idf, max_idf)
        sample = [ weighted_choice(tf) for i in range(n)]
        yield (lst, sample)


def title_len(lst):
    return int(len(lst) / DT_ratio)

def weighted_choice(dic):
    total = sum(dic.values())
    r = random.uniform(0, total)
    upto = 0
    for c, w in dic.iteritems():
        if upto + w > r:
            return c
        upto += w
    assert False, "Shouldn't get here"

@benchmark()  
def write_doctitle(docs, fdoc, ftitle):
    f1, f2 = [codecs.open(i, 'w', encoding='utf-8') for i in (fdoc, ftitle)]
    idf = get_idf(docs)
    for i, j in gen_doc_title(docs, idf):
        if len(j) <= 0:
            continue
        f1.write(u' '.join(i) + '\n')
        f2.write(u' '.join(j) + '\n')
    f1.close()
    f2.close()
    
    
def mul_write_docs((idf, docs, index, fdoc, ftitle)):
    print fdoc, ftitle, index, len(docs)
    f1, f2 = [codecs.open(i + '.%s' % index, 'w', encoding='utf-8') for i in (fdoc, ftitle)]
    for i, j in gen_doc_title(docs, idf):
        if len(j) <= 0:
            continue
        f1.write(u' '.join(i) + '\n')
        f2.write(u' '.join(j) + '\n')
    f1.close()
    f2.close()
    
    
def load_account_doc():
    nload = 2000
    docs = [i[0] for i in statist.get_DB('select doc from %s limit %d' % (ACCOUNT_LAB, nload + 1))]
    write_doctitle(docs, DOC_NAME, TITLE_NAME)

def test_wam(fdoc=DOC_NAME, ftitle=TITLE_NAME, dbtable=WORD_DICT):
    docs = codecs.open(fdoc, encoding='utf-8').readlines()
    test = docs.pop()
    print 'test doc:', test
    idf = get_idf(docs)
    max_idf = max(idf.values())
    print max_idf
    print 'start ibm M1 '
    model = m1.M1(fdoc, ftitle)
    for i in range(100):
        print 'iter:', i
        model.iterate(10, True)
        print round(model['人']['人'], 3)
        title = guess(model.t, test, idf, max_idf)
        save_diction(model.t, dbtable)
        for i in title:
            print i[0], i[1]
    
def t_guess(fdoc, ftest):
    docs = codecs.open(fdoc, encoding='utf-8').readlines()
    idf = get_idf(docs)
    max_idf = max(idf.values())
    if ftest:
        data = codecs.open(ftest, encoding='utf-8').read()
        words = list(gen_nounword(data))
        print len(data), len(words)
        test = u' '.join(words)
    else:
        (screen_name, test) = statist.get_DB(
         'select screen_name, doc from %s where uid=%s limit 1' % (ACCOUNT_LAB, 1711064324))[0]
        print 'screen_name:', screen_name
    print 'test doc:', test
    trans = {}
    res = statist.get_DB('select * from %s where p>%s' % (WORD_DICT, P_THRESHOLD))
    for dw, tw, p in res:
        trans.setdefault(dw, {})
        trans[dw][tw] = p
    title = guess(trans, test, idf, max_idf, 200)
    for i in title:
        print i[0], i[1]           

def is_latin(uchr):
    import unicodedata
    latin_letters = {}
    try: 
        return latin_letters[uchr]
    except KeyError:
        return latin_letters.setdefault(uchr, 'LATIN' in unicodedata.name(uchr))
     
def conv_file():
    with  codecs.open(data_folder + '1.txt', encoding='utf-8')  as f:
        enout = codecs.open(data_folder + '1en.txt', 'w', encoding='utf-8')
        csout = codecs.open(data_folder + '1cs.txt', 'w', encoding='utf-8')
        for txt in f:
            txt = txt.strip()
            if not txt:
                continue
            count = 0
            for i in list(txt)[:10]:
                if is_latin(i): 
                    count += 1
            outf = count > 4 and enout or csout 
            words = jieba.cut(txt)
            outf.write(u' '.join(words) + u'\r\n')
        enout.close()
        csout.close()
            
def write_xls():
    import xlrd
    zipname = data_folder + 'Monthly_5.zip'
    arc = xlrd.zipfile.ZipFile(zipname)
    docs = []
    print 'files in arc', len(arc.namelist())
    for fname in arc.namelist():
        print fname.decode('gbk')
        data = arc.read(fname)
        wb = xlrd.open_workbook(file_contents=data)
        sh1 = wb.sheet_by_index(0)
        head = sh1.row_values(0)
        channel_i, tweet_i = (head.index(i) for i in (u'频道名称', u'微博原始内容'))
        tweets = sh1.col_values(tweet_i, start_rowx=1)
        for txt in tweets:
            words = list(gen_nounword(txt))
            docs.append(u' '.join(words))
    print 'docs len:', len(docs)
    fdoc, ftitle = (data_folder + i for i in ('weibodoc', 'weibotitle'))
    write_doctitle(docs, fdoc, ftitle)
 
def build_cic_data():
    docs = []
    folder = '/data/expdata/'
    fname = folder + 'tweet_content_sian_201301.txt'
    docs_out = folder + 'docs.txt'
    fout = codecs.open(docs_out, 'w', encoding='utf-8')
    with open(fname) as fo:
        for l in fo:
            if not l:
                continue
            res = re.findall('"text":"([^"]+?)"', l)
            if not res:
                continue
            txt = res[0]
            txt = re.split(u'//[\s　]*?@', txt)[0]  # remove original content
            words = list(gen_nounword(txt))
#             docs.append(u' '.join(words))
            fout.write(u' '.join(words) + '\n')
    fout.close()

@benchmark()  
def gen_cic_title():
    folder = '/data/expdata/'
    docs = []
    for i in range(8):
        fname = folder + 'docs.%s.txt' % i
        print fname
        docs += codecs.open(fname, encoding='utf-8').readlines()
    ndoc = len(docs)
    print 'docs len:', ndoc
    fdoc, ftitle = (folder + i for i in ('cicdoc', 'cictitle'))
    idf = get_idf(docs)
    pool = Pool(processes=procnum)   
    params = [(idf, docs[(i * ndoc / procnum):((i + 1) * ndoc / procnum)], i, fdoc, ftitle) for i in range(procnum)]
    r = pool.map_async(mul_write_docs, params)
    r.wait()
    if not r.successful():
        print 'not completed'
    
def write_docs((infile, start, end, outfile)):
    fin = open(infile)
    fout = codecs.open(outfile, 'w', encoding='utf-8')
    fin.seek(start, 0)
    fin.readline()
    while fin.tell() < end:
        l = fin.readline()
        if not l:
            continue
        res = re.findall('"text":"([^"]+?)"', l)
        if not res:
            continue
        txt = res[0]
        txt = re.split(u'//[\s　]*?@', txt)[0]  # remove original content
        words = list(gen_nounword(txt))
        fout.write(u' '.join(words) + '\n')
    fout.close()
            
def batch_cicdata():
    pool = Pool(processes=procnum)   
    folder = '/data/expdata/'
    infile = folder + 'tweet_content_sian_201301.txt'
    folder = '/home/whille/Desktop/'
    infile = folder + 'uids.txt'
    fin = open(infile)
    fin.seek(0, 2)
    fsize = fin.tell()
    params = [(infile, i * fsize / procnum, (i + 1) * fsize / procnum, folder + 'docs.%s.txt' % i) for i in range(procnum)]
    fin.close()
    r = pool.map_async(write_docs, params)
    r.wait()
    if not r.successful():
        print 'not completed'
    
    
def build_news():
    import zipfile
    zipname = '/home/whille/machine.learning/SMT/corpus/news.zip'
    arc = zipfile.ZipFile(zipname)
    print 'files in arc', len(arc.namelist())
    fdoc, ftitle = (data_folder + i for i in ('newstitle' , 'newsdoc')) 
    f1, f2 = [codecs.open(i, 'w', encoding='utf-8') for i in (fdoc, ftitle)]
    for fname in arc.namelist():
        if not fname.endswith('.txt'):
            continue
        try:
            txt = arc.read(fname).decode('gbk')
        except:
            print fname
            continue
        title = fname.split('/')[1][:-4]
        words = list(gen_nounword(title))
        if len(words) <= 0:
            continue
        f1.write(u' '.join(words) + '\n')
        words = list(gen_nounword(txt))
        f2.write(u' '.join(words) + '\n')
    f1.close()
    f2.close()
        
def t_encs():
    model = m1.M1(hanse, hansf)
    for i in range(10):
        print 'iter:', i
        model.iterate(10, True)
        tmp = model.t.get('snow', {})
        for i in list(sortv_iter(tmp))[:10]:
            print i[0], i[1]
        save_diction(model.t, 'hans_dict')

if __name__ == '__main__':
#     build_news()
#    conv_file()
#    write_xls()
#     batch_cicdata()
#     gen_cic_title()
    folder = '/data/expdata/'
    # cat cicdoc.* >>cic_doc.txt
    # cat cictitle.* >>cic_title.txt
    fdoc, ftitle = (folder + i for i in ('cic_doc.txt', 'cic_title.txt'))
    test_wam(fdoc, ftitle, 'cic_dict')
#    t_guess(fdoc, '/home/whille/svnsrc/accountindex/1/accountindex/data/test.txt')
#   t_encs()
