#MMD chapter 3.3.5
import numpy as np

N=5
items=range(N)
Ss=[(0,3),(2,),(1,3,4),(0,2,3)]
M=len(Ss)

#characteristic matrix
def characters():
    CHA=np.zeros((N,M),dtype=np.int8)
    for c, S in enumerate(Ss):
        for r in S:
            CHA[r,c]=1

#hash functions
hs = (lambda r: (r+1)%N, lambda r: (3*r+1)%N)

#signature
SIG=np.ones((len(hs),M))*np.inf
for c, S in enumerate(Ss):
    for r in S:
        for i, h in enumerate(hs):
            SIG[i,c]=min(SIG[i,c], h(r))           
print SIG

