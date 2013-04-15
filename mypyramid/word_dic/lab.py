#encoding:utf-8

from tools_0 import *


def geomean(lst):
    mean = 1.0
    leng = len(lst)
    for i in lst:
        mean *= i ** (1.0 / leng)
    return mean

def find_incr_iter(ppath, sub):
    before = 0
    for blk_lst in iter_block(ppath, wc_threshold=10 ** 6):   #max threshold
        print len(blk_lst)
        for sen in blk_lst:
            old = 0
            i = sen.find(sub)
            while i >= 0:
                yield before + i - old
                before, old, i = 0, i, sen.find(sub, i + 1)
            else:
                before += (len(sen) - old)

def weight_ave(v_ws):
    total, w_sum = 0, 0
    for i in v_ws:
        total += i[0] * i[1]
        w_sum += i[1]
    average = 0
    if w_sum > 0:
        average = (float)(total) / w_sum
    return average


def test_spread():
    mosts = { '的':40766, '我':19937, '是':16393, }
    rpath = '/home/whille/Doc/novel/'
    ppaths = (
    'ice.fire/', '东野圭吾/', 'kafka',
    )
    for ppath in ppaths:
        for sub, freq in mosts.iteritems():
            lst, gm_fs = [], []
            sub = sub.decode('utf8')
            for pos in find_incr_iter(rpath + ppath, sub):
               lst.append(pos)
            if lst and lst[0] == 0:
                lst.remove(0)
            gm_fs.append([geomean(lst), freq])
        w_ave = weight_ave(gm_fs)
        print ppath, w_ave

"""
ice.fire/ 41.2078729992
kafka 28.7465955189

"""

if __name__ == "__main__":
    test_spread()
