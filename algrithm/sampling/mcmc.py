# # Metropolis algorithm demonstration. This program generates a number
# # of samples from the gaussian distribution, using the uniform
# # distribution to produce the underlying Markov chain.
# #
# # by Nicolau Werneck <nwerneck@gmail.com>, 2012-10-27

import sys
from pylab import *
from scipy import random, special

def pdf(x):
    return exp(-x ** 2)


if __name__ == '__main__':
    # # Number of samples to generate.
    Ttot = 10000

    # # Initial state.
    x = 0
    f_x = pdf(x)
    # # Scale parameter of uniform distribution.
    s = float(sys.argv[1])

    # # Vector to store the output.
    chain = zeros(Ttot)
    chain[0] = x

    # # Number of misses
    miss = 0
    # # Start the loop to produce each sample of the chain.
    for t in range(1, Ttot):
        y = x + s * random.uniform(-s, s)
        f_y = pdf(y)
        alpha = 1.0 if f_y > f_x else f_y / f_x
        if alpha > 1.0 or (random.uniform() < alpha):
            # # Make the transition.
            x = y
            f_x = f_y
        else:
            # # The trial was not accepted. Stay at the same state,
            # # and increment the "miss" counter.
            miss += 1
        # # Store current state.
        chain[t] = x

    mu = mean(chain)
    sig2 = var(chain)
    acorr = sum((chain[1:] - mu) * (chain[:-1] - mu)) / sig2 / Ttot

    # # K-S test
    sc = sort(chain)
    xx = mgrid[-5:5.01:0.01]
    yy = mgrid[0.0:Ttot] / (Ttot - 1)

    KS = max(abs(yy - (special.erf(sc) + 1) / 2))

    ion()
    figure(1, figsize=(5, 7))
    subplot(211)
    plot(chain)
    title('s=%.2f / miss:%d acorr:%.2f KS:%.2f' % (s, miss, acorr, KS))
    ylim(-3, 3)

    subplot(212)
    plot(xx, (special.erf(xx) + 1) / 2, 'k--')
    plot(sc, yy, 'r-')
    xlim(-3, 3)
    grid()

    suptitle('MCMC Gaussian sampling')

    savefig('s-%.2f.png' % s)
