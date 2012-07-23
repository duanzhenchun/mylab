import wave

f = wave.open("../t_wave/sample.wav", "rb")
params = f.getparams()
print params
nchannels, sampwidth, framerate, nframes = params[:4]
str_data = f.readframes(nframes)
f.close()

import urllib2
url = 'https://www.google.com/speech-api/v1/recognize?xjerr=1&pfilter=1&client=chromium&lang=zh-CN&maxresults=4' 
#wave file
headers = {'Content-Type' : 'audio/L16; rate=%d' %framerate}
print headers

req = urllib2.Request(url, str_data, headers)
response = urllib2.urlopen(req)

print response.read()
