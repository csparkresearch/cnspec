import time,sys
from MCALib import connect

#device = connect(autoscan = True) # automatically detect the hardware
device = connect(port = '/dev/ttyUSB0')  #Search on specified port

#check if connected
if not device.connected:
	print("device not found")
	sys.exit(0)

#Display the version number
print("Device Version",device.version,device.portname)

#start data acquisition
device.startHistogram()

#Wait for data collection
time.sleep(5)

# fetch data from the hardware
device.sync() 
#display the data
x = device.getHistogram()

#plot this data
from matplotlib import pyplot as plt
plt.plot(x)
plt.show()
