#!/usr/bin/env python
# encoding: utf-8


def build(Y):
    X=[]
    for y in Y:
        insert(X, y)


def insert(X, y, i = 0):
    if y < X[i]:
        X[i], t = y, X[i]
        insert(X, t)


def sort(X):
    while X:
        print X
        yield X[0]
        X[0] = X[len(X) - 1]
        X = X[:-1]
        sink(X, 0)


def sink(X, i=0):
    if 2 * i + 1 >= len(X):
        return
    t = i
    if X[i] > X[2 * i + 1]:
        t = 2 * i + 1
    if 2 * i + 2 < len(X):
        if X[2 * i + 1] < X[2 * i + 2] and t > i or X[i] > X[ 2 * i + 2]:
            t = 2 * i + 2
    if t > i:
        X[i], X[t] = X[t], X[i]
        sink(X, t)


def test_sort():
    X= [18,36,27,92,54,55]
    print 'X:', X
    res = list(sort(X))
    print 'sorted:', res
    for i in range(len(res) - 1):
        assert res[i] <= res[i+1]

if __name__ == '__main__':
    test_sort()
