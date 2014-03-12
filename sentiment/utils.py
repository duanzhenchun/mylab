# encoding:utf-8


def sortk_iter(dic):
    return sorted(dic.iteritems())


def sortk_iter_bylen(dic, decrease=True):
    return sorted(dic.iteritems(), key=lambda (k, v):(len(k), v), reverse=decrease)


def sortv_iter(dic):
    for key, value in sorted(dic.iteritems(), reverse=True, key=lambda (k, v): (v, k)):
        yield key, value

def decode_line(l):
    if not (type(l) is unicode):
        try:
            l = l.decode('utf-8')
        except:
            l = l.decode('gbk', 'ignore')
    return l
