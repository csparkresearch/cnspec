from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np
from scipy.optimize import leastsq

from .templates import ui_decayLayout as decayLayout
from utilities.templates import ui_regionWidget as ui_regionWidget

import sys, os, time, re
import pyqtgraph as pg

colors = [(0, 255, 0, 70), (255, 0, 0, 70), (255, 255, 100, 70), (10, 255, 255, 70)] + [
    (50 + np.random.randint(200), 50 + np.random.randint(200), 150 + np.random.randint(100), 50) for a in range(10)]


class temperatureHandler():
    def __init__(self):
        self.datapoints = []

    def add(self, val):
        self.datapoints.append(val)

    def get(self):
        if len(self.datapoints) == 0: return 0
        return np.average(self.datapoints)

    def clear(self):
        self.datapoints = []


class decayHandler():
    start = 0
    stop = 100
    position = 0
    max_rows = 1000
    interval = 10.

    def __init__(self, **kwargs):
        self.start = kwargs.get('start', 0)
        self.stop = kwargs.get('stop', self.stop)
        self.max_rows = kwargs.get('max_rows', self.max_rows)
        self.interval = kwargs.get('interval', self.interval)
        self.start_time = time.time()
        self.rows = np.zeros([2, self.max_rows])
        self.points = []

    def getElapsedTime(self):
        return time.time() - self.start_time

    def reset(self):
        self.position = 0
        self.start_time = time.time()

    def addToTable(self, table, counts):
        if self.position >= self.max_rows: return
        timeItem = QtWidgets.QTableWidgetItem();
        timeItem.setText('%.2f' % (time.time() - self.start_time))
        cItem = QtWidgets.QTableWidgetItem();
        cItem.setText('%.2f' % (counts))
        xItem = QtWidgets.QTableWidgetItem();
        xItem.setText("  X  ");
        table.setItem(self.position, 0, timeItem)
        table.setItem(self.position, 1, cItem)

        self.position += 1


class regionWidget(QtWidgets.QWidget, ui_regionWidget.Ui_Form):
    def __init__(self, graph, onDelete, calinv, num):
        super(regionWidget, self).__init__()
        self.MAXPOINTS = 3
        self.setupUi(self)
        self.plot = graph
        self.onDelete = onDelete
        self.cal = None
        self.calinv = calinv
        self.region = pg.LinearRegionItem()
        self.col = colors[num]
        self.region.setBrush(self.col)
        self.viewButton.setStyleSheet(
            "background-color: rgba(%d,%d,%d,%d);" % (self.col[0], self.col[1], self.col[2], 255))
        self.region.setZValue(10)
        for a in self.region.lines: a.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor));
        self.plot.addItem(self.region, ignoreBounds=False)
        self.region.sigRegionChangeFinished.connect(self.regionChanged)
        XR = self.plot.plotItem.vb.viewRange()[0]
        width = (XR[1] - XR[0]) / 6
        self.region.setRegion([XR[0] + width, XR[0] + 2 * width])
        self.info = AppWindow(self)

    def delete(self):
        self.setParent(None)
        self.plot.removeItem(self.region)
        self.onDelete(self)

    def appendPoint(self, time, point):
        self.viewButton.setText('View:%d' % self.info.ypos)
        self.info.appendPoint(time, point)

    def regionChanged(self, region=None):
        if type(region) == pg.graphicsItems.LinearRegionItem.LinearRegionItem:
            start, stop = region.getRegion()
            self.regionStart.setValue(int(start))
            self.regionStop.setValue(int(stop))
        else:
            self.region.setRegion([self.regionStart.value(), self.regionStop.value()])

    def viewData(self):
        # if not len(self.points):
        #	QtGui.QMessageBox.critical(self, 'Acquire Data', 'No points available. Please acquire some data first!')
        #	return
        self.info.show()
        self.info.setWindowState(QtCore.Qt.WindowState.WindowActive)
        self.info.activateWindow()

    def clearData(self):
        self.points = []
        self.info.reset()
        self.viewButton.setText('View')

    def updateCalibration(self, cal, calinv):
        # print('updating ',self.region.getRegion(),cal,calinv)
        self.cal = cal
        start, stop = self.region.getRegion()
        start = self.calinv(start)
        stop = self.calinv(stop)
        self.region.setRegion([cal(start), cal(stop)])
        self.calinv = calinv


