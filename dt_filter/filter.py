#coding=utf-8
import xlrd
import codecs
#import openpyxl
#from openpyxl.cell import get_column_letter

RESULT_FILE = 'result.csv'

def parse(buzz, dic):
    head = buzz.row_values(0)
    fo=codecs.open(RESULT_FILE, 'w', encoding='gbk')
#    workbook = openpyxl.Workbook(encoding = 'utf-8')  
#    sheet = workbook.create_sheet(title = 'result')  
    fo.write('keyword,txt\n')
#    for j, colname in enumerate(('keyword', 'txt')):    
#        col = get_column_letter(j+1)
#        sheet.cell('%s1' % col).value = colname 
#    i=2
    for colname in ('Subject','Content'):
        print colname
        rows = buzz.col_values(head.index(colname), start_rowx=1) 
        output(fo, rows, dic)
    fo.close()
#    workbook.save(RESULT_FILE)  

def output(fo, rows, dic):
    for row in rows:
        row = unicode(row).strip().lower()
        if not row:
            continue
        for khead, (ks, exps) in dic.iteritems():
            for k in ks:
                if row.find(k) >= 0:
                    break
            else:   #no keyword found
                continue
            for exp in exps:
                if row.find(exp) >= 0:
                    break #either expt is bad
            else:
                fo.write('%s, %s\n' %(khead, row))
#                for j, txt in enumerate((khead, row)):
#                    col = get_column_letter(j+1)
#                    sheet.cell('%s%s' % (col, i)).value = txt
                #sheet.write(i, 0, khead)#' '.join(ks))
                #sheet.write(i, 1, row)
#                i+=1


def build_ke(dt):
    head = dt.row_values(0)
    ks, exps = [dt.col_values(head.index(i), start_rowx=1) \
            for i in ('keyword','expword')]
    dic={}
    for k, e in zip(ks, exps):
        k = unicode(k).strip().lower()
        if not k:
            continue
        es = unicode(e).strip().lower().split()
        # space means OR, _ means AND
        ks = k.split()
        dic[ks[0]] = (ks, es)
    """
    for fn in f:
        key = [i.replace('_', ' ') for i in key.split()]
        exp = [i.replace('_', ' ') for i in exp.split()]
    """
    return dic

if __name__ == '__main__':
    fi = 'for whille.xlsx'
    data = xlrd.open_workbook(fi)
    buzz, dt = [data.sheet_by_name(i) for i in('data', 'DT')]
    dic = build_ke(dt)
    parse(buzz, dic)
