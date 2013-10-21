import wave, timeit
import numpy as np
import matplotlib.pyplot as plt

wr = wave.open('C:\\Python27\Nick\Kalimba.wav', 'r') #open the file for reading

sample_length = 10 #seconds
sample_rate = wr.getframerate()
sz = sample_length * sample_rate

## readframes() reads from sound file, returns the data as a string
## fromstring() converts binary string into an array of 16 bit integers
da = np.fromstring(wr.readframes(sz), dtype=np.int16)

## splits the array into the left and right channel arrays
#left, right = da[0::2], da[1::2]

tf = np.fft.rfft(da)

plt.figure(1)
a = plt.subplot(211)
r = 2**16/2
a.set_ylim([-r, r])
a.set_xlabel('time [s]')
a.set_ylabel('sample value [-]')
x = np.arange(44100)/44100
plt.plot(da)
b = plt.subplot(212)
b.set_xscale('log')
b.set_xlabel('frequency [Hz]')
b.set_ylabel('|amplitude|')
plt.plot(abs(tf))
plt.show()

