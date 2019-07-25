import os,glob,re,fnmatch
from .Qt import QtGui,QtCore,QtWidgets
import numpy as np

from . templates import ui_fileBrowser as fileBrowser
import pyqtgraph as pg

import logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
logger = logging.getLogger(__name__)

__all__ = ['PQG_ImageExporter']

'''
This entire class is required because of a bug in pyqtgraph which has been fixed now btw.
solution edited from https://stackoverflow.com/questions/51262056/pyqtgraph-imageexporter-bug-related-to-image-size
I am using 		self.params = pg.exporters.ImageExporter(item).parameters()
instead of recreating params because I want the exporter to faithfully reproduce the appearance
'''
class PQG_ImageExporter(pg.exporters.Exporter):
	Name = "Image File (PNG, TIF, JPG, ...)"
	allowCopy = True

	def __init__(self, item):
		pg.exporters.Exporter.__init__(self, item)
		tr = self.getTargetRect()
		if isinstance(item, QtGui.QGraphicsItem):
			scene = item.scene()
		else:
			scene = item
		# scene.views()[0].backgroundBrush()

		self.params = pg.exporters.ImageExporter(item).parameters()
		self.params.param('width').sigValueChanged.connect(self.widthChanged)
		self.params.param('height').sigValueChanged.connect(self.heightChanged)

	def widthChanged(self):
		sr = self.getSourceRect()
		ar = float(sr.height()) / sr.width()
		self.params.param('height').setValue(
			self.params['width'] * ar, blockSignal=self.heightChanged)

	def heightChanged(self):
		sr = self.getSourceRect()
		ar = float(sr.width()) / sr.height()
		self.params.param('width').setValue(
			self.params['height'] * ar, blockSignal=self.widthChanged)

	def parameters(self):
		return self.params

	def export(self, fileName=None, toBytes=False, copy=False,**kwargs):
		if 'height' in kwargs:
			self.params.param('height').setValue(kwargs.get('height'), blockSignal=self.heightChanged)
			sr = self.getSourceRect()
			ar = float(sr.width()) / sr.height()
			self.params.param('width').setValue(kwargs.get('height') * ar, blockSignal=self.widthChanged)

		if fileName is None and not toBytes and not copy:
			filter = ["*."+bytes(f).decode('utf-8')
					  for f in QtGui.QImageWriter.supportedImageFormats()]
			preferred = ['*.png', '*.tif', '*.jpg']
			for p in preferred[::-1]:
				if p in filter:
					filter.remove(p)
					filter.insert(0, p)
			self.fileSaveDialog(filter=filter)
			return

		targetRect = QtCore.QRect(
			0, 0, self.params['width'], self.params['height'])
		sourceRect = self.getSourceRect()

		#self.png = QtGui.QImage(targetRect.size(), QtGui.QImage.Format_ARGB32)
		# self.png.fill(pyqtgraph.mkColor(self.params['background']))
		w, h = self.params['width'], self.params['height']
		if w == 0 or h == 0:
			raise Exception(
				"Cannot export image with size=0 (requested export size is %dx%d)" % (w, h))
		bg = np.empty((int(self.params['width']), int(
			self.params['height']), 4), dtype=np.ubyte)
		color = self.params['background']
		bg[:, :, 0] = color.blue()
		bg[:, :, 1] = color.green()
		bg[:, :, 2] = color.red()
		bg[:, :, 3] = color.alpha()
		self.png = pg.functions.makeQImage(bg, alpha=True)

		# set resolution of image:
		origTargetRect = self.getTargetRect()
		resolutionScale = targetRect.width() / origTargetRect.width()
		#self.png.setDotsPerMeterX(self.png.dotsPerMeterX() * resolutionScale)
		#self.png.setDotsPerMeterY(self.png.dotsPerMeterY() * resolutionScale)

		painter = QtGui.QPainter(self.png)
		#dtr = painter.deviceTransform()
		try:
			self.setExportMode(True, {
							   'antialias': self.params['antialias'], 'background': self.params['background'], 'painter': painter, 'resolutionScale': resolutionScale})
			painter.setRenderHint(
				QtGui.QPainter.Antialiasing, self.params['antialias'])
			self.getScene().render(painter, QtCore.QRectF(
				targetRect), QtCore.QRectF(sourceRect))
		finally:
			self.setExportMode(False)
		painter.end()

		if copy:
			QtGui.QApplication.clipboard().setImage(self.png)
		elif toBytes:
			return self.png
		else:
			self.png.save(fileName)


PQG_ImageExporter.register()


