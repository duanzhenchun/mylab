#!/usr/bin/env python
# encoding=utf8

# 对于稀疏的长整型数据的映射，如何解决Hash冲突和Hash表大小的设计是一个很头疼的问题。
# radix树就是针对稀疏的长整型数据查找，能快速且节省空间地完成映射。

import radix
from make_ipdat import gen_data


class Radixer():
    # https://github.com/mjschultz/py-radix
    def __init__(self, f_txt):
        self.rtree = radix.Radix()
        c = 0  # show progress
        for ip_start, mask_len, info in gen_data(f_txt):
            c += 1
            rnode = self.rtree.add(ip_start, mask_len)
            rnode.data["info"] = info
            # if not c % 1e5:
                # break

    def lookup(self, ip_str):
        rnode = self.rtree.search_best(ip_str)
        if rnode:
            return rnode.data['info']
        else:
            return ''


def test():
    rad = Radixer('./ipdetail_s')
    print rad.lookup("1.1.2.3")


if __name__ == '__main__':
    test()
