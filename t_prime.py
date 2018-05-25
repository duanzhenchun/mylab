from utils import benchmark


@benchmark
def prime(N):
    A = [
        1,
    ] * (N + 1)
    A[:2] = 0, 0
    for i in range(2, int((N + 1)**.5)):
        if not A[i]:
            continue
        for j in range(i, N + 1):
            if i * j >= N + 1:
                break
            A[i * j] = 0
    return A


def show(A):
    for i in range(2, len(A)):
        if A[i]:
            print i,


N = 10**5
A = prime(N)
# show(A)
