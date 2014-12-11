import random


def gen_rand(n=20):
    return [random.randint(0,2*n) for i in range(n)]


def swap(lst, i,j):
    lst[i],lst[j] = lst[j],lst[i]


def qsort(lst, l, r):
    if l>=r:
        return
    X=lst[l]
    i,j = l,r
    while i<j:
        while i<j and lst[j]>=X:
            j-=1
        if i<j:
            lst[i]=lst[j]
            i+=1
        while i<j and lst[i]<=X:
            i+=1
        if i<j:
            lst[j]=lst[i]
            j-=1
    lst[i]=X
    qsort(lst, l, i-1)
    qsort(lst, i+1, r)
""" 
    i, pivot = l+1, r
    while i<pivot:
        if lst[i]<=lst[l]:
            i+=1
        else:
            swap(lst,i,pivot)
            pivot-=1
    if lst[l]>lst[i]:
        swap(lst,i,l)
        qsort(lst, l, i-1)
        qsort(lst, i+1,r)
    else:
        qsort(lst, l, i-1)
        qsort(lst, i,r)
"""


def confirm(lst):
    if not lst:
        return
    i=lst[0]
    for j in lst[1:]:
        assert i<=j
        i=j


def test():
    for lst in [[], [3], [5,4], [3,9,6]] +\
            [gen_rand() for i in range(50)]:
        qsort(lst, 0, len(lst)-1)
        confirm(lst)
        print lst

test()
