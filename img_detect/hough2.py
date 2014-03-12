from matplotlib import pyplot as plt
import numpy as np
import skimage.transform
from PIL import Image, ImageOps, ImageFilter


def gen_img():
    img = np.zeros((100, 150), dtype=bool)
    img[30, :] = 1
    img[:, 65] = 1
    img[35:45, 35:50] = 1
    for i in range(90):
        img[i, i] = 1
    img += np.random.random(img.shape) > 0.95


def img2arr(fname, inv=False):
    im = Image.open(fname).convert("L")
#    im = im.filter(ImageFilter.CONTOUR)
    if inv:
       im = ImageOps.invert(im)
    im.show()
#    plt.hist(im.getdata()); plt.show()
    img = np.asarray(im.getdata()).reshape(im.size)
#    img[img<200]=0
    return img, im.size


def main():
    fname = '/home/whille/Desktop/ball_detect/11_1.bmp'
    img, imgsize = img2arr(fname)
    print 'imgsize:', imgsize
    res = skimage.transform.probabilistic_hough(img, 
#            line_length = imgsize[0]/4,
#            threshold=250,
#            line_gap=5,
            )
    plt.gca().invert_yaxis()
    for l in res:
        plt.plot(*zip(*l), color='b')
    plt.show()

if __name__=='__main__':
    main()
