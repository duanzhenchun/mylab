
from random import randint
import Image

def r_pos(n):
    return tuple(map(lambda x:randint(0,x), (x,x)))

def r_size(size):
    return tuple(map(lambda x:randint(x/4,x), size))

def r_anglemaker(init):
    angle=[init,1]
    def clo():
        angle[1] *= -1
        return angle[0]*angle[1] + randint(0,angle[0]/2)-angle[0]/4
    return clo
r_angle=r_anglemaker(45)

import ImageEnhance
def r_color(img):
    enhancer = ImageEnhance.Brightness(img)
    factor = randint(2,8)/4.0
    return enhancer.enhance(factor)

def maketree():
    divs=(3,30)
    SIZE=400

    rows,cols=[map(lambda x:SIZE/div*x, range(1,div)) for div in divs]
    img=Image.open('leaf.png')
    for i in range(8):
        display(rows,cols,SIZE,img)

def display(rows,cols,bgsize,img):
    bgimg=Image.new('RGBA',size=(bgsize,)*2)
    for row in rows:
        for col in cols:
            im=img
            im=im.rotate(r_angle())
            im=im.resize(r_size(im.size))
            im=r_color(im)
            bands = im.split()
            new_pos=tuple(map(lambda (x,y):x-y/2, zip((row,col),im.size)))
            bgimg.paste(im, new_pos, mask=bands[3])
    bgimg.show()

maketree()
