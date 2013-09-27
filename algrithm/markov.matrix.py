import numpy as np

A=np.array([[0.8,0.05],[0.2,0.95]])
lams,S = np.linalg.eig(A)   
print lambs     # lambda=1 may not be in first index
x1=S[:,lams.argmax()]   
x1 /= x1.sum()   #let x1.sum()=1
print 'steady state', x1


