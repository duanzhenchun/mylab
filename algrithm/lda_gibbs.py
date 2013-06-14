"""
(C) Mathieu Blondel - 2010

Implementation of the collapsed Gibbs sampler for
Latent Dirichlet Allocation, as described in

Finding scientifc topics (Griffiths and Steyvers)
"""

import numpy as np
import scipy as sp
import scipy.misc
from scipy.special import gammaln
import matplotlib.pyplot as plt

def sample_index(p):
    """
    Sample from the Multinomial distribution and return the sample index.
    """
    return np.random.multinomial(1, p).argmax()

def word_indices(doc):
    """
    generate vocabulary indices of all words in doc
    """
    for idx in doc.nonzero()[0]:
        for i in xrange(int(doc[idx])):
            yield idx

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

class LdaSampler(object):

    def __init__(self, n_topics, alpha=.1, beta=0.01):
        """
        n_topics: desired number of topics
        alpha: a scalar (FIXME: accept vector of size n_topics)
        beta: a scalar (FIME: accept vector of size vocab_size)
        """
        self.n_topics = n_topics
        self.alpha = alpha
        self.beta = beta

    def _initialize(self, docs):
        n_docs, vocab_size = docs.shape

        # number of times document m and topic z co-occur
        self.nmk = np.zeros((n_docs, self.n_topics))
        # number of times topic z and word w co-occur
        self.nkt = np.zeros((self.n_topics, vocab_size))
        self.nm = np.zeros(n_docs)
        self.nk = np.zeros(self.n_topics)
        self.topics = {}

        for m in xrange(n_docs):
            for i, w in enumerate(word_indices(docs[m, :])):
                # choose an arbitrary topic as first topic for word i
                z = np.random.randint(self.n_topics)
                self.nmk[m, z] += 1
                self.nm[m] += 1
                self.nkt[z, w] += 1
                self.nk[z] += 1
                self.topics[(m, i)] = z

    def _conditional_distribution(self, m, w):
        """
        Conditional distribution (vector of size n_topics).
        """
        vocab_size = self.nkt.shape[1]
        left = (self.nkt[:, w] + self.beta) / \
               (self.nk + self.beta * vocab_size)
        right = (self.nmk[m, :] + self.alpha) / \
                (self.nm[m] + self.alpha * self.n_topics)
        p_z = left * right
        # normalize to obtain probabilities
        p_z /= np.sum(p_z)
        return p_z

    def loglikelihood(self):
        """
        Compute the likelihood that the model generated the data.
        look into: formula 90
        """
        vocab_size = self.nkt.shape[1]
        n_docs = self.nmk.shape[0]
        lik = 0

        for z in xrange(self.n_topics):
            lik += log_multi_beta(self.nkt[z, :] + self.beta)
            lik -= log_multi_beta(self.beta, vocab_size)

        for m in xrange(n_docs):
            lik += log_multi_beta(self.nmk[m, :] + self.alpha)
            lik -= log_multi_beta(self.alpha, self.n_topics)

        return lik

    def phi(self):
        """
        Compute phi = p(w|z).
        """
        V = self.nkt.shape[1]
        num = self.nkt + self.beta
        num /= np.sum(num, axis=1)[:, np.newaxis]
        return num

    def run(self, docs, maxiter=30):
        """
        Run the Gibbs sampler.
        """
        n_docs, vocab_size = docs.shape
        self._initialize(docs)

        for it in xrange(maxiter):
            for m in xrange(n_docs):
                for i, w in enumerate(word_indices(docs[m, :])):
                    z = self.topics[(m, i)]
#                     if it == maxiter - 1 and m == 0:
#                         print z,
                    self.nmk[m, z] -= 1
                    self.nm[m] -= 1
                    self.nkt[z, w] -= 1
                    self.nk[z] -= 1

                    p_z = self._conditional_distribution(m, w)
                    z = sample_index(p_z)

                    self.nmk[m, z] += 1
                    self.nm[m] += 1
                    self.nkt[z, w] += 1
                    self.nk[z] += 1
                    self.topics[(m, i)] = z

            # FIXME: burn-in and lag!
            yield self.phi()

if __name__ == "__main__":
    import os
    import shutil

    N_TOPICS = 10
    ntopic_guess = N_TOPICS
    DOCUMENT_LENGTH = 100
    DOC_NUM = 200
    FOLDER = "topicimg"
    def vertical_topic(width, topic_index, document_length):
        """
        Generate a topic whose words form a vertical bar.
        """
        m = np.zeros((width, width))
        m[:, topic_index] = int(document_length / width)
        return m.flatten()

    def horizontal_topic(width, topic_index, document_length):
        """
        Generate a topic whose words form a horizontal bar.
        """
        m = np.zeros((width, width))
        m[topic_index, :] = int(document_length / width)
        return m.flatten()

    def save_document_image(filename, doc, zoom=2):
        """
        Save document as an image.

        doc must be a square matrix
        """
        height, width = doc.shape
        zoom = np.ones((width * zoom, width * zoom))
        # imsave scales pixels between 0 and 255 automatically
        scipy.misc.imsave(filename, np.kron(doc, zoom))

    def create_Phi(n_topics, document_length):
        """
        Generate a word distribution for each of the n_topics.
        """
        width = n_topics / 2
        vocab_size = width ** 2
        phi = np.zeros((n_topics, vocab_size))

        for k in range(width):
            phi[k, :] = vertical_topic(width, k, document_length)
        for k in range(width):
            phi[k + width, :] = horizontal_topic(width, k, document_length)

        phi /= phi.sum(axis=1)[:, np.newaxis]  # turn counts into probabilities
        return phi

    def gen_document(Phi, n_topics, vocab_size, length=DOCUMENT_LENGTH, alpha=0.1):
        """
        Generate a document:
            1) Sample topic proportions from the Dirichlet distribution.
            2) Sample a topic index from the Multinomial with the topic
               proportions from 1).
            3) Sample a word from the Multinomial corresponding to the topic
               index from 2).
            4) Go to 2) if need another word.
        """
        theta = np.random.mtrand.dirichlet([alpha] * n_topics)
        v = np.zeros(vocab_size)
#         for n in xrange(length):
        for n in np.random.poisson(length, DOC_NUM):
            z = sample_index(theta)
            w = sample_index(Phi[z, :])
            v[w] += 1
        return v

    def gen_documents(Phi, n_topics, vocab_size, n):
        """
        Generate a document-term matrix.
        """
        docs = np.zeros((n, vocab_size))
        for i in xrange(n):
            docs[i, :] = gen_document(Phi, n_topics, vocab_size)
        return docs

    if os.path.exists(FOLDER):
        shutil.rmtree(FOLDER)
    os.mkdir(FOLDER)

    width = N_TOPICS / 2
    vocab_size = width ** 2
    Phi = create_Phi(N_TOPICS, DOCUMENT_LENGTH)
    docs = gen_documents(Phi, N_TOPICS, vocab_size, DOC_NUM)
    sampler = LdaSampler(ntopic_guess, 50.0 / N_TOPICS, 1.0 / vocab_size)

    for it, phi in enumerate(sampler.run(docs)):
#        print "i: ", it, "L: ",
        print sampler.loglikelihood()
        if it % 5 == 0:
            for z in range(ntopic_guess):
                save_document_image("topicimg/topic%d-%d.png" % (it, z),
                                    phi[z, :].reshape(width, -1))
