#coding=utf-8
import xlrd
import codecs
from collections import defaultdict


TARGETS = ('Subject','Content')
RESULT_FILE = 'result.csv'
STATS_FILE = 'stats.csv'
AND_SEP = '_'


def parse(buzz, dic):
    counts=defaultdict(int)
    head = buzz.row_values(0)
    fo=codecs.open(RESULT_FILE, 'w', encoding='gbk')
    fo.write('keyword, txt\n')
    for colname in TARGETS:
        print colname
        rows = buzz.col_values(head.index(colname), start_rowx=1) 
        output(fo, rows, dic, counts)
    fo.close()
    return counts


def output(fo, rows, dic, counts):
    for row in rows:
        row = unicode(row).strip().lower()
        if not row:
            continue
        for khead, (ks, exps) in dic.iteritems():
            for k in ks:
                for k_and in k:
                    if row.find(k_and)<0:
                        break
                else:
                    break  #all AND matched
            else:   #no keyword found
                continue
            for exp in exps:
                for e_and in exp:
                    if row.find(e_and) < 0:
                        break
                else:
                    break #either expt is bad
            else:
                fo.write('%s, %s\n' %(khead, row))
                counts[khead]+=1


def build_ke(dt):
    head = dt.row_values(0)
    cat1s, cat2s, ks, exps = [dt.col_values(head.index(i), start_rowx=1) \
            for i in ('cat1.cn', 'cat2.cn','keyword','expword')]
    dic={}
    dic_cat1={}
    dic_cat2={}
    for cat1, cat2, k, e in zip(cat1s, cat2s, ks, exps):
        khead = unicode(k).strip()
        if not khead:
            continue
        cat1=cat1.strip()
        cat2=cat2.strip()
        es = unicode(e).strip()
        # space means OR, _ means AND
        dic[khead] = [[i.split(AND_SEP) for i in tmp.lower().split()] for tmp in (khead,es)]
        dic_cat2[khead]=cat2
        dic_cat1[cat2]= cat1
    return dic, dic_cat1, dic_cat2

def upcounts(dic, dic_up):
    dic2=defaultdict(int)
    for k,v in dic_up.iteritems():
        dic2[v] += dic[k]
    return dic2


def tops(dic,title, fo):
    res = sorted(dic.iteritems(), key=lambda (k, v):v, reverse=True)
    fo.write(title+'\n')
    for i in res:
        fo.write('%s,%s\n' %(i[0], i[1]))


if __name__ == '__main__':
    fi = 'for whille.xlsx'
    data = xlrd.open_workbook(fi)
    buzz, dt = [data.sheet_by_name(i) for i in('data', 'DT')]
    dic, dic_cat1, dic_cat2 = build_ke(dt)
    counts = parse(buzz, dic)
    dic2 = upcounts(counts, dic_cat2)
    dic1 = upcounts(dic2, dic_cat1)
    fo=codecs.open(STATS_FILE, 'w', encoding='gbk')
    titles =('keywords_stat', 'cat2_stat', 'cat1_stat')
    for title, i in zip(titles, (counts, dic2, dic1)):
        tops(i, title, fo)
    fo.close()
