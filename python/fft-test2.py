#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import audioop
import alsaaudio as aa
from struct import unpack
import socket
from array import array
from itertools import chain
import colorsys
np.set_printoptions(precision=2)#formatter={'all':lambda x: '{:2d}'.format(x)})

# audio setup
sample_rate = 44100
no_channels = 2
chunk = 1024 # read chunk size, multiple of 8
data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL)
data_in.setchannels(no_channels)
data_in.setrate(sample_rate)
data_in.setformat(aa.PCM_FORMAT_S16_LE)
data_in.setperiodsize(chunk)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

num_leds=128
max_amp=0
while True:
    l, data = data_in.read()
    data_in.pause(1)
    data = unpack("%dh"%(len(data)/2), data)
    data = np.array(data, dtype='h')

#l = shorts[::2]
#r = shorts[1::2]

    T = 1.0/RATE
    N = data.shape[0]
    Pxx = (1./N)*np.fft.fft(data)
    f = np.fft.fftfreq(N,T)
    Pxx = np.fft.fftshift(Pxx)
    f = np.fft.fftshift(f)

    #return f.tolist(), (np.absolute(Pxx)).tolist()
    fourier = np.absolute(Pxx)).tolist()
    #hann = np.hanning(len(data))


    fourier = np.reshape(fourier, (num_leds, len(fourier)/num_leds))
    fourier = np.average(fourier, axis=1)
    print(fourier)
    #fourier = np.int_(fourier)
    #plt.plot(fourier)
    #plt.show()
    #fourier = fourier * np.arange(1, 129, 1, dtype=np.int32)
    max_amp = max_amp - 1
    if(max_amp<fourier.max()):
            max_amp=fourier.max()
    #scale = np.average(fourier) / max_amp
    #plt.plot(fourier)
    #plt.show()
    leds = fourier / fourier.max()
    leds = np.abs(leds) #occasional slightly negative value causes conversoin errors FIXME better?
    leds = np.nan_to_num(leds) #all zero input data results in NaN
    print(leds)
    #plt.plot(leds)
    #plt.show()
    #leds = array('B',list(chain.from_iterable(zip(leds, leds, leds))))
    stickdata = array('B',[])
    for h in leds:
        r, g, b = colorsys.hsv_to_rgb(h, 1., 1.)#scale)
        r, g, b = r * 255, g * 255, b * 255
        stickdata.extend((int(r), int(g), int(b)))
    sock.sendto(stickdata,("10.23.42.30", 2342))
    data_in.pause(0)

