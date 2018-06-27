#!/usr/bin/env python

# use diction to store prefix info


def build(dic):
    ldict = {}
    for word, v in dic.iteritems():
        ldict[word] = v
        for r in xrange(1, len(word) + 1):
            ldict[word[:r]] = 0     # speed up DAG by add pref = 0 to ldict
    print ldict


def search(ldict, word):
    for r in xrange(1, len(word) + 1):
        if word[:r] not in ldict:
            return False
        return True


def test(dic, word):
    ldict = build(dic)
    print search(ldict, word)
