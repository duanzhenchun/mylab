#!/usr/bin/env python
# encoding: utf-8


# time: O(N)
def trans_1(lst):
    prof, start, end = 0, 0, -1
    old_start, old_end = start, end
    if len(lst) < 2:
        return prof, start, end
    for i in range(1, len(lst)):
        v = lst[i]
        if v >= lst[start]:
            if end < 0:
                end = i
            if v - lst[start] > prof:
                old_start, old_end, prof = start, i, v - lst[start]
        else:
            if i < len(lst) - 1:
                start, end = i, -1  # history profit stays unchanged, try new data
            else:
                break
    return prof, old_start, old_end


def trans_2(lst):
    prof = 0
    for i in range(2):
        #  print 'lst:', lst
        if not lst:
            return 0
        delta, start, end = trans_1(lst)
        if delta <= 0:
            return 0
        prof += delta
        for i in (end, start):
            lst.pop(i)
    return prof


def test():
    samples = [[1, 3, 4, 2, 3, 1, 5], [2, 1], [2, 3, 1], [2, 1, 3, 1, 5], [],[4,9,1,2],[1,2,7,8]]
    for lst in samples:
        print "input:", lst
        print 'trans_1: (prof,star,end) = ', trans_1(lst)
        res = trans_2(lst)
        print 'trans_2: prof:', res

test()
