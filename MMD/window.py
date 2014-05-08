from collections import defaultdict

sample=list('abcbdacdabdcaab')

#exponentially decaying window
#max num is 2/c
def edw(iterable, threshold = 0.5, c=1e-9):
    dic = defaultdict(float)
    for i in iterable:
        for k in dic:
            dic[k] *= 1-c
        dic[i]+=1
        for k in dic.keys():
            if dic[k] < threshold:
                dic.pop(k)
    return sorted(dic.iteritems(), key=lambda (k, v): v, reverse=True)

print sample
print edw(sample, c = 0.3)

    

