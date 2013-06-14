from decimal import Decimal
import time

zero, one = 0.0, 1.0
# zero, one = Decimal(0), Decimal(1)

def norm_dict(dic):
    total = one * sum(dic.values())
    if total <= 0:
        return
    for i in dic:
        dic[i] /= total
            
def norm_dict2(dic):
    """
    normalize dict[i][j]
    """
    total = zero
    for i in dic:
        total += sum(dic[i].values())
    if total <= 0:
        return
    for i in dic:
        for j in dic[i]:
            dic[i][j] /= total
            
def benchmark(f):
    def wrapper(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print '%s %f %s' % (f.__name__, time.time() - t, 'sec')
        return res
    return wrapper
