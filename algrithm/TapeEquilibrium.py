#https://codility.com/demo/results/demoJ3K66Y-3HU/
"""
def solution(A):
    if not A:
        return 0
    elif len(A)==1:
        res=A[0]
    else:
        l,r = 0, len(A)-1
        res, M, N = 0,A[l],A[r]
        while l<r:
            res=M-N
            if res<=0:
                l+=1; M+=A[l]
            if res>=0:
                r-=1; N+=A[r]
    return (res>0) and res or -res
"""

def solution2(A):
    l,r = A[0], sum(A[1:])
    target=abs(l-r)
    for i in range(1,len(A)-1):
        l+=A[i]
        r-=A[i]
        target = min(target, abs(l-r))
    return target


for A in ([3,1,2,4,3], 
        [1,4],
        [6,-3],
        [-3,2, 4, -1],
        [1,3,4,5,6],
        [-1,-2,-3]):
    print solution2(A), A

