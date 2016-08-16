from collections import defaultdict
import matplotlib.pyplot as plt
import logging
import numpy as np

req_threhold = 100
BO_threhold = 10**6
Per_Reqs = "Slow Rt S4XX S499 S5XX SOther"
Hist_threshold = 0.9
Bw_threshold = 0.95
Abnormal_ratio = 2.0

Region_filters = ("Other_", "US_", "Asia", "Africa", "Vietnam", "Macao",
                  "Malaysia", "CA_", "Spain", "Australia")
values_title = "bw(Mbps), Rt/BO*1M, " + ", ".join([s1 + '/Req'
                                                   for s1 in Per_Reqs.split()])
legends = values_title.split(', ')

headers = []
iBO, inode, idomain, iregion, iregion, iDim, iReq, iRt = 0, 0, 0, 0, 0, 0, 0, 0

# nohup getDay.sh 1470488400


def rd_aggregation(timestamp_start, fnum=1440, filter_r=None, filter_d=None):
    rd_dic = defaultdict(lambda: []) # {(r,d): [vs]}
    for index in range(fnum):
        for vs in gen_file_vs(timestamp_start, index):
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

    print "len(rd_dic):", len(rd_dic)
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
        #  print legends[i], ": Hist range:", l, r
        lst[i] = filter(lambda x: l < x <= r, lst[i])
    return lst[1:]


class CDNData(object):
    def __init__(self, timestamp_start):
        self.data_dic = {}  #Dim(n/d/r): vs
        self.rdn_dic = defaultdict(
            lambda: defaultdict(lambda: list()))  # {r: {d: (bytesOut, node)}}
        for vs in gen_file_vs(timestamp_start):
            # bytesOut, node
            self.rdn_dic[vs[iregion]][vs[idomain]].append((vs[iBO], vs[inode]))
            self.data_dic[vs[iDim]] = vs[:-3]


def gen_file_vs(timestamp_start, index=0):
    with open("./data/%s/%d.csv" % (timestamp_start, index)) as f:
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
            print 'headers:', headers
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
            logging.warn("wrong data: %s", l)
            return
    return vs


# return {index:vs}
def target_data(timestamp_start, ndr_set, index):
    dic = {}
    with open("./data/%s/%d.csv" % (timestamp_start, index)) as f:
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
            # region, node
            print v[-1], v[-2]


def target_vs(ndr, vs):
    req = vs[iReq]
    bo = float(vs[iBO])
    bw = bo * 8 / 60 / 10**6
    rt = float(vs[iRt])
    try:
        return ndr, (bw, rt / bo * 10**6) + tuple([float(vs[headers.index(
            s)]) / req for s in (Per_Reqs.split())])
    except Exception, e:
        logging.warn('ndr: %s, vs: %s, e:%s' % (ndr, vs, e))
        return None, None


class Leaders(object):
    def __init__(self, rdn_dic, data_dic):
        self.rd_vs = {}  #{(r,d):(ndr, vs)}, bw leader by (r,d)
        self.r_vs = {}  #{r:(ndr,vs)}
        self.dr_vs = defaultdict( lambda: defaultdict(lambda: set()))  #{d:r:max(ndr,vs)}
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
        print len(self.dr_vs), len(self.dr_vs[domain])
        print self.dr_vs[domain]
        dic = {}
        for r, (ndr, vs) in self.dr_vs[domain].iteritems():
            dic[ndr] = vs
        return dic

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
                print ndr, vs


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
        print legends1[i], ": Hist range:", l, r
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
            print legends[i], ": Hist range:", l, r
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
            #  print "len: %d, accum threshold: %s, v: %s" % (len(am), i, am[i])
            break
    return min(i + 1, len(am))


def get_target_timeseries(timestamp_start, ndrs_set):
    dic = {}
    for i in range(1400):
        dic.update(target_data(timestamp_start, ndrs_set, i))
    lst = get_targets(dic)
    show_targets(lst, "leaders with index")


