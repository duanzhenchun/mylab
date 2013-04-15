from numpy import linalg as LA


a = np.array([[1., 2.], [3., 4.]])
ainv = LA.inv(a)
assert np.allclose(np.dot(a, ainv), np.eye(2))
assert np.allclose(np.dot(ainv, a), np.eye(2))

#If a is a matrix object, then the return value is a matrix as well:
ainv = LA.inv(np.matrix(a))
print ainv
