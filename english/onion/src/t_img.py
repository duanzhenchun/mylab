import math
from PIL import Image

def test():
    mode='RGBA'
    fs=open('/home/whille/english/novel/Bourne/The.Bourne.Supremacy.txt').read()
    x=int(math.ceil((len(fs)/4.)**.5))
    y=int(math.ceil(len(fs)/4.0/x))
    im = Image.new(mode, (x,y))
    bs=im.tostring()
    bs=fs+bs[len(fs):]
    im.fromstring(bs)
    im.save('/home/whille/Desktop/B2.png')

if __name__ == '__main__':
    test()
