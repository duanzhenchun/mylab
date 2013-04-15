#encoding:utf-8
import sys
sys.path.append('../')
import re
import os
from tools import *


Sorted_en = 'sorted_en'
Sorted_cs = 'sorted_cs'
Sif_dir = '/home/whille/Doc/novel/ice.fire/'
Titles = 'titles'
Plus_bak = 'plus.bak'


def gen(fname):
    f = open(fname, 'r')
    for line in f.readlines():
        if len(line) < 2:continue
        ch, en = map(str.strip, line.strip('\n').replace('：', ':').split(':'))
        if len(ch) < 1 or len(en) < 1: continue
        yield(ch, en)


def modify(fname, fpattern='*.txt'):
    for cs, en in gen(fname):
        os.system('sed -i "s/%s/%s/g" `ls %s`' % (cs, en, Sif_dir + '*.txt'))


def first_cs(u_line):
    for i in xrange(len(u_line)):
        if is_cs(u_line[i]):
            return i
    else:
        return - 1


def remove_title(titles, ens, css):
    if titles.has_key(ens[0]):
       if not css[-1].endswith(titles[ens[0]].decode('utf-8', 'ignore')):
           raise
       ens, css = ens[1:], css[:-1]
    return ens, css


def split_encs(line):
    u_line = line.decode('utf-8', 'ignore')
    p = first_cs(u_line)
    if p < 1: return None
    en, cs = u_line[:p], u_line[p:]
    ens = en.split()
    for i in (u'·', u'．', u' '):
        if i in cs:
            css = cs.split(i)
            break
    else:
        css = cs.split()
    titles = dict(gen(Titles))
    ens, css = remove_title(titles, ens, css)
    return dict(zip(ens, css))


def update_dic(plus=Plus_bak):
    out = Sorted_en
    dic = dict(gen(out))
    dic2 = dict((v, k) for k, v in gen(plus))
    dic.update(dic2)
    for v in dic.itervalues():
        for w in v.decode('utf-8', 'ignore'):
            if not is_cs(w):
                print v; break
    save_wdic(dic, out, overide=True)
    sortby_cs()


def sortby_cs(repair=False):
    r_dic = dict((v, k) for k, v in gen(Sorted_en))
    save_wdic(r_dic, Sorted_cs, iter_fn=sortk_iter_bylen, overide=True)
    if repair:
        repair_subname(r_dic)


def sortby_en(repair=False):
    r_dic = dict((v, k) for k, v in gen(Sorted_cs))
    save_wdic(r_dic, Sorted_en, overide=True)
    if repair:
        repair_subname(r_dic)

def repair_subname(dic):
    for w in dic.iterkeys():
        for w2 in dic.iterkeys():
            if w != w2 and w.find(w2) >= 0:
                print w2, w, w.replace(w2, dic[w2])
                os.system('sed -i "s/%s/%s/g" `ls %s`' % (w.replace(w2, dic[w2]), dic[w], Sif_dir + '*.txt'))


def repairline(fname):
    """repaire broken line"""
    txt = to_unicode(open(fname, 'r').read())
    pattern, repl = '(' + not_end + u')\r\n' + u_space + '(' + not_end + ')', r'\1\2'
    txt = re.sub(pattern, repl, txt)   # all are replaced
    wfile = open(fname, 'w')
    wfile.write(txt.encode('utf-8'))
    wfile.close()


def repair_fs():
    for i in xrange(1, 5):
        repairline(Sif_dir + 'sif%d.txt' % i)

notnames = [i.decode('utf8', 'ignore') for i in(
    '大', '小', '少', '老', '好', '野',
    '位', '的', '得', '下', '过', '和', '在', '为', '个', '从', '跟', '前', '对', '着', '住', '了', '向',
    '但', '而', '当', '这', '像', '有', '据', '把', '被',
    '都', '还', '只',
    '名', '些', '满', '叫', '与', '唤', '给', '是', '杀', '找', '诉', '丢', '管', '去', '取', '上', '到', '起', '看', '随', '等', '想', '说', '见', '穿', '进', '遵', '找', '要',
    '我', '他', '家',
    '助理', '乌贼', '盲眼', '恐怖', '猪头', '堂堂', '洋葱', '一名', '我们', '什么', '就如', '比如', '许多', '此刻',
    '如果', '所以', '其他', '由于', '不以', '保护', '协助', '觉得', '引导', '无须', '随后', '许多', '如今', '也许', '遵照', '吩咐', '等待', '并非', '结果', '更多', '难道', '离开',
    )]


def find_name_title(dic, line):
    titles = dict(gen('titles'))
    for cs in titles.values():
        cs = cs.decode('utf-8', 'ignore')
        index = line.find(cs)
        if index > 0 and is_cs(line[index - 1]) and (line[index - 1] not in notnames) and(line[index - 2:index] not in notnames):
            incr(dic, line[index - 5:index] + cs)


def find_cs_dot(dic, line):
    index = line.find(u'・')
    if index > 0 and (is_cs(line[index - 1]) or is_cs(line[index + 1])) and (line[index - 1] not in notnames):
        incr(dic, line[index - 5:index + 5])


def check_all(fpattern, fn):
    dic = {}
    for line in iter_lines(fpattern):
        fn(dic, line)
    save_wdic(dic, fn.func_name)


def get_VIP():
    dic = dict(gen(Sorted_en))
    statdic = {}
    for k in dic:
        count = os.popen('grep -o "%s"  *.txt  |wc -l' % k).read().strip('\n')
        statdic[k] = int(count)
    save_wdic(statdic, 'names_stat', iter_fn=sortv_iter, overide=True)

