#http://zh.wikipedia.org/wiki/%E5%AF%B9%E8%A7%92%E5%8C%96


import numpy as np
from numpy import linalg as LA


A = np.array([(1, 2, 0),
              (0, 3, 0),
              (2, -4, 2),
            ])
lams, vs = LA.eig(A)
assert np.allclose(np.diag(lams),
                   np.dot(np.dot(LA.inv(vs), A), vs)
                   )
