#!/usr/bin/python
# -*- coding: utf-8 -*-

import Image

def regulate_img(f):
    img=Image.open(f)
    size = (256, 256)
    return img.resize(size).convert('RGB')

def split_img(img, (pw, ph) = (64, 64)):
	w, h = img.size
	assert w % pw == h % ph == 0
	return [img.crop((i, j, i+pw, j+ph)).copy() \
				for i in xrange(0, w, pw) \
				for j in xrange(0, h, ph)]

import pylab as pl

def similar(lh, rh, show=False):
	assert len(lh) == len(rh)
	if show:
	    pl.plot(lh,'g',rh,'b')
	    pl.show()
	return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

def hist_similar(li, ri,split=True):
    if not split:
        return similar(li.histogram(), ri.histogram())
    else:
        return sum(similar(l.histogram(), r.histogram()) for l, r in zip(split_img(li), split_img(ri))) / 16.0
			

def calc_similar(lf, rf):
	return hist_similar(*map(regulate_img, (lf,rf)))

def draw_4x4_img(lf, rf):
	li, ri = map(regulate_img, (lf,rf))
	li.save(lf + '_regalur.png')
	ri.save(rf + '_regalur.png')
	fd = open('stat.csv', 'w')
	fd.write('\n'.join(l + ',' + r for l, r in zip(map(str, li.histogram()), map(str, ri.histogram()))))
	fd.close()
	import ImageDraw
	li = li.convert('RGB')
	draw = ImageDraw.Draw(li)
	for i in xrange(0, 256, 64):
		draw.line((0, i, 256, i), fill = '#ff0000')
		draw.line((i, 0, i, 256), fill = '#ff0000')
	li.save(lf + '_lines.png')
	

if __name__ == '__main__':
	path = r'test/TEST%d/%d.JPG'
	for i in xrange(1, 7):
		print 'test_case_%d: %.3f%%'%(i, \
			calc_similar('test/TEST%d/%d.JPG'%(i, 1), 'test/TEST%d/%d.JPG'%(i, 2))*100)
	
	#draw_4x4_img('test/TEST4/1.JPG', 'test/TEST4/2.JPG')

