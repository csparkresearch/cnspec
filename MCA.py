#!/usr/bin/python3

import os,sys,time,platform
from utilities.Qt import QtGui, QtCore, QtWidgets
_translate = QtCore.QCoreApplication.translate

from utilities.templates import ui_layout as layout

import constants

class myTimer():
	def __init__(self,interval,active=True):
		self.interval = interval
		self.reset()
		self.active = active #deactivate if necessary.(e.g. autostop)
		self.start_time = time.time()

	def reset(self,interval=None):
		if interval is not None:
			self.interval = interval
		self.start_time = time.time()
		self.timeout = self.start_time + self.interval
		self.active=True

	def deactivate(self):
		self.active = False

	def ready(self):
		T = time.time()
		dt = T - self.timeout
		if dt>0 and self.active==True: #timeout is ahead of current time 
			self.timeout = T - dt%self.interval + self.interval
			return True
		return False

	def progress(self):
		return 100*(self.interval - self.timeout + time.time())/(self.interval)			

class pulseRate():
	def __init__(self):
		self.SIZE = 20 #Increase to improve averaging
		self.counts = np.zeros([self.SIZE,2])
		self.datapoints = 0
	def clear(self):
		self.datapoints = 0
		self.counts = np.zeros([self.SIZE,2])

	def getRate(self):
		if self.datapoints <= 1: return 0
		pfinal = self.counts[self.SIZE-1]
		pfirst = self.counts[ max(0,self.SIZE-1-self.datapoints+1) ]  #no element less than zeroeth element.
		rate = (pfinal[1] - pfirst[1])/(pfinal[0] - pfirst[0])
		return rate

	def getInstantRate(self):
		if self.datapoints <= 1: return 0
		pfinal = self.counts[self.SIZE-1]
		psecondfinal = self.counts[self.SIZE-2]
		rate = (pfinal[1] - psecondfinal[1])/(pfinal[0] - psecondfinal[0])
		return rate


	def getBothRates(self):
		#Latest, Average.
		return [self.getInstantRate(), self.getRate()]

	def addPoint(self,t,c):
		self.counts = np.roll(self.counts,-1,0)
		self.counts[self.SIZE - 1][0] = t
		self.counts[self.SIZE - 1][1] = c
		self.datapoints+=1

