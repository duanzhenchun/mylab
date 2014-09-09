"""
IBM model 3
parameter:
n
t
d
p1(phi-0)

refer:
A Statistical MT Tutorial Workbook, Kevin Knight, 1999
"""
from collections import defaultdict
from numpy import argmax
import m1
    
class M2(m1.M1):
    def __init__(self, source, target, t=None):
        super(M2, self).__init__(source, target, t)
        self.a = defaultdict(float)
        for (e, f) in m1.bitext(self.source, self.target):
            l, m = len(e), len(f)
            for j in range(m):
                tmp = 1.0 / l
                for i in range(l):
                    self.a[i, j, m, l] = tmp
                
    def EM(self, delta_threshold):
        # E step:
        c_fe = defaultdict(float)
        c_e = defaultdict(float)
        c_ijml = defaultdict(float)
        c_jml = defaultdict(float)
        for (e, f) in m1.bitext(self.source, self.target):
            l, m = len(e), len(f)
            for j in range(m):
                tmpdic = defaultdict(float)
                total = 0.0
                for i in range(l):
                    tmp = self.t[e[i]][f[j]] * self.a[i, j, m, l] 
                    tmpdic[f[j], e[i]] = tmp
                    total += tmp
                if total <= 0: 
                    continue
                for i in range(l):
                    tmp = tmpdic[f[j], e[i]] / total
                    c_fe[e[i], f[j]] += tmp  # (27)
                    c_e[e[i]] += tmp
                    c_ijml[i, j, m, l] = tmp  # (28)
                    c_jml[j, m, l] += tmp
            
        # M step:
        accepted = 0
        for e, f in c_fe:
            if c_e[e] <= 0:
                continue
            tmp = c_fe[e, f] / c_e[e]
            if delta_threshold > abs(self.t[e][f] - tmp):
                accepted += 1
            self.t[e][f] = tmp
        for k in c_ijml:
            if c_jml[k[1:]] <= 0:
                continue
            self.a[k] = c_ijml[k] / c_jml[k[1:]]
        return accepted
    
    def decode_pair(self, e, f):
        l, m = len(e), len(f)
        for j in range(m):
            lst = [self.t[e[i]][f[j]] * self.a[i, j, m, l] for i in range(l)]
            aj = argmax(lst)
            yield e[aj], f[j]
            
