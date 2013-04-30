# -*- coding: utf-8 -*-

"""
http://blog.josephwilk.net/projects/latent-semantic-analysis-in-python.html

D1:”The cat in the hat disabled”
D2:”A cat is a fine pet ponies.”
D3:”Dogs and cats make good pets”
D4:”I haven’t got a hat.”

Note the Word ‘disabl’ despite not being in D4 now has a weighting in that document.
"""


from scipy import linalg, array, dot, mat
from math import *
from pprint import pprint


class LSA:
    """ Latent Semantic Analysis(LSA). 
        Apply transforms to a document-term matrix to bring out latent relationships. 
        These are found by analysing relationships between the documents and the terms they 
        contain.
    """
    def __init__(self, matrix):
        self.matrix = array(matrix) * 1.0

    def __repr__(self,):
        """ Make the matrix look pretty """
        stringRepresentation = ""
        rows, cols = self.matrix.shape
        for row in xrange(0, rows):
            stringRepresentation += "["
            for col in xrange(0, cols):
                stringRepresentation += "%+0.2f " % self.matrix[row][col]
            stringRepresentation += "]\n"
        return stringRepresentation

    def __getTermDocumentOccurences(self, col):
        """ Find how many documents a term occurs in"""
        termDocumentOccurences = 0
        rows, cols = self.matrix.shape
        for n in xrange(0, rows):
            if self.matrix[n][col] > 0: #Term appears in document
                termDocumentOccurences += 1
        return termDocumentOccurences

    def tfidfTransform(self,):
        """ Apply TermFrequency(tf)*inverseDocumentFrequency(idf) for each matrix element. 
            This evaluates how important a word is to a document in a corpus
               
            With a document-term matrix: matrix[x][y]
            tf[x][y] = frequency of term y in document x / frequency of all terms in document x
            idf[x][y] = log( abs(total number of documents in corpus) / abs(number of documents with term y)  )
            Note: This is not the only way to calculate tf*idf
        """
        documentTotal = len(self.matrix)
        rows, cols = self.matrix.shape
        for row in xrange(0, rows): #For each document
            wordTotal = reduce(lambda x, y: x + y, self.matrix[row])
            for col in xrange(0, cols): #For each term
                #For consistency ensure all self.matrix values are floats
                self.matrix[row][col] = float(self.matrix[row][col])
                if self.matrix[row][col] != 0:
                    termDocumentOccurences = self.__getTermDocumentOccurences(col)
                    termFrequency = self.matrix[row][col] / float(wordTotal)
                    inverseDocumentFrequency = log(abs(documentTotal / float(termDocumentOccurences)))
                    self.matrix[row][col] = termFrequency * inverseDocumentFrequency

    def lsaTransform(self, dimensions=1):
        """ Calculate SVD of objects matrix: U . SIGMA . VT = MATRIX 
            Reduce the dimension of sigma by specified factor producing sigma'. 
            Then dot product the matrices:  U . SIGMA' . VT = MATRIX'
        """
        rows, cols = self.matrix.shape
        if dimensions <= rows: #Its a valid reduction
            #Sigma comes out as a list rather than a matrix
            u, sigma, vt = linalg.svd(self.matrix)
            #Dimension reduction, build SIGMA'
            for index in xrange(len(sigma) - dimensions, len(sigma)):
                sigma[index] = 0
            #print linalg.diagsvd(sigma,len(self.matrix), len(vt))        
            #Reconstruct MATRIX'
            reconstructedMatrix = dot(dot(u, linalg.diagsvd(sigma, len(self.matrix), len(vt))), vt)
            #Save transform
            self.matrix = reconstructedMatrix
            return u, sigma, vt
        else:
            print "dimension reduction cannot be greater than %s" % rows

if __name__ == '__main__':
    #Example document-term matrix
    # Vector dimensions: good, pet, hat, make, dog, cat, poni, fine, disabl
    matrix = [[0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0],
            [1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
#    matrix = [
#              [4, 4, 5],
#              [4, 5, 5],
#              [3, 3, 2],
#              [4, 5, 4],
#              [4, 4, 4],
#              [3, 5, 4],
#              [4, 4, 3],
#              [2, 4, 4],
#              [5, 5, 5],
#              ]
    #Create
    lsa = LSA(matrix)
    print lsa
    #Prepare
    lsa.tfidfTransform()
    print lsa
    #Perform
    u, sigma, vt = lsa.lsaTransform()
    print lsa
