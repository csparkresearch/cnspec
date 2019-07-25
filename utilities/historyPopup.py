
import sys,os

from .Qt import QtWidgets,QtGui,QtCore
from . templates import ui_spectrumHistory
import pyqtgraph as pg
from .fileBrowser import PQG_ImageExporter
from . import plot3DTools,fitting
from collections import OrderedDict 
import numpy as np

def htmlfy_fit(vals):
	cols = ['#77cfbb','#b0e0e6','#98fb98','#fa8072','#d8bfd8','#ffe4e1']
	items = len(vals[0][2])
	html=''
	if not items:
		html='''<span style="font-family:arial,helvetica,sans-serif;font-size:11pt;">No regions inserted in the graph!</span> '''
	html+='''<table border="1" align="center" cellpadding="3" cellspacing="0" style="font-family:arial,helvetica,sans-serif;font-size:9pt;">
	<tbody><tr><td colspan="%d" style="padding:5px;">Fit Results</td></tr>'''%(1+items*2)

	html+='''<tr><td style="background-color:#77cfbb;">Time,Temp</td>'''
	for a in range(items):
		html+='''<td style="background-color:%s;">Centroid</td><td style="background-color:%s;">FWHM</td>'''%(cols[a],cols[a])
	html+='</tr>'

	for row in vals: #row = [time,temperature,FITS]
		m, s = divmod(row[0], 60)
		h, m = divmod(m, 60)
		ST = "%d:%02d:%02d" % (h, m, s)

		html+='<tr><td>%s(%.2f)</td>'%(ST,row[1])
		for a in row[2]:
			if a is None:
				html+='''<td colspan="2">Failed</td>'''
				continue
			html+='''<td>%.2f</td><td>%.2f(%.2f %%)</td>'''%(a['centroid'],a['fwhm'],100*a['fwhm']/a['centroid'])
		html+='</tr>'

	html+="</tbody></table>"	
	return html


