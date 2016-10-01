#!/usr/bin/env python

import socket
from array import array
import time
import sys
import copy
import pdb;
import colorsys
import random
from itertools import chain

import audioop
import alsaaudio as aa
from time import sleep
from struct import unpack
import numpy as np
np.set_printoptions(formatter={'all':lambda x: '{:2f}'.format(x)})

UDP_PORT = 2342

red=array('B',[75,0,0])
green=array('B',[0,75,0])
blue=array('B',[0,0,75])
space = array('B',[0,0,0])

TIME=0.03
UPDATE_FACTOR=3

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class Lightstick():
    def __init__(self, numleds, ip="10.23.42.30"):
        self.leds = []
        self.numleds=numleds
        default = array('B',(0,)*3)
        self.ip = ip
        for i in range(0,numleds):
            self.leds.append(copy.copy(default))

    def setAllLeds(self, r, g, b):
        for i in range(0,numleds-1):
            self.leds[i] = [r,g,b]
        self.updateLeds()

    def setLed(self, led, red, green, blue):
        #old = copy.copy(self.leds[led])
        self.leds[led][0] = red
        self.leds[led][1] = green
        self.leds[led][2] = blue
        #return old

    def setLeds(self, leds):
        for i in range(0,self.numleds-1):
            self.leds[i]=copy.copy(leds[i])
        self.updateLeds()

    def updateLeds(self):
        message = array('B',[])
        for x in self.leds:
            message.extend(x)
        sock.sendto(message,(self.ip, UDP_PORT))

    def setRawLeds(self,a):
        sock.sendto(a,(self.ip, UDP_PORT))

# audio setup
sample_rate = 44100
no_channels = 2
chunk = 1024 # read chunk size, multiple of 8
data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL)
data_in.setchannels(no_channels)
data_in.setrate(sample_rate)
data_in.setformat(aa.PCM_FORMAT_S16_LE)
data_in.setperiodsize(chunk)
# stick constants
num_leds = 128

def calculate_levels(data, chunk, sample_rate):
    # convert raw chunk to numpy array
    data = unpack("%dh"%(len(data)/2), data)
    data = np.array(data, dtype='h')
    # apply fft - real data so rfft used
    fourier=np.fft.rfft(data, norm="ortho")
    #freq=np.fft.rfftfreq(chunk)
    # make it the same size as chunk
    #print ("len ",len(freq))
    fourier=np.delete(fourier, len(fourier)-1)
    # and the way we do this is, we calculate an amplitude! </feynman>
    ##power = np.log10(np.abs(freq))**2
    fourier=np.abs(fourier)
    # reshape array into rows for the LEDs
    fourier = np.reshape(fourier, (num_leds, chunk/num_leds))
    fourier = np.int_(np.average(fourier, axis=1))
    print(list(fourier))
    #normed = matrix / matrix.max()
    #scale= np.average(matrix)/40

    return fourier #scale, normed

def main(argv):
    stick = Lightstick(num_leds)
    while True:
        l, data = data_in.read()
        data_in.pause(1)
        if l:
            try:
                matrix=calculate_levels(data, chunk, sample_rate)
                #print (matrix)
#                stick.setRawLeds(array('B',list(chain.from_iterable(zip(matrix, matrix, matrix)))))
                stickdata = array('B',[])
                #print(scale)
                #for h in matrix:
                #    r, g, b = colorsys.hsv_to_rgb(h, 1., 1.)
                #    r, g, b = r * 255, g * 255, b * 255
                #    stickdata.extend((int(r), int(g), int(b)))
                #print(list (stickdata))
                #stick.setRawLeds(stickdata)
            except audioop.error as e:
                if e.message != "not a whole number of frames":
                    raise e
        sleep(0.001)
        data_in.pause(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
