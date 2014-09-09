import heapq


class TopN(object):
    """
    v format: (num, value)
    
    after looking into http://hg.python.org/cpython/file/2.7/Lib/heapq.py, 
    i find heappushpop already optimize, no need bottom value
    
    feed() can be optimize further, if needed:
        using func object instead of compare len(self.h) each time
    """
    def __init__(self, N):
        self.N = N
        self.h = []        
    
    def feed(self, v):  
        if len(self.h) < self.N:
            heapq.heappush(self.h, v)
        else:
            heapq.heappushpop(self.h, v)
            
    def result(self):
        self.h.sort(reverse=True)
        return self.h

def t_topn():
    topn = TopN(10)
    for i in xrange(5):
        topn.feed((i, str(i)))
    res = topn.result()    
    assert sorted(res, reverse=True) == res 
    
def t_topn_random():
    import random
    topn = TopN(10)
    for i in xrange(100):
        x = random.randint(0, 1e4)
        topn.feed((x, str(x)))
    res = topn.result()    
    assert sorted(res, reverse=True) == res 
        
if __name__ == '__main__':
    t_topn()
    t_topn_random()
