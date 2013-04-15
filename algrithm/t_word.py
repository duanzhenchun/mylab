#coding=utf-8

import re
import math


re_han, re_skip = re.compile(ur"([\u4E00-\u9FA5]+)"), re.compile(ur"[^a-zA-Z0-9+#\r\n]")
STATES = 'BMES'
trans, obs, emiss = {}, {}, {}
TAG = u'|'


#trans = dict(zip('BMES', (dict(zip('BMES', (0,)*4)),)*4))
#obs = dict(zip('BMES', (0,)*4))
#emiss = dict(zip('BMES', ({},)*4))


def gen_line():
    with open('../icwb2-data/gold/pku_test_gold.utf8', 'r') as f:
        for line in f:
            yield line

def gen_w():
    for line in gen_line():
        for seg in line.strip().split(u'  '):
            if not re_han.match(seg):
                yield None, None
            elif len(seg) == 1:
                yield seg, 'S'
            else:
                for i in xrange(len(seg)):
                    if 0 == i:
                        s = 'B'
                    elif i < len(seg) - 1:
                        s = 'M'
                    else:
                        s = 'E'
                    yield seg[i], s

def norm(dic):
    for k in dic:
        all = sum(dic[k].values())
        for w, v in dic[k].iteritems():
            dic[k][w] = v * 1.0 / all

def build(wordmodel=False):
    first = True
    for w, s in gen_w():
        if w == None:
            first = True
            continue
        if wordmodel:
            s = (w + (s in 'SE' and TAG or ''))
        obs[s] = obs.get(s, 0) + 1
        emiss.setdefault(s, {})
        emiss[s][w] = emiss[s].get(w, 0) + 1
        if first:
            first = False
            pre = s
        else:
            trans.setdefault(pre, {})
            trans[pre][s] = trans[pre].get(s, 0) + 1
        pre = s
    all = sum(obs.values())
    for k, v in obs.iteritems():
        obs[k] = v * 1.0 / all
    norm(trans)
    norm(emiss)
    return obs, trans, emiss


def test_seg():
    from t_viterbi import viterbi

    PI, A, B = build(True)
    for k in B.keys():
        if '|' == k[-1]:
            B[k[:-1]] = {k[:-1]: 1.0}
        else:
            B[k + '|'] = B[k]
    S = B.keys()
    for k in S:
        if k not in PI:
            PI[k] = 0.0
    samples = [
     u'改判被告人死刑立即执行',
     u'检察院鲍绍坤检察长',
     u'小明硕士毕业于中国科学院计算所',
     ]
    for sen in samples:
        Y = tuple(sen)
        prob, X = viterbi(Y, S, PI, A, B)
        print prob, u''.join(X)

if __name__ == '__main__':
    test_seg()

