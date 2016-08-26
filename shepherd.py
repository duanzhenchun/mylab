import os
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

req_threhold = 100
BO_threhold = 10**9
Per_Reqs = "Slow Rt S4XX S499 S5XX SOther"
iSlow = 2
i4XX = 4
Hist_threshold = 0.9
Bw_threshold = 0.95
Abnormal_ratio = 2.0

Curpath = os.path.dirname(os.path.abspath(__file__))

import logging
import logging.config
logging.config.fileConfig("%s/shepherd.conf" % Curpath)
# create logger
logger_root = logging.getLogger('root')  #qualname
logger_neg = logging.getLogger('negativeData')
logger_guard = logging.getLogger('guard')
logger_quality = logging.getLogger('quality')

Region_filters = ("Other_", "US_", "Asia", "Africa", "Vietnam", "Macao",
                  "Malaysia", "CA_", "Spain", "Australia")
values_title = "bw(Mbps), Rt/BO*1M, " + ", ".join([s1 + '/Req'
                                                   for s1 in Per_Reqs.split()])
legends = values_title.split(', ')

headers = []
iBO, inode, idomain, iregion, iregion, iDim, iReq, iRt = 0, 0, 0, 0, 0, 0, 0, 0

# nohup getDay.sh 1470488400
"""
TODO:
    dynamic load conf buy kill -HUP
    serielized data for restart
"""


def rd_aggregation(start, fnum=1440, filter_r=None, filter_d=None):
    rd_dic = defaultdict(lambda: [])  # {(r,d): [vs]}
    for index in range(fnum):
        for vs in gen_file_vs(start, index):
            ndr = vs[iDim]
            if filter_r and ndr.split('/')[2] != filter_r:
                continue
            if filter_d and ndr.split('/')[1] != filter_d:
                continue
            _, vs = target_vs(ndr, vs)
            if vs:
                d, r = ndr.split('/')[1:]
                rd_dic[(r, d)].append(vs)
    s_lst = [[] for i in range(len(legends) - 1)]

    for (r, d), vs in rd_dic.iteritems():
        lst = filter_lst(vs)
        for i in range(len(s_lst)):
            s_lst[i] += lst[i]

    thresholds = show_targets_without_bw(s_lst, "s_lst", show=True)
    return thresholds


def filter_lst(lst):
    lst1 = sorted(lst, reverse=True)
    lst = zip(*lst1)
    lst = trim_by_bw(lst)

    for i in range(len(lst)):
        res = np.histogram(lst[i])
        j = hist_threshold_index(res[0])
        l, r = res[1][0], res[1][j + 1]
        lst[i] = filter(lambda x: l < x <= r, lst[i])
    return lst[1:]


class CDNData(object):
    def __init__(self, start, index=0):
        self.data_dic = {}  #Dim(n/d/r): vs
        self.rdn_dic = defaultdict(
            lambda: defaultdict(lambda: list()))  # {r: {d: (bytesOut, node)}}
        for vs in gen_file_vs(start, index):
            # bytesOut, node
            self.rdn_dic[vs[iregion]][vs[idomain]].append((vs[iBO], vs[inode]))
            self.data_dic[vs[iDim]] = vs[:-3]


def gen_file_vs(start, index=0):
    with open("./data/%s/%d.csv" % (start, index)) as f:
        for l in f:
            vs = process_line(l)
            if not vs:
                continue
            if vs[iReq] < req_threhold:
                continue
            if vs[iBO] < BO_threhold:
                continue
            bfilter = False
            for sf in Region_filters:
                if vs[iregion].startswith(sf):
                    bfilter = True
                    break
            if bfilter:
                continue
            for v in vs[-3:]:
                if "" == v:  # empty r,d or n
                    break
            else:
                yield vs


def process_line(l):
    global iBO, inode, idomain, iregion, iregion, iDim, iReq, iRt, headers
    l = l.strip()
    # neglect name, time
    vs = l.split(',')[2:]
    if vs[0] == "Dim":
        if len(headers) < 1:  # headers not initialed
            headers = vs
            logger_root.info('headers: %s' % headers)
            iBO = headers.index('bytesOut')
            inode = headers.index('node')
            idomain = headers.index('domain')
            iregion = headers.index('region')
            iDim = headers.index('Dim')
            iReq = headers.index('Req')
            iRt = headers.index('Rt')
        return
    for i in range(1, len(vs) - 3):
        vs[i] = int(vs[i])
        if vs[i] < 0:
            logger_neg.info(l)
            return
    return vs


