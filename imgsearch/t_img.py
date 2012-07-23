import Image
import pylab as pl

def t_info(img):
    print img.mode, img.size
    img.show()
    h=img.convert('RGB').histogram()
    pl.plot(h)
    pl.show()

def t_convert(img):
    modes=('1','L','P','RGB','RGBA','CMYK','YCbCr','l','F')
    for m in modes[:4]:
        img.convert(m).show(m)

    rgb2xyz = (
        0.412453, 0.357580, 0.180423, 0,
        0.212671, 0.715160, 0.072169, 0,
        0.019334, 0.119193, 0.950227, 0 )

def t_enhance(img):
    import ImageEnhance
    for method in ('Brightness','Color','Contrast','Sharpness',):
        enhancer = eval('ImageEnhance.' + method)(img)
        for i in range(8):
            factor = i / 4.0
            enhancer.enhance(factor).show("Sharpness %f" % factor)

def allupper(txt):
    return all(c.isupper() for c in txt)
    
def t_filter(img):
    import ImageFilter
    # underscore are allowed 
    modes = filter(lambda s:s.isupper(), ImageFilter.__dict__.keys())
    for fil in modes:
        img.filter(eval('ImageFilter.'+fil)()).show(fil)
    
whitepix=(255,)*4
    
def t_transparent():
    img = Image.open('img.png')
    img = img.convert("RGBA")
    pdata = img.load()
    w,h=img.size
    for x in xrange(w):
        for y in xrange(h):
            if pdata[x,y] == whitepix:
                pdata[x,y]=pdata[x,y][:-1]+(0,)
    img.show()

def t_edge(img):
    img.filter(ImageFilter.MedianFilter).filter(ImageFilter.FIND_EDGES).show()

def isporn(fname):  
    img = Image.open(fname).convert('YCbCr')  
    data = img.getdata()  
    count = 0  
    for i, (y,cb,cr) in enumerate(data):  
        if 86 <= cb <= 117 and 140 <= cr <= 168:  
            count += 1  
    print img.size, count
    return count > 0.3 * reduce(lambda x,y:x*y, img.size)

def test():
    img = Image.open('origin.png')   
    t_enhance(img)
