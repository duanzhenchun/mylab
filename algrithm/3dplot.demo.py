# -*- coding: utf-8 -*-
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def randrange(n, vmin, vmax):
    return (vmax - vmin) * np.random.rand(n) + vmin

def test():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    n = 100
    for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
        xs = randrange(n, 23, 32)
        ys = randrange(n, 0, 100)
        zs = randrange(n, zl, zh)
        ax.scatter(xs, ys, zs, c=c, marker=m)
    
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    
    plt.show()

def pltdata(fname='/home/whille/Desktop/3ddata.xlsx'):
    import xlrd
    data = xlrd.open_workbook(fname)
    startrow = 1
    sh1 = data.sheets()[0]
    head = sh1.row_values(0)
    cols = u'粉丝数', u'Health rate', u'interacticity'
    res = []
    for i in range(head.index(cols[0]), head.index(cols[-1]) + 1):
        res.append(sh1.col_values(i, start_rowx=startrow))

    res2 = zip(*res)
    ave0=map(lambda x: sum(x)*1.0/len(x), res)
    print ave0
    return
    ave=[400, 1, 2]
    cls=[[],[]]
    for i in res2:
        big=False
        for index, j in enumerate(i):
            if j> ave[index]:
                big = True
                break
        cls[big].append(i)
    print len(cls[0]), len(cls[1])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(0,max(res[0]))
    ax.set_ylim(0,max(res[1]))
    ax.set_zlim(0,max(res[2]))
    ax.set_xlabel('#fans')
    ax.set_ylabel(cols[1])
    ax.set_zlabel(cols[2])
    ax.view_init(azim=30, elev=30)
    
    for i, (c,m) in enumerate((('y','o'), ('b','o'))):
        if not cls[i]:
            continue
        ax.scatter(*zip(*cls[i]), c=c, marker=m)
    plt.show()
    
if __name__ == '__main__':
#     test()
    pltdata()