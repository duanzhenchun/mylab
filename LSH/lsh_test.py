import numpy
import math
 
# LSH signature generation using random projection
def get_signature(user_vector, rand_proj): 
    res = 0
    for p in (rand_proj):
        res <<= 1
        if p.dot(user_vector) >= 0:
            res |= 1
    return res
 
 
# angular similarity using definitions
# http://en.wikipedia.org/wiki/Cosine_similarity
def angular_similarity(a,b):
    dot_prod = numpy.dot(a,b)
    sum_a = sum(a**2) **.5
    sum_b = sum(b**2) **.5
    cosine = dot_prod/sum_a/sum_b # cosine similarity
    theta = math.acos(cosine)
    return 1.0-(theta/math.pi)
 
if __name__ == '__main__':
    dim = 200 # number of dimensions per data
    d = 2**10 # number of bits per signature
    
    nruns = 24 # repeat times
    
    avg = 0
    for run in xrange(nruns):
        user1 = numpy.random.randn(dim)
        user2 = numpy.random.randn(dim)
        randv = numpy.random.randn(d, dim)    
        r1 = get_signature(user1, randv)
        r2 = get_signature(user2, randv)
        xor = r1^r2
        true_sim, hash_sim = (angular_similarity(user1, user2), (bin(xor).count('0'))/float(d))
        diff = abs(hash_sim-true_sim)/true_sim
        avg += diff
        print 'true %.4f, hash %.4f, diff %.4f' % (true_sim, hash_sim, diff) 
    print 'avg diff' , avg / nruns
 
"""running result:
true 0.5010, hash 0.5098, diff 0.0176
true 0.4936, hash 0.4814, diff 0.0247
...
avg diff 0.0257997833009"""