# return {index:vs}
def target_data(start, ndr_set, index):
    dic = {}
    with open("./data/%s/%d.csv" % (start, index)) as f:
        for l in f:
            vs = process_line(l)
            if not vs:
                continue
            if vs[iDim] not in ndr_set:
                continue
            ndr = vs[iDim]
            # bytesOut, node
            _, vs = target_vs(ndr, vs)
            if vs:
                dic["%s_%d" % (ndr, index)] = vs
    return dic


def g_leaders(cdndata):
    iBO = headers.index('bytesOut')
    iregion = headers.index('region')
    dic_r = defaultdict(lambda: defaultdict(lambda: []))
    for v in cdndata.data_dic.values():
        n = v[iregion]
        if n not in dic_r:
            dic_r[n] = v
        elif dic_r[n][iBO] < v[iBO]:
            dic_r[n] = v
    return dic_r


def get_CMCC_region_node():
    dic_r = g_leaders()
    for r, v in dic_r.iteritems():
        if r.endswith('_CMCC'):
            logger_root.debug("region: %s, node: %s" % (v[-1], v[-2]))


"""
len(rd_dic): 5693
Rt/BO*1M : Hist range: 0.0 656.927836493
Slow/Req : Hist range: 0.0 0.127
Rt/Req : Hist range: 0.0 108.309574468
S4XX/Req : Hist range: 0.0 0.1
S499/Req : Hist range: 0.0 0.0991869918699
S5XX/Req : Hist range: 0.0 0.0147058823529
SOther/Req : Hist range: 0.0 0.0993464052288
"""


def target_vs(ndr, vs):
    req = vs[iReq]
    bo = float(vs[iBO])
    bw = bo * 8 / 60 / 10**6
    rt = float(vs[iRt])
    try:
        return ndr, (bw, rt / bo * 10**6) + tuple([float(vs[headers.index(
            s)]) * 100 / req for s in (Per_Reqs.split())])
    except Exception, e:
        logger_root.warn('ndr: %s, vs: %s, e:%s' % (ndr, vs, e))
        return None, None


class Leaders(object):
    def __init__(self, rdn_dic, data_dic):
        self.rd_vs = {}  #{(r,d):(ndr, vs)}, bw leader by (r,d)
        self.r_vs = {}  #{r:(ndr,vs)}
        self.dr_vs = defaultdict(
            lambda: defaultdict(lambda: set()))  #{d:r:max(ndr,vs)}
        self.n_vs = {}  #{n:(ndr,vs)}
        for r, v in rdn_dic.iteritems():
            for d, v2 in v.iteritems():
                n = max(v2)[1]
                ndr = '/'.join((n, d, r))
                _, vs = target_vs(ndr, data_dic[ndr])
                if vs:
                    self.rd_vs[(r, d)] = (ndr, vs)
                    if not self.dr_vs[d][r] or self.dr_vs[d][r][1][0] < vs[0]:
                        self.dr_vs[d][r] = (ndr, vs)
        for (r, d), (ndr, vs) in self.rd_vs.iteritems():
            if r not in self.r_vs or self.r_vs[r][1][0] < vs[0]:
                self.r_vs[r] = (ndr, vs)
        for ndr, vs in data_dic.iteritems():
            n, d, r = ndr.split('/')
            vs = target_vs(ndr, vs)
            if n not in self.n_vs or self.n_vs[n][1][0] < vs[0]:
                self.n_vs[n] = vs

    def get_bydomain(self, domain):
        logger_root.debug("domain: %s, len: %d" %
                          (domain, len(self.dr_vs[domain])))
        dic = {}
        for r, (ndr, vs) in self.dr_vs[domain].iteritems():
            dic[ndr] = vs
        return dic

    def gen_domains(self):
        for domain in self.dr_vs:
            yield domain, self.get_bydomain(domain)

    def get_region(self):
        dic = {}
        for (ndr, vs) in self.r_vs.values():
            dic[ndr] = vs
        return dic

    def get_node(self):
        dic = {}
        for (ndr, vs) in self.n_vs.values():
            dic[ndr] = vs
        return dic

    def show_vars(self, cdndata):
        for ndr in cdndata.data_dic:
            _, d, r = ndr.split('/')
            _, vs = target_vs(ndr, cdndata.data_dic[ndr])
            if not vs:
                continue
            _, vs2 = self.rd_vs.get((r, d))
            for i, v in enumerate(vs):
                print v, ':', vs2[i], ',',
            print

    def trial(self, r0="TianJin_CNC"):
        for (r, d), (ndr, vs) in self.rd_vs.iteritems():
            if r == r0 and vs[0] > 200:
                logger_root.debug("ndr: %s, vs: %s" % (ndr, vs))


