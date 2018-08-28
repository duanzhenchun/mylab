#!/usr/bin/env python
# encoding: utf-8

max_n = 5


def build(Y):
    X = []
    for y in Y:
        insert(X, y)


def insert(X, y, i=0):
    if y < X[i]:
        X[i], t = y, X[i]
        insert(X, t)


def sort(X):
    while X:
        yield X[0]
        X[0] = X[len(X) - 1]
        X = X[:-1]
        sink(X, 0)


def sink(X, i=0):
    print 'sink', X, i
    if 2 * i + 1 >= len(X):
        return
    t = i
    if X[i] > X[2 * i + 1]:
        t = 2 * i + 1
    if 2 * i + 2 < len(X):
        if X[2 * i + 1] < X[2 * i + 2] and t > i or X[i] > X[2 * i + 2]:
            t = 2 * i + 2
    if t > i:
        X[i], X[t] = X[t], X[i]
        sink(X, t)


def test_sort():
    X = [18, 36, 27, 92, 54, 55]
    print 'X:', X
    lst = list(sort(X))
    print 'sorted:', lst
    check(lst)


def check(lst):
    for i in range(len(lst) - 1):
        assert lst[i] <= lst[i + 1], 'i: %s, a: %s, b: %s' % (i, lst[i],
                                                              lst[i + 1])


def test_random():
    import random
    X = []
    for x in random.randint(100):
        X.append(x)


if __name__ == '__main__':
    test_sort()
