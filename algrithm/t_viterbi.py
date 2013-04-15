# ref: http://zh.wikipedia.org/wiki/%E7%BB%B4%E7%89%B9%E6%AF%94%E7%AE%97%E6%B3%95
from math import log


states = ('Healthy', 'Fever')
observations = ('normal', 'cold', 'dizzy', 'cold', 'dizzy', 'normal')
start_probability = {'Healthy': 0.6, 'Fever': 0.4}
transition_probability = {
   'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},
   'Fever' : {'Healthy': 0.4, 'Fever': 0.6},
   }
emission_probability = {
   'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
   'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6},
   }

def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = start_p[y] * emit_p[y].get(obs[0], 0)
        path[y] = [y]

    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            if obs[t] not in emit_p[y]:
                continue
            lst = []
            for y0 in path:
                if y0 not in trans_p:
                    trans_p.setdefault(y0, {})
                if y not in trans_p[y0]:
                    trans_p[y0][y] = 1.0 / 8000
                if y0 not in V[t - 1]:
                    V[t - 1][y0] = 1.0 / 8000
                lst.append((V[t - 1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0))
            (prob, state) = max(lst)
            if state not in path:
                continue
            V[t][y] = prob
            newpath[y] = path[state] + [y]
        # Don't need to remember the old paths
        path = newpath

#    print_dptable(V)
    (prob, state) = max([(V[len(obs) - 1].get(y, 0), y) for y in states])
    return (prob, path[state])

def example():
    print 'observations:', observations
    return viterbi(observations,
                   states,
                   start_probability,
                   transition_probability,
                   emission_probability)


def print_dptable(V):
    print "    ",
    for i in range(len(V)): print "%7d" % i,
    print

    for y in V[0].keys():
        print "%.5s: " % y,
        for t in range(len(V)):
            print u"%.7s" % ("%f" % V[t].get(y, 0)),
        print

if __name__ == '__main__':
    print example()