class AppWindow(QtWidgets.QMainWindow, decayLayout.Ui_MainWindow):
    def __init__(self, parent):
        super(AppWindow, self).__init__(parent)
        self.setupUi(self)
        self.closeshortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self)
        self.closeshortcut.activated.connect(self.close)

        self.copyshortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+C"), self)
        self.copyshortcut.activated.connect(self.copyToClipboard)

        self.maxRows = 0
        self.ypos = 0
        self.previousCount = 0

        self.X = [];
        self.temp_X = []
        self.Y = [];
        self.dY = [];
        self.temp_dY = [];
        self.fit_dY = []

        self.fittingEnabled = True

        self.table.setHorizontalHeaderLabels(['Time(s)', 'Counts', 'Increment'])

        self.plot = pg.PlotWidget(name='mainPlot')
        self.plotLayout.addWidget(self.plot)
        self.plot.getAxis('bottom').setLabel('Time', units='S')
        self.plot.getAxis('left').setLabel('Increment')
        self.plot.addLegend()
        #### CROSSHAIRS
        self.plot.setTitle('Fitted data will be shown here after a minimum of 5 datapoints are available')
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.plot.addItem(self.vLine, True)
        self.plot.addItem(self.hLine, True)

        self.proxy = pg.SignalProxy(self.plot.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

        self.curve = pg.PlotCurveItem(name='Data')
        self.fitcurve = pg.PlotCurveItem(name='Fit', pen=[255, 0, 0])
        self.plot.addItem(self.curve);
        self.plot.addItem(self.fitcurve);

        self.reset()

        '''
		#For debugging purposes
		tmp = np.loadtxt('tmp.csv',delimiter=',')
		self.X = tmp[:,0]
		self.dY = tmp[:,1]
		self.rebinAndPlot()
		'''

    def mouseMoved(self, evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.plot.sceneBoundingRect().contains(pos):
            mousePoint = self.plot.plotItem.vb.mapSceneToView(pos)
            try:
                index = np.abs(self.temp_X - mousePoint.x()).argmin()
            except:
                return
            if index >= 0 and index < len(self.fit_dY):
                self.plot.plotItem.titleLabel.setText(
                    "<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>counts=%d</span>,   <span style='color: green'>fitted=%.1f</span>" % (
                    mousePoint.x(), self.temp_dY[index], self.fit_dY[index]))
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())

    def reset(self):
        self.X = [];
        self.temp_X = []
        self.Y = [];
        self.dY = [];
        self.temp_dY = [];
        self.fit_dY = []

        self.maxRows = 2
        self.ypos = 0
        self.table.setRowCount(self.maxRows)
        self.curve.clear()
        self.fitcurve.clear()
        self.previousCount = 0

    def appendPoint(self, X, Y):
        # Y = 10000*(1-np.exp(-0.1*X))  #Standard charging curve. For debugging

        dY = Y - self.previousCount
        self.previousCount = Y

        self.X.append(X)
        self.Y.append(Y)
        self.dY.append(dY)

        item1 = QtWidgets.QTableWidgetItem()
        self.table.setItem(self.ypos, 0, item1)
        item1.setText('%.2f' % X)

        item2 = QtWidgets.QTableWidgetItem()
        self.table.setItem(self.ypos, 1, item2)
        item2.setText('%d' % Y)

        item3 = QtWidgets.QTableWidgetItem()
        self.table.setItem(self.ypos, 2, item3)
        item3.setText('%d' % (dY))
        if self.ypos == 0:  # First item
            item1.setBackground(QtCore.Qt.red)
            item2.setBackground(QtCore.Qt.red)
            item3.setBackground(QtCore.Qt.red)

        #########################  REBINNING/AVERAGING ####################
        self.rebinAndPlot()

        self.ypos += 1

        if self.ypos >= self.maxRows:
            self.maxRows = self.ypos + 5
            self.table.setRowCount(self.maxRows)

    def rebinAndPlot(self):
        av = self.averageBox.value()
        self.temp_dY = np.array(self.dY[1:])  # Ignore row #1
        self.temp_X = np.array(self.X[1:]) - self.X[0]  # Ignore row #1. consider it the baseline
        if av != 1:
            end = len(self.temp_dY)
            end -= end % av
            self.temp_dY = np.sum(self.temp_dY[:end].reshape(-1, av), 1)
            self.temp_X = self.temp_X[:end:av]
        self.curve.setData(self.temp_X, self.temp_dY)
        #########################  FITTING ####################
        if self.fittingEnabled:
            self.fitAndPlot()

    def enableFitting(self, state):
        self.fittingEnabled = state
        if state:
            self.fitAndPlot()
        else:
            self.fitcurve.clear()

    '''
	def fitAndPlot(self):
		if len(self.temp_X)>4: #Atleast 4 points are necessary to attempt an exponential fit.
			try:
				self.fit_dY,po = self.fit_exp(self.temp_X,self.temp_dY)
				if po is not None:
					print po
					self.plot.plotItem.titleLabel.setText(" <span style='color: green'>N0 = %.2f , Decay Coefficient = %.2e , Offset = %.2f</span>"%(po[0],po[1],po[2]))
					self.fitcurve.setData(self.temp_X,self.fit_dY)
				else:
					print "fit didn't work"
			except Exception as e:
				print e
		else:
			self.fitcurve.clear()
	'''

    def fitAndPlot(self):
        if len(self.temp_X) > 4:  # Atleast 4 points are necessary to attempt an exponential fit.
            try:
                A, K = self.fit_exp_linear(self.temp_X, self.temp_dY, 0)  # No offset expected
                self.fit_dY = A * np.exp(K * self.temp_X)  # + offset
                # print A,K
                self.plot.plotItem.titleLabel.setText(
                    " <span style='color: green'>N0 = %.2f , Decay Coefficient = %.2e, Half life = %.2f Min </span>" % (
                    A, K, 0.693 / K / 60))
                self.fitcurve.setData(self.temp_X, self.fit_dY)
            except Exception as e:
                print(e)
        else:
            self.fitcurve.clear()

    ### FITTING ROUTINE WHICH USES LOG BASED LINEARIZATION ###
    def fit_exp_linear(self, t, y, C=0):
        y = y - C
        y = np.log(y)
        K, A_log = np.polyfit(t, y, 1)
        A = np.exp(A_log)
        return A, K

    ### FITTING ROUTINE FROM EYEMATH.PY ###
    def exp_erf(self, p, y, x):
        return y - p[0] * np.exp(p[1] * x) + p[2]

    def exp_eval(self, x, p):
        return p[0] * np.exp(p[1] * x) - p[2]

    def fit_exp(self, xa, ya):
        size = len(xa)
        maxy = max(ya)
        halfmaxy = maxy / 2.0
        halftime = 1.0
        for k in range(size):
            if abs(ya[k] - halfmaxy) < halfmaxy / 100:
                halftime = xa[k]
                break
        par = [maxy, -halftime, 0]  # Amp, decay, offset
        plsq = leastsq(self.exp_erf, par, args=(ya, xa))
        if plsq[1] > 4:
            return None, None
        yfit = self.exp_eval(xa, plsq[0])
        return yfit, plsq[0]

    def copyToClipboard(self):
        import pyqtgraph.exporters
        self.exporter = pg.exporters.ImageExporter(self.plot.plotItem)
        self.exporter.parameters()['width'] = self.imageWidthBox.value()
        self.exporter.export(copy=True)
        QtWidgets.QMessageBox.about(self, 'Copy Plot', 'Plot Image Copied to clipboard')

    def save(self):  # Save as CSV
        path, _filter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '~/', 'CSV(*.csv)')
        if path:
            import csv
            with open(unicode(path), 'wb') as stream:
                delim = [' ', '\t', ',', ';']
                writer = csv.writer(stream, delimiter=delim[self.delims.currentIndex()])
                if self.headerBox.isChecked():
                    headers = []
                    try:
                        for column in range(self.table.columnCount()): headers.append(
                            self.table.horizontalHeaderItem(column).text())
                        writer.writerow(headers)
                    except:
                        pass
                # writer.writeheader()
                for row in range(self.table.rowCount()):
                    rowdata = []
                    for column in range(self.table.columnCount()):
                        item = self.table.item(row, column)
                        if item is not None:
                            rowdata.append(unicode(item.text()).encode('utf8'))
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)

    def openFile(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open half life data file', '.', "Data files (*.csv *.txt)")
        if path:
            path = str(path)
            with open(path) as f:
                header = f.readline()
                skiprows = 1  # Skip the header line while reading actual data
                while header[0] == '#':  # Ignore any comments
                    header = f.readline()
                    skiprows += 1
                line2 = f.readline()
                if ',' in line2:
                    delim = ','
                else:
                    delim = ' '
                if re.search('[a-df-zA-DF-Z]', header):  # Header has letters
                    ar = np.loadtxt(path, skiprows=skiprows, delimiter=delim)
                else:
                    try:
                        ar = np.loadtxt(path, skiprows=0, delimiter=delim)
                    except Exception as e:
                        print('could not load.', delim, e)
                        return
            self.reset()
            for a in ar:
                self.appendPointDecay(a[0], a[1])

    def appendPointDecay(self, X, dY):  # X vs counts per unit time
        Y = self.previousCount + dY
        self.previousCount = Y

        self.X.append(X)
        self.Y.append(Y)
        self.dY.append(dY)

        item1 = QtWidgets.QTableWidgetItem()
        self.table.setItem(self.ypos, 0, item1)
        item1.setText('%.2f' % X)

        item2 = QtWidgets.QTableWidgetItem()
        self.table.setItem(self.ypos, 1, item2)
        item2.setText('%d' % Y)

        item3 = QtWidgets.QTableWidgetItem()
        self.table.setItem(self.ypos, 2, item3)
        item3.setText('%d' % (dY))
        if self.ypos == 0:  # First item
            item1.setBackground(QtCore.Qt.red)
            item2.setBackground(QtCore.Qt.red)
            item3.setBackground(QtCore.Qt.red)

        #########################  REBINNING/AVERAGING ####################
        self.rebinAndPlot()

        self.ypos += 1

        if self.ypos >= self.maxRows:
            self.maxRows = self.ypos + 5
            self.table.setRowCount(self.maxRows)
