#!/usr/bin/env python
import contextlib
import codecs
import mmap
import struct
from IpSearch import ip2long

record_start = 4 + 8 * 256


def gen_data(f_txt):
    with open(f_txt, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            ip_range, info = line.split()
            ip_start, ip_len = ip_range.split('/')
            yield ip_start, 32 - int(ip_len), info


def create_dat(f_txt, f_dat):
    N = -1
    with open(f_txt, 'r') as f:
        with codecs.open(f_dat, 'wb', encoding='utf8') as fo:
            s_info = set()
            len_record = 0
            for line in f:
                _, info = line.strip().split()
                s_info.add(info)
                len_record += 1
            dic_info = {}
            pos_info = 0
            for info in s_info:
                dic_info[info] = pos_info
                pos_info += len(info)
            info_start = record_start + len_record * 8
            N = info_start + pos_info
            print "record_start: %d, info_start: %d, N: %d, len_record: %d, len(s_info): %d" % (
                record_start, info_start, N, len_record, len(s_info))
            fo.write("\0" * N)
    if N < 0:
        return
    with open(f_dat, 'r+') as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0)) as mm:
            process(mm, f_txt, dic_info, info_start, len_record)


def process(mm, f_txt, dic_info, info_start, len_record):
    dic_info_r = dict((v, k) for k, v in dic_info.iteritems())
    lst_record = [[] for i in range(256)]
    for ip_start, ip_len, info in gen_data(f_txt):
        ipdot = ip_start.split('.')
        prefix = int(ipdot[0])
        if prefix < 0 or prefix > 255 or len(ipdot) != 4:
            raise ValueError("invalid ip address")
        int_ip_start = ip2long(ip_start)
        int_ip_end = int_ip_start + ip_len
        lst_record[prefix].append((int_ip_end, dic_info[info]))
    mm[:4] = struct.pack('<L', len_record)
    left = record_start
    record_i = 0
    for prefix, arr in enumerate(lst_record):
        arr.sort()
        # write prefix dat
        loc = 4 + 8 * prefix
        mm[loc:loc + 4] = struct.pack('<L', record_i)
        mm[loc + 4:loc + 8] = struct.pack('<L', record_i + len(arr))
        record_i += len(arr)
        for j, (int_ip_end, pos_info) in enumerate(arr):
            loc = left + 8 * j
            mm[loc:loc + 4] = struct.pack('<L', int_ip_end)
            len_info = len(dic_info_r[pos_info])
            mm[loc + 4:loc + 8] = struct.pack('<L', info_start + pos_info)[:-1] + struct.pack('B', len_info)
        left += 8 * len(arr)
    for pos_info, info in dic_info_r.iteritems():
        mm[info_start + pos_info:info_start + pos_info + len(info)] = info
    mm.close()


def make_dat():
    f_txt = './ipdetail'
    f_dat = './ip-3.0.dat'
    create_dat(f_txt, f_dat)


if __name__ == "__main__":
    make_dat()
