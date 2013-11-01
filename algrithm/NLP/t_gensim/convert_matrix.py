# Compatibility with NumPy and SciPy
# converting from/to numpy matrices:
import gensim
corpus = gensim.matutils.Dense2Corpus(numpy_matrix)
numpy_matrix = gensim.matutils.corpus2dense(corpus)

# and from/to scipy.sparse matrices:
corpus = gensim.matutils.Sparse2Corpus(scipy_sparse_matrix)
scipy_csc_matrix = gensim.matutils.corpus2csc(corpus)
