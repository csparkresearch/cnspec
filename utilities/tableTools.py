from .Qt import QtGui,QtCore
import numpy as np

from utilities.templates import ui_calTable as calTable
from utilities.templates import ui_calibWidget as ui_calibWidget

import sys,os,time,functools


class calibWidget(QtGui.QWidget,ui_calibWidget.Ui_Form):
	def __init__(self,channel,energy,onDelete,updatePoly):
		super(calibWidget, self).__init__()
		self.setupUi(self)
		self.onDelete = onDelete
		self.updatePoly = updatePoly
		self.channel.setValue(channel)
		self.energy.setValue(energy)

	def onFinish(self):
		self.updatePoly()
		
	def getXY(self):
		return self.channel.value(),self.energy.value()	

	def delete(self):
		self.onDelete(self)
		self.updatePoly()



class AppWindow(QtGui.QMainWindow, calTable.Ui_MainWindow):
	def __init__(self,onReload,parentLabel=None):
		super(AppWindow, self).__init__()
		self.setupUi(self)
		self.onReload = onReload
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)
		self.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self), QtCore.SIGNAL('activated()'), self.close)

		self.rows = []
		self.parentLabel = parentLabel
		

	def reloadCalibration(self):
		self.onReload()

	def removeRow(self,R):
		R.setParent(None)
		self.rows.remove(R)
		
	def addPair(self,BIN,ENERGY):
		R = calibWidget(BIN,ENERGY,self.removeRow,self.updatePolyString)
		self.widgetLayout.addWidget(R)
		self.rows.append(R)
		print ('ADDING',BIN,ENERGY)
		self.updatePolyString()

	def updatePolyString(self):
		_,p,_ = self.getPolynomial()
		self.polyLabel.setText("Calibration : x' = %s"%(str(p).strip()))
		self.parentLabel.setText("X' = %s"%(str(p).strip()))
		self.identifyZero()
		return str(p)

	def identifyZero(self):
		for a in self.rows:
			if a.energy.value()==0:
				a.energy.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(204, 0, 0, 255), stop:0.995283 rgba(255, 26, 205, 255));");
			else:
				a.energy.setStyleSheet("");

	def getPolynomial(self):
		self.identifyZero()
		try:
			if len(self.rows)==0:
				msg = 'No datapoints have been selected.\nThe calibration will be cleared and the x-axis will be reset to represent bins'
				return msg,np.poly1d([1,0]),np.poly1d([1,0])
			elif len(self.rows)==1:
				A,B = self.rows[0].getXY()
				poly = np.poly1d([B/A,0])
				msg = 'The following data points were used to create a calibration polynomial\nBIN\tENERGY\n0\t0\n%.1f\t%.1f\n\npolynomial : %s'%(A,B,str(poly))
				return msg,poly,np.poly1d([A/B,0])
			elif len(self.rows)==2:
				A,B = self.rows[0].getXY()
				A2,B2 = self.rows[1].getXY()
				poly = np.poly1d(np.polyfit([A,A2],[B,B2],1))
				msg = 'The following data points were used to create a calibration polynomial\nBIN\tENERGY\n%.1f\t%.1f\n%.1f\t%.1f\n\npolynomial : %s'%(A,B,A2,B2,str(poly))
				return msg,poly,np.poly1d(np.polyfit([B,B2],[A,A2],1))
			elif len(self.rows)==3:
				A,B = self.rows[0].getXY()
				A2,B2 = self.rows[1].getXY()
				A3,B3 = self.rows[2].getXY()
				poly = np.poly1d(np.polyfit([A,A2,A3],[B,B2,B3],2))
				msg = 'The following data points were used to create a calibration polynomial\nBIN\tENERGY\n%.1f\t%.1f\n%.1f\t%.1f\n%.1f\t%.1f\n\npolynomial : %s'%(A,B,A2,B2,A3,B3,str(poly))
				return msg,poly,np.poly1d(np.polyfit([B,B2,B3],[A,A2,A3],2))
		except:
			self.show()
			return "Could not fit, Please check the calibration datapoints",None,None


