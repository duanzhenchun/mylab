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
from scipy.misc import comb
from math import factorial
from math import log
from numpy import argmax
from collections import defaultdict
import m1


# sec 20
def d_estimate(dc, i, l, m):
    Z = sum([dc(j, i, l, m) for j in m]) 
    return dc(j, i, l, m) / Z

def p1_estimate(m, n_phi):
    p1 = n_self.phi0 / (m - n_self.phi0)
    return p1

class M3(m1.M1):
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
            
    
    # sec 25
    def P_af_e(self, e, f, phi, p1, n):
        """
        P(a,f|e)
        """
        l, m = len(e), len(f)
        p = 1.0
        p *= comb(m - self.phi0, self.phi0) * (1 - self.p1) ** (m - 2 * self.phi0) * self.p1 ** self.phi0
        for i in range(l):
            p *= factorial(phi[i]) * n(phi[i], e[i])
        for j in range(m):
            p *= self.t[e[i]][f[j]] * self.a[i, j, m, l] 
        p *= factorial(self.phi0) ** (-1)
        return p 
        
    def M(self):
        self.t = None
        self.a = None
        self.phi0 = None
        self.phi = None
        self.p1 = None
        
    # sec35, method 4
    def c_phi_e(self, l, m, phi, times, big_gamma, e, f):
        phi_max = max(phi)
        alpha = {}
        c = {}
        for i in range(l):
            for k in range(phi_max):
                beta = 0.0
                for j in range(m):
                    beta += (self.t[e[i]][f[j]] / (1 - self.t[e[i]][f[j]])) ** k
                alpha[i, k] = (-1) ** (k + 1) * beta / k
        for i in range(l):
            r = 1.0
            for j in range(m):
                r *= (1 - self.t[e[i]][f[j]])
            for phi in range(phi_max):
                sum = 0.0
                for p in big_gamma(phi):
                    prod = 1.0
                    for k in range(phi):
                        prod *= alpha[i, k] ** times(p, k) / factorial(times(p, k))
                    sum += prod
                c[phi, e[i]] += r * sum
        return c
        
# sec 13
def perplexity(P , f, e, N):
    return 2 ** (-log(P(f, e)) / N)

# sec 30
def topn_distortion(n=100):
    """
    for CPU issue, choose best n alignment pairs
    """
    pass

    