class fileBrowser(QtWidgets.QFrame,fileBrowser.Ui_Form):
	trace_names = ['#%d'%a for a in range(10)]
	trace_colors = [(0,255,0),(255,0,0),(255,255,100),(10,255,255)]
	textfiles=[]
	_browserPath = './'
	_pattern = '*'
	allowed_extensions = ['dat','csv','txt']
	def __init__(self,*args,**kwargs):
		super(fileBrowser, self).__init__()
		self.setupUi(self)
		if self.plotType.currentIndex()==0: 
			self.newPlotFrame.setVisible(False)

		self.thumbList = {}
		self.allowed_extensions = kwargs.get('extensions',self.allowed_extensions)

		self.thumbnailSubdir = kwargs.get('thumbnail_directory','thumbnails')
		self.loadHistogram = kwargs.get('clickCallback',None)
		self.recordToHistory = kwargs.get('recordToHistory',None)
		self._browserPath = kwargs.get('path',self._browserPath)

		self.app = kwargs.get('app',None)
		self.generateThumbnails()

	def itemDoubleClicked(self,sel):
		fname = self.thumbList[str(sel.text())][1]
		self.clickCallback( fname )

	def itemClicked(self,sel):
		fname = self.thumbList[str(sel.text())][1]
		self.comments.append('''<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt; color:#058879;">%s</span></p>\n'''%fname)
		with open(fname) as f:
			while True:
				header = f.readline().strip()
				if header[0]=='#':
					if len(header)>2:
						self.comments.append(header[1:])
					continue
				break
			self.comments.append('---------')

	def browseFile(self):
		filename = QtGui.QFileDialog.getOpenFileName(self," Open a data file", "", "Data Files (*.txt *.csv *.dat)")
		if filename:
			pcs = filename[0].split('.')
			if pcs[-1] in self.allowed_extensions:  #check if extension is acceptable 
				self.loadHistogram(filename[0]) 
			
	def changeDirectory(self):
		dirname = QtGui.QFileDialog.getExistingDirectory(self,"Load a folder containing data", os.path.expanduser(self._browserPath),  QtGui.QFileDialog.ShowDirsOnly)
		if not dirname:return
		self._browserPath=str(dirname)
		self.pathLabel.setText(self._browserPath)
		self.generateThumbnails(self._browserPath)
	
	def loadProject(self):
		###### For loading directories containing files which look like data_xxxmin.txt
		import fnmatch
		datadir = QtGui.QFileDialog.getExistingDirectory(self,"Load a folder containing timestamped files -> data_xxmins.txt/csv ", os.path.expanduser(self._browserPath))
		if datadir:
			files = os.listdir(datadir)
			files = self.sorted_alphanumeric(fnmatch.filter(files,'data_*.csv'))
			for a in files:
				try:
					self.loadHistogram(os.path.join(datadir,a))
					t = a.split('data_')[1]
					t = float(t.split('mins')[0])*60
					self.recordToHistory(time = t)
				except Exception as e:
					print (e)
		###### For testing spectrum history


	def patternChanged(self):
		self.generateThumbnails(self._browserPath)


	def clearThumbnails(self):
		for a in self.thumbList:
			self.listWidget.takeItem(self.listWidget.row(self.thumbList[a][0]))
		self.thumbList={}

	def sorted_alphanumeric(self,data):
		convert = lambda text: int(text) if text.isdigit() else text.lower()
		alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
		return sorted(data, key=alphanum_key)
		
	def generateThumbnails(self,directory='.',**kwargs):
		self.clearThumbnails()
		
		if directory=='.':directory = os.path.expanduser('~')
		self.app.processEvents()
		P2=pg.PlotWidget(enableMenu = False)
		curves = []
		for name,col in zip(self.trace_names,self.trace_colors):
			C=pg.PlotCurveItem(name = name);C.setPen(color=col, width=3)
			P2.addItem(C)
			curves.append(C)

		self.textfiles = []
		homedir = os.path.expanduser('~')
		thumbdir = os.path.join(homedir,self.thumbnailSubdir)
		if not os.path.isdir(thumbdir):
			#print ('Directory missing. Will create')
			os.makedirs(thumbdir)
		thumbFormat = 'png'
		#self.exporter = pg.exporters.ImageExporter(P2.plotItem)
		self.exporter = PQG_ImageExporter(P2.plotItem)

		# Get all files from PWD
		all_files = os.listdir(directory)
		pattern = str(self.pattern.text())
		# Make a reduced set based on matching parameters
		filtered_files = fnmatch.filter(all_files, pattern)
		files_to_show = self.sorted_alphanumeric(filtered_files)
		
		for a in files_to_show:
			pcs = a.split('.')
			if pcs[-1] in self.allowed_extensions:  #check if extension is acceptable 
				fname = ".".join(pcs[:-1])
				filepath = os.path.join(directory,a)
				timestamp = int(os.path.getctime(filepath))
				thumbpath = os.path.join(thumbdir,fname+str(timestamp)+'.'+thumbFormat)

				if not os.path.exists(thumbpath):  #need to create fresh thumbnail
					try:
						self.pathLabel.setText('Generating thumbnail for %s'%(filepath));self.app.processEvents()
						map(os.remove, glob.glob(os.path.join(thumbdir,fname)+'*.'+thumbFormat)) #remove old thumbnails (different timestamp) if any
						self.loadFromFile(P2,curves,filepath) 
						self.exporter.export(thumbpath)
					except Exception as e:
						logging.exception(e)
						print ('problem',fname,e)
						continue
				try:
					self.pathLabel.setText('Loading thumbnail for %s'%(filepath));self.app.processEvents()
					#print ('hm : Loading thumbnail for %s'%(filepath))
					x = QtGui.QIcon(thumbpath)
					a = QtGui.QListWidgetItem(x,fname)
					self.listWidget.addItem(a)
					self.thumbList[fname] = [a,filepath]
				except Exception as e:
					print('failed to load thumbnail for ',fname,e.message)
		self.pathLabel.setText('Current path : %s'%directory)

	def plotTypeChanged(self,tp):
		if tp==0: #Histogram. Disable fitting option.
			self.newPlotFrame.setVisible(False)
		elif tp==1: #Half life data.
			self.newPlotFrame.setVisible(True)


		
	def clickCallback(self,fname):
		if self.plotType.currentIndex()==1: #Open the plot in a new window
			log = self.plotLog.isChecked()
			errorBars = self.errorBars.isChecked()
			fit = [False,True][self.fitType.currentIndex()]
			self.showNewPlot(fname, fit = fit, log = log,errorBars = errorBars)# ,histMode = histMode)
		elif self.plotType.currentIndex()==0: #Open the plot in the existing histogram of the software
			self.loadHistogram(fname)


	def showNewPlot(self,fname,**kwargs):
		#pg.setConfigOptions(antialias=True, background='w',foreground='k')
		self.newwin = pg.GraphicsWindow(title="Data from file | %s"%fname)
		self.newwin.resize(800,600)
		#self.newwin.setWindowTitle('pyqtgraph example: Plotting')
		self.p1 = self.newwin.addPlot()
		self.newcurves=[]


		for name,col in zip(self.trace_names,self.trace_colors):
			if kwargs.get('fit',False):
				C=pg.PlotCurveItem(name = name,pen = col, symbolBrush=(0,0,200), symbolPen='w', symbol='o', symbolSize=14)
			else:
				C=pg.PlotCurveItem(name = name,pen = col)
			self.p1.addItem(C)
			self.newcurves.append(C)

		self.loadFromFile( self.p1,self.newcurves,fname, fit=kwargs.get('fit',False), log=kwargs.get('log',False), errorBars=kwargs.get('errorBars',False) ) 


	def loadFromFile(self,plot,curves,filename,**kwargs):
		with open(filename) as f:
			comments=''
			delim = ','
			while True:
				header = f.readline()
				if header[0]=='#':
					comments+=header[1:]
					continue
				data1 = header.strip()
				if ',' in data1:
					delim = ','
				elif '  ' in data1:
					delim = '  '
				elif '\t' in data1:
					delim = '\t'
				else:
					delim = ' '
				break
			#print (filename,comments)
			if re.search('[a-df-zA-DF-Z]', header): #Header has letters
				ar = np.loadtxt(filename,skiprows=1,delimiter=delim)
				try:                               	#parse headers and set them as axis labels
					header = header.replace(' ',',')
					p=header.split(',')
					if len(p)>=2:
						plot.getAxis('bottom').setLabel(p[0])
						plot.getAxis('left').setLabel(p[1])
				except Exception as e:
					plot.getAxis('bottom').setLabel('channel')
					plot.getAxis('left').setLabel('count')
			else:
				try:
					ar = np.loadtxt(filename,delimiter=delim)
				except Exception as e:
					logging.exception(e)					
					print('error loading:',filename,delim,e)
					return False
					
		#XR = [0,0];YR=[0,0]
		fit = kwargs.get('fit',False)
		if fit: plot.addLegend()
		z=ar
		for A in range(int(len(ar[0])/2)): #integer division
			self.x =ar[:,int(A)*2]
			self.y =ar[:,int(A)*2+1]
			if kwargs.get('histMode',False):
				pen=(155, 255, 155,180)			
				if A<len(self.trace_colors):
					brush = list(self.trace_colors[A][:3])+[120]
				else:
					brush=(0, 20, 255,130)
				if A<len(curves): curves[A].setData(self.x,self.y[:-1], stepMode=True, fillLevel=0, brush=brush,pen = pen)
			else:
				if fit: #Exponential decay fitting.
					self.x = self.x/60 #convert to minutes
					Amp, K , log_Amp, res = self.fit_exp_linear(self.x,self.y, 0) #No offset expected
					fit_dY = Amp * np.exp(K * self.x) # + offset
					fitcurve = pg.PlotCurveItem(name = " <span style='color: green'>N0 = %.2f , Decay Coefficient = %.2e, Half life = %.2f Min </span>"%(Amp,K,0.693/K) , pen = curves[A].opts['pen'])
					plot.addItem(fitcurve)
					
					print ('N0=%.2f ; Residual=%.3f SD of slope (log mode) = '%(Amp, res),np.sqrt(  (1./(len(self.x)-2))*sum((log_Amp+K*self.x - np.log(self.y))**2)/sum((self.x - np.average(self.x))**2)  ))
					
					if kwargs.get('log',False):
						fitcurve.setData(self.x,log_Amp+K*self.x)
						legendY = np.log(self.y.max())
						legendY -= A*legendY/10
					else:
						#print 'SD of slope :',np.sqrt(  (1./(len(self.x)-2))*sum((fit_dY - self.y)**2)/sum((self.x - np.average(self.x))**2)  )
						fitcurve.setData(self.x,fit_dY)
						legendY = self.y.max()
						legendY -= A*legendY/20.

					#text = pg.TextItem(html=" <span style='color: green'>N0 = %.2f , Decay Coefficient = %.2e, Half life = %.2f Min </span>"%(Amp,K,0.693/K), anchor=(-0.3,0.5), border='r')
					#plot.addItem(text)
					#text.setPos(0,legendY )
				if kwargs.get('log',False):
					Y = np.log(self.y)
				else:
					Y = self.y

				if kwargs.get('errorBars',False):
					if kwargs.get('log',False):
						errbar = 1./np.sqrt(self.y)
					else:
						errbar = np.sqrt(Y)/2.
						
					bw = (self.x[1]-self.x[0])/2.
					err = pg.ErrorBarItem(x=self.x, y=Y, top=errbar, bottom=errbar, beam=bw)
					plot.addItem(err)

				if fit:
					tmpc = plot.plot(self.x,Y,pen=None, symbolBrush=(0,100,200), symbolPen='b', symbol='star', symbolSize=12)
				else:
					curves[int(A)].setData(self.x,Y,symbolBrush=(0,0,200), symbolPen='w', symbol='o', symbolSize=14)

				#	curves[A].setData(self.x,self.y, symbolBrush=(0,0,200), symbolPen='w', symbol='o', symbolSize=14)

			#if( min(self.x) < XR[0] ):XR[0] = min(self.x)-abs(min(self.x))*.1
			#if( max(self.x) > XR[1] ):XR[1] = max(self.x)+abs(max(self.x))*.1
			#if( min(self.y) < YR[0] ):YR[0] = min(self.y)-abs(min(self.y))*.1
			#if( max(self.y) > YR[1] ):YR[1] = max(self.y)+abs(max(self.y))*.1

		plot.getAxis('left').setGrid(170)
		plot.getAxis('bottom').setGrid(170)

		#self.autoScale(plot,XR[0],XR[1],YR[0],YR[1]);
		plot.enableAutoRange()
		return True

	def autoScale(self,plot,xMin,xMax,yMin,yMax):
			plot.setLimits(xMin=xMin,xMax=xMax,yMin=yMin,yMax=yMax);plot.setXRange(xMin,xMax);plot.setYRange(yMin,yMax)




	######################## FITTING ROUTINES. EXTRA STUFF #######################
	### FITTING ROUTINE WHICH USES LOG BASED LINEARIZATION ###

	def fit_exp_linear(self,t, y, C=0):
		y = y - C
		y = np.log(y)
		p,res,_,_,_ = np.polyfit(t, y, 1,full=True)
		K, A_log = p
		A = np.exp(A_log)
		return A,K ,A_log,res   

	### FITTING ROUTINE FROM EYEMATH.PY ###
	def exp_erf(self,p,y,x):
		return y - p[0] * np.exp(p[1]*x) + p[2]

	def exp_eval(self,x,p):
		return p[0] * np.exp(p[1]*x)  -p[2]

	def fit_exp(self,xa, ya):
		size = len(xa)
		maxy = max(ya)
		halfmaxy = maxy / 2.0
		halftime = 1.0
		for k in range(size):
			if abs(ya[k] - halfmaxy) < halfmaxy/100:
				halftime = xa[k]
				break 
		par = [maxy, -halftime,0] 					# Amp, decay, offset
		plsq = leastsq(self.exp_erf, par,args=(ya,xa))
		if plsq[1] > 4:
			return None,None
		yfit = self.exp_eval(xa, plsq[0])
		return yfit,plsq[0]





