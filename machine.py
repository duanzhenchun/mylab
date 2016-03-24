#!/usr/bin/env python
# encoding: utf-8

# ref: http://echorand.me/site/notes/articles/python_linux/article.html#building-command-line-utilities

from __future__ import print_function
from collections import OrderedDict
from collections import namedtuple
import glob
import re
import os
import hashlib


def cpuinfo():
    ''' Return the information in /proc/cpuinfo
    as a dictionary in the following format:
    cpu_info['proc0']={...}
    cpu_info['proc1']={...}

    '''
    info = OrderedDict()
    procinfo = OrderedDict()

    nprocs = 0
    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                # end of one processor
                info['proc%s' % nprocs] = procinfo
                nprocs = nprocs + 1
                # Reset
                procinfo = OrderedDict()
            else:
                if len(line.split(':')) == 2:
                    procinfo[line.split(':')[0].strip()
                             ] = line.split(':')[1].strip()
                else:
                    procinfo[line.split(':')[0].strip()] = ''

    return info


def meminfo():
    ''' Return the information in /proc/meminfo
    as a dictionary '''
    info = OrderedDict()

    with open('/proc/meminfo') as f:
        for line in f:
            info[line.split(':')[0]] = line.split(':')[1].strip()
    return info


def netdevs():
    ''' RX and TX bytes for each of the network devices '''

    with open('/proc/net/dev') as f:
        net_dump = f.readlines()

    device_data = {}
    data = namedtuple('data', ['rx', 'tx'])
    for line in net_dump[2:]:
        line = line.split(':')
        if line[0].strip() != 'lo':
            device_data[line[0].strip()
                        ] = data(float(line[1].split()[0]) / (1024.0 * 1024.0),
                                 float(line[1].split()[8]) / (1024.0 * 1024.0))

    return device_data

# Add any other device pattern to read from
dev_pattern = ['sd.*', 'mmcblk*']


def size(device):
    nr_sectors = open(device + '/size').read().rstrip('\n')
    sect_size = open(device + '/queue/hw_sector_size').read().rstrip('\n')

    # The sect_size is in bytes, so we convert it to GiB and then send it back
    return (float(nr_sectors) * float(sect_size)) / (1024.0 * 1024.0 * 1024.0)


def ident():
    """ Return the machine information and its sha1 digest
    """
    s = ''
    info = cpuinfo()
    for processor in info.keys():
        s += info[processor]['model name']
    info = meminfo()
    s += 'Total memory: {0}'.format(info['MemTotal'])
    for device in glob.glob('/sys/block/*'):
        for pattern in dev_pattern:
            if re.compile(pattern).match(os.path.basename(device)):
                s += ('Device:: {0}, Size:: {1} GiB'.format(device,
                                                            size(device)))
    o = hashlib.sha1()
    o.update(s)
    return s, o.hexdigest()


if __name__ == '__main__':
    print(ident())
