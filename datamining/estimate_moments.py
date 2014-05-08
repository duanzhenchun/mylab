from collections import defaultdict
import random

sample=list('abcbdacdabdcaab')

def Moment(lst, m=2):
    dic = defaultdict(int)
    for i in lst:
        dic[i]+=1
    return sum([(v**m) for v in dic.values()])

def AMS(lst, m=2):
    def f(m):
        dic = {1:lambda v: v, 2:(lambda v: 2*v-1), 3:(lambda v: 3*v**2-3*v+1)}
        return dic[m]
    n = len(lst)
    k = int(n**.5)
    pos = sorted(random.sample(xrange(n), k))
#    pos = [i-1 for i in [3,8,13]]
    dic=defaultdict(int)
    fm = f(m)
    for i in xrange(pos[0], n):
        x = lst[i]
        if x in dic or i in pos:
            dic[x]+=1
    return sum([n * fm(v) for v in dic.values()])/len(pos)

m=2
print Moment(sample, m)
print AMS(sample, m)


