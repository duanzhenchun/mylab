#coding:utf-8
import xlrd
import numpy as np
from scipy import sparse
from lshash import LSHash
import jieba
from utils import *

fname = 'sap.etc.xlsx'
shtname = 'Sheet1'
target = u'微博原始内容'
start_rowx=1
#First_cs = ord(u'\u4e00')
#Last_cs = ord(u'\ufaff')
        
jieba.initialize()
Index = dict(zip(jieba.FREQ.keys(), range(len(jieba.FREQ))))
dim = len(Index) + 1 # -1 for excluded

data = xlrd.open_workbook(fname)
sht = data.sheet_by_name(shtname)
head = sht.row_values(0)
tweets = sht.col_values(head.index(target), start_rowx)

hash_size = int(np.ceil(np.log2(len(tweets))))
print 'hash_size: %d, dim: %d' %(hash_size, dim)
lsh=LSHash(hash_size, dim)

for tweet in tweets:
    x = spar.csr_matrix((1,dim) ,dtype=np.int8)
#    x = np.zeros(dim, np.bool8)
    ws = jieba.cut(tweet)
    try:
        for w in ws:
            x[Index.get(w, -1)] = 1
        lsh.index(x)
    except Exception, e:
        print e
        print tweet

sent = True
while sent:
    sent = raw_input('input sentence...\n')
    res = lsh.query(sent, distance_func = 'hamming')
    for i in res:
        print i[0], i[-1]

