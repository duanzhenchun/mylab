# XOR example:
# http://scikit-learn.org/stable/auto_examples/svm/plot_svm_nonlinear.html

import numpy as np
from sklearn.svm import SVC 

X = np.array([[1, 1], [2, 2], [3, 3], [1, 2], [2, 1]])
y = np.array([1, 1, 2, 1, 1])
 
clf = SVC()
clf.fit(X, y)  # doctest: +NORMALIZE_WHITESPACE
print(clf.predict([[0.8, 2], [4, 2], [4, 3]]))
print clf.support_ 
print clf.support_vectors_
print clf.dual_coef_
