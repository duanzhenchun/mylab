# -*- coding: utf-8 -*-

from util import *
import urllib2  
import speex

def recorgnize(data, rate, fmt='L16'):
    # see http://sebastian.germes.in/blog/2011/09/googles-speech-api/ for a good description of the url  
    url = 'https://www.google.com/speech-api/v1/recognize?xjerr=1&pfilter=1&client=chromium&lang=zh-CN-&maxresults=4'  
    header = {'Content-Type' : 'audio/%s; rate=%d' %(fmt,rate)}  
    req = urllib2.Request(url, data, header)  
    data = urllib2.urlopen(req)  
    print data.read()  

import sys

def test1(): 
    aus=Austreamer()
    voice=[]
    for i in aus.record():
        voice.append(i)
    fname='test.wav'
    aus.save(''.join(voice),fname)
    play(fname)
    show(fname,aus.channels)
    
from datetime import datetime     
def test2():
    aus=Austreamer()
    for i in aus.record2():
        fname = datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".wav" 
        aus.save(i,fname)
        recorgnize(i,aus.rate)
        
def test3():
    sys.path.append('../')
    from hexdump import dump
    data,params=load('test.wav')
    print dump(data)
    enc = speex.Encoder() 
    spx_data= enc.encode(data)
    print dump(spx_data)
#    open('tmp.spx','wb').write(spx_data)

#    dec=speex.Decoder() 
#    dec.decode(spx_data)

test3()
#recorgnize(voice)
#recorgnize(data,'x-speex-with-header-byte')
#python fromvoice2.py | speexenc -w  - - |speexdec - out.wav

