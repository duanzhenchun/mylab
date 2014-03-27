# coding=utf-8
import xlrd
import networkx as nx
from collections import defaultdict
import sys
import codecs
sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout) 

start_rowx=1
N=50


def sortv_iter(dic, reverse=False):
    for key, value in sorted(dic.iteritems(), reverse=reverse, key=lambda (k, v): (v, k)):
        yield key, value


def Dell():
    fname = "Dell mention.xlsx"
    shtname = "Sina"
    targets = (u'发帖人昵称', u'发帖人账号编号', u'原文发帖人账号编号',
               u'原文发帖人昵称', u'发帖人粉丝数')
    process(fname, shtname, targets)

def Starbucks():
    fname = u"星巴克.xlsx"
    shtname = "Sheet4"
    targets = (u'SCREEN_NAME', u'USER_ID', u'RT_USER_ID',
               u'RT_SCREEN_NAME', u'FOLLOWS_COUNT')
    engages = ('RT_COUNT', 'CT_COUNT', 'LIKE_COUNT')
    process(fname, shtname, targets, engages)

def to_ints(lst):
    return [i and int(i) or None for i in lst]

def process(fname, shtname, targets, engages=[]):
    data = xlrd.open_workbook(fname)
    sht = data.sheet_by_name(shtname)
    head = sht.row_values(0)
    unames, uids, puids, puname, nfans = [sht.col_values(head.index(t), start_rowx) for t in targets]
    uids, puids, nfans = [to_ints(lst) for lst in (uids, puids, nfans)]
    udic={}
    for uid, uname, nfan in zip(uids, unames, nfans):
        udic[uid]=(uname, nfan)

    if engages:
        engs = [sht.col_values(head.index(t), start_rowx) for t in engages]
        eng_counts = []
        for i in zip(*engs):
            eng_counts.append(sum([int(j) for j in i]))
        u_eng=dict(zip(uids, eng_counts))
        topn = list(sortv_iter(u_eng, True))[:N]
        print "#engagement topn"
        show_topn(topn, udic)
    edges=defaultdict(int)
    for uid, puid, eng in zip(uids, puids, eng_counts):
        if not puid:    #original 
            continue
        if uid == puid: #self loop
            continue
        edges[(uid,puid)] += eng
    for k in edges:
        edges[k] = max(0.1, edges[k]) #(edges[k] * max(1, udic[k[0]][1]))**0.5
    for wt in (True, False):
        kol(edges, udic, wt)


def kol(edges, udic, weight=False):
    print weight
    G=nx.DiGraph()
    if weight:
        G.add_weighted_edges_from([(uid,puid,v) for (uid,puid),v in edges.iteritems()])
    else:
        G.add_edges_from(edges.keys())
    ranks = nx.pagerank(G, tol=1e-4)
    topn = list(sortv_iter(ranks, True))[:N]
    print "kol topn"
    show_topn(topn, udic)

def show_topn(topn, udic):
    print "#format: uid rank uname nfan"
    for (uid, rank) in topn:
        print uid, rank, 
        tmp = udic.get(uid)
        if tmp:
            print tmp[0], tmp[1]
        else:
            print


if __name__=="__main__":
#    Dell()
    Starbucks()
