#!/usr/bin/env python
# _*_encoding:utf-8 _*_
import os
import requests
from os.path import exists
from math import log
from multiprocessing import Pool

TAOBAO_URL = "http://ip.taobao.com/service/getIpInfo.php"


#在wget下来的html中寻找出CN/ipv4的行,并yield 网段和并计算出的掩码
def net_catch():
    with open('./src.html', 'r') as f:
        for line in f.readlines():
            if line.startswith('apnic|CN|ipv4'):
                '''
                the line example:
                    apnic|IN|ipv4|103.27.84.0|1024|20130701|assigned
                '''
                net, cnt = line.strip().split('|')[3:5]
                yield net, int(32 - log(float(cnt)) / log(2))


def net_list_file():
    if exists('netlist.file'):
        os.remove('netlist.file')
    with open('netlist.file', 'w+') as f:
        for net, mask in net_catch():
            f.write('/'.join([net, str(mask)]) + '\n')
        print 'all net has been write to file'


def ip_list():
    for net, mask in net_catch():
        net = net[:-1] + str(int(net[-1]) + 1)
        yield net, mask


def ip_resolve(ip, mask):
    r = requests.get(
        '{}?ip={}'.format(TAOBAO_URL, ip), timeout=0.09)
    print r.status_code
    if r.status_code == 200:
        response_json = r.json()
        print response_json
        if response_json.get('code') == 0:
            isp_name = response_json.get('data').get('isp')
            if isp_name:
                ip.split('.')[:3].append('0')
                with open(isp_name + '.acl', 'a+') as f:
                    f.write(ip + '/' + str(mask) + '\n')
    else:
        # TODO again?
        ip_resolve(ip, mask)


def main():
    try:
        p = Pool(4)
        for ip, mask in ip_list():
            p.apply_async(ip_resolve, args=(ip, mask))
        print('Waiting for all subprocesses done...')
        p.close()
        p.join()
    except Exception as e:
        print 'Error: %s' % e

    print('All subprocesses done.')


def get_src():
    if not exists('src.html'):
        os.system(
            "wget 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest' -O src.html")


if __name__ == '__main__':
    #    os.chdir('/home/zhxfei/learning/workspace')
    get_src()
    main()
#     net_list_file()
#
