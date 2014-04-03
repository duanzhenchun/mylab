# coding=utf-8
import jieba.posseg
import codecs
import os
import random
from utils import *
import sys

def to_suite_fmt():
    fout = 'prepare.txt'
    folder, fn  = get_data_f_fn()
    fout = codecs.open('%s/%s' %(folder, fout), 'w', encoding='utf8')
    docs = list(fn(folder))
    #random.shuffle(docs)
    for doc, is_pos in docs:
        for w_pos in jieba.posseg.cut(doc):
            w, pos = w_pos.word, w_pos.flag
            w = w.strip()
            if not w:
                continue
            fout.write('%s %s %s%s' %(w, pos, Sen_dic[is_pos], os.linesep))
        fout.write(os.linesep)

if __name__ == "__main__":
    to_suite_fmt()
