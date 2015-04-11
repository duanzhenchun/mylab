"""
modified from
http://www.mblondel.org/journal/2010/08/21/latent-dirichlet-allocation-in-python/

another parallel LDA in C++: 
https://code.google.com/p/plda/
"""

import numpy as np
import scipy.misc
from scipy.special import gammaln


def sample_index(p):
    """
    Sample from the Multinomial distribution and return the sample index.
    """
    return np.random.multinomial(1, p).argmax() #sample once, return index


def word_indices(doc):
    for w, n in enumerate(doc):
        for _ in xrange(n):
            yield w

def log_multi_beta(alpha, K=None):
    """
    Logarithm of the multinomial beta function.
    """
    if K is None:
        # alpha is assumed to be a vector
        return np.sum(gammaln(alpha)) - gammaln(np.sum(alpha))
    else:
        # alpha is assumed to be a scalar
        return K * gammaln(alpha) - gammaln(K * alpha)


class LDA(object):
    def __init__(self, docs, topics_guess):
        self.docs = docs
        self.M, self.V = self.docs.shape
        self.K = topics_guess
        self.alpha = 1.0 / self.K
        self.beta = 1.0 / self.V
        self.nmz = np.zeros((self.M, self.K))  # num(document m and topic z)
        self.nzw = np.zeros((self.K, self.V))  # num(topic z and word w)
        self.topics = {}
        for m in xrange(self.M):
            for i, w in enumerate(word_indices(self.docs[m, :])):
                z = np.random.randint(self.K)
                self.nmz[m, z] += 1
                self.nzw[z, w] += 1
                self.topics[(m, i)] = z

    def _conditional_distribution(self, m, w):
        left = (self.nzw[:, w] + self.beta) / \
               (self.nzw.sum(axis=1) + self.beta * self.V)
        right = (self.nmz[m, :] + self.alpha) / \
                (self.nmz.sum(axis=0) + self.alpha * self.K - 1)
        p_zi = left * right
        p_zi /= np.sum(p_zi)  # normalize to obtain probabilities
        return p_zi

    def loglikelihood(self):
        """
        Compute the likelihood that the model generated the data.
        look into: formula 90
        """
        lik = 0
        for z in xrange(self.K):
            lik += log_multi_beta(self.nzw[z, :] + self.beta)
            lik -= log_multi_beta(self.beta, self.V)
        for m in xrange(self.M):
            lik += log_multi_beta(self.nmz[m, :] + self.alpha)
            lik -= log_multi_beta(self.alpha, self.K)
        return lik

    def phi(self):
        """
        P(w|z)
        """
        self.p_zw = self.nzw + self.beta
        self.p_zw /= np.sum(self.p_zw, axis=1)[:, np.newaxis]
        return self.p_zw

    def predict(self):
        """
        P(z|w), for all w in V
        """
        return self.nzw.argmax(axis=0)
    
    def train_gibbs(self, maxiter=30):
        ms = range(self.M)
        for _ in xrange(maxiter):
            np.random.shuffle(ms)  # random choice doc to improve convergence
            for m in ms:
                for i, w in enumerate(word_indices(self.docs[m, :])):
                    z = self.topics[(m, i)]
                    self.nmz[m, z] -= 1
                    self.nzw[z, w] -= 1

                    p_z = self._conditional_distribution(m, w)
                    z = sample_index(p_z)

                    self.nmz[m, z] += 1
                    self.nzw[z, w] += 1
                    self.topics[(m, i)] = z

            # FIXME: burn-in and lag!
            yield self.phi()
            

def gen_topic(width, k, doc_len):
    """
    Generate a topic whose words form a vertical/horizontal bar.
    """
    m = np.zeros((width, width))
    if k >= width:
        m[:, k - width] = int(doc_len / width)
    else:
        m[k, :] = int(doc_len / width)
    return m.flatten()

