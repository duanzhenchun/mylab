from numpy import allclose

states = ('Healthy', 'Fever')
observations = ('normal', 'cold', 'dizzy', 'cold', 'normal')
transition_probability = {
   'Healthy' : {'Healthy': 0.69, 'Fever': 0.3},
   'Fever' : {'Healthy': 0.2, 'Fever': 0.8},
}
start_probability = {'Healthy': 0.5, 'Fever': 0.5}
emission_probability = {
   'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
   'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6},
}

T = len(observations)
end_state = states[0]


def fwd_bkw(Y, O, S, PI, A, B, xT):
    def forward():
        alpha = []
        f_prev = {}
        for t, yt in enumerate(Y):
            f_curr = {}
            for j in S:
                if t == 0:   # base case for the forward part
                    prev_f_sum = PI[j]
                else:
                    prev_f_sum = sum(f_prev[i] * A[i][j] for i in S)
                f_curr[j] = B[j][yt] * prev_f_sum
            alpha.append(f_curr)
            f_prev = f_curr

        pT = sum(f_curr[i] * A[i][xT] for i in states)
        return alpha, pT

    def backward():
        beta = []
        b_prev = {}
        for t, yt_plus in enumerate(reversed(Y[1:] + (None,))): # y(i+1)
            b_curr = {}
            for i in S:
                if t == 0:   # base case for backward part
                    b_curr[i] = A[i][xT]
                else:
                    b_curr[i] = sum(A[i][j] * B[j][yt_plus] * b_prev[j] for j in S)
            beta.insert(0, b_curr)
            b_prev = b_curr
        p0 = sum(PI[i] * B[i][Y[0]] * b_curr[i] for i in states)
        return beta, p0

    def Gamma():
        alpha, pT = forward()
        beta, p0 = backward()
        assert allclose(pT, p0)
        try:
            gamma = [dict((i, alpha[t][i] * beta[t][i]) for i in S) for t in xrange(T)]
        except:
            gamma = [{}, ]*T
        for t in xrange(T):
            all = sum(gamma[t].values())
            if not all:
                break
            for i in S:
                gamma[t][i] /= all
        return gamma, alpha, beta

    def Xi(alpha, beta):
        def normalize(dic):
            all = 0.0
            for i in dic:
                for j in dic[i]:
                    all += dic[i][j]
            if all <= 0:
                return
            for i in dic:
                for j in dic[i]:
                    dic[i][j] /= all

        xi = []
        for t in xrange(T - 1):
            dic = {}
            for i in S:
                dic.setdefault(i, {})
                for j in S:
                    dic[i][j] = alpha[t][i] * A[i][j] * B[j][Y[t + 1]] * beta[t + 1][j]
            normalize(dic)
            xi.append(dic)
        return xi

    def Ae(gamma, xi):
        A_e = {}
        for i in S:
            A_e[i] = {}
            for j in S:
                f1, f2 = (0.0,)*2
                for t in xrange(T - 1):
                    f1 += xi[t][i][j]
                    f2 += gamma[t][i]
                A_e[i][j] = f2 and 1.0 * f1 / f2 or 0.0
        return A_e

    def Be(gamma):
        B_e = {}
        for j in S:
            B_e[j] = {}
            for k in O:
                f1, f2 = (0.0,)*2
                for t in xrange(T):
                    if Y[t] == k:
                        f1 += gamma[t].get(j, 0.0)
                    f2 += gamma[t].get(j, 0.0)
                B_e[j][k] = f2 and 1.0 * f1 / f2 or 0.0
        return B_e

    gamma, alpha, beta = Gamma()
    xi = Xi(alpha, beta)
    PI_e = gamma[0]
    A_e = Ae(gamma, xi)
    B_e = Be(gamma)
    return PI_e, A_e, B_e

def example():
    Y, O, S, PI, A, B, xT = (observations,
                           set(observations),
                           states,
                           start_probability,
                           transition_probability,
                           emission_probability,
                           end_state)
    for i in xrange(100):
        PI, A, B = fwd_bkw(Y, O, S, PI, A, B, xT)
    print 'done'

example()