def get_targets(dic):
    lst = sorted(dic.iteritems(), reverse=True, key=lambda (k, v): v[0])
    #  bwlst = [i[0] for i in lst]
    vslst = zip(*[i[1] for i in lst])
    return trim_by_bw(vslst)


def trim_by_bw(vslst):
    thld_idx = accum_threshold(vslst[0])
    for i in range(len(vslst)):
        vslst[i] = vslst[i][:thld_idx]
    return vslst


def show_targets_without_bw(lst, xlabel, show=True):
    plt.clf()
    thresholds = []
    legends1 = legends[1:]
    for i in range(len(lst)):
        plt.subplot(len(lst), 2, 2 * i + 1)
        plt.xlabel(legends1[i])
        plt.ylabel('count')
        res = plt.hist(lst[i])
        j = hist_threshold_index(res[0])
        l, r = res[1][0], res[1][j + 1]
        logger_root.debug("%s: Hist range: %s %s" % (legends1[i], l, r))
        thresholds.append(r)
        if show:
            plt.subplot(len(lst), 2, 2 * i + 2)
            plt.xlabel(xlabel)
            plt.ylabel(legends1[i])
            plt.plot(lst[i])
            plt.legend([legends1[i]], loc='upper right')
            for v in (l, r):
                plt.plot([v] * len(lst[0]))
    if show:
        plt.show()
    return thresholds


def calc_bw_weight(lst):
    weights = []
    norm_bw = normorlize(lst[0])
    for lstk in lst[1:]:
        s = sum([norm_bw[i] * v for i, v in enumerate(lstk)])
        weights.append(s)
    return weights


def show_targets(lst, xlabel, show=True):
    weights = calc_bw_weight(lst)

    plt.clf()
    thresholds = []
    for i in range(len(lst)):
        plt.subplot(len(lst), 2, 2 * i + 1)
        #  plt.title("histograph")
        #  plt.grid(True)
        plt.xlabel(legends[i])
        plt.ylabel('count')
        res = plt.hist(lst[i])
        if i > 0:
            j = hist_threshold_index(res[0])
            l, r = res[1][0], res[1][j + 1]
            logger_root.debug("%s: Hist range: %s %s" % (legends[i], l, r))
            thresholds.append(r)
        if show:
            plt.subplot(len(lst), 2, 2 * i + 2)
            plt.xlabel(xlabel)
            plt.ylabel(legends[i])
            plt.plot(lst[i])
            plt.legend([legends[i]], loc='upper right')
            if i > 0:
                for v in (weights[i - 1], l, r):
                    plt.plot([v] * len(lst[0]))
    if show:
        plt.show()
    return thresholds


def hist_threshold_index(lst):
    accm, s = 0.0, sum(lst)
    if s == 0.0:
        return 0
    for j in range(len(lst)):
        accm += lst[j]
        if accm / s > Hist_threshold:
            break
    return j


def accum(lst):
    s = 0
    res = []
    for i in lst:
        s += i
        res.append(s)
    return res


def normorlize(lst):
    s = sum(lst)
    lst_norm = [float(i) / s for i in lst]
    return lst_norm


def accum_threshold(lst, thld=Bw_threshold):
    lst_norm = normorlize(lst)
    am = accum(lst_norm)
    i = len(am)
    for v in am[::-1]:
        i -= 1
        if v < thld:
            logger_root.debug("len: %d, accum threshold: %s, v: %s" %
                              (len(am), i, am[i]))
            break
    return min(i + 1, len(am))


