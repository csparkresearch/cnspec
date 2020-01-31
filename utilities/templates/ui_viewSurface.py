# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewSurface.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(762, 481)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.labelC = QtWidgets.QLabel(self.frame)
        self.labelC.setObjectName("labelC")
        self.gridLayout.addWidget(self.labelC, 0, 2, 1, 1)
        self.countB = QtWidgets.QLCDNumber(self.frame)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.countB.setFont(font)
        self.countB.setDigitCount(6)
        self.countB.setObjectName("countB")
        self.gridLayout.addWidget(self.countB, 2, 1, 1, 1)
        self.countA = QtWidgets.QLCDNumber(self.frame)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.countA.setFont(font)
        self.countA.setDigitCount(6)
        self.countA.setObjectName("countA")
        self.gridLayout.addWidget(self.countA, 1, 1, 1, 1)
        self.labelA = QtWidgets.QLabel(self.frame)
        self.labelA.setObjectName("labelA")
        self.gridLayout.addWidget(self.labelA, 1, 2, 1, 1)
        self.labelB = QtWidgets.QLabel(self.frame)
        self.labelB.setObjectName("labelB")
        self.gridLayout.addWidget(self.labelB, 2, 2, 1, 1)
        self.countC = QtWidgets.QLCDNumber(self.frame)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.countC.setFont(font)
        self.countC.setDigitCount(6)
        self.countC.setObjectName("countC")
        self.gridLayout.addWidget(self.countC, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 2, 0, 1, 4)
        self.scaleZSlider = QtWidgets.QSlider(self.centralwidget)
        self.scaleZSlider.setMinimum(0)
        self.scaleZSlider.setMaximum(1000)
        self.scaleZSlider.setSingleStep(1)
        self.scaleZSlider.setPageStep(100)
        self.scaleZSlider.setProperty("value", 1)
        self.scaleZSlider.setOrientation(QtCore.Qt.Vertical)
        self.scaleZSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.scaleZSlider.setObjectName("scaleZSlider")
        self.gridLayout_2.addWidget(self.scaleZSlider, 0, 3, 2, 1)
        self.plotView = GLViewWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotView.sizePolicy().hasHeightForWidth())
        self.plotView.setSizePolicy(sizePolicy)
        self.plotView.setObjectName("plotView")
        self.gridLayout_2.addWidget(self.plotView, 0, 2, 2, 1)
        self.imageView = ImageView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageView.sizePolicy().hasHeightForWidth())
        self.imageView.setSizePolicy(sizePolicy)
        self.imageView.setObjectName("imageView")
        self.gridLayout_2.addWidget(self.imageView, 0, 1, 2, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.scaleZSlider.valueChanged['int'].connect(MainWindow.scaleZ)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Coincidence Plots: Heat Map and 3D Surface View"))
        self.label.setText(_translate("MainWindow", "Spectrometer A"))
        self.label_3.setText(_translate("MainWindow", "Coincident Events"))
        self.label_2.setText(_translate("MainWindow", "Spectrometer B"))
        self.labelC.setText(_translate("MainWindow", "-"))
        self.labelA.setText(_translate("MainWindow", "TextLabel"))
        self.labelB.setText(_translate("MainWindow", "TextLabel"))

from pyqtgraph import ImageView
from pyqtgraph.opengl import GLViewWidget
