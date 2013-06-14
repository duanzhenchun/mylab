#!/usr/bin/python
 
from scipy.cluster.vq import kmeans, vq
from numpy import array, reshape, zeros
from PIL import Image

vqclst = [2, 10, 100, 256]
imgfile = 'stallman.png'

def read(filename):
    """\
    Read the image data from filename and return an array object.
    """
    return array(Image.open(filename))

def write(filename, data):
    """\
    Save the image data (array object) to file.
    """
    Image.fromarray(data).save(filename)
     
 
data = read(imgfile)
(height, width, channel) = data.shape
 
data = reshape(data, (height * width, channel))
for k in vqclst:
    print 'Generating vq-%d...' % k
    (centroids, distor) = kmeans(data, k)
    (code, distor) = vq(data, centroids)
    print 'distor: %.6f' % distor.sum()
    im_vq = centroids[code, :]
    write('result-%d.jpg' % k, reshape(im_vq,
        (height, width, channel)))