def save_document_image(filename, doc, zoom=2):
    """
    Save document as an image. Doc must be a square matrix
    """
    height, width = doc.shape
    zoom = np.ones((width * zoom, width * zoom))
    # imsave scales pixels between 0 and 255 automatically
    scipy.misc.imsave(filename, np.kron(doc, zoom))

def ini_phi(K, doc_len):
    """
    Generate a word distribution for each of the K.
    """
    width = K / 2
    V = width ** 2
    Phi = np.zeros((K, V))
    for k in range(K):
        Phi[k, :] = gen_topic(width, k, doc_len)
    Phi /= Phi.sum(axis=1)[:, np.newaxis]  # turn counts into probabilities
    return Phi

def gen_doc(Phi, K, V, doc_len):
    """
    Generate a document, statistic related with topic dstributio:
        1) Sample topic proportions from the Dirichlet distribution.
        2) Sample a topic index from the Multinomial with the topic
           proportions from 1).
        3) Sample a word from the Multinomial corresponding to the topic
           index from 2).
        4) Go to 2) if need another word.
    return v:
        vector of lengh V, recording each word's count, sequence of words in doc is neglected 
    """
    alpha = 1.0 / K
    theta = np.random.mtrand.dirichlet([alpha] * K) #topic distribution of doc_m
    v = np.zeros(V)
    for _ in xrange(doc_len):
        z = sample_index(theta)
        w = sample_index(Phi[z, :])
        v[w] += 1
    return v


def gen_docs(K, V, n):
    """
    Generate a document-term matrix.
    """
    Phi = ini_phi(N_TOPICS, AVE_DOC_LEN)
    docs = np.zeros((n, V), dtype=int)
    doclens = np.random.poisson(AVE_DOC_LEN, n)
    for i in xrange(n):
        docs[i, :] = gen_doc(Phi, K, V, doclens[i])
    return docs
    

def test_gensim(docs):
    import gensim
    from gensim import corpora, models, similarities
    import logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    corpus = gensim.matutils.Dense2Corpus(docs, False)
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    dic = corpora.Dictionary.from_corpus(corpus); 
    model = models.LsiModel(corpus_tfidf, num_topics=N_TOPICS)  # , passes=20) 
    for i in [j * 5 for j in range(5)]:
        bow2 = [(i, 20), (i + 1, 20), (i + 2, 20), (i + 3, 20), (i + 4, 20)]
        print model[bow2]
    for i in range(5):
        bow2 = [(i, 20), (i + 5, 20), (i + 10, 20), (i + 15, 20), (i + 20, 20)]
        print model[bow2]

    for doc in docs:
        doc_bow = dic.doc2bow([str(i) for i in doc])
        print sorted(model[doc_bow], key=lambda item:-item[1])[0][0],
        
    index = similarities.MatrixSimilarity(model[corpus])
    sims = index[doc_bow]
    sims = sorted(enumerate(sims), key=lambda item:-item[1])
    print sims
    corpus_mod = model[corpus_tfidf]
    for doc in corpus_mod: 
        print doc     
    

if __name__ == "__main__":
    import os
    import shutil

    N_TOPICS = 10   #assumed
    AVE_DOC_LEN = 100
    DOC_NUM = 200
    FOLDER = "topicimg"
    if os.path.exists(FOLDER):
        shutil.rmtree(FOLDER)
    os.mkdir(FOLDER)

    topic_guess = 10
    width = N_TOPICS / 2
    V = width ** 2
    docs = gen_docs(N_TOPICS, V, DOC_NUM)
    lda = LDA(docs, topic_guess)

#     test_gensim(docs)
    
    for it, phi in enumerate(lda.train_gibbs(50)):
        print 'loglikelihood:', lda.loglikelihood()
        print 'predict P(z|w):', lda.predict()
        if it % 5 == 0:
            for z in range(topic_guess):
                save_document_image("%s/topic%d-%d.png" % (FOLDER, it, z),
                                    phi[z, :].reshape(width, -1))
