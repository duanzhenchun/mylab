#classical package problem, using dynamic programming method
import numpy as np


def solve(V,P,V_pack):
    """
    i: item index
    j: volumn, integer
    V[i]: package volumn of item i, start form 1 actually 
    P[i]: price of item i
    Q[i,j]: max package price, using first i items, and j volumn, iteger value
    E:  seleceted items
    general situation: when i=4, j=6, V[i]=3,P[i]=5, Q[i,j] can be divide to bigger value of two problem: given j=6 using first 3 items; or given j=6-3, using first 3 items and Q+5
    """
    n=len(V)
    Q=np.zeros((n,V_pack+1),int)
    for i in range(n):
        for j in range(1,V_pack+1):
            if j<V[i]:
                Q[i,j]=Q[i-1,j]
            else:
                Q[i,j]=max(Q[i-1,j-V[i]]+P[i], Q[i-1,j])

    j=V_pack
    E=np.zeros(n,int)
    for i in range(n-1,-1,-1):
        if Q[i,j]>Q[i-1,j]:
            E[i]=1
            j-=V[i]

    print "seleceted items:", E
    print "V:",V,"\nP:",P, "\nQ:\n",Q
    print "max package:", Q[-1,-1]  #last one
    assert E.dot(P)==Q[-1,-1]
    assert E.dot(V)<=V_pack
    return Q[-1,-1], E


def test():
    V_pack=10                       
    V=np.array([0,1,4,2,6,3],int)   
    P=np.array([0,4,5,3,2,6],int)   
    solve(V,P,V_pack)

    V,P=list(random_gen())
    solve(V,P,V_pack)


def random_gen():
    for i in (6, 10):
        a=np.random.randint(1,i,size=n+1)
        a[0]=0
        yield a
    

test()

