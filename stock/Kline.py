# coding:utf8
from pylab import *
from matplotlib.dates import DateFormatter, WeekdayLocator, HourLocator, \
DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo, candlestick,\
plot_day_summary, candlestick2
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc",size=18)
# 定义起始、终止日期和股票代码
date1 = ( 2012, 12, 25 )
date2 = ( 2013, 6, 1 )
stock_num = '000001.sz'
# 定义日期格式
mondays = WeekdayLocator(MONDAY)
alldays = DayLocator()
weekFormatter = DateFormatter('%b %d')
dayFormatter = DateFormatter('%d')
# 获取股票数据
quotes = quotes_historical_yahoo(stock_num, date1, date2)
if len(quotes) == 0:
    raise SystemExit
# 绘制蜡烛线或美国线
fig = figure()
fig.subplots_adjust(bottom=0.2)
ax = fig.add_subplot(111)
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(alldays)
ax.xaxis.set_major_formatter(weekFormatter)
#注释掉下面的其中一行，可以得到蜡烛线或美国线
candlestick(ax, quotes, width=0.6)
#plot_day_summary(ax, quotes, ticksize=3)
ax.xaxis_date()
ax.autoscale_view()
setp( gca().get_xticklabels(), rotation=45, horizontalalignment='right')
title(u'平安银行 2012,12,25-2013,6,1',fontproperties=font)
show()