class AppWindow(QtWidgets.QDockWidget, ui_spectrumHistory.Ui_DockWidget):
	regions = []
	history=[]
	def __init__(self, parent,**kwargs):
		super(AppWindow, self).__init__(parent)#, QtCore.Qt.WindowStaysOnTopHint)
		self.addshortcut = QtWidgets.QShortcut(QtGui.QKeySequence("3"), self)
		self.addshortcut.activated.connect(self.make3D)
		self.regions = kwargs.get('regions',None)

		self.short2d = QtWidgets.QShortcut(QtGui.QKeySequence("2"), self)
		self.short2d.activated.connect(self.make2D)

		self.saveShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), self)
		self.saveShortcut.activated.connect(self.saveAll)


		self.setupUi(self)
		self.plot = pg.PlotWidget()
		self.curve=pg.PlotCurveItem()#name = name);C.setPen(color=col, width=3)
		self.plot.addItem(self.curve)
		self.exporter = PQG_ImageExporter(self.plot.plotItem)
		#3D Plot
		try:
			self.plot3D = plot3DTools.AppWindow()
		except:
			pass

		#2D plot (surface)
		self.win = QtGui.QMainWindow()
		self.win.resize(800,800)
		imv = pg.ImageView()
		self.win.setCentralWidget(imv)

		## Create random 3D data set with noisy signals
		img = pg.gaussianFilter(np.random.normal(size=(200, 200)), (5, 5)) * 20 + 100
		img = img[np.newaxis,:,:]
		decay = np.exp(-np.linspace(0,0.3,100))[:,np.newaxis,np.newaxis]
		data = np.random.normal(size=(100, 200, 200))
		data += img * decay
		data += 2

		## Add time-varying signal
		sig = np.zeros(data.shape[0])
		sig[30:] += np.exp(-np.linspace(1,10, 70))
		sig[40:] += np.exp(-np.linspace(1,10, 60))
		sig[70:] += np.exp(-np.linspace(1,10, 30))

		sig = sig[:,np.newaxis,np.newaxis] * 3
		data[:,50:60,30:40] += sig


		## Display the data and assign each frame a time value from 1.0 to 3.0
		imv.setImage(data, xvals=np.linspace(1., 3., data.shape[0]))

		## Set a custom color map
		colors = [
			(0, 0, 0),
			(45, 5, 61),
			(84, 42, 55),
			(150, 87, 60),
			(208, 171, 141),
			(255, 255, 255)
		]
		cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 6), color=colors)
		imv.setColorMap(cmap)

		self.makeMenu()


	def saveAll(self):
		directory = QtGui.QFileDialog.getExistingDirectory(self,"Select a folder to dump all spectra into", os.path.expanduser("~"),  QtGui.QFileDialog.ShowDirsOnly)
		print('dumping project to: ',directory)
		if not len(self.history):return
		x = np.array(range(len(self.history[0]['y'])))
		for a in self.history:
			np.savetxt(os.path.join(directory,'data_%.2fmins.csv'%(a['time']/60.)),np.column_stack([x,a['y']]),delimiter=',',fmt="%.3f")

	def makeMenu(self):
		menu = QtWidgets.QMenu()
		menu.addSeparator()
		menu.addAction('Clear All', self.clear)
		menu.addAction('Save All', self.saveAll)
		self.optionButton.setMenu(menu)


	def addSpectrum(self,y,**kwargs):
		x = np.array(range(len(y)+1))
		self.curve.setData(x[:-2],y[:-2], stepMode=True, fillLevel=0, brush='#7C0A02',pen = '#FFFDFA')

		png = self.exporter.export(None,True,height = 100)
		ico = QtGui.QIcon(QtGui.QPixmap.fromImage(png))

		m, s = divmod(kwargs.get('time',0), 60)
		h, m = divmod(m, 60)
		ST = "%d:%02d:%02d" % (h, m, s)
		a = QtWidgets.QListWidgetItem(ico,ST)
		self.thumbs.addItem(a)

		tmp = kwargs
		tmp['y']=y
		self.history.append(tmp)


	def gaussianAnalysis(self):
		if not len(self.history):return None
		x = np.array(range(len(self.history[0]['y'])+1))
		previous_y = np.zeros(len(self.history[0]['y']))

		result=[]
		for data in self.history:
			fits=[]
			for R in self.regions:
				if self.differentialSpectrum.isChecked():
					res = fitting.gaussfit(x,data['y']-previous_y,R.region.getRegion())
					previous_y = data['y']
				else:
					res = fitting.gaussfit(x,data['y'],R.region.getRegion())
				if res is None:
					fits.append(None)
					continue
				Xmore,Y,par,FIT = res
				fits.append(FIT)
			result.append([data.get('time',0),data.get('temp',0),fits])
		self.analysisBrowser.setHtml(htmlfy_fit(result))
		return result

	def gaussianTailAnalysis(self):
		if not len(self.history):return None
		x = np.array(range(len(self.history[0]['y'])+1))
		previous_y = np.zeros(len(self.history[0]['y']))
		
		result=[]
		for data in self.history:
			fits=[]
			for R in self.regions:
				if self.differentialSpectrum.isChecked():
					res = fitting.gausstailfit(x,data['y']-previous_y,R.region.getRegion())
					previous_y = data['y']
				else:
					res = fitting.gausstailfit(x,data['y'],R.region.getRegion())
				if res is None:
					fits.append(None)
					continue
				Xmore,Y,par,FIT = res
				fits.append(FIT)
			result.append([data.get('time',0),data.get('temp',0),fits])
		self.analysisBrowser.setHtml(htmlfy_fit(result))
		return result


	def clear(self):
		self.history = []
		self.thumbs.clear()

	def make2D(self):
		self.win.show()

	def make3D(self):
		if self.plot3D is None:return
		self.plot3D.clear()
		if len(self.history):
			t0 = self.history[0]['time']
			x = np.array(range(len(self.history[0]['y'])))
			previous_y = np.zeros(len(self.history[0]['y']))
		for t in self.history:
			try:
				if self.differentialSpectrum.isChecked():
					self.plot3D.addCurve(x,t['y']-previous_y,t['time']-t0)
					previous_y = t['y']
				else:
					self.plot3D.addCurve(x,t['y'],t['time']-t0)

			except Exception as e:
				print(e)
		self.plot3D.show()
		self.plot3D.setWindowState(QtCore.Qt.WindowActive)
		self.plot3D.activateWindow()
