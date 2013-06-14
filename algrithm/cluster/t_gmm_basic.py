import numpy as np
from sklearn import mixture

np.random.seed(1)
# mix 2 Gaussian distribution data
obs = np.concatenate((np.random.randn(100, 1), 10 + np.random.randn(300, 1)))

g = mixture.GMM(n_components=2)
g.fit(obs)
print np.round(g.weights_, 2)
print np.round(g.covars_, 2)
print g.predict([[0], [2], [9], [10]])
print np.round(g.score([[0], [2], [9], [10]]), 2)

# Refit the model on new data (initial parameters remain the
# same), this time with an even split between the two modes.
g.fit(20 * [[0]] + 20 * [[10]])
print np.round(g.weights_, 2)
