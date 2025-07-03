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
device.setThreshold(30) #Set threshold
device.startHistogram() #start data acquisition

print('started',device.bytes_per_bin)
time.sleep(2) #Wait for data collection

device.sync() # fetch data from the hardware
x = device.getHistogram() #Copy data to a variable called x
print(x)

output = ",\n".join(str(i) for i in x)
print(np.sum(x),output)

#actual time
from datetime import datetime
now = datetime.now()

# now we want to save on file
#file = open("C:\CSpark_MCA\output.txt", "w")
file = open("tmp.txt", "w") 
file.write("var time=['"+ now.strftime("%d/%m/%Y %H:%M:%S") +"'];\n")
file.write("var ydata=[")
file.write(output)
file.write("];")
file.close()
