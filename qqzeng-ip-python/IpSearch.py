#!/usr/bin/env python
# encoding: utf-8
import mmap
import struct
import socket


def ip2long(ip):
    _ip = socket.inet_aton(ip)
    return struct.unpack("!L", _ip)[0]


def long2ip(n):
    return socket.inet_ntoa(struct.pack("!L", n))


class IpSearch:
    def __init__(self, file_name):
        self._handle = open(file_name, "rb")
        self.data = mmap.mmap(
            self._handle.fileno(), 0, access=mmap.ACCESS_READ)
        record_size = self.int_from_4byte(0)        # size <= 2**32
        self.prefArr = []
        for i in range(256):
            p = i * 8 + 4
            self.prefArr.append(
                [self.int_from_4byte(p),
                 self.int_from_4byte(p + 4)])

        self.endArr = []        # record的结束ip位置
        self.addrArr = []       # 地区流, len(info) < 2**8 = 256
        for j in range(record_size):
            p = 2052 + (j * 8)  # 4 + 256 * 8
            offset = self.int_from_3byte(4 + p)     # 可能性 <= 2 **(3*8)
            length = self.int_from_1byte(7 + p)
            self.endArr.append(self.int_from_4byte(p))
            self.addrArr.append(
                self.data[offset:offset + length].decode('utf-8'))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def close(self):
        self._handle.close()

    def lookup(self, ip):
        ipdot = ip.split('.')
        prefix = int(ipdot[0])
        if prefix < 0 or prefix > 255 or len(ipdot) != 4:
            raise ValueError("invalid ip address")
        intIP = ip2long(ip)
        low, high = self.prefArr[prefix]
        cur = low if low == high else self.binary_search(low, high, intIP)
        return self.addrArr[cur]

    def binary_search(self, low, high, k):
        M = 0
        while low <= high:
            mid = (low + high) // 2
            end_ip_num = self.endArr[mid]
            if end_ip_num >= k:
                M = mid
                if mid == 0:
                    break
                high = mid - 1
            else:
                low = mid + 1
        return M

    def int_from_4byte(self, offset):
        return struct.unpack('<L', self.data[offset:offset + 4])[0]

    def int_from_3byte(self, offset):
        return struct.unpack('<L', self.data[offset:offset + 3] + b'\x00')[0]

    def int_from_1byte(self, offset):
        return struct.unpack('B', self.data[offset:offset + 1])[0]
