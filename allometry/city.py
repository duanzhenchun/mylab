# http://stackoverflow.com/questions/3310681/finding-blank-regions-in-image

# normalize
# http://en.wikipedia.org/wiki/Normalization_%28image_processing%29

import numpy as np
import scipy as sp
#import scipy.ndimage.morphology
from scipy.misc import fromimage, toimage
import Image
import pylab as plt
import math
from util import *    
    
def tofloat(img):
    imgfloat = img.astype(np.float32) / 255.
    return imgfloat

def touint(imgfloat):    
    img8 = (imgfloat * 255).round().astype(np.uint8)  
    return img8
    
def tholdimg(img, k):
    return np.where(img > k, 1, 0)
    
def showimg(img):
    img2 = toimage(img)
    img2.show()
#    img.save('small.out.png')

def plotdic(dic):
    if not dic:
        return
    res = sorted(dic.values())
    x, y = zip(*res)
    #super linear, use math.log
    x, y = map(lambda i:math.log(i), x), map(lambda i:math.log(i), y)
    return calclinalg(x, y)
#    plt.plot(x,y)

def calcmorph(imgf, k):
    imgbin = tholdimg(imgf, k)
    # Fill hollows 
#    filled = sp.ndimage.morphology.binary_fill_holes(imgbin)
    labeled_array, num_features = sp.ndimage.label(imgbin)  # len is row num
    dic = {}
    shape = labeled_array.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            dic.setdefault(labeled_array[i, j], [0, 0.0])
            dic[labeled_array[i, j]][0] += 1
            dic[labeled_array[i, j]][1] += imgf[i, j]
    del dic[0]
    return plotdic(dic)
                
def DGBD():
    np.random.seed(10)
    a, m = 3., 1.
    s = np.random.pareto(a, 1000) + m
    s = list(s)
    s2 = sorted(s, reverse=True)
    r = map(lambda i: s2.index(i), s)
    plt.loglog(r, s, 'bo')
    plt.show()

    Y = np.log(s)
    X1 = [np.log(max(r) + 1 - i) for i in r]
    X2 = np.log(r)
    X = np.array(zip(X1, X2))
    #pip install scikit-learn
    
def draw_circle(draw, (x, y), R):
    maxclor = 64
    draw.point((x, y), (maxclor,)*3)
    for r in range(R):
        pos = (x - r, y - r, x + r, y + r)
        clor = (int((1 - float(r) / R) ** 5 * maxclor),)*3
        draw.ellipse(pos, outline=clor)
        
import ImageDraw, Image

def fakeimg():
    img = Image.new('RGB', (200, 200))
    draw = ImageDraw.Draw(img)
    draw_circle(draw, (20, 20), 20)
    draw_circle(draw, (170, 20), 25)
    draw_circle(draw, (160, 80), 30)
    draw_circle(draw, (60, 100), 40)
    draw_circle(draw, (150, 150), 35)
    img.show()
    imgname = 'img/fake.png'
    img.save(imgname)
    main(imgname)
    
def main(imgname):
    img = Image.open(imgname, 'r')
    img2 = img.convert('L')
    imgarr = fromimage(img2)
    imgf = tofloat(imgarr)
    hints = []
    Ks = [.025 * i for i in range(1, 10)]
    Ms = []
    for k in Ks:
        Ms.append(calcmorph(imgf, k))
        hints.append('k:%f' % k)
    calclinalg(Ks, Ms, True)
#    plt.legend(hints, 'upper center', shadow=True)    
#    plt.show()
        
#    object_slices =  sp.ndimage.find_objects(labeled_array)
#    res=[]
#    for i in object_slices:
#        c = imgbin[i].sum()
#        res.append(c)

if __name__ == '__main__':
#    fakeimg()
    main('img/islandSmall.png')
