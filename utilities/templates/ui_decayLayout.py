# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'decayLayout.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(942, 430)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(1, 1, 1, 1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table.sizePolicy().hasHeightForWidth())
        self.table.setSizePolicy(sizePolicy)
        self.table.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.table.setAutoScrollMargin(10)
        self.table.setAlternatingRowColors(True)
        self.table.setRowCount(100)
        self.table.setColumnCount(3)
        self.table.setObjectName("table")
        self.table.horizontalHeader().setDefaultSectionSize(120)
        self.table.horizontalHeader().setMinimumSectionSize(35)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setCascadingSectionResizes(True)
        self.table.verticalHeader().setDefaultSectionSize(20)
        self.table.verticalHeader().setHighlightSections(True)
        self.table.verticalHeader().setMinimumSectionSize(15)
        self.gridLayout_2.addWidget(self.table, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.line_3 = QtWidgets.QFrame(self.frame)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 0, 1, 2, 2)
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 2, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 4, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 5, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 4, 2, 1)
        self.delims = QtWidgets.QComboBox(self.frame)
        self.delims.setMaximumSize(QtCore.QSize(200, 16777215))
        self.delims.setObjectName("delims")
        self.delims.addItem("")
        self.delims.addItem("")
        self.delims.addItem("")
        self.delims.addItem("")
        self.gridLayout.addWidget(self.delims, 0, 5, 2, 1)
        self.headerBox = QtWidgets.QCheckBox(self.frame)
        self.headerBox.setChecked(True)
        self.headerBox.setObjectName("headerBox")
        self.gridLayout.addWidget(self.headerBox, 1, 2, 1, 1)
        self.plotSaveFrame = QtWidgets.QFrame(self.frame)
        self.plotSaveFrame.setEnabled(True)
        self.plotSaveFrame.setMinimumSize(QtCore.QSize(0, 0))
        self.plotSaveFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.plotSaveFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.plotSaveFrame.setObjectName("plotSaveFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.plotSaveFrame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_7 = QtWidgets.QFrame(self.plotSaveFrame)
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.horizontalLayout.addWidget(self.line_7)
        self.gridLayout.addWidget(self.plotSaveFrame, 3, 4, 1, 3)
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 0, 3, 2, 1)
        self.gridLayout_2.addWidget(self.frame, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(10, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.plotLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.plotLayout.setContentsMargins(0, 0, 0, 0)
        self.plotLayout.setSpacing(3)
        self.plotLayout.setObjectName("plotLayout")
        self.gridLayout_2.addWidget(self.frame_2, 1, 1, 2, 1)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.averageBox = QtWidgets.QSpinBox(self.frame_3)
        self.averageBox.setMinimum(1)
        self.averageBox.setMaximum(1000)
        self.averageBox.setObjectName("averageBox")
        self.horizontalLayout_2.addWidget(self.averageBox)
        self.checkBox = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_2.addWidget(self.checkBox)
        self.gridLayout_2.addWidget(self.frame_3, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.close)
        self.pushButton_2.clicked.connect(MainWindow.save)
        self.averageBox.editingFinished.connect(MainWindow.rebinAndPlot)
        self.checkBox.clicked['bool'].connect(MainWindow.enableFitting)
        self.pushButton_3.clicked.connect(MainWindow.openFile)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Save Your Results"))
        self.pushButton_3.setText(_translate("MainWindow", "Open file"))
        self.pushButton.setText(_translate("MainWindow", "Cancel"))
        self.pushButton_2.setText(_translate("MainWindow", "Save Data"))
        self.label.setText(_translate("MainWindow", "Delim:"))
        self.delims.setItemText(0, _translate("MainWindow", "space"))
        self.delims.setItemText(1, _translate("MainWindow", "tab"))
        self.delims.setItemText(2, _translate("MainWindow", "comma"))
        self.delims.setItemText(3, _translate("MainWindow", "semicolon"))
        self.headerBox.setText(_translate("MainWindow", "Include Headers"))
        self.label_2.setText(_translate("MainWindow", "Half Life Calculation: Counts in the selected region"))
        self.label_3.setText(_translate("MainWindow", "Cumulation Interval :"))
        self.averageBox.setToolTip(_translate("MainWindow", "Group n points together to reduce statistical fluctuation"))
        self.averageBox.setSuffix(_translate("MainWindow", " Row(s)"))
        self.checkBox.setText(_translate("MainWindow", "Exponential Decay Fit"))

