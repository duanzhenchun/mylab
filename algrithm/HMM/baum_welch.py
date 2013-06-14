""" 
Baum-Welch algorithm, also called forward-backward algorithm
local optimum value is reached
"""
import random
from util import *
import math


def fwd_bkw(Y, S):
    def rand_prob(keys):
        n = len(keys)
        lst = [random.randint(1, 10) for i in xrange(n)]
        dic = dict(zip(keys, lst))
        norm_dict(dic)
        return dic
    
    def init_model(states):
        PI = dict(zip(states, (1.0 / len(states),) * len(states)))  # equal probability
        A, B = {}, {}
        for i in states:
            A[i] = rand_prob(states)
            B[i] = rand_prob(set(Y))
        return PI, A, B

    def forward():
        """
        alpha(t,i): probability of Si in t, given observations from 0~t
        """
        alpha = []
        f_prev = {}
        for t, yt in enumerate(Y):
            f_curr = {}
            for j in S:
                if t == 0:  # base case for the forward part
                    prev_f_sum = PI[j]
                else:
                    prev_f_sum = sum(f_prev[i] * A[i][j] for i in S)
                f_curr[j] = prev_f_sum * B[j][yt]
            alpha.append(f_curr)
            f_prev = f_curr
#         pT = sum(f_curr[i] * A[i][xT] for i in S)
        return alpha

    def backward():
        """
        beta(t,i): probability of Si in t, given observations from t+1~T
        """
        beta = []
        b_prev = {}
        for t, yt_plus in enumerate(reversed(Y[1:] + (None,))):  # y(i+1)
            b_curr = {}
            for i in S:
                if t == 0:  # base case for backward part
                    b_curr[i] = A[i][xT]
                else:
                    b_curr[i] = sum(A[i][j] * B[j][yt_plus] * b_prev[j] for j in S)
            beta.insert(0, b_curr)
            b_prev = b_curr
#         p0 = sum(PI[i] * B[i][Y[0]] * b_curr[i] for i in S)
        return beta

    def Gamma_Xi(PI, A, B):
        """
        gamma: probability of State i in t, given Observations and model
        xi: probability of State i in t and State j in t+1, given Observations and model
        """
        alpha = forward()
        beta = backward()
        try:
            gamma = [dict((i, alpha[t][i] * beta[t][i]) for i in S) for t in xrange(T)]
        except:
            gamma = [{}, ] * T
        for t in xrange(T):
            norm_dict(gamma[t])
        xi = []
        for t in xrange(T - 1):
            dic = {}
            for i in S:
                dic.setdefault(i, {})
                for j in S:
                    dic[i][j] = alpha[t][i] * A[i][j] * B[j][Y[t + 1]] * beta[t + 1][j]
            norm_dict2(dic)
            xi.append(dic)
        return gamma, xi

    def A_E(gamma, xi):
        A_e = {}
        for i in S:
            A_e[i] = {}
            for j in S:
                f1, f2 = (0.0,) * 2
                for t in xrange(T - 1):
                    f1 += xi[t][i][j]
                    f2 += gamma[t][i]
                A_e[i][j] = f2 and 1.0 * f1 / f2 or 0.0
            norm_dict(A_e[i])
        return A_e

    def B_E(gamma):
        B_e = {}
        for j in S:
            B_e[j] = {}
            for k in set(Y):
                f1, f2 = (0.0,) * 2
                for t in xrange(T):
                    if Y[t] == k:
                        f1 += gamma[t].get(j, 0.0)
                    f2 += gamma[t].get(j, 0.0)
                B_e[j][k] = f2 and 1.0 * f1 / f2 or 0.0
        return B_e

    def iteration(PI, A, B, iter_limit=1000, threshold=1e-5):
        for i in xrange(iter_limit):
            # E steps
            gamma, xi = Gamma_Xi(PI, A, B)
            # M steps
            PI, A_e, B_e = gamma[0], A_E(gamma, xi), B_E(gamma)
            dif = diff(A, A_e) + diff(B, B_e)
            if threshold > dif:
                break
            A, B = A_e, B_e
        print i, dif
        return PI, A, B
    
    def diff(M, M0):
        dif = 0.0
        for i in M:
            for j in M[i]:
                dif += (M[i][j] - M0[i][j]) ** 2
        return dif
        
    PI, A, B = init_model(S)
    T = len(Y)
    xT = S[0]
    return iteration(PI, A, B)
    
def example():
    observations = ('normal', 'dizzy', 'cold', 'cold', 'normal')
    observations = tuple([random.randint(0, 9) for i in range(100)])
    states = ('Healthy', 'Fever')
    print fwd_bkw(observations, states)

if __name__ == '__main__':
    example()
