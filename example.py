import time,sys
from MCALib import connect

device = connect(autoscan = True) # automatically detect the hardware
if not device.connected:
	print("device not found")
	sys.exit(0)

print("Device Version",device.version,device.portname)
device.setSqr1(100)
#start data acquisition
device.startHistogram()

#Wait for data collection
time.sleep(2)

# fetch data from the hardware
print('started',device.bytes_per_bin)
device.sync()
#display the data
x = device.getHistogram()

#plot this data
from matplotlib import pyplot as plt
plt.plot(x)
plt.show()
