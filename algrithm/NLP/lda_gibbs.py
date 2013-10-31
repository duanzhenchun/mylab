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
    return np.random.multinomial(1, p).argmax()

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
        self.nmz = np.zeros((self.M, self.K))  # n( document m and topic z)
        self.nzw = np.zeros((self.K, self.V))  # n(topic z and word w)
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
                (self.nmz.sum(axis=0) + self.alpha * self.K)
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
        p_wz = self.nzw + self.beta
        p_wz /= np.sum(p_wz, axis=1)[:, np.newaxis]
        return p_wz

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

if __name__ == "__main__":
    import os
    import shutil

    N_TOPICS = 10
    AVE_DOC_LEN = 100
    DOC_NUM = 200
    FOLDER = "topicimg"
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

    def ini_phi(n_topics, doc_len):
        """
        Generate a word distribution for each of the n_topics.
        """
        width = n_topics / 2
        vocab_size = width ** 2
        phi = np.zeros((n_topics, vocab_size))

        for k in range(n_topics):
            phi[k, :] = gen_topic(width, k, doc_len)

        phi /= phi.sum(axis=1)[:, np.newaxis]  # turn counts into probabilities
        return phi

    def gen_doc(Phi, n_topics, vocab_size, doc_len, alpha=0.1):
        """
        Generate a document:
            1) Sample topic proportions from the Dirichlet distribution.
            2) Sample a topic index from the Multinomial with the topic
               proportions from 1).
            3) Sample a word from the Multinomial corresponding to the topic
               index from 2).
            4) Go to 2) if need another word.
        return :
            vector of lengh V, recording each v's count, sequence of words in doc is neglected 
        """
        theta = np.random.mtrand.dirichlet([alpha] * n_topics)
        v = np.zeros(vocab_size)
        for _ in xrange(doc_len):
            z = sample_index(theta)
            w = sample_index(Phi[z, :])
            v[w] += 1
        return v

    def gen_docs(n_topics, vocab_size, n):
        """
        Generate a document-term matrix.
        """
        phi = ini_phi(N_TOPICS, AVE_DOC_LEN)
        docs = np.zeros((n, vocab_size), dtype=int)
        doclens = np.random.poisson(AVE_DOC_LEN, n)
        for i in xrange(n):
            docs[i, :] = gen_doc(phi, n_topics, vocab_size, doclens[i])
        return docs

    if os.path.exists(FOLDER):
        shutil.rmtree(FOLDER)
    os.mkdir(FOLDER)

    width = N_TOPICS / 2
    vocab_size = width ** 2
    docs = gen_docs(N_TOPICS, vocab_size, DOC_NUM)
    lda = LDA(docs, N_TOPICS)

    for it, phi in enumerate(lda.train_gibbs()):
        print lda.loglikelihood()
        if it % 10 == 0:
            for z in range(N_TOPICS):
                save_document_image("topicimg/topic%d-%d.png" % (it, z),
                                    phi[z, :].reshape(width, -1))
