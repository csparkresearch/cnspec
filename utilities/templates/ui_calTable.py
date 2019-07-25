# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calTable.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(416, 170)
        MainWindow.setStyleSheet("QCheckBox,QPushButton{border:1px solid #424242; padding:2px;color:#000000;background:#CCC;}\n"
"QCheckBox:hover,QPushButton:hover{background:rgb(26, 177, 191) ; color:white; border-color:#FFFFFF;}\n"
"QPushButton::disabled{background:#333333 ; color:black;}\n"
"#countLabel{border:1px solid green; padding:0px;color:#FFF;background:rgba(0,0,0,0);}\n"
"/*#calibrationButton{border:0px none; padding:0px;color:#FFF;background:rgba(0,0,0,0);}*/\n"
"QPushButton,QPushButton{min-height24px; min-width:30px;}  \n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.widgetLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.widgetLayout.setContentsMargins(0, 0, 0, 0)
        self.widgetLayout.setSpacing(3)
        self.widgetLayout.setObjectName("widgetLayout")
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 3)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.polyLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.polyLabel.sizePolicy().hasHeightForWidth())
        self.polyLabel.setSizePolicy(sizePolicy)
        self.polyLabel.setObjectName("polyLabel")
        self.gridLayout.addWidget(self.polyLabel, 1, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.close)
        self.pushButton_2.clicked.connect(MainWindow.reloadCalibration)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Calibration Datapoints"))
        self.pushButton_2.setText(_translate("MainWindow", "Calibrate Using Polynomial"))
        self.pushButton.setText(_translate("MainWindow", "Close"))
        self.polyLabel.setText(_translate("MainWindow", "Polynomial:"))

