import time,sys
import numpy as np
from MCALib import connect

dev = connect()

fname = 'DATA/bi212_19mA_10min_31mar18/data_240mins.csv'
dev.loadFile(fname)

# Get the data. Supply an optional name argument in case of multiple files/connected hardware.
x = dev.getHistogram() #name = fname / name='/dev/ttyUSB0'

#print the whole array. No decimal Points. Suppress scientific notation
np.set_printoptions(threshold = np.inf,precision = 0,suppress=True) #
print (x)

#plot the loaded spectrum
import matplotlib.pyplot as plt
plt.plot(x) #Plot RAW data

FIT = dev.gaussianTailFit([750,850]) #Apply a gaussian+Lorentzian FIT between 700 and 900 channel, and overlay it.
if FIT:
	plt.plot(FIT['X'],FIT['Y']) #Plot fitted data
	print('Gaussian+low energy tail Fit : ',FIT['centroid'],FIT['fwhm'])

FIT = dev.gaussianFit([500,600]) #Apply a gaussian FIT between 500 and 600 channel.
if FIT:
	plt.plot(FIT['X'],FIT['Y']) #Plot fitted data
	print('Gaussian Fit : ',FIT['centroid'],FIT['fwhm'])

plt.show()

