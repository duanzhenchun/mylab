from utils import *
import cPickle as pickle
from matplotlib import pyplot as plt


url0 = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=NS&sty=NSS&st=12&sr=true&ps=50'
pages=25
rows='id,?,?,股票简称,股票代码,申购代码,发行总数,网上发行总数,申购上限,申购资金上限,发行价格,申购日期,中签号公布日,上市日期,发行市盈率,中签率(%),冻结资金(元),询价累计报价倍数,每中一签(元),板块,一签股数,初步询价累计报价股数,网上有效申购股数,最新价,首日收盘价,打新收益(%),详情webpage,主营业务,?,?,?,?,?,?'
data_pkl = './new_shares.pkl'

"""
询价累计报价倍数 = 初步询价阶段累计报价股数 / 初步询价阶段网下配售股数
打新收益率 = 中一签的股数*(该新股上市首日均价-发行价) / 每中一签需要的资金
"""

rows=rows.split(',')
nrow=len(rows)

def crawl():
    shares=[]
    for i in range(pages):
        url=url0+'&p=%d' %(i+1)
        txt=getpage(url)
        data = ast.literal_eval(txt)
        assert data
        for d in data:
            share = d.split(',')
            assert len(share) == nrow
            shares.append(share)

    print len(shares)
    pickle.dump(shares, open(data_pkl, 'w'))


def load():
    return pickle.load(open(data_pkl))

def win_stat():
    aims = ('发行价格', '首日收盘价', '最新价')
    infos = ('股票简称','上市日期')
    indexes = [rows.index(i) for i in aims]
    iinfo = [rows.index(i) for i in infos]
    shares=load()

    nwins=[0,0]
    ratios=[]
    print ':'.join(infos + aims)
    for share in shares:
        try:
            vs = [float(share[i]) for i in indexes]
        except:
            continue
        ratios.append(vs[1]/vs[0])
        nwins[vs[0]<vs[1]] += 1
        if vs[0]>vs[1]:
            print ':'.join([share[i] for i in iinfo]), vs
    print nwins

    plt.scatter(range(len(ratios)), ratios)
    plt.show()
