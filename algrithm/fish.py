def solution(A, B):
    n=len(A)
    count = 0
    Q=[]
    for i in range(n):
        if 1 == B[i]:
            Q.append(A[i])
        else:            
            if not Q:
                count+=1
            else:
                while Q:
                    tmp=Q.pop()
                    if tmp>A[i]:
                        Q.append(tmp)
                        break
                if not Q:
                    count+=1
    return count + len(Q)

for A,B in (
        ([4,3,2,1,5],[0,1,0,0,0]),
        ([1,2],[0,1]),
        ([2,1],[1,1]),
        ([5],[1]),
        ):
    print A,B, solution(A,B)

