# -*- coding: utf-8 -*-

import numpy as np
import statsmodels.api as sm

n = 1000000

y = np.random.rand(n)
x1 = y + np.random.rand(n)
x2 = np.random.rand(n)
x = np.column_stack((x1, x2))  # 要把所有的自变量按列排成一个矩阵x, 统计学上称为design matrix，可见这个包用的是矩阵算法来估计OLS参数
x = sm.add_constant(x, prepend=True)  # design matrix的第一列初始值是常数1
res = sm.OLS(y, x).fit()  # 拟合

print res.params  # 回归拟合参数
print res.bse  # 拟合参数的标志误差
print res.summary()  # 长的比较详细的结果表

# 如上所示，100万数据点一秒内搞定无压力，所以还是可以用的。
print res.predict((1, 2, 3))