def test_major(cdndata,
               domain=None,
               get_region=False,
               get_node=False,
               show=True):
    leaders = Leaders(cdndata.rdn_dic, cdndata.data_dic)
    if domain:
        dic = leaders.get_bydomain(domain)
    elif get_node:
        dic = leaders.get_node()
    elif get_region:
        dic = leaders.get_region()
    else:
        return

    lst = get_targets(dic)
    thresholds = show_targets(lst, 'order by bw', show=show)
    print "thresholds:", thresholds
    print "abnormal record below:"
    for ndr in dic:
        _, vs = target_vs(ndr, cdndata.data_dic[ndr])
        if not vs:
            continue
        for i in range(len(thresholds)):
            if vs[i + 1] / thresholds[i] > Abnormal_ratio:
                print("ndr, vs: %s, %s" % (ndr, vs))


def leader_timeseries(timestamp_start, cdndata):
    leaders = Leaders(cdndata.rdn_dic, cdndata.data_dic)
    ndrs_set = set([v[0] for v in leaders.r_vs.values()])
    get_target_timeseries(timestamp_start, ndrs_set)


def count_ndr(timestamp_start, index):
    global headers, iDim
    dims = set()
    sum_less60BO, sumBO, = 0,0
    s60=set()
    with open("./data/%s/%d.csv" % (timestamp_start, index)) as f:
        for l in f:
            vs = process_line(l)
            if not vs:
                continue
            if int(vs[iReq]) < 60:
                newDim='//%s' %vs[iDim].split('/')[-1]
                s60.add(newDim)
                sum_less60BO += vs[iBO]
            else:
                dims.add(vs[iDim])
            sumBO += vs[iBO]
    dims.update(s60)
    print 'len(s60):', len(s60), 'all:', len(dims), 'sum_less60BO:', sum_less60BO, 'sumBO:', sumBO, 'BO%:', float(sum_less60BO)/sumBO
    return dims


def test_ndrs(timestamp_start):
    dims_all = set()
    for i in range(1440):
        dims = count_ndr(timestamp_start, i)
        dims_all = dims_all.union(dims)
        print 'file index: %d, len(dims): %d, len(dims_all): %d' % (
            i, len(dims), len(dims_all))

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

def show_abnormal(timestamp_start, fnum=10, filter_r=None, filter_d=None):
    thresholds = [657, 0.127, 108, 0.1, 0.1]
    for index in range(fnum):
        for vs in gen_file_vs(timestamp_start, index):
            ndr = vs[iDim]
            if filter_r and ndr.split('/')[2] != filter_r:
                continue
            if filter_d and ndr.split('/')[1] != filter_d:
                continue
            ndr, targets = target_vs(ndr, vs)
            if targets[2] > thresholds[1] * 2: # Slow rate
                    print ndr, targets
            #  for i in range(len(thresholds)):
                #  if targets[i+1] > thresholds[i]:
                    #  print ndr, targets
                    #  break


if __name__ == "__main__":
    timestamp_start = 1470488400
    #  rd_aggregation(
        #  timestamp_start,10,
        #  filter_r='ShanDong_CNC',
        #  filter_d="js.a.yximgs.com",
    #  )
    #  show_abnormal(timestamp_start, 10,
        #  filter_r='ShanDong_CNC',
        #  filter_d="js.a.yximgs.com",
            #  )
    #  test_ndrs(timestamp_start)
    cdndata = CDNData(timestamp_start)
    # test_major(cdndata, get_region=True)
    test_major(cdndata, domain="js.a.yximgs.com", show=True)
    #  target_node = 'cdntjun01'
    #  get_target_timeseries(timestamp_start, 'cdnlinyun01/js.a.yximgs.com/ShanDong_CNC')
    #leader_timeseries(timestamp_start, cdndata)
    #  get_CMCC_region_node()
