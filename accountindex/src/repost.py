# coding=utf-8
""" 
weibo user:   4-30位字符：英文、数字或中文均可，不重复
"""

import os
import logging
import re
import Queue
import heapq
from utils import benchmark, tounicode, toutf8
DEBUG = False

class TopN(object):
    """
    v format: (num, value)
    
    after looking into http://hg.python.org/cpython/file/2.7/Lib/heapq.py, 
    i find heappushpop already optimize, no need bottom value
    
    feed() can be optimize further, if needed:
        using func object instead of compare len(self.h) each time
    """
    def __init__(self, N):
        self.N = N
        self.h = []        
    
    def feed(self, v):  
        if len(self.h) < self.N:
            heapq.heappush(self.h, v)
        else:
            heapq.heappushpop(self.h, v)
            
    def result(self):
        self.h.sort(reverse=True)
        return self.h

def getparent(txt, user, rootid, root, reposters):
    parents = re.findall(r'//\s*?@(.*?)\s*?:', txt.replace(u'：', u':'))
    if not parents:
        parents = [root]
    for parent in parents:
        if parent == root or (parent != user and parent in reposters):
            break
    else:
        parent = root
    return reposters[parent]

            
def travel(root, res, ill):
    total = 0
    visit = Queue.Queue()
    visit.put(root)
    
    verify = res.keys()
    while not visit.empty():
        cur = visit.get()
        verify.remove(cur)
        count, acum, children = res[cur]
        if not children:
            continue
        if DEBUG and count != len(children):
            logging.warn("res[%s]: reposts: %d, child_len:%d" % (cur, count, len(children)))
                
        total += len(children)
        for i in children:
            if i in res:
                visit.put(i)
        if DEBUG:
            info = cur + ": "
            for i in children:
                info += i + ','
            logging.debug(info[:-1])
    if verify:
        logging.warn('not included: %s' % verify)
        ill += len(verify)
    logging.info('total: %s' % res[root][0])
    logging.info('total reposts(after trim ill route): %s' % total)
    logging.info('ill: %d\n' % ill)
    assert res[root][1] == total
    
@benchmark()    
def exposure_sum(all, root):
    visit = Queue.Queue()
    visit.put((root, 0))
    route = []
    parent_dic = {}
    newall = {}  # direct repost, accumulated, sub_lst, beta_exposure
    maxlvl = 0
    lvlsum = {}
    beta = 1
    while not visit.empty():
        cur, lvl = visit.get(0)
        route.append(cur)
        lst = []
        for child in all[cur][1]:
            if child in all:
                visit.put((child, lvl + 1)) 
                parent_dic[child] = cur  
                lst.append(child)
        count = len(all[cur][1]) 
        beta = max(beta, count)
        newall[cur] = [count, count, lst, count]      
        maxlvl = max(maxlvl, count > 0 and lvl + 1  or lvl)   
        lvlsum.setdefault(lvl + 1, 0)
        lvlsum[lvl + 1] += count
    beta = float(beta)
    print 'beta =', beta
    route.pop(0)  # root
    for i in reversed(route):  
        newall[parent_dic[i]][1] += newall[i][1]
        newall[parent_dic[i]][-1] += newall[i][1] / beta
    parent_dic[root] = root
    trim_leaf(newall)
    lvlsum.pop(maxlvl + 1, 0)
    
    return newall, maxlvl, parent_dic, lvlsum

def trim_leaf(dic):
    if len(dic)<2:    # only root node
        return 
    for i in dic.keys():
        if dic[i][0] < 1:
            del dic[i]
    
def getfile(fname):
    with open(fname, 'r') as f:
        for line in reversed(f.readlines()):
            if len(line) < 2:
                continue
            count, userid, user, id, txt = line.split(' ', 4)
            yield int(count), int(userid), tounicode(user), tounicode(txt.strip('\n'))
            
def get_rlist(li):
    return reversed(li)
        
@benchmark(getcost=True)
def build(rootid, root, data, getfn=getfile):
    """
    assume data are sorted, neglect self repost and multi repost
    """
    res = {rootid:[0, set()]}  
    linenum = 0
    ill = 0
    reposters = {root:rootid}  # uname:uid
    parent_uids = {0:rootid}  # id:userid 
    # data are sorted along timeline
    for (count, userid, user, Id, pid) in getfn(data):
        parent_uids[Id] = userid
        parent = parent_uids.get(pid, 0)
        if not parent:
            txt = ''
#            print "pid not exist in parent_uids", pid, len(parent_uids)
            parent = getparent(txt, userid, rootid, root, reposters)
            parent_uids[pid] = parent
        if not user:
            user = unicode(userid)
        linenum += 1
        if userid == rootid:
            ill += 1
            continue
        if userid in res:
            ill += 1
            if DEBUG:
                logging.warning('user already in res: ' + 
                          ' '.join((str(count), str(userid), user, parent)))
            continue
        reposters[user] = userid
        res.setdefault(parent, [0, set()])
        if userid in res[parent][1]:
            ill += 1
            if DEBUG:
                logging.warn('duplicated repost: ' + ','.join(
                           (str(count), str(userid), user, parent)))  
        else:       
            res[parent][1].add(userid)
        res.setdefault(userid, [count, set()])
        res[userid][0] = count
    res[rootid][0] = linenum
#     print 'ill: %d\n' % ill
    
    newall, maxlvl, parent_dic, lvlsum = exposure_sum(res, rootid)
    return newall, maxlvl, lvlsum, topreposters(newall, reposters, rootid, parent_dic)

def topreposters(All, reposters, rootid, parent_dic, N=20):
    """
    topn without root
    """
    topn = TopN(N + 1)
    for k, v in All.iteritems():
        topn.feed((int(round(v[-1])), k))
    result = topn.result()
    lst = []  # accumu_num, uid, uname, parent
    r_dic = dict((v, k) for k, v in reposters.iteritems())
    for i in result:
        if i[1] != rootid:
            lst.append((i[0], i[1], r_dic[i[1]], parent_dic[i[1]]))
    if len(lst) > N:
        lst.pop()
    return lst
    
def connect_islands(res, root):
    records = res.keys()
    records.remove(root)
    for v in res.itervalues():
        if not records:
            break
        for i in v[1]:
            if i in records:
                records.remove(i)
    res[root][1] += records
            
def ini_log():
    logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    ini_log()
    t_data = [
        # format: root, sample_file,total_reposts
        [u"A", "normal", 2],
        [u"circle", "circle", 2],
        [u"circle", "circle2", 2],
        [u"方糖气球", "sample", 3170282535],  # http://weibo.com/3170282535/z8cG6DBMT
        ]
    path = 'data'
    for i in t_data:
        build(i[2], i[0], os.sep.join((path, i[1])))
