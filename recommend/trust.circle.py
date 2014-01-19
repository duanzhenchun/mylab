import numpy as np


#input
numC=3
numU=5
#user rating to each category
C = [[1,2,3],[1,2],[2,3],[1,3],[1,3]]
#Social relationships: trust/knows/follow
S0 = [[3,5],[1,3,4],[2],[1,5],[3]]

#num of ratings that user u assigned to items in category c
N=np.zeros((numC,numU), dtype=int)
for u,cu in enumerate(C):
    for c in cu: #start from 1
        N[c-1][u] = 1

#S in each Category
Sc = np.zeros((numC,numU,numU))
S=np.zeros((numU,numU))
for u,vs in enumerate(S0):
    for v in vs:
        S[u][v-1]=1
    
for c in range(numC):
    for u in range(numU):
        if N[c][u] <= 0:
            continue
        for v in range(numU):
            if N[c][v] <=0:
                continue
            if S[u][v]<=0:
                continue
            Sc[c][u][v]=1.0

def CircleCon1():
    return normalize(Sc)

def CircleCon2():
    Ec=np.zeros_like(Sc)
    #follower distribution
    Dw=np.ones_like(N,dtype=float)*N
    for w in range(numU):
        All=N[:,w].sum()
        if All>0:
            Dw[:,w]/=All
    for c in range(numC):
        for u in range(numU):
            V=Sc[c][u]
            for i in range(numU):
                if V[i]>0:
                    Fv = S[i]
                    Ec[c][u][i] = N[c][i] * Dw[c].dot(Fv)
    return normalize(Ec)

def normalize(Sc):
    Sc_star=Sc.copy()
    for c in range(numC):
        for u in range(numU):
            All=Sc[c][u].sum()
            if All>0:
                Sc_star[c][u]/=All
    return Sc_star

def CircleCon3():
    res=np.zeros_like(Sc)
    for c in range(numC):
        for u in range(numU):
            V=Sc[c][u]
            for i in range(numU):
                if V[i]>0:
                    res[c][u][i] = 1.0 * N[c][i]/N[:,i].sum()
    return normalize(res)

if __name__=="__main__":
    print CircleCon1()
    print CircleCon2()
    print CircleCon3()
