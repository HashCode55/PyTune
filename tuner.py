from __future__ import division
import pyaudio
import numpy as np
from matplotlib.mlab import find
from scipy.signal import butter, lfilter, fftconvolve

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1 
RATE = 20000 
RECORD_SECONDS = 20

class FrequencyDetector(object):
	def __init__(self, pa, chunk, format_, rate):
		self.stream = stream 
		self.chunk = chunk
		self.format = format_
		self.rate = rate 

	def get_frequency(self, signal):
		"""
		
		"""
		# convert to 16 bit integer 
		signal = np.fromstring(signal, 'Int16')	
		# filter the signal 
		filtered_signal = self.low_pass_filter(signal)		
		# get the zero crossings 	
		crossings = np.sum(np.diff(np.sign(filtered_signal)) != 0)	
		# get the frequency 	
		frequency = (crossings * self.rate) / (2 * self.chunk)
		return frequency

	def get_frequency_ac(self, signal):
		"""
		"""
		# autocorrelation using numpy 
		signal = np.fromstring(signal, 'Int16')			
		corr = fftconvolve(signal, signal[::-1], mode='full')
		corr = corr[len(corr)//2:]

		d = np.diff(corr)
		start = find(d > 0)[0]
		peak = np.argmax(corr[start:]) + start
		px, py = self.parabolic(corr, peak)
		return self.rate / px

	def parabolic(self, f, x):
		xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
		yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
		return (xv, yv)
    	

	def low_pass_filter(self, signal):
		fs = self.rate 
		cutoff = 500 # 100 Hz
		B, A = butter(1, cutoff / (fs / 2)) # 1st order Butterworth low-pass
		filtered_signal = lfilter(B, A, signal, axis=0)		
		return filtered_signal

	def start(self):
		while(1 == 1):
			data = self.stream.read(self.chunk)
			frequency = self.get_frequency_ac(data)
			print 'Frequency {}'.format(frequency)


if __name__ == '__main__':
	# create a pyaudio object 
	pa = pyaudio.PyAudio()
	# create a stream 
	stream = pa.open(format = FORMAT,
		channels = CHANNELS,
		rate = RATE,
		input = True, 
		output = True,
		frames_per_buffer = CHUNK)
	# create fd object 
	fd = FrequencyDetector(stream, CHUNK, np.uint16, RATE)
	# call the engine 
	fd.start()