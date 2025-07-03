import time
import numpy as np
import matplotlib.pyplot as plt
from MCALib import *

dev=connect(autoscan=True)


NS=2000
w = 40
TG=0.5
fig=plt.figure()
plt.axis([0, w*TG/1000, 0, 2])
plt.ion()
plt.show()


va =ta = range(50)
line, = plt.plot(ta,va)


for a in range(5):
	dev.capture_init(0, NS, TG, False)
	time.sleep(1e-6 * dev.samples * dev.timebase + 0.1)
	y = dev.calPoly10(dev.__retrieveBufferData__(0, dev.samples))
	y = dev.get_filtered_pulse(y,w)
	x = np.linspace(0, 1e-3 * dev.timebase * len(y), w)
	#x,y = dev.get_pulse(0,NS,TG,False)
	if(y.max()>0.01):
		print(NS, max(y))
		line.set_xdata(x)
		line.set_ydata(y)
		plt.draw()
	plt.pause(0.05) 
	
