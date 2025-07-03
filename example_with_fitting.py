import time,sys
import numpy as np
from MCALib import connect

device = connect(autoscan = True) # automatically detect the hardware . or. connect(port = '/dev/ttyUSB0')  #Search on specified port
#check if connected
if not device.connected:
	print("device not found")
	sys.exit(0)

print("Device Version",device.version,device.portname) #Display the version number
device.clearHistogram()
device.setThreshold(50) #Set threshold
device.startHistogram() #start data acquisition

print('started',device.bytes_per_bin)
time.sleep(2) #Wait for data collection

device.sync() # fetch data from the hardware
x = device.getHistogram() #Copy data to a variable called x

#plot this data
from matplotlib import pyplot as plt
plt.plot(x)

#Fit the data
FIT = device.gaussianFit([350,400]) #Apply a gaussian FIT between - and - channel. see also : device.gaussianTailFit
if FIT:
	plt.plot(FIT['X'],FIT['Y']) #Plot fitted data
	print('Gaussian Fit : ',FIT['centroid'],FIT['fwhm'],FIT['area'],np.sum(x))
plt.show()
