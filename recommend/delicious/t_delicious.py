import json
import cPickle as pickle
import traceback
import math
import ast
import os
from collections import defaultdict


Categories = ('user', 'link', 'tag')
Dicx = {}
Sep = ', '
user_home = os.path.expanduser('~')
Data_dir = user_home + '/bak/data/delicious/'
fi_name = Data_dir + 'delicious-rss-1250k'
fo_name = './%s.inx' % fi_name
Dicx_fname = Data_dir + 'Dicx.pkl'
score_fname = Data_dir + 'score.txt'
Threshold_tag = 10

tf_u, tf_i, n_u, n_i, u_, i_, dic_tag = [
    defaultdict(int) for i in range(7)]
max_tfu = 0
max_tfi = 0
iuf, iif, bm25_u, bm25_i = {}, {}, {}, {}
dic_lu, dic_ul, dic_li, dic_il = [defaultdict(set) for i in range(4)]


def pre():
    fi = open(fi_name)
    fo = open(fo_name, 'wb')
    fo.write('#format: user_id, link_id, *tag_id\n')
    for cat in Categories:
        Dicx[cat] = {}
    for line in fi:
        try:
            uname, link, tags = parse(line)
            m = indexing(uname, 'user')
            n = indexing(link, 'link')
            ls = [indexing(t, 'tag') for t in tags]
            fo.write(Sep.join((m, n, Sep.join(ls))) + '\n')
        except Exception, e:
            # print traceback.format_exc()
            pass
    fo.close()
    pickle.dump(Dicx, open(Dicx_fname, 'wb'))


def parse(txt):
    o = json.loads(txt)
    uname, link = [o[i] for i in ('author', 'link')]
    assert 'tags' in o
    tags = [t['term'] for t in o['tags']]
    return uname, link, tags


def indexing(s, cat):
    if s in Dicx[cat]:
        n = Dicx[cat][s]
    else:
        n = Dicx[cat][s] = len(Dicx[cat])
    return str(n)


def train_test(test_ratio=0.2):
    # sort -t',' --key=1 delicious-rss-1250k.inx|uniq -u>sorted.txt
    fold = int(1 / test_ratio)
    print 'test_ratio=%f, fold=%d' % (test_ratio, fold)
    ftrain, ftest = [open(fo_name + i, 'wb') for i in ('.train', '.test')]
    cur = -1
    c = 0
    lst = []
    for m, n, ls in gen_data(fo_name + '.sorted'):
        if cur == m:
            c += 1
            lst.append(
                Sep.join((str(m), str(n), Sep.join([str(i) for i in ls]))))
            continue
        if c >= Threshold_tag:
            n_test = int(c * test_ratio)
            for lst_i, fo in zip((lst[:-n_test], lst[-n_test:]), (ftrain, ftest)):
                for line in lst_i:
                    fo.write(line + '\n')
                # yield lst[-n_test:], lst[:-n_test]
        cur = m
        c = 0
        lst = []
    ftrain.close()
    ftest.close()


def gen_data(fname):
    print fname
    first = True
    for line in open(fname):
        if first:
            first = False
            continue
        line = [int(i) for i in line.split(Sep)]
        m, n, ls = line[0], line[1], line[2:]
        yield m, n, ls


# paper: content-based recommendation in social tagging systems
def train():
    #Dicx = pickle.load(open(Dicx_fname))
    b, k1 = 0.75, 2.0
    for m, n, ls in gen_data(fo_name + '.train'):
        for l in ls:
            dic_tag[l] += 1
            tf_u[m, l] += 1
            tf_i[n, l] += 1
    for (m, l) in tf_u:
        n_u[l] += 1
        u_[m] += 1
    for (n, l) in tf_i:
        n_i[l] += 1
        i_[n] += 1
    M, N, L = len(u_), len(i_), len(n_u)
    print 'M, N, L=', M, N, L
    # M, N, L= 23008 250510 119180
    for l in n_u:
        iuf[l] = math.log(M * 1.0 / n_u[l])
    avg_u = 1.0 * sum(u_.values()) / len(u_)
    for m, l in tf_u:
        bm25_u[m, l] = tf_u[
            m, l] * (k1 + 1) * iuf[l] / (tf_u[m, l] + k1 * (1 - b + b * u_[m] / avg_u))
    for l in n_i:
        iif[l] = math.log(N * 1.0 / n_i[l])
    avg_i = 1.0 * sum(i_.values()) / len(i_)
    for n, l in tf_i:
        bm25_i[n, l] = tf_i[
            n, l] * (k1 + 1) * iif[l] / (tf_i[n, l] + k1 * (1 - b + b * i_[n] / avg_i))

    for m, l in tf_u:
        dic_lu[l].add(m)
        dic_ul[m].add(l)
    for n, l in tf_i:
        dic_li[l].add(n)
        dic_il[n].add(l)
    max_tfu = max(tf_u.values())
    max_tfi = max(tf_i.values())