class AppWindow(QtWidgets.QMainWindow, layout.Ui_MainWindow):
	total_bins = 1024
	version_number=0
	p=None
	menu_entries=[]
	currentState = False
	dataDumpPath = None
	calibrationChanged = QtCore.pyqtSignal(object,object, name='calibrationChanged')
	plot = None
	pulsePlot = None
	vLine = None
	switchingPlot = False
	surfacePlot = None
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.setTheme("default")
		#self.setTheme("material2")
		self.statusBar = self.statusBar()
		self.splash = kwargs.get('splash',None)
		self.vacuum_enabled = True
		self.pulseStretchState = False
		self.SCOPE_ENABLED = True
		self.scope_ready_time = 0

		global app
		self.fileBrowser = fileBrowser(thumbnail_directory = 'MCA_thumbnails',app=app, clickCallback = self.loadPlot,recordToHistory = self.recordToHistory, loadList = self.loadList)
		self.saveLayout.addWidget(self.fileBrowser)
		
		#Calibration Menu & storage
		self.calibrationEnabled = False

		self.calPoly = np.poly1d([1,0])
		self.calPolyInv = np.poly1d([1,0])
		self.calibrationMenu = QtWidgets.QMenu()
		

		self.y=[];
		self.y2=[];
		self.spectrumTime = time.time()
		self.offlineData  = True
		self._browserPath = '.'
		self.saved={}
		self.thumbList={}
		self.markers=[]

		# PLOT creation
		self.createMainPlot()
		#self.createMainPlot('w','k')
		
		#Region Widget
		#self.regionLayout.setAlignment(QtCore.Qt.AlignTop)
		self.regionWindow = regionPopup.AppWindow(self,insertRegion=self.insertRegion,getData = self.getData,hltime = self.halflifeTime,changeDirectory = self.changeDirectory,enablePeriodicSpectrumSaving = self.enablePeriodicSpectrumSaving )
		self.regionWindow.widgetLayout.setAlignment(QtCore.Qt.AlignTop)
		self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.regionWindow)
		#self.regionWindow.setFloating(True)
		self.regionWindow.close()

		#Spectrum History Widget
		self.historyWindow = historyPopup.AppWindow(self,regions = self.regionWindow.regions)
		self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.historyWindow)
		self.historyWindow.setFloating(True)
		self.historyWindow.close()

		#Define some keyboard shortcuts for ease of use
		self.shortcutActions={}
		self.shortcuts={"+":self.summation,"s":self.start,"f":self.fit,"u":self.load,"r":self.insertRegion,"g":self.fitWithTail,"h":self.historyWindow.show,"Ctrl+S":self.save,"o":self.selectDevice,"p":self.setParameter,"Ctrl+t":self.writeFlash,"c":self.setCut,"1":functools.partial(self.setCutRegion,0),"2":functools.partial(self.setCutRegion,1)}
		for a in self.shortcuts:
			shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(a), self)
			shortcut.activated.connect(self.shortcuts[a])
			self.shortcutActions[a] = shortcut


		# exporter
		self.exporter = PQG_ImageExporter(self.plot.plotItem)# pg.exporters.ImageExporter(self.plot.plotItem)

		#Auto-Update Menu
		self.autoUpdateMenu = QtWidgets.QMenu()
		#self.autoUpdateMenu.addAction("Interval",self.setAutoUpdateTime)
		self.autoUpdateTimerAction = QtWidgets.QWidgetAction(self.autoUpdateMenu)
		self.autoUpdateTimerInterval = QtWidgets.QSpinBox()
		self.autoUpdateTimerInterval.setMinimum(5);self.autoUpdateTimerInterval.setMaximum(3600);self.autoUpdateTimerInterval.setValue(constants.AUTOUPDATE_INTERVAL); self.autoUpdateTimerInterval.setSuffix(' S');
		self.autoUpdateTimerInterval.valueChanged['int'].connect(self.setAutoUpdateInterval)
		self.autoUpdateTimerAction.setDefaultWidget(self.autoUpdateTimerInterval)
		self.autoUpdateMenu.addAction(self.autoUpdateTimerAction)


		self.autoUpdateSettings.setMenu(self.autoUpdateMenu)

		self.calibWindow = calPopup.AppWindow(self,application=self.setCalibration)

		self.splash.showMessage("<h2><font color='Black'>Connecting...</font></h2>", QtCore.Qt.AlignLeft, QtCore.Qt.black)
		self.splash.pbar.setValue(7)

		
		self.pending = {
		'status':myTimer(constants.STATUS_UPDATE_INTERVAL),
		'update':myTimer(constants.AUTOUPDATE_INTERVAL),
		'current':myTimer(constants.CURRENT_UPDATE_INTERVAL),
		'temperature':myTimer(constants.TEMPERATURE_UPDATE_INTERVAL),
		'halflife':myTimer(self.regionWindow.decayInterval.value()),
		'autostop':myTimer(0,False),
		'datadump':myTimer(self.regionWindow.saveAllInterval.value()*60) #convert minutes to seconds		
		}

		rateMonitorOptions = {'name':'Counts per Second', 'init':print, 'read':None,
				'fields':['rate','average'],
				'min':[0,0],
				'max':[3000,3000],
			}

		vacuumMonitorOptions = {
				'name':'Pressure Sensor',
				'init':self.initPressureMonitor,
				'read':self.readPressureMonitor,
				'fields':['Pressure','Temp','Humidity'],
				'min':[0,0,0],
				'max':[1600,100,100],
				}

		from utilities import MCAGraphicsLib
		self.rateMonitor = MCAGraphicsLib.RATEMONITOR(self,rateMonitorOptions)
		if self.vacuum_enabled: 
			self.vacMonitor = MCAGraphicsLib.RATEMONITOR(self,vacuumMonitorOptions)
		
		self.temperature = decayTools.temperatureHandler()

		self.initializeCommunications()

		
		self.startTime = time.time()
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.updateEverything)
		self.timer.start(200)

		
		#Auto-Detector
		self.shortlist=MCALib.getFreePorts(None)
		self.deviceSelector.setList(self.shortlist,self.p)
		
		#self.loadPlot('DATA/212Bi.csv')
		#self.showGammaMarkers('137Cs')
		#self.loadPlot('DATA/eu152.dat')
		#self.loadList('DATA/list_sample.csv')
		#self.loadFromMemory('tmp2.npy',128)

		self.splash.showMessage("<h2><font color='Black'>Ready!</font></h2>", QtCore.Qt.AlignLeft, QtCore.Qt.black)
		self.splash.pbar.setValue(8)

	
	def setTheme(self,theme):
		self.setStyleSheet("")
		self.setStyleSheet(open(os.path.join(path["themes"],theme+".qss"), "r").read())

	def plotRangeChanged(self,val):
		Y = self.plot.plotItem.vb.viewRange()[1]
		H = (Y[1]-Y[0])*.95 + Y[0]
		for _,a in self.markers:
			a.setPos(a.x(), H)

	def showAlphaMarkers(self,state):
		self.showMarkers(constants.ALPHAS,state)

	def showGammaMarkers(self,state):
		self.showMarkers(constants.GAMMAS,state)

	def showMarkers(self,markerList,state):
		for a,b in self.markers:
			self.plot.removeItem(a)
			self.plot.removeItem(b)
		self.markers=[]
		H = self.plot.plotItem.vb.viewRange()[1][1]*.95
		energies = markerList.get(state,[])
		for a in energies:
			line = pg.InfiniteLine(angle=90, movable=False)
			line.setPos(a)
			self.plot.addItem(line, ignoreBounds=True)
			text = pg.TextItem(html='<div style="text-align: center"><span style="color: #FFF;font-size: 7pt;">%.1fkeV</span><br><span style="color: #FF0; font-size: 8pt;">%s</span></div>'%(a,energies[a]), anchor=(-0.1,0),border='w', fill=(0, 0, 100, 100))
			self.plot.addItem(text)
			text.setPos(a, H)
			self.markers.append([line,text])



	def createMainPlot(self,bg=QtGui.QColor(0,0,0),fg = QtGui.QColor(200,200,200)):
		#destroy any old plot
		if self.plot:
			if self.vLine:
				self.plot.removeItem(self.vLine)
				self.plot.removeItem(self.chanLabel)
			self.plot.removeItem(self.arrow)
			self.plot.removeItem(self.markerarrow)
			self.plot_area.removeWidget(self.plot)
			self.plot.destroy()
			
		# Go about creating a new plot
		pg.setConfigOptions(antialias=True, background=bg,foreground=fg)
		self.plot=pg.PlotWidget()
		self.plot.setMinimumHeight(250)
		self.plot_area.addWidget(self.plot)
		self.plot.getAxis('left').setGrid(170)
		self.plot.getAxis('bottom').setGrid(170); 		self.plot.getAxis('bottom').setLabel('Channel Number')
		self.plot.sigYRangeChanged.connect(self.plotRangeChanged)

		if bg=='w': #Light background
			self.pen = pg.mkPen((0,0,0), width=1)
			self.pen2 = pg.mkPen((255,100,100), width=1)
			self.brush = pg.mkBrush((26, 197, 220,150))
		else:
			self.pen = pg.mkPen((255,255,255), width=1)
			self.pen2 = pg.mkPen((255,0,0), width=1)
			self.brush = pg.mkBrush((26, 197, 220,100))

		self.curve = pg.PlotCurveItem(name = 'Data')
		self.curve2 = pg.PlotCurveItem(name = 'Data2')
		self.trendline = pg.PlotCurveItem(name = 'background')
		self.plot.addItem(self.trendline);

		self.fitcurves = []
		self.plot.addItem(self.curve);
		self.plot.addItem(self.curve2);
		self.plot.scene().sigMouseClicked.connect(self.onClick)


		self.moveproxy = pg.SignalProxy(self.plot.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)


		self.arrow = pg.ArrowItem(angle=-60,tipAngle = 90, headLen=7, tailLen=9, tailWidth=5, pen={'color': 'g', 'width': 1}) 
		self.plot.addItem(self.arrow)
		self.arrow.setPos(0,0)
		#self.vLine = pg.InfiniteLine(angle=90, movable=False)
		#self.plot.addItem(self.vLine, ignoreBounds=True)

		
		## Create text object, use HTML tags to specify color/size

		self.currentPeak = None
		self.markerarrow = pg.ArrowItem(angle=-160,tipAngle = 90, headLen=7, tailLen=9, tailWidth=5, pen={'color': 'r', 'width': 1}) 
		self.plot.addItem(self.markerarrow)
		self.markerarrow.setPos(0,0)
		self.toggleLog(self.logBox.isChecked())  #Change to log scale if necessary
		self.pulseRateCounter = pulseRate()
		
		if self.pulsePlot:
			self.pulsePlotLayout.removeWidget(self.pulsePlot)
			self.pulsePlot.destroy()
		#Create pulse plot
		self.pulsePlot=pg.PlotWidget()
		self.pulsePlot.setMaximumWidth(200)
		self.pulsePlotLayout.addWidget(self.pulsePlot)
		#self.pulsePlot.getPlotItem().hideAxis('left')
		self.pulsePlot.getAxis('left').setGrid(200)
		self.pulsePlot.getAxis('bottom').setGrid(200);
		self.pulsePlot.setYRange(0,2)
		self.pulseCurve = pg.PlotCurveItem(name = 'Signal')
		self.pulsePlot.addItem(self.pulseCurve)

	def enableCalibration(self):
		self.calibrateOnOff.setChecked(True)
	

	def enableTemperatureMonitor(self,state):
		if state:
			self.temperatureLabel.show()
		else:
			self.temperatureLabel.hide()
		
	def enableCurrentMonitor(self,state):
		if state:
			self.currentFrame.show()
			self.currentMonitorAvailable = True
		else:
			self.currentFrame.hide()
			self.currentMonitorAvailable = False

	def getTotalBins(self):
		return self.total_bins # self.channelList[self.channelBox.currentIndex()]
		
	def setTotalBins(self,bins):
		self.total_bins = bins
		self.binLabel.setText('Bins: %d'%(bins))
		#self.channelBox.setCurrentIndex(self.channelList.index(bins))

			
	def initializeCommunications(self,port=False):
		if self.p:
			try:self.p.fd.close()
			except:pass
		if port:
			self.p = MCALib.connect(port = port)
		else:
			self.p = MCALib.connect(autoscan=True)
		self.decayHandler = decayTools.decayHandler()
		if self.p.connected:
			self.listFrame.hide()
			#print([str(bin(a)) for a in self.p.scanI2C()])

			if self.p.activeSpectrum.datatype=='list':
				traces = []
				for b in range(self.p.activeSpectrum.parameters):
					traces.append('%s:%d'%(self.p.portname,b+1))
				#self.updateTraceList(traces)
				if self.p.activeSpectrum.parameters==2: #Dual list mode. Open 2D plots
					self.listFrame.show()
					from utilities import plot3DTools
					if self.surfacePlot: 
						self.surfacePlot.close()
						del self.surfacePlot
					self.surfacePlot = plot3DTools.surface3d(self,self.p.activeSpectrum.HISTOGRAM2D,self.p.activeSpectrum.BINS2D)
			else:
				pass
				#self.updateTraceList(['%s'%self.p.portname])

			try:
				self.setTotalBins(self.p.total_bins)
				self.version_number = float(self.p.version[-3:])
				self.decayHandler.interval = self.regionWindow.decayInterval.value()
				self.pulseRateCounter.clear()
				#self.p.setSqr1(2000,10) #TODO : REMOVE in production

			except Exception as e:
				print(e)

		self.enableCurrentMonitor(False)
		self.enableTemperatureMonitor(False)
		if self.p.connected==False:
			self.showStatus("System Status | Device not found. Dummy mode.",True)
			self.setWindowTitle('MCA : Error : device not found')
		else:
			self.showStatus("System Status | Connected to device. Version : %s"%(self.p.version))
			self.setWindowTitle("CSpark Research : %s"%(self.p.name))
			#if self.p.VOLTMETER_ENABLED:
			#	self.enableTemperatureMonitor(True)
			#if self.p.CCS_ENABLED:  #Current source monitoring is only available from version 2.0 onwards, and in alpha detector integrated boards only
			#	self.enableCurrentMonitor(True)
			
		self.makeBottomMenu()

		self.plot.setLimits(xMin=0,xMax=self.total_bins,yMin=0,yMax=(1<<32));self.plot.setXRange(0,self.total_bins)


	def makeBottomMenu(self):
		try:self.pushbutton.setParent(None)
		except:pass
		self.pushbutton = QtWidgets.QPushButton('Menu')
		menu = QtWidgets.QMenu()
		menu.addAction(self.controlDock.toggleViewAction())
		menu.addAction(self.historyWindow.toggleViewAction())
		menu.addAction('Set Square Wave', self.sqr1)
		if self.version_number>=2.0:
			menu.addAction('Set Threshold', self.set_threshold)
		
		menu.addSeparator()

		self.plotColorAction = QtWidgets.QAction('Light Theme', menu, checkable=True)
		self.plotColorAction.triggered.connect(self.setPlotColor)
		menu.addAction(self.plotColorAction)
		

		self.removeCalBox = QtWidgets.QAction('File Load: Remove Calibration', menu, checkable=True)
		self.removeCalBox.triggered.connect(menu.show)
		menu.addAction(self.removeCalBox)

		#self.pileUpAction = QtWidgets.QAction('PileUp Reject', menu, checkable=True)
		#self.pileUpAction.triggered.connect(self.pileUpRejection)
		#self.pileUpAction.triggered.connect(menu.show)
		#menu.addAction(self.pileUpAction)

		#self.coincidencegate = QtWidgets.QAction('External Gate', menu, checkable=True)
		#self.coincidencegate.triggered.connect(self.externalGate)
		#self.coincidencegate.triggered.connect(menu.show)
		#menu.addAction(self.coincidencegate)

		###### Constant current source and voltmeter monitors ######
		menu.addSeparator()
		self.CCSMonitor = QtWidgets.QAction('Monitor Current Source', menu, checkable=True)
		self.CCSMonitor.triggered.connect(self.enableCurrentMonitor)
		menu.addAction(self.CCSMonitor)

		self.TMonitor = QtWidgets.QAction('Monitor Temperature', menu, checkable=True)
		self.TMonitor.triggered.connect(self.enableTemperatureMonitor)
		menu.addAction(self.TMonitor)


		menu.addSeparator()

		menu.addAction('Set Window Opacity', self.setOpacity)
		menu.addAction('Save Window as Svg', self.exportSvg)
		menu.addAction('Enable Pressure Monitor(optional)', self.vacMonitor.launch)

		#Theme
		self.themeAction = QtWidgets.QWidgetAction(menu)
		themes = [a.split('.qss')[0] for a in os.listdir(path["themes"]) if '.qss' in a]
		self.themeBox = QtWidgets.QComboBox(); self.themeBox.addItems(themes)
		self.themeBox.currentIndexChanged['QString'].connect(self.setTheme)
		self.themeAction.setDefaultWidget(self.themeBox)
		menu.addAction(self.themeAction)

		#Alpha Markers
		self.markerAction = QtWidgets.QWidgetAction(menu)
		self.markerBox = QtWidgets.QComboBox(); self.markerBox.addItems(['Add Alpha Energy Guides']+list(constants.ALPHAS.keys()))
		self.markerBox.currentIndexChanged['QString'].connect(self.showAlphaMarkers)
		self.markerAction.setDefaultWidget(self.markerBox)
		menu.addAction(self.markerAction)
		
		#Gamma Markers
		self.markerActionG = QtWidgets.QWidgetAction(menu)
		self.markerBoxG = QtWidgets.QComboBox(); self.markerBoxG.addItems(['Add Gamma Energy Guides']+list(constants.GAMMAS.keys()))
		self.markerBoxG.currentIndexChanged['QString'].connect(self.showGammaMarkers)
		self.markerActionG.setDefaultWidget(self.markerBoxG)
		menu.addAction(self.markerActionG)


		#Graph Colour
		self.traceRow = traceRowWidget(self.curve)

		self.colAction = QtWidgets.QWidgetAction(menu)
		self.colAction.setDefaultWidget(self.traceRow)
		menu.addAction(self.colAction)
		
		#TRACE2
		self.traceRow2 = traceRowWidget(self.curve2)
		self.colAction2 = QtWidgets.QWidgetAction(menu)
		self.colAction2.setDefaultWidget(self.traceRow2)
		menu.addAction(self.colAction2)

		# Quit
		menu.addAction('Exit', self.askBeforeQuit)

		self.pushbutton.setMenu(menu)
		self.extraLayout.addWidget(self.pushbutton)
		#self.statusBar.addPermanentWidget(self.pushbutton)
		self.deviceSelector = self.portSelectionDialog()

	def changeActiveTrace(self,s):
		if self.p.activeSpectrum.datatype=='list':
			if self.p.activeSpectrum.parameters==2:
				try:
					num = int(str(s).split(':')[-1])
					self.p.activeSpectrum.selectDataset(num-1)
				except:
					pass

	'''
	def updateTraceList(self,traces):
		self.activeTrace.clear()
		for a in traces:
			self.activeTrace.addItem(a)

	def pileUpRejection(self,state):
		if not self.checkConnectionStatus():return
		if self.p.PILEUP_REJECT_ENABLED:
			self.p.pileupRejection(state)

	def externalGate(self,state):
		if not self.checkConnectionStatus():return
		if self.p.EXTERNAL_TRIGGER_ENABLED:
			self.p.externalGate(state)
	'''
	def initPressureMonitor(self):
		if not self.checkConnectionStatus():return [0,0,0]
		return self.p.BMP280_init()
	def readPressureMonitor(self):
		if not self.checkConnectionStatus():
			return [0,0,0]
		return self.p.BMP280_all()
		

	def setPlotColor(self,state):
		self.switchingPlot = True
		if state: #Light background
			self.createMainPlot('w','k')
		else:
			self.createMainPlot()
		self.switchingPlot = False

	def showTrendline(self):
		print('generating trendline')
		order = 2
		x= self.p.activeSpectrum.xaxis(self.calibrationEnabled)
		z = np.polyfit(x, self.y, order)
		p= np.poly1d(z)

		pen=pg.mkPen('r', width=5)
		self.trendline.setData(x,p(x),pen=pen)

	def setAutoUpdateInterval(self,val):
		self.showStatus("Updated auto-refresh interval to %d seconds"%val,False)
		self.pending['update'] = myTimer(val)
		
	def autoUpdateEnable(self,state):
		self.progressBar.setValue(0)
		self.progressBar.setEnabled(state)
		if state:
			self.pending['update'].reset()

	def updateEverything(self):
		# For diagnostics 
		#if self.regionWindow.saveAllCheckbox.isChecked():
		#	if self.pending['datadump'].ready():
		#		self.dataDump()

		self.locateDevices()
		#self.setTheme("default")
		if not self.checkConnectionStatus():return
		if self.progressBar.isEnabled():
			self.progressBar.setValue(int(self.pending['update'].progress()))

		if self.pending['status'].ready():
			self.updateStatus()

		if self.pending['autostop'].ready():
			self.p.stopHistogram()
			self.pending['autostop'].deactivate()
			self.showStatus('Stopped Acquisition',True)
			self.load()


		if self.currentMonitorAvailable:
			if self.pending['current'].ready():			
				self.updateCurrent()

		if self.p.VOLTMETER_ENABLED:
			if self.pending['temperature'].ready():			
				pass#self.updateTemperature()

		if self.switchingPlot: #Skip this if the plot is being regenerated with new colours
			return

		if self.autoUpdateBox.isChecked() and self.currentState:#Only do this if it's running
			if self.pending['update'].ready():			
				self.load()

				if self.pending['halflife'].ready():			
					vals = self.summationRaw()
					T = self.decayHandler.getElapsedTime()
					for a in vals:
						a[0].appendPoint (T,a[3])
				if self.regionWindow.saveAllCheckbox.isChecked():
					if self.pending['datadump'].ready():
						self.dataDump()

	def halflifeTime(self):
		self.pending['halflife'] = myTimer(self.regionWindow.decayInterval.value())
		self.showStatus('Count logging interval changed to %s Seconds'%(self.regionWindow.decayInterval.value()) )

	def load(self):
		if not self.checkConnectionStatus(True):return
		try:
			self.p.sync() #Get latest data from the hardware. List/Hist.
			if self.p.activeSpectrum.datatype=='list':
					self.y = self.p.activeSpectrum.getHistogram(trace=0)
					if self.p.activeSpectrum.parameters==2: #fetch second one as well
						self.y2 = self.p.activeSpectrum.getHistogram(trace=1)
			else: #Single parameter list / histogram.
				self.y = self.p.activeSpectrum.getHistogram(trace=0)

			#self.showStatus("System Status | Data Refreshed : %s"%time.ctime())
			T = self.pending['autostop']
			T = time.time() - self.startTime
			m, s = divmod(T, 60)
			h, m = divmod(m, 60)
			ST = "%d:%02d:%02d" % (h, m, s)
			self.clearButton.setText('CLEAR %s'%(ST))
			self.clearFits()
			
			self.offlineData  = False

			self.refreshPlot()
			self.recordToHistory(resetTemperature=True)

		except Exception as e:
			self.showStatus("System Status | Load Error %s"%str(e),True)

	def recordToHistory(self,**kwargs):
		self.spectrumTime = time.time()- self.startTime
		TIME = kwargs.get('time',self.spectrumTime)
		TEMP = kwargs.get('temp',self.temperature.get())
		if kwargs.get('resetTemperature',False):self.temperature.clear()

		self.historyWindow.addSpectrum(np.copy(self.p.activeSpectrum.getHistogram()), time = TIME,temp = TEMP)

	def insertRegion(self):
		R = decayTools.regionWidget(self.plot,self.deleteRegion,self.p.activeSpectrum.calPolyInv if self.calibrationEnabled else np.poly1d([1,0]),len(self.regionWindow.regions))
		self.calibrationChanged.connect(R.updateCalibration)
		self.regionWindow.widgetLayout.addWidget(R)
		self.regionWindow.regions.append(R)

	def removeRegion(self):
		#simply switch to the second tab which shows the region list
		if len(self.regionWindow.regions):
			self.regionWindow.show() #tabWidget.setCurrentWidget(self.additionalParameters)
			self.regionWindow.activateWindow() #tabWidget.setCurrentWidget(self.additionalParameters)
		else:
			self.showStatus("No more regions available for deletion",True)
	def showMainTab(self):
		self.tabWidget.setCurrentWidget(self.mainTab)
		
	def deleteRegion(self,R):
		#R.setParent(None)
		self.regionWindow.regions.remove(R)
		self.showStatus("Deleted Region",True)

	def locateDevices(self):
		try:L = MCALib.getFreePorts(self.p.portname)
		except Exception as e:print(e)
		total = len(L)
		menuChanged = False
		if L != self.shortlist:
			menuChanged = True

			self.deviceSelector.setList(L,self.p)
			#Check for, and handle disconnect event
			if self.p.connected:
				if platform.system() == "Windows": return #Ignore disconnect event on windows
				if self.p.portname not in L:
						self.showStatus('Device Disconnected',True)
						self.setWindowTitle('Error : Device Disconnected')
						QtWidgets.QMessageBox.warning(self, 'Connection Error', 'Device Disconnected. Please check the connections')
						try:
							self.p.portname = None
							self.p.fd.close()
						except:pass
						self.p.connected = False

			elif True in L.values():
				reply = QtWidgets.QMessageBox.question(self, 'Connection', 'Device Available. Connect?', QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
				if reply == QtWidgets.QMessageBox.Yes:
					self.initializeCommunications()

			#update the shortlist
			self.shortlist=L

		
	####################

	def selectDevice(self):
		if self.deviceSelector.exec_():
			self.initializeCommunications(port = self.deviceSelector.getSelection())


	class portSelectionDialog(QtWidgets.QDialog):
		def __init__(self,parent=None):
			super(AppWindow.portSelectionDialog, self).__init__(parent)
			self.button_layout = QtWidgets.QVBoxLayout()
			self.setLayout(self.button_layout)
			self.btns=[]
			self.doneButton = QtWidgets.QPushButton("Done")
			self.button_layout.addWidget(self.doneButton)
			self.doneButton.clicked.connect(self.finished)
			

		def setList(self,L,handler):
			for a in self.btns:
				a.setParent(None)
				del a
			self.btns=[]

			self.button_group = QtWidgets.QButtonGroup()

			#moods[0].setChecked(True)
			pos=0
			for i in L:
				# Add each radio button to the button layout
				btn = QtWidgets.QRadioButton(i)
				self.button_layout.addWidget(btn)
				self.btns.append(btn)
				if handler:
					if handler.connected:
						if handler.portname == i:
							btn.setStyleSheet("color:green;")
				if not L[i]: #Port in use
					btn.setEnabled(False)

				self.button_group.addButton(btn, pos)
				pos+=1

			# Set the layout of the group box to the button layout

		#Print out the ID & text of the checked radio button
		def finished(self):
			if self.button_group.checkedId()!= -1:
				self.done(QtWidgets.QDialog.Accepted)
		def getSelection(self):
			if self.button_group.checkedId()!= -1:
				return self.button_group.checkedButton().text()
			else:
				return False

	def checkConnectionStatus(self,dialog=False):
		if self.p.connected:return True
		else:
			if dialog: QtWidgets.QMessageBox.warning(self, 'Connection Error', 'Device not connected. Please connect an MCA to the USB port')
			return False
			
	def sqr1(self):
		if not self.checkConnectionStatus(True):return
		val,ok = QtWidgets.QInputDialog.getDouble(self,"Set Square Wave", 'Enter Frequency for 10% square wave(10Hz - 100KHz)',20e3,0,100e3)
		if ok :
			if val<8e6:
				self.p.setSqr1(val,10)

	def setCut(self):
		if self.p.activeSpectrum.datatype=='hist':
			QtWidgets.QMessageBox.information(self, 'Not Available', 'Not for histogram data. Only list mode.')
			return
		
		if not len(self.regionWindow.regions):
			QtWidgets.QMessageBox.information(self, 'Not Available', 'No region inserted. Press R to insert and position')
			return

		start,end=self.regionWindow.regions[0].region.getRegion() #choose the first region
		b1text = 'Set trace 1(blue) to only events where trace 2(red) is between %.1f and %.1f'%(start,end)
		b2text = 'Set trace 2(red) to only events where trace 1(blue) is between %.1f and %.1f'%(start,end)
		self.gateDialog = regionPopup.gateDialog(self,b1 = b1text, b2= b2text)
		self.gateDialog.setStyleSheet('color:black');
		retval = self.gateDialog.exec_()
		if not retval:
			return
		option = self.gateDialog.options.checkedId()
		print(option)
		if option == -2 : #option 1
			self.setCutRegion(0)
		elif option == -3 : #option 2
			self.setCutRegion(1)
		elif option == -4 : #option 3  . reset all gates
			self.setCutRegion(-1)
		else:
			QtWidgets.QMessageBox.information(self, 'Not Available', 'Please select one')
			


	def setCutRegion(self,channel=0):
		if self.p.activeSpectrum.datatype=='hist':
			print('not for histograms')
			return
		start,end=self.regionWindow.regions[0].region.getRegion() #choose the first region
		if channel == -1: #reset gates
			start =0; end=0; channel = 0 
		self.p.activeSpectrum.cut(start,end,trace = channel)
		self.toggleLog(self.logBox.isChecked())
		self.calibrateOnOff.setChecked(False)
		self.calibrateOnOff.setChecked(True)


	def setParameter(self):
		if not self.checkConnectionStatus(True):return
		val,ok = QtWidgets.QInputDialog.getText(self,"Set Parameter", 'Enter Parameter name')
		if ok :
				val2,ok = QtWidgets.QInputDialog.getInt(self,"Enter Value", 'Enter Parameter Value')
				if ok:
					val = str(val.strip())
					self.p.setParameter(val.upper(), val2)

	def writeFlash(self):
		if not self.checkConnectionStatus(True):return
		try:
			val = self.p.readBulkFlash(2000)
			val = val.split(b'\0')[0]
			val = val.decode()
		except:
			val = 'enter conf...'
		val,ok = QtWidgets.QInputDialog.getMultiLineText(self,"Edit Configuration", 'Enter Configuration Text',val)
		if ok :
			val = str(val.strip())
			self.p.writeBulkFlash(val+'\0')


	def set_threshold(self):
		if not self.checkConnectionStatus(True):return
		val,ok = QtWidgets.QInputDialog.getInt(self,"Set Threshold", 'Enter Number of initial channels to reject [0 -> x].',self.p.threshold,0,4000)
		if ok :
			self.p.setThreshold(val)

	def setOpacity(self):
		val,ok = QtWidgets.QInputDialog.getDouble(self,"Set Opacity", 'Enter Opacity (in %)',100,20,100)
		if ok :
			self.setWindowOpacity(val/100.)

	def closeEvent(self, evnt):
		evnt.ignore()
		self.askBeforeQuit()

	def askBeforeQuit(self):
		self.calibWindow.close()
		reply = QtWidgets.QMessageBox.question(self, 'Warning', 'Really quit?', QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
		if reply == QtWidgets.QMessageBox.Yes:
			global app
			#self.timer.stop()
			app.quit()
			#sys.exit()

	def pulseStretch(self):
		if self.pulseStretchState:
			self.pulseStretchState = False
			self.pulseStretchButton.setText('PULSE')
		else:
			self.pulseStretchState = True
			self.pulseStretchButton.setText('STRETCHED')
			
	def updateStatus(self):
		if not self.checkConnectionStatus():
			self.countLabel.setText('Not Connected')
			return
		try:
			state,cnt = self.p.getStatus()
			self.currentState = state
			if self.vacuum_enabled :
				if self.vacMonitor.isVisible():
					self.vacMonitor.setValue(self.vacMonitor.read())

			if not self.currentState: #Histogram acquisition is paused.
				if self.p.SCOPE_ENABLED and self.SCOPE_ENABLED and time.time() > self.scope_ready_time:
					self.pulsePlotFrame.show()
					NS = 2000
					TG = 0.5
					w = 40
					y = self.p.calPoly10(self.p.__retrieveBufferData__(0, self.p.samples))
					y = self.p.get_filtered_pulse(y,w)
					x = np.linspace(0, 1e-3 * self.p.timebase * len(y), w)
					if(y.max()>0.05):
						pen = pg.mkPen((255,255,0), width=2)
						self.pulseCurve.setData(x,y, pen=pen)									
					self.p.capture_init(0, NS, TG, self.pulseStretchState)
					#time.sleep(1e-6 * self.p.samples * self.p.timebase + 0.1)
					self.scope_ready_time = time.time()+1e-6 * self.p.samples * self.p.timebase + 0.1

				return

			self.pulsePlotFrame.hide()
			self.pulseRateCounter.addPoint(time.time(),cnt)
			self.rateMonitor.setValue(self.pulseRateCounter.getBothRates())
			#self.rateMonitor.setValue([self.pulseRateCounter.getRate()])
			if self.p.activeSpectrum.datatype=='list':
				self.p.sync()
			
			#state,cnt = self.p.getStatus()
			#self.currentState = state
			if self.p.activeSpectrum.datatype=='list':
				T = time.time()-self.startTime
				if self.p.activeSpectrum.parameters==2:
					A = np.sum(self.p.activeSpectrum.spectra[0].data)
					B = np.sum(self.p.activeSpectrum.spectra[1].data)
					C = self.p.activeSpectrum.totalCoincidences

					if self.surfacePlot.isVisible():
						self.surfacePlot.setData(self.p.activeSpectrum.HISTOGRAM2D)
						self.surfacePlot.countA.display(A)
						self.surfacePlot.countB.display(B)
						self.surfacePlot.countC.display(C)

						self.surfacePlot.labelA.setText('/%d [%.2f%%]'%(A+B,100*A/(A+B)))
						self.surfacePlot.labelB.setText('/%d [%.2f%%]'%(A+B,100*B/(A+B)))

						self.coincidenceLabel.setText('C: %d [%d , %d]'%(C,A,B) )


					self.coincidenceLabel.setText('C: %d [%d , %d]'%(self.p.activeSpectrum.totalCoincidences,A,B) )
				self.countLabel.setText('%s: %d'%("%d in %dS"%(self.p.activeSpectrum.totalCoincidences,T) if state else "Paused",cnt))
			else:
				self.countLabel.setText('%s: %d'%("Running" if state else "Paused",cnt))
		except Exception as e:
			self.countLabel.setText('Disconnect!')
			print(e)
			self.showStatus('Device Disconnected',True)
			if platform.system() == "Windows": 
				QtWidgets.QMessageBox.warning(self, 'Connection Error', 'Device Disconnected. Please check the connections')
				try:
					self.p.portname = None
					self.p.fd.close()
					self.p.connected = False
				except:pass

			#self.p.fd.close()

	def updateCurrent(self):
		if not self.checkConnectionStatus():
			self.currentLabel.setText('Device not Connected')
			return
		V = self.p.getCCS()
		self.currentLabel.setText('Source Preparation: %.3fV'%(V))
		if V>2.5 or V<0.1:self.currentLabel.setStyleSheet("QLabel{color:red}");
		else:self.currentLabel.setStyleSheet("QLabel{color:#8F8}");

	def updateTemperature(self):
		if not self.checkConnectionStatus():
			self.temperatureLabel.setText('Device not Connected')
			return
		T = self.p.getTemperature()
		self.temperature.add(T)
		self.temperatureLabel.setText('Temperature: %.1f C(%.2f)'%(T,self.temperature.get()))
		#if V>2.5 or V<0.1:self.currentLabel.setStyleSheet("QLabel{color:red}");
		#else:self.currentLabel.setStyleSheet("QLabel{color:#8F8}");


	def clearCount(self):
		'''
		Reset the total pulse counter
		'''
		if not self.checkConnectionStatus(True):return
		self.p.startCount()
	def launchRateMonitor(self):
		self.rateMonitor.launch()

	def stateHighlight(self,state):
		self.startButton.setProperty("class", "active" if state else "") ; self.startButton.style().unpolish(self.startButton); self.startButton.style().polish(self.startButton)
		self.pauseButton.setProperty("class", "" if state else "active") ; self.pauseButton.style().unpolish(self.pauseButton); self.pauseButton.style().polish(self.pauseButton)

	def start(self):
		if not self.checkConnectionStatus(True):return
		
		self.SCOPE_ENABLED = False

		self.startDialog = regionPopup.startDialog(self,threshold = self.p.threshold,autoRefresh = self.autoUpdateTimerInterval.value())
		retval = self.startDialog.exec_()
		if not retval:
			return
		self.p.threshold = self.startDialog.getThreshold()
		self.autoUpdateTimerInterval.setValue(self.startDialog.getRefreshInterval())
		stoptime = self.startDialog.stopBox.value()
		self.showStatus("System Status | Acquisition Started : %s"%time.ctime())

		if self.startDialog.clearBox.isChecked():
			self._clear()
		self.p.setThreshold(self.p.threshold)

		if stoptime != 0:
			self.pending['autostop'].reset(stoptime)
			self.showStatus("Acquisition Started : %s. Stop after %d seconds"%(time.ctime(),stoptime))
			print('acquisition will automatically stop after %d seconds'%stoptime)


		if self.p.SCOPE_ENABLED:
			self.pulsePlotFrame.hide()

		self.p.startHistogram()
		self.stateHighlight(True)
		self.pulseRateCounter.clear()
		
	def pause(self):
		if not self.checkConnectionStatus(True):return
		self.showStatus("System Status | Acquisition Stopped : %s"%time.ctime())
		self.p.stopHistogram()
		self.stateHighlight(False)
		self.SCOPE_ENABLED = True

	def clear(self):
		reply = QtWidgets.QMessageBox.question(self, 'Warning', 'Clear the entire histogram?\nThis will erase data stored in the hardware also.', QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
		if reply == QtWidgets.QMessageBox.Yes:
			self._clear()

	def _clear(self):
			self.clearPlot()
			self.clearAllSums()
			self.p.activeSpectrum.clearData()
			self.showStatus("System Status | Data cleared : %s"%time.ctime())
			if not self.checkConnectionStatus():return
			self.p.clearHistogram()
			self.clearCount()
			self.pending['update'].reset()
			self.historyWindow.clear()
			self.temperature.clear()

	def clearPlot(self):
		#if not self.checkConnectionStatus(True):return
		self.y=[];self.y2=[];
		self.curve.clear();self.curve2.clear();
		self.trendline.clear();
		self.clearFits()

		self.markerarrow.setPos(0,0)
		self.startTime = time.time()
		self.clearButton.setText('CLEAR')

	def clearFits(self):
		for a in self.fitcurves:
			a.clear()
			self.plot.removeItem(a)
		self.fitcurves=[]
		
	def showStatus(self,msg,error=None):
		if error: self.statusBar.setStyleSheet("color:#F77")
		else: self.statusBar.setStyleSheet("color:#000000")
		self.statusBar.showMessage(msg)

	def toggleLog(self,state):
		if not self.p: return
		if not self.p.activeSpectrum: return
		self.p.activeSpectrum.setLog(state)
		if state:
			self.plot.getAxis('left').setLabel('Log(Count)')
		else:
			self.plot.getAxis('left').setLabel('Count')

		if self.p.activeSpectrum.datatype=='list':
			self.y = self.p.activeSpectrum.getHistogram(trace=0)
			if self.p.activeSpectrum.parameters==2:
				self.y2 = self.p.activeSpectrum.getHistogram(trace=1)
		else: #Single parameter list / histogram.
			self.y = self.p.activeSpectrum.getHistogram(trace=0)

		self.refreshPlot()

	def launch3D(self):
		self.surfacePlot.show()

	def refreshPlot(self):
		x = self.p.activeSpectrum.xaxis(self.calibrationEnabled)
		if self.plotAEnabled.isChecked():
			self.curve.setData(x,self.y[:-1], stepMode='center', fillLevel=0,pen = self.pen,brush=self.brush)#, brush=brush,pen = pen)
		else:
			self.curve.clear()
		yMax = max(self.y[:-2])*1.05

		if self.p.activeSpectrum.datatype=='list':
			if self.p.activeSpectrum.parameters ==2:
				brush=(126, 97, 220,100)
				if  self.plotBEnabled.isChecked():
					self.curve2.setData(x,self.y2[:-1], stepMode=True, fillLevel=0, brush=brush,pen = self.pen2)
				else:
					self.curve2.clear()
				yMax = max( max(self.y[:-2]), max(self.y2[:-2]))*1.05
			
		self.plot.setLimits(xMax=max(x)*1.1,yMax = max(10,yMax)*1.05)
		self.plot.setYRange(0,max(10,yMax)*1.05)

		self.plot.getAxis('bottom').setLabel(self.p.activeSpectrum.get_xlabel())

	##################  SUMMATION ROUTINES #################
	def showRegionWindow(self):
		self.regionWindow.show()
		self.regionWindow.activateWindow() #tabWidget.setCurrentWidget(self.additionalParameters)
	def getData(self):
		return self.p.activeSpectrum.xaxis(self.calibrationEnabled),self.p.activeSpectrum.getHistogram()

	def summationRaw(self):
		sums = []
		x = self.p.activeSpectrum.xaxis(self.calibrationEnabled)
		YDATA = self.p.activeSpectrum.getHistogram()
		for a in self.regionWindow.regions:
			start,end=a.region.getRegion()
			start = self.closestIndex(x,start)
			end = self.closestIndex(x,end)
			sums.append([a,x[start],x[end],sum(YDATA[start:end])])
		return sums


	def selectTraceManually(self):
		if self.p.activeSpectrum.datatype=='list':
			if self.p.activeSpectrum.parameters==2:
				msgbox = QtWidgets.QMessageBox()
				msgbox.setIcon(QtWidgets.QMessageBox.Information)
				msgbox.setText('Set the dataset for this operation[Default 1]')
				msgbox.setWindowTitle("Select Input")
				msgbox.addButton(QtWidgets.QMessageBox.Yes)
				msgbox.addButton(QtWidgets.QMessageBox.No)
				msgbox.button(msgbox.No).setText("Input 1(Blue)")
				msgbox.button(msgbox.Yes).setText("Input 2(Red)")
				reply = msgbox.exec_()
				if reply == QtWidgets.QMessageBox.No:
					print("Chose trace 1")
					self.changeActiveTrace("T:1")
					self.selectTraceButton.setText("Trace 1")
				else:
					print("Chose trace 2")
					self.changeActiveTrace("T:2")
					self.selectTraceButton.setText("Trace 2")


	def summation(self):
		self.selectTraceManually()
		vals = self.summationRaw()
		msg = ''
		if vals == []: #No regions present / x is empty
				msg = ' Data Unavailable. Please select a peak using the region utility. '

		for a in vals:
			region,start,end,count = a
			msg += u'\u2211[%.2f:%.2f] : %d\n'%(start,end,count)
		QtWidgets.QMessageBox.information(self, 'Summation (Region) ', msg)
	def clearAllSums(self):
		for a in self.regionWindow.regions:
			a.clearData()

	def saveAllSums(self):
		for a in self.regionWindow.regions:
			print(a)




	def fit(self,**kwargs):
		#self.calibWindow.show()
		self.selectTraceManually()

		if not self.p.activeSpectrum.hasData():
			QtWidgets.QMessageBox.information(self, 'Data Unavailable ', 'please acquire a spectrum')
			return
		elif len(self.regionWindow.regions)==0:
			QtWidgets.QMessageBox.information(self, 'Regions Unavailable ', 'Please insert regions and center them around the peaks to be fitted.')
			#self.regionLabel.color_anim.start()
			return
		tail = kwargs.get('fitTail',self.lowTailBox.isChecked())
		fitres = []
		if not len(self.regionWindow.regions):return

		self.clearFits()

		YDATA = self.p.activeSpectrum.getHistogram()
		for R in self.regionWindow.regions:
			try:
				if not tail:  # REGULAR GAUSSIAN
					try:
						x = self.p.activeSpectrum.xaxis(self.calibrationEnabled)
						res = fitting.gaussfit(x,YDATA,R.region.getRegion())
					except:
						res = None
					if res is None:
						continue
					Xmore,Y,par,FIT = res

					fitcurve = pg.PlotCurveItem(name = 'Fit',pen = [255,0,0]);self.plot.addItem(fitcurve)
					self.fitcurves.append(fitcurve)
					fitcurve.setData(Xmore,Y, stepMode=False,fillLevel=0, brush=(126, 197, 220,100)) #Curve
					#QtWidgets.QMessageBox.critical(self, 'Fit Results', msg)
					msg = 'Amplitude= %5.1f  Centroid= %5.2f  sigma = %5.2f'%(par[0], par[1], par[2])
					if self.calibrationEnabled: FIT['channel'] = self.p.activeSpectrum.calPolyInv(par[1])
					else: FIT['channel'] = par[1]
					fitres.append(FIT)
				else:
					x = self.p.activeSpectrum.xaxis(self.calibrationEnabled)
					res = fitting.gausstailfit(x,YDATA,R.region.getRegion())
					if res is None:
						continue
					Xmore,Y,par,FIT = res

					fitcurve = pg.PlotCurveItem(name = 'Fit',pen = [255,0,0]);self.plot.addItem(fitcurve)
					self.fitcurves.append(fitcurve)

					fitcurve.setData(Xmore,Y, stepMode=False,fillLevel=0, brush=(126, 197, 220,100)) #Curve
					msg = 'Amplitude= %5.1f  Centroid= %5.2f  S = %5.2f G = %5.2f'%(par[0], par[1], par[2], par[3])
					if self.calibrationEnabled: FIT['channel'] = self.p.activeSpectrum.calPolyInv(par[1])
					else: FIT['channel'] = par[1]
					fitres.append(FIT)
					
			except Exception as e:
				QtWidgets.QMessageBox.critical(self, 'Fit Failed', str(e))
		
		self.calibWindow.show()
		self.calibWindow.setFitList(fitres)
		
	def fitWithTail(self):
		self.fit(fitTail=True)

	def showCalibrationEditor(self):
		self.calibWindow.show()

	def toggleCalibration(self,state):
		self.calibrationEnabled = state
		self.currentPeak = None			
		self.clearFits()
		self.markerarrow.setPos(0,0)

		x = self.p.activeSpectrum.xaxis(self.calibrationEnabled,trace=0) #first trace
		
		self.plot.setLimits(xMax=max(x) );self.plot.setXRange(0,max(x) )
		if state: #Calibration needs to be applied
			self.plot.getAxis('bottom').setLabel('Energy (KeV)')
			self.calibrationChanged.emit(self.p.activeSpectrum.calPoly,self.p.activeSpectrum.calPolyInv)
		else:
			'''
			Calibration reset on the graph. but user defined calibration is not reset to original values.
			'''
			self.calibrationChanged.emit(np.poly1d([1,0]),np.poly1d([1,0])) #reset calibration
			self.plot.getAxis('bottom').setLabel('Channel Number')

		self.plot.setLimits(xMax=max(x)*1.05 ); self.plot.setXRange(0,max(x)*1.05 ); self.plot.setYRange(0,max(self.y)*1.05)
		self.curve.setData(np.array(x),self.y[:-1], stepMode=True, fillLevel=0,pen=self.pen, brush=self.brush)
		if self.p.activeSpectrum.datatype=='list':
			if self.p.activeSpectrum.parameters==2:
				x = self.p.activeSpectrum.xaxis(self.calibrationEnabled,trace=1) #xaxis for second plot.
				self.curve2.setData(np.array(x),self.y2[:-1], stepMode=True, fillLevel=0, brush=(0,0,255,150))

	def addSelectedPoint(self):
		if not self.currentPeak:
			QtWidgets.QMessageBox.critical(self, 'Peak not selected', 'Please locate a peak first, by clicking on it<br>Then apply the calibration after typing its known energy')
			return
		msg=''


	def setCalibration(self,**kwargs):
		if not self.p.activeSpectrum.hasData():
			return
		###	
		points = self.calibWindow.getCalibrationPoints()
		if len(points)>1:
			self.p.setCalibration(points)
			self.calibrateOnOff.setToolTip(_translate("MainWindow",'''
			<html><head/><body>
			<p><span style=\" font-size:14pt;color:#939\">Polynomial:%s</span></p>
			<p><span style=\" font-size:12pt;\">Enable/Disable the calibration polynomial.</span></p>
			<p><span style=\" font-size:12pt;\">Switch to the calibration tab for details</span></p>
			</body></html>'''%(self.p.activeSpectrum.calPoly)))

		###
		self.calibrateOnOff.setChecked(True)
		self.toggleCalibration(True) # refresh plots etc.
		msg = kwargs.get('msg','Calibration Enabled')
		self.showStatus(msg,True)


	def onClick(self,event):
		if not self.p.activeSpectrum.hasData():return
		if not len(self.y): return
		pos = event.scenePos()
		if self.plot.sceneBoundingRect().contains(pos):
			mousePoint = self.plot.plotItem.vb.mapSceneToView(pos)
			index = mousePoint.x()
			#XR = self.plot.plotItem.vb.viewRange()[0]
			#XR = (XR[1]-XR[0])/30.
			#if(len(self.regions)):
			#	self.regions[-1].region.setRegion([index-XR,index+XR])
			if self.p.activeSpectrum.hasData:
				x = self.p.activeSpectrum.xaxis(self.calibrationEnabled)
				P = (np.abs(x - index ) ).argmin()

				self.markerarrow.setPos(x[P],self.y[P])
				self.currentPeak = x[P]
				self.showStatus("Selected Peak  >  X : %.2f(%d) , Y : %.2f"%(x[P],P,self.y[P]))
		else:
			self.markerarrow.setPos(0,0)
			self.currentPeak = None
			self.showStatus("Unselected Peak")

	def closestIndex(self,arr,val):
		return (np.abs(arr-val)).argmin()

	def mouseMoved(self,event):
		if not self.p.activeSpectrum.hasData():return
		if not len(self.y): return
		pos = event[0]
		if self.plot.sceneBoundingRect().contains(pos):
			mousePoint = self.plot.plotItem.vb.mapSceneToView(pos)
			index = mousePoint.x()
			x = self.p.activeSpectrum.xaxis(self.calibrationEnabled)
			P = self.closestIndex(x,index)
			self.arrow.setPos(x[P],self.y[P])
			if self.vLine:
				self.vLine.setPos(mousePoint.x())
				self.chanLabel.setText('[x=%0.1f, %d]' % (mousePoint.x(), self.y[P]))
			#self.chanLabel.setPos(mousePoint.x(),self.y[P]+1)

	def save(self):
		if self.p.activeSpectrum.datatype=='list':
			from utilities import plotSaveWindow
			comments = 'Histogram (X, Y)\n'
			info = plotSaveWindow.AppWindow(self,[[self.p.activeSpectrum.xaxis(self.calibrationEnabled),self.p.activeSpectrum.getHistogram()]],self.plot,comments = comments)
		else:
			if not self.p.activeSpectrum.hasData():
				QtWidgets.QMessageBox.critical(self, 'Acquire Data', 'Please acquire some data first!')
				return
			from utilities import plotSaveWindow
			#info = plotSaveWindow.AppWindow(self,[self.curve,self.fitcurve],self.plot)
			comments = ''
			if len(self.fitcurves):
				for a in self.calibWindow.fitList:
					if a['centroid'] == a['channel']:
						centroidString = '%.2f'%(a['centroid'])
					else:
						centroidString = '%.2f keV (channel:%.2f)'%(a['centroid'],a['channel'])
					comments+="Region: %s\nAmplitude: %.2f\nCentroid: %s\nFWHM: %.3f(%.2f%%)\nArea: %.2f\n-----------"%(a['region'],a['amplitude'],centroidString,a['fwhm'],100*a['fwhm']/a['centroid'],a['area'])
				#info = plotSaveWindow.AppWindow(self,[[self.x,self.y]]+[a.getData() for a in self.fitcurves],self.plot,comments = comments)
			info = plotSaveWindow.AppWindow(self,[[self.p.activeSpectrum.xaxis(self.calibrationEnabled),self.y]],self.plot,comments = comments)
		info.show()


	def loadPlot(self,fname):
		self.offlineData  = True
		self.showStatus("Loaded File | %s  (Click UPDATE to return)"%fname,True)
		self.loadFromFile( self.plot,[self.curve],fname ,True) 
		self.tabWidget.setCurrentIndex(0)
		self.calibrateOnOff.setChecked(False)

	def loadFromFile(self,plot,curves,filename,histMode=True):
		self.p.loadFile(filename,self.removeCalBox.isChecked())
		#self.y = self.p.activeSpectrum.getHistogram(self.logBox.isChecked()) # No need. The togglelog function will set it.
		self.toggleLog(self.logBox.isChecked())
		self.clearFits()

		head, tail = os.path.split(filename)
		#self.updateTraceList(['%s'%tail])

		#self.recordToHistory(time = self.spectrumTime)

	def loadList(self,fname):
		self.offlineData  = True
		self.showStatus("Loaded File | %s  (Click UPDATE to return)"%fname,True)
		self.p.loadListFile(fname,self.removeCalBox.isChecked())
		
		traces = []
		head, tail = os.path.split(self.p.activeSpectrum.filename)
		for b in range(self.p.activeSpectrum.parameters):
			traces.append('%s:%d'%(tail,b+1))
		#self.updateTraceList(traces)
		self.clearPlot()
		self.toggleLog(self.logBox.isChecked())
		self.tabWidget.setCurrentIndex(0)
		self.calibrateOnOff.setChecked(False)

		from utilities import plot3DTools
		if self.surfacePlot: 
			self.surfacePlot.close()
			del self.surfacePlot
		self.surfacePlot = plot3DTools.surface3d(self,self.p.activeSpectrum.HISTOGRAM2D,self.p.activeSpectrum.BINS2D)
		A = np.sum(self.p.activeSpectrum.spectra[0].data)
		B = np.sum(self.p.activeSpectrum.spectra[1].data)
		C = np.sum(self.p.activeSpectrum.HISTOGRAM2D)
		self.surfacePlot.countA.display(A)
		self.surfacePlot.countB.display(B)
		self.surfacePlot.countC.display(C)

		self.surfacePlot.labelA.setText('/%d [%.2f%%]'%(A+B,100*A/(A+B)))
		self.surfacePlot.labelB.setText('/%d [%.2f%%]'%(A+B,100*B/(A+B)))

		self.coincidenceLabel.setText('C: %d [%d , %d]'%(C,A,B) )

		self.listFrame.show()
		self.surfacePlot.show()
	
	def loadFromMemory(self,mem,BINS):
		data_2d = np.memmap(mem, dtype='int64', mode='r',shape = (BINS,BINS))
		from utilities import plot3DTools
		if self.surfacePlot: 
			self.surfacePlot.close()
			del self.surfacePlot
		self.surfacePlot = plot3DTools.surface3d(self,data_2d,BINS)

		self.listFrame.show()
		self.surfacePlot.show()
		
	def setListSaveFilename(self):
		path, _filter  = QtWidgets.QFileDialog.getSaveFileName(self, 'Specify filename to dump list data', '~/')
		if path:
			if self.p.activeSpectrum.datatype == 'list':
				self.p.activeSpectrum.setOutputFilename(path)
				self.showStatus("List data being saved to:%s"%(path))
				
	def autoScale(self):
		xMin,xMax = self.p.activeSpectrum.getCalibratedRange()
		self.plot.setLimits(xMin = xMin, xMax=xMax,yMax = max(20,max(self.y)*1.1))
		self.plot.setXRange(xMin, xMax);self.plot.setYRange(0,max(20,max(self.y)*1.1))

	############ DATA DUMPING #############
	def changeDirectory(self):
		dirname = QtWidgets.QFileDialog.getExistingDirectory(self,"Select a folder in which spectra will be periodically saved", os.path.expanduser("./"),  QtWidgets.QFileDialog.ShowDirsOnly)
		if not dirname:return

		self.dataDumpPath=str(dirname)
		self.pathLabel.setText(self.dataDumpPath)

	def dataDumpTime(self):
		self.pending['datadump'] = myTimer(self.regionWindow.saveAllInterval.value()*60) #in minutes
		self.showStatus('Spectrum save interval changed to %s Minutes'%(self.regionWindow.saveAllInterval.value()) )

	def dataDump(self):
		dt = time.time() - self.startTime
		m, s = divmod(dt, 60)
		h, m = divmod(m, 60)
		ST = "%d:%02d:%02d" % (h, m, s)
		np.savetxt(os.path.join(self.dataDumpPath,'data_%.1fmins'%dt),np.column_stack([self.p.activeSpectrum.xaxis(self.calibrationEnabled),self.y]))
		self.regionWindow.savedSpectraCounter.setValue(self.regionWindow.savedSpectraCounter.value()+1)

	def enablePeriodicSpectrumSaving(self):
		if self.dataDumpPath is None:
			self.changeDirectory()
		if self.dataDumpPath is None:
			self.regionWindow.saveAllCheckbox.setChecked(False)
		

	######## WINDOW EXPORT SVG
	def exportSvg(self):
		from utilities.Qt import QtSvg
		path, _filter  = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '~/')
		if path:
			generator = QtSvg.QSvgGenerator()
			generator.setFileName(path)
			target_rect = QtCore.QRectF(0, 0, 800, 600)
			generator.setSize(target_rect.size().toSize())#self.size())
			generator.setViewBox(self.rect())
			generator.setTitle("Your title")
			generator.setDescription("some description")
			p = QtGui.QPainter()
			p.begin(generator)
			self.render(p)
			p.end()

	############ THUMBNAILS FOR DATA LOGGER ##########
		



def translators(langDir, lang=None):
	"""
	create a list of translators
	@param langDir a path containing .qm translation
	@param lang the preferred locale, like en_IN.UTF-8, fr_FR.UTF-8, etc.
	@result a list of QtCore.Qtranslator instances
	"""
	if lang==None:
			lang=QtCore.QLocale.system().name()
	result=[]
	qtTranslator=QtCore.Qtranslator()
	qtTranslator.load("qt_" + lang,
			QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath))
	result.append(qtTranslator)

	# path to the translation files (.qm files)
	sparkTranslator=QtCore.Qtranslator()
	sparkTranslator.load(lang, langDir);
	result.append(sparkTranslator)
	return result

def firstExistingPath(l):
	"""
	Returns the first existing path taken from a list of
	possible paths.
	@param l a list of paths
	@return the first path which exists in the filesystem, or None
	"""
	for p in l:
		if os.path.exists(p):
			return p
	return None

def common_paths():
	"""
	Finds common paths
	@result a dictionary of common paths
	"""
	path={}
	curPath = os.path.dirname(os.path.realpath(__file__))
	path["current"] = curPath
	sharedPath = "/usr/share/csmca"
	path["translation"] = firstExistingPath(
			[os.path.join(p, "lang") for p in
			 (curPath, sharedPath,)])
	path["utilities"] = firstExistingPath(
			[os.path.join(p,'utilities') for p in
			 (curPath, sharedPath,)])
	path["templates"] = firstExistingPath(
			[os.path.join(p,'utilities','templates') for p in
			 (curPath, sharedPath,)])

	path["splash"] = firstExistingPath(
			[os.path.join(p,'utilities','templates','splash.png') for p in
			 (curPath, sharedPath,)])
	path["themes"] = firstExistingPath(
			[os.path.join(p,'utilities','themes') for p in
			 (curPath, sharedPath,)])

	lang=str(QtCore.QLocale.system().name()) 
	shortLang=lang[:2]
	path["help"] = firstExistingPath(
			[os.path.join(p,'HELP') for p in
			 (os.path.join(curPath,"help_"+lang),
			  os.path.join(sharedPath,"help_"+lang),
			  os.path.join(curPath,"help_"+shortLang),
			  os.path.join(sharedPath,"help_"+shortLang),
			  os.path.join(curPath,"help"),
			  os.path.join(sharedPath,"help"),
			  )
			 ])
	return path

def showSplash(pth = "splash"):
	path = common_paths()
	# Create and display the splash screen
	splash_pix = QtGui.QPixmap(path[pth])
	splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
	splash.setMask(splash_pix.mask())

	progressBar = QtWidgets.QProgressBar(splash)
	progressBar.setStyleSheet('''

	QProgressBar {
		border: 2px solid grey;
		border-radius: 5px;	
		border: 2px solid grey;
		border-radius: 5px;
		text-align: center;
	}
	QProgressBar::chunk {
		background-color: #012748;
		width: 10px;
		margin: 0.5px;
	}
	''')
	progressBar.setMaximum(10)
	progressBar.setGeometry(0, splash_pix.height() - 50, splash_pix.width(), 20)
	progressBar.setRange(0,8)

	splash.show()
	splash.pbar = progressBar
	splash.show()
	return splash


if __name__ == "__main__":
	path = common_paths()
	from utilities.animTools import traceRowWidget
	app = QtWidgets.QApplication(sys.argv)
	#for t in translators(path["translation"]):
	#	app.installTranslator(t)

	# Create and display the splash screen
	splash = showSplash()
	splash.showMessage("<h2><font color='Black'>Initializing...</font></h2>", QtCore.Qt.AlignLeft, QtCore.Qt.black)

	for a in range(5):
		app.processEvents()
		time.sleep(0.01)

	#IMPORT LIBRARIES
	splash.showMessage("<h2><font color='Black'>Importing libraries...</font></h2>", QtCore.Qt.AlignLeft, QtCore.Qt.black)
	splash.pbar.setValue(1)
	import string,glob,functools

	splash.showMessage("<h2><font color='Black'>Importing communication library...</font></h2>", QtCore.Qt.AlignLeft, QtCore.Qt.black)
	import MCALib

	splash.showMessage("<h2><font color='Black'>Importing Numpy...</font></h2>", QtCore.Qt.AlignLeft, QtCore.Qt.black)
	splash.pbar.setValue(2)
	import numpy as np
	splash.showMessage("<h2><font color='Black'>Importing Scipy...</font></h2>", QtCore.Qt.AlignLeft, QtCore.Qt.black)
	splash.pbar.setValue(3)
	from scipy import optimize 
	from scipy.optimize import curve_fit,leastsq
	
	splash.showMessage("<h2><font color='Black'>Importing PyQtgraph...</font></h2>", QtCore.Qt.AlignLeft, QtCore.Qt.black)
	splash.pbar.setValue(4)
	import pyqtgraph as pg
	from pyqtgraph import exporters
	#pg.setConfigOptions(antialias=True, background='w',foreground='k')
	splash.showMessage("<h2><font color='Black'>Importing Utilities...</font></h2>", QtCore.Qt.AlignLeft, QtCore.Qt.black)
	splash.pbar.setValue(5)
	from utilities.fileBrowser import fileBrowser,PQG_ImageExporter
	try:
		import pyqtgraph.opengl as gl
		GL_ENABLED = True
	except:
		GL_ENABLED = False

	from utilities import calPopup,regionPopup,historyPopup
	from utilities import decayTools,fitting

	#RUN APP
	splash.showMessage("<h2><font color='Black'>Launching GUI...</font></h2>", QtCore.Qt.AlignLeft, QtCore.Qt.black)
	splash.pbar.setValue(6)
	myapp = AppWindow(app=app, path=path, splash=splash)
	myapp.show()
	splash.finish(myapp)
	r = app.exec_()
	app.deleteLater()
	sys.exit(r)



