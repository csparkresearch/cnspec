
from .Qt import QtGui,QtCore,QtWidgets
from . templates import ui_plotSave as plotSave
import sys,os,time
import pyqtgraph as pg
import numpy as np




class AppWindow(QtGui.QMainWindow, plotSave.Ui_MainWindow):
	def __init__(self, parent ,curveList,plot,extra=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.closeshortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self)
		self.closeshortcut.activated.connect(self.close)

		self.imgshortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl-P"), self)
		self.imgshortcut.activated.connect(self.printImage)

		self.copyshortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl-C"), self)
		self.copyshortcut.activated.connect(self.copyToClipboard)

		arr = []
		for a in curveList:
			x,y = a
			arr.append(x);arr.append(y)
		if extra is not None:
			arr.append(extra)
		arr = np.array(arr)
		self.curvelist = arr.T
		self.comments.setText(kwargs.get('comments',''))
		self.contents.setHtml(self.arrayToHtml(self.curvelist))
		'''
		for a in self.curvelist:
			x,y=a
			name = ['Extracted Data','Fitted data','.','.'][int(colnum/2)]
			#x,y = a.getData()
			#name = a.name()
			if x is not None and y is not None:
				if len(x) and len(y):
					self.setColumn(colnum,x);colnum+=1
					self.setColumn(colnum,y);colnum+=1
					labels.append('%s(X)'%(name));labels.append('%s(Y)'%(name));
		'''

		self.headers = ["x","y","fx","fy"]
		headers = ",".join(self.headers)
		self.headerText.setText(headers)

		self.plot = plot
		if plot:
			self.imageWidthBox.setEnabled(True)
			self.saveImageButton.setEnabled(True)
			self.imageWidthBox.setValue(self.plot.plotItem.width())
			
			
	def arrayToHtml(self,curvelist):
		html='''<table border="1" align="left" cellpadding="5" cellspacing="0" style="font-family:arial,helvetica,sans-serif;font-size:10pt;">
		<tbody><tr><td colspan="2" style="padding:5px;">Contents to write'''

		html+='''<tr style="background-color:#77cfbb;"><td >X</td><td>Y</td></tr>'''

		for a in curvelist:
			row = ''.join(['<td>%.3f</td>'%x for x in a])
			html+='''
				<tr>
				%s
				</tr>
				'''%(row)
		html+="</tbody></table>"	
		return html	

	def delimiterChanged(self,i):
		delim = [' ','\t',',',';']
		delimiter = delim[self.delims.currentIndex()]
		headers = delimiter.join(self.headers)
		self.headerText.setText(headers)

	def saveImage(self):  #Save as png or something
		path, _filter  = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '~/')
		if path:
			pieces = path.split('.')
			if len(pieces)<2: #No extension specified
				path+='.png'
			elif pieces[-1] not in QtGui.QImageWriter.supportedImageFormats(): #Wrong extension specified
				import string
				path = string.join(pieces[:-1]+['png'],'.')
				QtGui.QMessageBox.about(self,'Invalid Filename','Modified : '+path)
			import pyqtgraph.exporters
			exporter = pg.exporters.ImageExporter(self.plot.plotItem)
			exporter.parameters()['width'] = self.imageWidthBox.value()
			exporter.export(path)

	def printImage(self): 
		import pyqtgraph.exporters
		self.exporter = pg.exporters.PrintExporter(self.plot.plotItem)
		#exporter.parameters()['width'] = self.imageWidthBox.value()
		self.exporter.export()

	def copyToClipboard(self): 
		import pyqtgraph.exporters
		self.exporter = pg.exporters.ImageExporter(self.plot.plotItem)
		self.exporter.parameters()['width'] = self.imageWidthBox.value()
		self.exporter.export(copy=True)
		QtGui.QMessageBox.about(self,'Copy Plot','Plot Image Copied to clipboard')

	

	def save(self):  #Save as CSV
		path, _filter  = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '~/', 'CSV(*.csv)')
		if path:
			#check if file extension is CSV
			if path[-3:] not in ['csv','txt','dat'] :
				path+='.csv'
			self.writeToPath(path)

	def writeToPath(self,path):
		if not isinstance(path,str): path = str(path).decode()
		delim = [' ','\t',',',';']
		delimiter = delim[self.delims.currentIndex()]
		header = ''
		if self.headerBox.isChecked():
			header = self.headerText.text()
		header += "\n"+self.comments.toPlainText()
		
		np.savetxt(path,self.curvelist,header = header,delimiter=delimiter,fmt="%.3f")
	def projectSummary(self):
		pass
		
		
		
