import numpy as np
from numpy import linalg as LA


A = np.random.rand(4, 4)
lams, vs = LA.eig(A)
for i in range(4):
    assert np.allclose(np.dot(A, vs[:, i]),
                       np.dot(lams[i], vs[:, i]))
