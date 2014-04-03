from collections import defaultdict

Auth='auth'
Hub = 'hub'

def test():
    G={'a':{Hub:('b','c')},
       'd':{Hub:('a')},
    }
    return G

def construct(G):
    G1 = defaultdict(lambda:defaultdict(lambda:[set(), 1.0]))
    for a, b in ((Auth, Hub), (Hub, Auth)):
        for p in G:
            for q in G[p].get(a, ()):
                G1[p][a][0].add(q)
                G1[q][b][0].add(p)
    return G1


def hits(G, maxIter=10):
    for iter in xrange(maxIter):
        for a, b in ((Auth, Hub), (Hub, Auth)):
            s=0.0
            for p in G:
                G[p][a][1] = 0.0
                for q in G[p][b][0]:
                    G[p][a][1] += G[q][b][1]
                s += G[p][a][1] **2
            s = s**0.5
            if s<=0.0:
                continue
            for p in G:
                G[p][a][1] /= s


def main():
    G=construct(test())
    hits(G)
    print G

if __name__ == '__main__':
    main()
