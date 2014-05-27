# coding=utf-8
import xlrd
import codecs
from collections import defaultdict


FILE_IN = 'whole.xlsx'  # 'Coppertone Product Whille.xlsx'
DATA_SHEETS = ('Data', )  # ('pink', 'blue', 'green', 'other')
TARGETS = ('Subject', 'Content')
DTSHEET = 'DT'
DT_NAMES = ('cat1.cn', 'cat2.cn', 'keyword', 'expword')
RESULT_FILE = 'result.csv'
STATS_FILE = 'stats.csv'
AND_SEP = '_'


def writef(fname):
    return codecs.open(fname, 'w', encoding='gb18030')


def parse(result_fname, buzz, dic):
    counts = defaultdict(int)
    head = buzz.row_values(0)
    fo = writef(result_fname)
    fo.write('keyword, txt\n')
    for colname in TARGETS:
        print colname
        # , end_rowx=10)
        rows = buzz.col_values(head.index(colname), start_rowx=1)
        output(fo, rows, dic, counts)
    fo.close()
    return counts


def output(fo, rows, dic, counts):
    for row in rows:
        first = True
        row = unicode(row).strip().lower()
        if not row:
            continue
        for khead, (ks, exps) in dic.iteritems():
            for k in ks:
                for k_and in k:
                    if row.find(k_and) < 0:
                        break
                else:
                    break  # all AND matched
            else:  # no keyword found
                continue
            for exp in exps:
                for e_and in exp:
                    if row.find(e_and) < 0:
                        break
                else:
                    break  # either expt is bad
            else:
                fo.write(u'%s, %s\n' % (khead, first and row or ''))
                first = False
                counts[khead] += 1


def build_ke(dt):
    head = dt.row_values(0)
    cat1s, cat2s, ks, exps = [
        dt.col_values(head.index(i), start_rowx=1) for i in DT_NAMES]
    dic = {}
    dic_cat1 = {}
    dic_cat2 = {}
    for cat1, cat2, k, e in zip(cat1s, cat2s, ks, exps):
        khead = unicode(k).strip()
        if not khead:
            continue
        cat1 = cat1.strip()
        cat2 = cat2.strip()
        if not cat2:
            cat2 = cat1 + '_cat2'
        es = unicode(e).strip()
        # space means OR, _ means AND
        dic[khead] = [
            [i.split(AND_SEP) for i in tmp.lower().split()] for tmp in (khead, es)]
        dic_cat2[khead] = cat2
        dic_cat1[cat2] = cat1
    return dic, dic_cat1, dic_cat2


def upcounts(dic, dic_up):
    dic2 = defaultdict(int)
    for k, v in dic_up.iteritems():
        dic2[v] += dic[k]
    return dic2


def tops(dic, title, fo):
    res = sorted(dic.iteritems(), key=lambda (k, v): v, reverse=True)
    fo.write(title + '\n')
    for i in res:
        fo.write('%s, %s\n' % (i[0], i[1]))


if __name__ == '__main__':
    data = xlrd.open_workbook(FILE_IN)
    dt = data.sheet_by_name(DTSHEET)
    dic, dic_cat1, dic_cat2 = build_ke(dt)
    for datasheet in DATA_SHEETS:
        print datasheet
        buzz = data.sheet_by_name(datasheet)
        counts = parse('%s_%s' % (datasheet, RESULT_FILE), buzz, dic)
        dic2 = upcounts(counts, dic_cat2)
        dic1 = upcounts(dic2, dic_cat1)
        fo = writef('%s_%s' % (datasheet, STATS_FILE))
        titles = ('keywords_stat', 'cat2_stat', 'cat1_stat')
        for title, i in zip(titles, (counts, dic2, dic1)):
            tops(i, title, fo)
        fo.close()
