
import sys,os,time,re

from .Qt import QtCore,QtWidgets
from . templates import ui_regionPopup2,ui_regionWidget
import pyqtgraph as pg
import numpy as np
from . import decayTools

from scipy.optimize import leastsq


class AppWindow(QtWidgets.QDockWidget, ui_regionPopup2.Ui_DockWidget):
	regions = []
	def __init__(self, parent,**kwargs):
		super(AppWindow, self).__init__(parent)#, QtCore.Qt.WindowStaysOnTopHint)
		self.insertRegion = kwargs.get('insertRegion',None)
		self.getData = kwargs.get('getData',None)
		self.halflifeTime = kwargs.get('hltime',None)
		self.enablePeriodicSpectrumSaving = kwargs.get('enablePeriodicSpectrumSaving',None)
		self.changeDirectory = kwargs.get('changeDirectory',None)
		self.setupUi(self)
		

		#self.statusBar = self.statusBar()

	def closestIndex(self,arr,val):
		return (np.abs(arr-val)).argmin()

			
	def fit(self,**kwargs):
		self.x,self.y = self.getData()
		if not len(self.x):
			self.statusBar.setText('Data Unavailable : please acquire a spectrum')
			return
		elif len(self.regions)==0:
			self.statusBar.setText('Selection Unavailable : Please insert a region')
			return
		tail = kwargs.get('fitTail',self.lowTailBox.isChecked())
		fitres = []

		#self.clearFits()

		for R in self.regions:
			FIT = {}
			start,end= R.region.getRegion()
			FIT['region'] = '%.1f - %.1f'%(start,end)
			start = self.closestIndex(self.x,start)
			end = self.closestIndex(self.x,end)


			try:
				X = np.array(self.x[start:end])
				Y = np.array(self.y[start:end])
				
				#X+=(X[1]-X[0])/2.0  #Move the center to the center of the bins

				size = len(X)
				maxy = max(Y)
				halfmaxy = maxy / 2.0
				mean = sum(X*Y)/sum(Y)
				
				halfmaxima = X[int(len(X)/2)]
				for k in range(size):
					if abs(Y[k] - halfmaxy) < halfmaxy/10:
						halfmaxima = X[k]
						break
				sigma = mean - halfmaxima
				
				if not tail:  # REGULAR GAUSSIAN
					par = [maxy, mean, sigma] # Amplitude, mean, sigma				
					plsq = leastsq(self.gauss_erf, par,args=(X,Y))
					if plsq[1] > 4:
						print('fit failed')
						return None
					par = plsq[0]
					Xmore = np.linspace(X[0],X[-1],1000)


					#fitcurve = pg.PlotCurveItem(name = 'Fit',pen = [255,0,0]);self.plot.addItem(fitcurve)
					#self.fitcurves.append(fitcurve)
					par[1] += (X[1]-X[0])/2.0 #Move centroid to the center of the bins.
					Y = self.gauss_eval(Xmore, par)
					FIT['area'] = np.trapz(Y,dx = (Xmore[1]-Xmore[0]) )
					#fitcurve.setData(Xmore,Y, stepMode=False,fillLevel=0, brush=(126, 197, 220,100)) #Curve
					msg = 'Amplitude= %5.1f  Centroid= %5.2f  sigma = %5.2f'%(par[0], par[1], par[2])
					FIT['amplitude'] = par[0]; FIT['centroid'] = par[1]; FIT['channel'] = self.unconvert(par[1])
					FIT['fwhm'] = abs(par[2]*2.355) #FWHM = sigma*2.355				
					FIT['type'] = 'gaussian'
					fitres.append(FIT)
				else:
					gamma = 2 # Lorentzian
					par = [maxy, mean, sigma,gamma] # Amplitude, mean, sigma				
					plsq = leastsq(self.gausstail_erf, par,args=(X,Y))
					if plsq[1] > 4:
						print('fit failed')
						return None
					par = plsq[0]
					Xmore = np.linspace(X[0]*0.8,X[-1]*1.5,5000)

					#fitcurve = pg.PlotCurveItem(name = 'Fit',pen = [255,0,0]);self.plot.addItem(fitcurve)
					#self.fitcurves.append(fitcurve)
					par[1] += (X[1]-X[0])/2.0 #Move centroid to the center of the bins.

					Y = self.gausstail_eval(Xmore, par)
					FIT['area'] = np.trapz(Y,dx = (Xmore[1]-Xmore[0]) )

					#fitcurve.setData(Xmore,Y, stepMode=False,fillLevel=0, brush=(126, 197, 220,100)) #Curve

					msg = 'Amplitude= %5.1f  Centroid= %5.2f  S = %5.2f G = %5.2f'%(par[0], par[1], par[2], par[3])
					FIT['amplitude'] = par[0]; FIT['centroid'] = par[1];  FIT['channel'] = self.unconvert(par[1])
					FIT['fwhm'] = abs(par[2]*1.17741 + par[3]) #FWHM = sigma*1.17741+gamma				
					FIT['gamma'] = par[3]
					FIT['type'] = 'gaussiantail'
					fitres.append(FIT)
					
			except Exception as e:
				self.statusBar.setText('Fit Failed')
		
		#self.calibWindow.show()
		#self.calibWindow.setFitList(fitres)


	def log(self,msg,append=False):
		if append:
			self.textBrowser.append(msg)
		else:
			self.textBrowser.setHtml(msg)
