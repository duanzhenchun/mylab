import numpy as np
from sklearn import linear_model
from sklearn.gaussian_process import GaussianProcess
from matplotlib import pyplot as pl


def f(x):
    return x * np.sin(x)
    return np.vectorize(gaussian)(x, x.mean())
    
def addOne(X):
    return np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)

def gaussian(x, mu=0.0, sigma=2.0):
    return np.exp(-np.linalg.norm(x-mu)**2/(2*sigma**2))

def sigmoid(z, mu=0.0, sigma=1.0):
    return 1.0 / (1 + np.exp(-(z-mu)/sigma))

def polynomial_linear(X, M=5):
    """
    x+x^2+x^3+... => x1,x2,x3,...
    """
    X = np.power(X, range(1, M))
    return addOne(X)

def gaussian_linear(X, M=5):
    mu = np.linspace(X.min(), X.max(), M) 
    sigma = X.max() - X.min()
    sigma =1.0
    X1 = np.zeros((len(X),M)) 
    for i in range(len(X)):
        for j in range(M):
            X1[i,j] = sigmoid(X[i], mu[j], sigma)
            X1[i,j] = gaussian(X[i], mu[j], sigma)
    return X1
    
def gen_noisedata():
    X = np.linspace(0, 100, 50)
    X = np.atleast_2d(X).T
    y = f(X).ravel()
#    X *=100
    span = np.abs(y).max()
    dy = 0.5 + 1.0 * np.random.random(y.shape)
    noise = np.random.normal(0, span * 0.1 * dy)
    y += noise
    return X,y,dy

def confidence_plot(X, y,y_pred, dy):
    # Plot the function, the prediction and the 95% confidence interval based on
# the MSE
    fig = pl.figure()
    pl.errorbar(X.ravel(), y, dy, fmt='r.', markersize=10, label=u'Observations')
    pl.plot(X, y_pred, 'b-', label=u'Prediction')
    pl.fill(np.concatenate([X, X[::-1]]),
            np.concatenate([y_pred - 1.9600 * sigma,
                           (y_pred + 1.9600 * sigma)[::-1]]),
            alpha=.5, fc='b', ec='None', label='95% confidence interval')
    pl.xlabel('$x$')
    pl.ylabel('$f(x)$')
    pl.show()

def main():
    M=40
    X0, y, dy = gen_noisedata()
    #X = polynomial_linear(X0, M)
    X = gaussian_linear(X0, M)
    clf = linear_model.LinearRegression()
    #clf = linear_model.Ridge()
    clf = GaussianProcess(corr='cubic', theta0=1e-2, thetaL=1e-4, thetaU=1e-1,
                     random_start=100)
    clf.fit(X,y) 
    print clf.score(X,y)
    y_pred = clf.predict(X) 
    pl.plot(X0,y, 'r:', label='$f(x)$')
    pl.plot(X0, y_pred, 'b-', label='linear regression of $f(x)$')
    pl.show()

if __name__ == "__main__":
    main()
