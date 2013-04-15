#encoding:utf-8
import logging
import os
import re


g_char = u'[\+\-a-zA-Z0-9\u4e00-\u9fa5]'
g_div = u'[^(\+\-a-zA-Z0-9\u4e00-\u9fa5)]+'
g_noncsdiv = u'[^\u4e00-\u9fa5]+'
g_nonendiv = u'[^\w]+'
not_end = u'[a-zA-Z0-9，\u4e00-\u9fa5]'
u_space = u'[ 　]+'


def split_sens(txt):
  txt = to_unicode(txt.strip())
  lst = re.split(g_noncsdiv, txt)
  lst = filter(None, lst)
  if lst and is_cs(txt[-1]):
    return lst[:-1], lst[-1]
  else:
    return lst, u''


def is_cs(word):
    return  u'\u4e00' < word < u'\u9fa5'


def is_en(word):
    return word.isalpha()


def head_n(dic, n):
    i = 0
    for k, v in sortv_iter(dic):
        i += 1
        print k, v
        if i > n:
            return


# v: [count,start,end]
def incr(dic, w, curpos):
    if len(w) > 1 and w in dic:
        if curpos - dic[w][2] + 1 < 3 * len(w): # neglect too near, e.g.: 嘶嘶嘶嘶, 阿多阿多
            return
    dic.setdefault(w, [0, curpos, curpos, {}, {}])  # count,first,last,left_1,right_1
    dic[w][0] += 1
    dic[w][2] = curpos


def sortk_iter(dic):
    return sorted(dic.iteritems())


def sortk_iter_bylen(dic, decrease=True):
    return sorted(dic.iteritems(), key=lambda (k, v):(len(k), v), reverse=decrease)


def sortv_iter(dic):
    for key, value in sorted(dic.iteritems(), reverse=True, key=lambda (k, v): (v, k)):
        yield key, value


def save_wdic(dic, fname, iter_fn=sortk_iter, overide=False):
    if not overide:
        fname = fname + '_out'
    with open(fname, 'w') as f:
        f.write('#k:freq\n')
        for k, v in iter_fn(dic):
            out_line = "%s:%s\r\n" % (k, v)
            if type(out_line) == unicode:
                out_line = out_line.encode('utf-8')
            f.write(out_line)


def iter_block(ppath, wc_threshold, target='.txt'):
    """neglect tail < threshold"""
    blk_lst, wc = [], 0
    for fname in iter_fname(ppath, target):
        logging.info(fname)
        remain = u''
        for line in open(fname, 'r'):
            line = line.replace(' ', '').replace('　', '')
            wc += len(line)
            sens, tail = split_sens(line)
            if sens:
                sens[0] = remain + sens[0]
                blk_lst += sens
            remain = tail
            if wc >= wc_threshold:
                yield blk_lst
                blk_lst, wc = [], 0
        if remain:
            blk_lst.append(remain)


def to_unicode(s):
    if type(s) != unicode:
        s = s.decode('utf-8', 'ignore')
    return s


def rela_name(fname):
    return fname[fname.rfind(os.sep) + 1:]


#@dulp_dec
def iter_fname(ppath, target):
    if ppath.find(os.sep) < 0:
        yield ppath
        return
    for path, dirs, files in os.walk(ppath):
        for filename in files:
            fullpath = os.path.join(path, filename)
            suffix = filename[filename.rfind('.'):].lower()
            if suffix == target.lower():
                logging.info(fullpath)
                yield fullpath


def iter_fname_end(ppath, end):
    if ppath.find(os.sep) < 0:
        yield ppath
        return
    for path, dirs, files in os.walk(ppath):
        for filename in files:
            fullpath = os.path.join(path, filename)
            if filename.endswith(end):
                logging.info(fullpath)
                yield fullpath
