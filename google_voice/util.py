# -*- coding: utf-8 -*-
import wave
import pylab as pl
import numpy as np 
import pyaudio
import sys

LEVEL=1000
NCOUNT=10
NUM_SAMPLES = 160

class Austreamer:
    def __init__(self,
            channels = 1, 
            rate = 16000,  
            frames_per_buffer = NUM_SAMPLES,
            fmt = pyaudio.paInt16, 
            samplewith = None,
            inp = True, 
            out = False,  
            ):
        self.p = pyaudio.PyAudio()  
        if samplewith:
            fmt = self.p.get_format_from_width(samplewith)
        self.samplewith=self.p.get_sample_size(fmt)
        self.channels=channels
        self.rate=rate
        self.frames_per_buf=frames_per_buffer
        self.stream = self.p.open(format=fmt, channels=self.channels, rate=self.rate, input=inp, output=out, frames_per_buffer=self.frames_per_buf)          
        
    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()  
    
    def record(self, nquit=160):
        """wait nquit to break"""
        nover = 0  
        while True:  
            data = self.stream.read(self.frames_per_buf) 
            yield data
            audio_data = np.fromstring(data, dtype=np.short) 
            over_count = np.sum( audio_data > LEVEL ) 
            if over_count > NCOUNT:
                nover=0  
            else:  
                nover+=1  
            print '\r%2.1f (%d%% quiet)      '%(over_count, NCOUNT*100/nquit),
            if nover >= nquit:
                break

    def record2(self,save_len=64):
        """record every N samples, use ^+C to break"""   
        save_buffer=[] 
        save_count=0
        print 'start recording! ^+C to break'
        while True:  
            try:
                data = self.stream.read(self.frames_per_buf) 
                audio_data = np.fromstring(data, dtype=np.short) 
                over_count = np.sum( audio_data > LEVEL ) 
                print '\r max: %10d, over_count:%5d         ' %(np.max(audio_data), over_count),
                if over_count > NCOUNT:
                    save_count=save_len
                else:
                    save_count-=1
                if save_count < 0: 
                    save_count = 0 
                if save_count > 0: 
                    save_buffer.append(data) 
                elif len(save_buffer) > 0:
                    self.stream.stop_stream()
                    yield ''.join(save_buffer)
                    self.stream.start_stream()
                    save_buffer = [] 
                    
            except KeyboardInterrupt:
                print 'stop recording!'
                break    
                
    
    def save(self,str_data,fname): 
        f = wave.open(fname, 'wb') 
        f.setnchannels( self.channels) 
        f.setsampwidth(self.samplewith) 
        f.setframerate(self.rate) 
        f.writeframes(str_data) 
        f.close() 
    
    
def load(fname):
    f = wave.open(fname, "rb")
    params = f.getparams()
    print 'wav format:', params
    nchannels, sampwidth, framerate, nframes = params[:4]
    str_data = f.readframes(nframes)
    f.close()    
    return str_data,params
    
    
def play(fname, nsamples=NUM_SAMPLES):
    f = wave.open(fname, 'rb')
    aus=Austreamer( samplewith = f.getsampwidth(),
                    channels = f.getnchannels(),
                    rate = f.getframerate(),
                    out = True)
    while True:
        data = f.readframes(nsamples)
        if data == "": break
        aus.stream.write(data)
        
            
def show(fname,channels):
    str_data,params=load(fname)
    nchannels, sampwidth, framerate, nframes = params[:4]
    wave_data = np.fromstring(str_data, dtype=np.short)
    # if nchannels == 2, data will be: LRLRLRLR....LR
    wave_data.shape = -1, nchannels  # shape: dimension size; -1: means auto
    wave_data = wave_data.T #Transpose
    time = np.arange(0, nframes) * (1.0 / framerate)
    
    for i in range(channels):
        pl.subplot(211+i) #L channel
        pl.plot(time, wave_data[i])
    pl.xlabel("time (seconds)")
    pl.show()    
    