def get_target_timeseries(start, ndrs_set):
    dic = {}
    for i in range(1400):
        dic.update(target_data(start, ndrs_set, i))
    lst = get_targets(dic)
    show_targets(lst, "leaders with index")


def test_major(cdndata,
               domain=None,
               get_region=False,
               get_node=False,
               all_domain=False,
               show=True):
    leaders = Leaders(cdndata.rdn_dic, cdndata.data_dic)
    dic = None
    if domain:
        dic = leaders.get_bydomain(domain)
        show_major(cdndata, dic, show, domain)
    elif all_domain:
        for domain, dic in leaders.gen_domains():
            if len(dic) < 5:
                continue
            show_major(cdndata, dic, show, domain)
    elif get_node:
        dic = leaders.get_node()
        show_major(cdndata, dic, show)
    elif get_region:
        dic = leaders.get_region()
        show_major(cdndata, dic, show)
    else:
        return


def show_major(cdndata, dic, show, title=None):
    lst = get_targets(dic)
    thresholds = show_targets(lst, title and title or 'order by bw', show=show)
    logger_root.debug("thresholds: %s" % thresholds)
    for ndr in dic:
        _, vs = target_vs(ndr, cdndata.data_dic[ndr])
        if not vs:
            continue


def leader_timeseries(start, cdndata):
    leaders = Leaders(cdndata.rdn_dic, cdndata.data_dic)
    ndrs_set = set([v[0] for v in leaders.r_vs.values()])
    get_target_timeseries(start, ndrs_set)


def count_ndr(start, index):
    global headers, iDim
    dims = set()
    sum_less60BO, sumBO, = 0, 0
    s60 = set()
    with open("./data/%s/%d.csv" % (start, index)) as f:
        for l in f:
            vs = process_line(l)
            if not vs:
                continue
            if int(vs[iReq]) < 60:
                newDim = vs[iDim].rsplit('/',1)[0]+'/-' # replace r with -
                s60.add(newDim)
                sum_less60BO += vs[iBO]
            else:
                dims.add(vs[iDim])
            sumBO += vs[iBO]
    dims.update(s60)
    logger_root.warn(
        'len(s60): %d, all: %d, sum_less60BO: %s, sumBO: %s, BO(%%): %.1f%%' %
        (len(s60), len(dims), sum_less60BO, sumBO, 100 * float(sum_less60BO) / sumBO))
    return dims


def test_ndrs(start):
    dims_all = set()
    for i in range(1440):
        dims = count_ndr(start, i)
        dims_all = dims_all.union(dims)
        logger_root.info('file index: %d, len(dims): %d, len(dims_all): %d' %
                         (i, len(dims), len(dims_all)))


def show_abnormal(start, fnum=10, filter_r=None, filter_d=None):
    thresholds = [657, 0.127, 108, 0.1, 0.1]
    for index in range(fnum):
        for vs in gen_file_vs(start, index):
            ndr = vs[iDim]
            if filter_r and ndr.split('/')[2] != filter_r:
                continue
            if filter_d and ndr.split('/')[1] != filter_d:
                continue
            ndr, targets = target_vs(ndr, vs)
            for i in range(len(thresholds)):
                if targets[i + 1] > thresholds[i]:
                    logger_root.debug("ndr: %s, targets: %s" % (ndr, targets))
                    break


