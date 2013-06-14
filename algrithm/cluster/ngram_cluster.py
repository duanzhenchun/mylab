import re
import random
import cPickle as pickle
from itertools import permutations
from sys import stdout
from os import path
from operator import itemgetter
from numpy import zeros
from scipy.io import savemat, loadmat

from munkres import Munkres
# from mltk.cluster.kmedoids import kmedoids
from scipy.cluster.vq import kmeans


class Profile(object):
    def __init__(self, path, N=3, psize=400):
        self.N = N
        self.psize = psize
        self.build_profile(path)

    sep = re.compile(r'\W+')
    def build_profile(self, path):
        grams = {}
        with open(path) as inf:
            for line in inf:
                for tok in self.sep.split(line):
                    for n in range(self.N):
                        self.feed_ngram(grams, tok, n + 1)
        self.create_profile(grams.items())

    def create_profile(self, grams):
        # keep only the top most psize items
        grams.sort(key=itemgetter(1), reverse=True)
        grams = grams[:self.psize]

        self.profile = dict()
        for i in range(len(grams)):
            self.profile[grams[i][0]] = i

    def __getitem__(self, key):
        idx = self.profile.get(key)
        if idx is None:
            return len(self.profile)
        return idx

    def dissimilarity(self, o):
        dis = 0
        for tok in self.profile.keys():
            dis += abs(self[tok] - o[tok])
        for tok in o.profile.keys():
            dis += abs(self[tok] - o[tok])
        return dis

    def feed_ngram(self, grams, tok, n):
        if n != 0:
            tok = '_' + tok
        tok = tok + '_' * (n - 1)
        for i in range(len(tok) - n + 1):
            gram = tok[i:i + n]
            grams.setdefault(gram, 0)
            grams[gram] += 1

def prepare_data(idx_file, cache_file):
    if path.exists(cache_file):
        print 'Loading cached profiles...'
        with open(cache_file, 'rb') as inf:
            profiles = pickle.load(inf)
        print 'Done.'
    else:
        profiles = []
        print 'Build profiles...'
        count = 0
        with open(idx_file) as inf:
            for line in inf:
                count += 1
                profiles.append(Profile(line.strip()))

                stdout.write('.'); stdout.flush()
                if count % 50 == 0:
                    print '(%d)' % count
        print "\nSaving profiles to cache..."
        with open(cache_file, 'wb') as outf:
            pickle.dump(profiles, outf)
        print 'Done.'
    return profiles

def make_distmat(profiles_gen, cache_file):
    if path.exists(cache_file):
        print 'Loading cached distmat...'
        distmat = loadmat(cache_file, appendmat=False)['distmat']
        print 'Done.'
    else:
        profiles = profiles_gen()
        N = len(profiles)
        distmat = zeros((N, N))
        print 'Calculating distances...'
        for i in range(N):
            for j in range(i + 1, N):
                dist = profiles[i].dissimilarity(profiles[j])
                distmat[i, j] = distmat[j, i] = dist
            print '%.2f%% done...' % ((i + 1) * 100 / float(N))
        print 'Saving distmat to cache...'
        savemat(cache_file, {'distmat': distmat}, appendmat=False)
        print 'Done.'
    return distmat

def eval_result(labels, result_gen, cache_file):
    if path.exists(cache_file):
        print 'Loading cached result...'
        with open(cache_file, 'rb') as inf:
            lbl_clst = pickle.load(inf)
        print 'Done.'
    else:
        lbl_clst = result_gen()
        print 'Saving result to cache...'
        with open(cache_file, 'wb') as outf:
            pickle.dump(lbl_clst, outf)
        print 'Done.'
    all_langs = ['da', 'de', 'el', 'en', 'es', 'fi', 'fr', 'it', 'nl', 'pt', 'sv']

    print 'Constructing cost matrix...'
    nObj = len(labels)
    nLang = len(all_langs)
    G = [[0 for j in range(nLang)] for i in range(nLang)]
    for i in range(nLang):
        for j in range(nLang):
            G[i][j] = -sum([(lbl_clst[k] == i and \
                                 labels[k] == all_langs[j]) \
                                for k in range(nObj)])
    print 'Finding best mapping...'
    m = Munkres()
    idx = m.compute(G)
    print 'Calculating accuracy...'
    total = 0
    for row, col in idx:
        total += G[row][col]
    accuracy = -total / float(nObj)
    print 'Accuracy = %.4f' % accuracy

def extract_labels(idx_file):
    labels = []
    pat_label = re.compile(r'/txt/([^/]+)/')
    with open(idx_file) as inf:
        for line in inf:
            labels.append(pat_label.search(line).group(1))
    return labels

def make_sample_idx(N, nsmp=1100, cache_file='sample_idx.pkl', use_all=False):
    if use_all:
        return range(N)
    if path.exists(cache_file):
        with open(cache_file, 'rb') as inf:
            idx = pickle.load(inf)
            if len(idx) != nsmp:
                print 'cached index is not of the same length, re-generate, but not saving...'
                return random.sample(range(N), nsmp)
            else:
                return idx
    else:
        idx = random.sample(range(N), nsmp)
        with open(cache_file, 'wb') as outf:
            pickle.dump(idx, outf)
        return idx

if __name__ == '__main__':
    labels_all = extract_labels('docs.txt')
    sample_idx = make_sample_idx(len(labels_all), use_all=True)
    labels = [labels_all[i] for i in sample_idx]
    def profiles_gen():
        profiles_all = prepare_data('docs.txt', 'profiles.pkl')
        profiles = [profiles_all[i] for i in sample_idx]
        return profiles

    def result_gen():
        distmat = make_distmat(profiles_gen, 'distmat.mat')
        (medoids, lbl_clst) = kmeans(distmat, 11, verbose=True)
        return lbl_clst

    eval_result(labels, result_gen, 'result.pkl')