def sim_tf_u(m, n):
    return sim_tf(m, n, tf_u, dic_il, max_tfu)


def sim_tf_i(m, n):
    return sim_tf(n, m, tf_i, dic_ul, max_tfi)


def sim_bm25_u(m, n):
    return sim_bm25(m, n, bm25_u, dic_il)


def sim_bm25_i(m, n):
    return sim_bm25(n, m, bm25_i, dic_ul)


def sim_bm25(m, n, A, dic):
    g = 0
    for l in dic[n]:
        if (m, l) in A:
            g += A[m, l]
    return g


def sim_cos_tf(m, n):
    return sim_cos(m, n, tf_u, tf_i)


def sim_cos_tfidf(m, n):
    return sim_cos(m, n, tf_u, tf_i, True)


def sim_cos_bm25(m, n):
    return sim_cos(m, n, bm25_u, bm25_i)


def sim_tf(m, n, A, dic, b):
    a = 0.0
    for l in dic[n]:
        if (m, l) in A:
            a += A[m, l]
    if b <= 0:
        g = 0.0
    else:
        g = a * 1.0 / b
    return g


def sim_bm25(m, n, A, dic):
    g = 0.0
    for l in dic_il[n]:
        if (m, l) in A:
            g += A[m, l]
    return g


def sim_cos(m, n, A, B, with_idf=None):
    a, b1, b2 = 0, 0, 0
    if with_idf:
        fA = lambda m, l: A[m, l] * iuf[l]
        fB = lambda n, l: B[n, l] * iif[l]
    else:
        fA = lambda m, l: A[m, l]
        fB = lambda n, l: B[n, l]
    for l in dic_il[n]:
        if (m, l) in A:
            A_ = fA(m, l)
            B_ = fB(n, l)
            a += A_ * B_
            b1 += A_ ** 2
            b2 += B_ ** 2
    if b1 <= 0 or b2 <= 0:
        g = 0.0
    else:
        g = a * 1.0 / (b1 ** 0.5 * b2 ** 0.5)
    return g

sim_fs = (sim_tf_u, sim_tf_i, sim_cos_tf, sim_cos_tfidf,
          sim_bm25_u, sim_bm25_i, sim_cos_bm25)


def best(dic, n):
    return sorted(dic.iteritems(), key=lambda (k, v): v, reverse=True)[:n]


def predict(m, tags, k=600):
    links = reduce(set.union, [dic_li[l] for l in popular(tags, 10)])
    dics = [{} for i in range(len(sim_fs))]
    for n in links:
        for i, f in enumerate(sim_fs):
            dics[i][n] = f(m, n)
    res = []
    for dic in dics:
        candi = k
        for i, j in enumerate(best(dic, k)):
            if j[0] == n:
                candi = i
                break
        res.append(candi)
    return res


def test():
    for m, n, ls in gen_data(fo_name + '.test'):
        res = predict(m, ls)
        print m, n, res


def popular(tags, k=3):
    if len(tags) <= 3:
        return tags
    dic = {}
    for tag in tags:
        dic[tag] = dic_tag[tag]
    return [i[0] for i in best(dic, k)]

# Mean reciprocal rank


def MRR(lst):
    assert len(lst) > 0
    a = sum([1.0 / (i + 1) for i in lst])
    return a / len(lst)


def evaluate():
    n_eval = len(sim_fs)
    lsts = [[] for i in range(n_eval)]
    dismiss = [600, ] * len(sim_fs)
    for line in open(score_fname):
        m, n, ls = line.split(' ', 2)
        m, n, ls = int(m), int(n), ast.literal_eval(ls)
        if ls == dismiss:
            continue
        for i in range(n_eval):
            lsts[i].append(ls[i])
    #[0.0413, 0.0413, 0.0468, 0.0468, 0.0525, 0.0437, 0.0471]
    #[0.0888, 0.0888, 0.10112, 0.1012, 0.1135, 0.094, 0.1016], dismiss
    return [MRR(lst) for lst in lsts]


if __name__ == '__main__':
    #    pre()
    # train_test()
    # train()
    # test()
    print evaluate()