#  alert aims: to ignore const abnormal, single peak
#  |||        |         ||
#  |||        |         ||
#  |||        |         ||
#  |||       |||       ||||
#  |||       |||       ||||
#  once     ignore    once & recover
class Guard(object):
    Empty = -1
    period_num = 60
    weights = {iSlow: 0.9, i4XX: 0.1}  # arbitary

    def __init__(self):
        self.dic = {}  # {ndr: (v,alerted)}
        self.cache = defaultdict(lambda: [])  #{d: []}

    def get_cache(self, domain):
        if domain not in self.cache:
            return None
        res = [[] for i in range(len(self.cache[domain][0]))]
        for lst in self.cache[domain]:
            for i in range(len(lst)):
                res[i] += lst[i]
        return res

    def caching(self, domain, lst):
        if len(self.cache[domain]) >= self.period_num:
            self.cache[domain].pop(0)
        self.cache[domain].append(lst)

    def is_abnormal(self, domain, v, threshold):
        return v / max(1e-6, threshold) > Abnormal_ratio

    def evaluate(self, vs, level_edges):
        s = 0.0
        for aim, w in self.weights.iteritems():
            s += float(vs[aim] * 10) / level_edges[aim] * w
        return s

    def check(self, ndr, vs, thresholds, ts):
        # begin with Slow/Req, then S4XX,...
        v, threshold = vs[iSlow], thresholds[iSlow]

        v_old, alerted_old = self.dic.get(ndr, (self.Empty, False))
        d = ndr.split('/')[1]
        if v_old == self.Empty:
            alerted = self.is_abnormal(d, v, threshold)
            if alerted:
                self.alert(ts, ndr, v, d, threshold, initial=True)
                self.dic[ndr] = (v, True)
        else:
            v = min(v, v_old)
            alerted = self.is_abnormal(d, v, threshold)
            if not alerted:
                if alerted_old == True:
                    self.recover(ts, ndr, v, d, threshold)
            else:
                if alerted_old == False:
                    self.alert(ts, ndr, v, d, threshold)
            self.dic[ndr] = (v, alerted)
        if alerted:
            return ndr

    def alert(self, ts, ndr, v, domain, threshold, initial=False):
        logger_guard.info(
            "Abnormal, ts: %s, ndr: %s, v: %s, threshold: %s%s" %
            (ts, ndr, v, threshold, initial and ', ____1st____' or ''))

    def recover(self, ts, ndr, v, domain, threshold):
        logger_guard.info("Recover, ts: %s, ndr: %s, v: %s threshold: %s" %
                          (ts, ndr, v, threshold))


g_guard = Guard()


def play_back(start, fnum=1440):
    for index in range(fnum):
        ts = start + 60 * index
        logger_root.info('timestamp: %s, index: %s' % (ts, index))
        cdndata = CDNData(start, index)
        leaders = Leaders(cdndata.rdn_dic, cdndata.data_dic)
        qualities = defaultdict(lambda: defaultdict(lambda: defaultdict(int))
                                )  #{r:{d: {n: level}}}
        for domain, dic in leaders.gen_domains():
            cache_lst = g_guard.get_cache(domain)
            if not cache_lst:
                cache_lst = get_targets(dic)
            thresholds, level_edges = [], []
            for i in range(len(cache_lst)):
                res = np.histogram(cache_lst[i])
                j = hist_threshold_index(res[0])
                r = res[1][j + 1]
                logger_root.debug('domain: %s,  j: %s, r: %s' % (domain, j, r))
                thresholds.append(r)
                level_edges.append(res[1][-1])
            for ndr in dic.keys():
                _, vs = target_vs(ndr, cdndata.data_dic[ndr])
                if not vs:
                    continue
                alert_ndr = g_guard.check(ndr, vs, thresholds, ts)
                if alert_ndr in dic:
                    del dic[alert_ndr]
                else:
                    n, d, r = ndr.split('/')
                    qualities[r][d][n] = g_guard.evaluate(vs, level_edges)
            if dic:  # not del to empty
                g_guard.caching(domain, get_targets(dic))
        r = "GuangDong_CT"
        for d, v in qualities[r].iteritems():
            for n, level in v.iteritems():
                logger_quality.info("rdn: %s/%s/%s, level: %d" %
                                    (r, d, n, level))


if __name__ == "__main__":
    start = 1470488400
    test_ndrs(start)
    #  play_back(start, 4319)
    #  rd_aggregation(
    #  start,10,
    #  filter_r='ShanDong_CNC',
    #  filter_d="js.a.yximgs.com",
    #  )
    #  show_abnormal(start, 10,
    #  filter_r='ShanDong_CNC',
    #  filter_d="js.a.yximgs.com",
    #  )
    #  cdndata = CDNData(start)
    # test_major(cdndata, get_region=True)
    #  test_major(cdndata, domain="js.a.yximgs.com", show=True)
    #  test_major(cdndata, all_domain=True, show=False)
    #  target_node = 'cdntjun01'
    #  get_target_timeseries(start, 'cdnlinyun01/js.a.yximgs.com/ShanDong_CNC')
    #leader_timeseries(start, cdndata)
    #  get_CMCC_region_node()
