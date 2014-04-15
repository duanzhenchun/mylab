# -*- coding: utf-8 -*-
import re


def split_cs(s):
    r = re.compile(u'\\w+|[\u4e00-\ufaff]|[^\\s]')
    res = r.findall(s)
    return res

def t_split_cs():
    print split_cs(u"Testing English text我爱蟒蛇")

def ngram(lst, n=2):
    for i in range(len(lst)-n+1):
        yield lst[i:i+n]

if __name__ == "__main__":
    t_split_cs()
