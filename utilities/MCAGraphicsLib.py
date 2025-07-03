from .templates import ui_ratemonitor as ratemonitor
from .templates.gauge import Gauge
from .Qt import QtGui,QtCore,QtWidgets
import numpy as np
import time

colors=[(0,255,0),(255,0,0),(255,255,100),(10,255,255)]+[(50+np.random.randint(200),50+np.random.randint(200),150+np.random.randint(100)) for a in range(10)]

class RATEMONITOR(QtWidgets.QDialog,ratemonitor.Ui_Dialog):
	def __init__(self,parent,sensor):
		super(RATEMONITOR, self).__init__(parent)
		name = sensor['name']
		self.initialize = sensor['init']
		self.read = sensor['read']
		self.isPaused = False
		self.setupUi(self)
		self.currentPage = 0
		self.max = sensor.get('max',None)
		self.min = sensor.get('min',None)
		self.fields = sensor.get('fields',None)
		self.widgets =[]
			
		self.graph.setRange(xRange=[-5, 0])

		self.curves = {}
		self.gauges = {}
		self.datapoints=0
		self.T = 0
		self.time = np.empty(300)
		self.start_time = time.time()
		row = 1; col=1;
		for a,b,c in zip(self.fields,self.min,self.max):
			gauge = Gauge(self)
			gauge.setObjectName(a)
			gauge.set_MinValue(b)
			gauge.set_MaxValue(c)
			self.gaugeLayout.addWidget(gauge,row,col)
			col+= 1
			if col == 4:
				row += 1
				col = 1
			self.gauges[gauge] = [a,b,c] #Name ,min, max value
			
			curve = self.graph.plot(pen=colors[len(self.curves.keys())])
			self.curves[curve] = np.empty(300)
		self.setWindowTitle('Monitor : %s'%name)

	def next(self):
		if self.currentPage==1:
			self.currentPage = 0
			self.switcher.setText("Data Logger")
		else:
			self.currentPage = 1
			self.switcher.setText("Analog Gauge")

		self.monitors.setCurrentIndex(self.currentPage)

	def setValue(self,vals):
		if vals is None:
			print('check connections')
			return
		if self.currentPage == 0: #Update Analog Gauges
			p=0
			for a in self.gauges:
				a.update_value(vals[p])
				p+=1
		elif self.currentPage == 1: #Update Data Logger
			if self.isPaused: return
			p=0
			self.T = time.time() - self.start_time
			self.time[self.datapoints] = self.T
			if self.datapoints >= self.time.shape[0]-1:
				tmp = self.time
				self.time = np.empty(self.time.shape[0] * 2) #double the size
				self.time[:tmp.shape[0]] = tmp

			for a in self.curves:
				self.curves[a][self.datapoints] = vals[p]
				if not p: self.datapoints += 1 #Increment datapoints once per set. it's shared

				if self.datapoints >= self.curves[a].shape[0]-1:
					tmp = self.curves[a]
					self.curves[a] = np.empty(self.curves[a].shape[0] * 2) #double the size
					self.curves[a][:tmp.shape[0]] = tmp
				a.setData(self.time[:self.datapoints],self.curves[a][:self.datapoints])
				a.setPos(-self.T, 0)
				p+=1

	def pause(self,val):
		self.isPaused = val

	def launch(self):
		self.initialize()
		self.show()
