import random
import math
from itertools import product
import pylab as plt
import math
from util import *  


SHOW = True
dimention = 3

def randpos(space):
    return tuple([random.random()*space for i in xrange(dimention)])
    
def cell(pos, near):
    return tuple(map(lambda x: int(x / near), pos))
    

def adjacent_grid(centre, near):
    near = int(near)
    steps = product(range(-near, near + 1), repeat=len(centre))
    return (tuple(c + d for c, d in zip(centre, delta)) for delta in steps)

def distance(p1, p2):
    res = 0.0
    for i in range(len(p1)):
        res += (p1[i] - p2[i]) ** 2
    return res ** (1.0 / len(p1))

def ptkey(p):
    s = '_'.join(['%.10f' for i in p])
    return s % p
    
def getgamma(near=1.0, steps=10, space=100, surviveratio=0.1):
    def mergecluster(From, to):
        nodes[to] += nodes[From]
        edges[to] += edges[From]
        for i in nodes[From]:
            rdic[i] = to
        del nodes[From]
        del edges[From]
    
    def getallometry():
        x, y = [], []
        for k, v in nodes.iteritems():
            x.append(len(v))
            y.append(len(edges[k]) + 1)     # add 1 to edge, to avoid 0
        x, y = map(lambda i:math.log(i), x), map(lambda i:math.log(i), y)
        x, y = zip(*(sorted(zip(x, y))))
        return calclinalg(x, y)

    assert near > 0
    if SHOW:
        plt.ion() 
    colors = list(iter('bgrcmyk'))

    p = randpos(space)
    cel = cell(p, near)
    celldic = {cell: [p]}
    nodes = {p: [p]}
    edges = {p:[]}
    rdic = {p:p}
    visited = set([p])
    drawnode(p)

    for c in range(steps):
        print c,
        p = randpos(space)
        if p in visited:
            continue
        cel = cell(p, near)
        survive = False
        visit = set()
        for i in adjacent_grid(cel, near):
            for p2 in celldic.get(i, []):
                if distance(p, p2) <= near:
                    survive = True
                    visit.add(p2)
        if survive:
            clus = set([rdic[i] for i in visit])
            head = clus.pop()
            for i in clus:
                mergecluster(i, head)
            nodes[head].append(p)    
            for i in visit:
                edges[head].append((p, i))
                drawedge(p, i)
            rdic[p] = head
        secondlife = False    
        if not survive and random.random() < surviveratio:
            nodes[p] = [p]
            edges[p] = []
            rdic[p] = p
            secondlife = True
            
        if survive or secondlife:
            celldic.setdefault(cel, [])
            celldic[cel].append(p)
            visited.add(p)
            drawnode(p)
    assert len(nodes) == len(edges)
    assert len(visited) == len(rdic)
    gamma = getallometry()
    return gamma[0]

def drawnode(p):
    if not SHOW:
        return
    plt.plot((p[0]), (p[1]), 'b.')
    plt.draw()
    
def drawedge(p, p2, show=False):
    if not SHOW:
        return
    xy = zip(p, p2)
    plt.plot(xy[0], xy[1], 'b')
    if show:
        plt.draw()
    
def main():    
    Ns = [(i + 1) * 100 for i in range(1, 10)]
    Ms = []
    for N in Ns:
        Ms.append(getgamma(10, N, 400))
    calclinalg(Ns, Ms, True)
    plt.draw()
    
if __name__ == '__main__':
    main() 