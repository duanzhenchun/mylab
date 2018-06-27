#!/usr/bin/env python

import radix
from make_ipdat import gen_data


class Radixer():
    # https://github.com/mjschultz/py-radix
    def __init__(self, f_txt):
        self.rtree = radix.Radix()
        c = 0   # show progress
        for ip_start, mask_len, info in gen_data(f_txt):
            c += 1
            rnode = self.rtree.add(ip_start, mask_len)
            if not c % 1e4:
                print c
            rnode.data["info"] = info

    def lookup(self, ip_str):
        rnode = self.rtree.search_best(ip_str)
        return rnode.data['info']


def test():
    rad = Radixer('./ipdetail_s')
    print rad.lookup("1.1.2.3")


if __name__ == '__main__':
    test()
