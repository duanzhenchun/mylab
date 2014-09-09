#!/usr/bin/env python
# 
# Copyright (c) 2012-2013 Kyle Gorman <gormanky@ohsu.edu>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
# m1.py: IBM Model 1 machine translation
# 
# Trains an IBM model one translation table from bitexts. See the included
# m1.py script for an example application. A small tokenized and uppercased
# portion of the Canadian Hansards, parlimentary proceedings in French and 
# English, is included in the data/ directory. The full set of data can be 
# found at the following URL:
# 
# <http://www.isi.edu/natural-language/download/hansard/>
# 
# IBM Model 1 is described in the following paper: 
# 
# Brown, P., Della Pietra, V., Della Pietra, S., and Mercer, R. 1993. The
# mathematics of statistical machine translation: Parameter estimation. 
# Computational Linguistics 19(2): 263-312.
# 
# In the standard description of this model my "s" ("source") is called "f"
# ("French") and my "t" ("target") is called "e" ("English"). The Python
# None type is used to represent alignments to nulls (i.e., insertion or
# deletion).
# 
# You will probably want to translate your training data into all uppercase or
# all lowercase characters if you're using languages that distinguish between
# the two. 
# 
# Given a trained M1 instance `model1`, `model1[None]` returns the distribution
# over possible insertions. Given a source word `X`, its deletion
# probability is given by `model1[X][None]`. `1 - model1[None][None]` is the
# insertion probability itself. There is no unary deletion probability: all
# deletion probabilities are lexically conditioned.
# 
# To limit memory requirements of this code, sentence-pairs are not stored in 
# memory, but rather are read online. The IO penalty appears to be minimal, as
# runs of m1.py tend to sit at near 100% CPU utilization.
# 

from sys import stderr
from math import log, exp
from collections import defaultdict
from numpy import argmax


ACCEPT_RATIO = 1e4 

def bitext(source, target):
    """
    Run through the bitext files, yielding one sentence at a time.
    """
    sfile = source if hasattr(source, 'read') else open(source, 'r')
    tfile = target if hasattr(target, 'read') else open(target, 'r')
    for (s, t) in zip(sfile, tfile):
        if s.strip() and t.strip():
            yield ([None] + s.strip().decode('utf8').split(), t.strip().decode('utf8').split())
        # null on source side only


class M1(object):
    def __init__(self, source, target, t=None):
        """
        Takes two arguments, specifying the paths (or a file-like objects
        with appropriate 'read' methods) of source and target bitexts
        """
        self.source = source
        self.target = target
        self.n = 0  # number of iterations thus far
        if not t:
            self.t = defaultdict(lambda: defaultdict(float))  # p(s|t)
            self.init()
        else:
            self.t = t
        
    def init(self):
        self.efcount = defaultdict(lambda: defaultdict(int))
        # compute raw co-occurrence frequencies 
        for (es, fs) in bitext(self.source, self.target):
            for e in es: 
                for f in fs: 
                    self.efcount[e][f] += 1
                    self.t[e][f] += 1
        self._normalize()
 
    def __repr__(self):
        return 'M1({0}, {1})'.format(self.source, self.target)

    def __getitem__(self, item):
        return self.t[item]

    def _normalize(self):
        for (e, fdic) in self.t.iteritems():
            Z = sum(fdic.values())
            if Z <= 0:
                continue
            for f in fdic:
                fdic[f] = fdic[f] / Z

    def EM(self, delta_threshold):
        c_ef = defaultdict(float)
        c_f = defaultdict(float)
        # E-step
        for e, fdic in self.efcount.iteritems():
            for f in fdic:
                c = self.t[e][f] * self.efcount[e][f] 
                c_ef[(e, f)] += c 
                c_f[f] += c 
        # M-step
        accepted = 0
        for ((e, f), val) in c_ef.iteritems():
            assert f in c_f
            if delta_threshold > self.t[e][f] - val / c_f[f]:
                accepted += 1
            self.t[e][f] = val / c_f[f]
        self._normalize()
        return accepted
                
    def iterate(self, n=1, verbose=False, delta_threshold=0.001):
        for i in xrange(n):
            if verbose:
                print >> stderr, 'iteration {0}...'.format(self.n)
            accepted = self.EM(delta_threshold)
            self.n += 1
            # check
            total = sum(len(i) for i in self.t.values())
            if verbose:
                print 'accepted, total: ', accepted, total
            if (total - accepted) * ACCEPT_RATIO < total:
                break
        return self.n
    
    def decode_pair(self, e, f):
        l, m = len(e), len(f)
        for j in range(m):
            lst = [self.t[e[i]][f[j]] for i in range(l)]
            aj = argmax(lst)
            yield e[aj], f[j]

    def decode_training(self):
        """
        Generator of the optimal decodings for the training sentences
        """
        for es, fs in bitext(self.source, self.target):
            yield list(self.decode_pair(es, fs))
