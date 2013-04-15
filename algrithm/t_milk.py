# https://pypi.python.org/pypi/milk/

import numpy as np
import milk

# prepare data
# 2d array of features: 100 examples of 10 features each
features = np.random.rand(100, 10)
labels = np.zeros(100)
features[50:] += .5
labels[50:] = 1

confusion_matrix, names = milk.nfoldcrossvalidation(features, labels)
print 'Accuracy:', confusion_matrix.trace() / float(confusion_matrix.sum())

# train
learner = milk.defaultclassifier()
model = learner.train(features, labels)

# Now you can use the model on new examples:
example = np.random.rand(10)
print model.apply(example)

example2 = np.random.rand(10)
example2 += .5
print model.apply(example2)
