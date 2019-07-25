
from .Qt import QtCore,QtWidgets
from . templates import ui_calRow,ui_calPopup,ui_calTitle
import sys,os,time
import pyqtgraph as pg
import numpy as np

def htmlfy_fit(vals):
	html='''<table border="1" align="center" cellpadding="3" cellspacing="0" style="font-family:arial,helvetica,sans-serif;font-size:9pt;">
	<tbody><tr><td colspan="5" style="padding:5px;">Fitting: %s [%s]</td></tr>'''%('Gaussian' if vals[0]['type']=='gaussian' else 'Gaussian+Lorentzian tail',time.ctime())

	html+='''<tr><td style="background-color:#77cfbb;">Channels</td><td style="background-color:#77cfbb;">Amplitude</td>
	<td style="background-color:#77cfbb;">Centroid</td><td style="background-color:#77cfbb;">FWHM</td><td style="background-color:#77cfbb;">Area</td></tr>'''


	for a in vals:
		if a['centroid'] == a['channel']:
			centroidString = '%.2f'%(a['centroid'])
		else:
			centroidString = '%.2f (channel:%.2f)'%(a['centroid'],a['channel'])
		html+='''
			<tr>
				<td>%s</td>
				<td>%.2f</td>
				<td>%s</td>
				<td>%.3f (%.1f %%)</td>
				<td>%.2f</td>
			</tr>
			'''%(a['region'],a['amplitude'],centroidString,a['fwhm'],100*a['fwhm']/a['centroid'],a['area'])
	html+="</tbody></table>"	
	return html

def htmlfy_p(msg,color='blue'):
	return '''<p style="color:%s;">%s</p>'''%(color,msg)


class calibWidget(QtWidgets.QWidget,ui_calRow.Ui_Form):
	def __init__(self,toggleCallback=None):
		super(calibWidget, self).__init__()
		self.setupUi(self)
		self.toggleCallback = toggleCallback

	def getXY(self):
		return [self.channel.value(),self.energy.value()]
	def setXY(self,x,y):
		self.channel.setValue(x)
		self.energy.setValue(y)
	def enabled(self):
		return self.enable.isChecked()
	def toggled(self):
		self.toggleCallback()

class calibTitle(QtWidgets.QWidget,ui_calTitle.Ui_Form):
	def __init__(self,toggleCallback=None):
		super(calibTitle, self).__init__()
		self.setupUi(self)


class AppWindow(QtWidgets.QMainWindow, ui_calPopup.Ui_MainWindow):
	def __init__(self, parent,**kwargs):
		super(AppWindow, self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint)
		self.setupUi(self)
		self.applyCalibration = kwargs.get('application',None)
		self.statusBar = self.statusBar()
		self.points = []
		self.p1=np.poly1d([1,0]); self.p2=np.poly1d([1,0])
		self.msg = 'no calibration set'
		R = calibTitle()
		self.fitList=[]
		self.widgetLayout.addWidget(R)
		for a in range(4):
			R = calibWidget(self.configureZeroPoint)
			if a==0: #Special. 0,0 for 2 point calibration if only one is provided
				R.setEnabled(False)
				R.setStyleSheet('border: 1px solid gray')
			self.widgetLayout.addWidget(R)
			self.points.append(R)

	def dumpToLog(self):
		print ('dumped')

	def configureZeroPoint(self):
		points = []
		for a in self.points[1:]: #Ignore first
			if a.enabled():
				points.append(a.getXY())
		self.points[0].enable.setChecked(len(points)==1) #Enable 0 point if only one extra point is available

	def getCalibrationPoints(self):
		points = []
		for a in self.points:
			if a.enabled():
				points.append(a.getXY())
		return np.array(points)

	def generatePolynomial(self):
		points = self.getCalibrationPoints()
		if len(points)>1:
			self.statusBar.showMessage('attempting %d point calibration'%len(points))
			try:
				self.p1 = np.poly1d(np.polyfit(points[:,0],points[:,1],len(points)-1))
				self.p2 = np.poly1d(np.polyfit(points[:,1],points[:,0],len(points)-1))
				self.msg = 'polynomial : %s, inverse: %s'%(self.polystr(self.p1),self.polystr(self.p2))
				self.log(htmlfy_p(self.msg,'green'),True)
				self.polyLabel.setText(self.msg)
				return True
			except Exception as e:
				self.log(htmlfy_p('Could not fit, Please check the calibration datapoints','red'),True)
				self.p1=np.poly1d([1,0]); self.p2=np.poly1d([1,0])
				self.msg = 'polynomial : %s, inverse: %s'%(self.polystr(self.p1),self.polystr(self.p2))
				self.log(htmlfy_p(self.msg,'red'),True)
				self.polyLabel.setText(self.msg)
				return False
		else:
			self.statusBar.showMessage('please provide at least one channel-energy pair')
			return False

	def polystr(self,p):
		msg = ''
		for a in range(len(p)+1):
			msg = ('%.2f '%p[a]) + ('x^%d  + '%a if a else '') + msg
		return msg
		
	def applyCalibration(self):
		if self.generatePolynomial():
			self.applyCalibration(p1=self.p1, p2=self.p2, msg=self.msg)

	##################  FITTING ROUTINES

	def setFitList(self,fitList):
		self.fitList = fitList
		self.log(htmlfy_fit(fitList))
		for n in range(1,4):
			if(n<=len(fitList)):
				self.points[n].setXY(fitList[n-1]['channel'],0)
				self.points[n].enable.setChecked(True)
			else:
				self.points[n].enable.setChecked(False)
		self.configureZeroPoint()

	def log(self,msg,append=False):
		if append:
			self.textBrowser.append(msg)
		else:
			self.textBrowser.setHtml(msg)
