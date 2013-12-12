from math import *

def pdf_gaussian(mu, sigma2, x):
    return 1/sqrt(2.*pi*sigma2) * exp(-.5*(x-mu)**2 / sigma2)

print pdf_gaussian(10.,4.,10.) #Change the 8. to something else!

def update(mean1, var1, mean2, var2):
    new_mean = (var2 * mean1 + var1 * mean2) / (var1 + var2)
    new_var = 1/(1/var1 + 1/var2)
    return [new_mean, new_var]

def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]

measurements = [5., 6., 7., 9., 10.]
motion = [1., 1., 2., 1., 1.]
measurement_sig = 4.
motion_sig = 2.
mu = 0
sig = 10000

for measure, mot in zip(measurements, motion):
    mu, sig = update(mu,sig, measure,measurement_sig)
    mu,sig = predict(mu,sig, mot, motion_sig)
print [mu, sig]
