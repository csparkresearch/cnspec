# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view3d.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(565, 409)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 4)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.heightEdit = QtWidgets.QLineEdit(self.frame)
        self.heightEdit.setMaximumSize(QtCore.QSize(220, 16777215))
        self.heightEdit.setObjectName("heightEdit")
        self.horizontalLayout_10.addWidget(self.heightEdit)
        self.shaderCombo = QtWidgets.QComboBox(self.frame)
        self.shaderCombo.setObjectName("shaderCombo")
        self.horizontalLayout_10.addWidget(self.shaderCombo)
        self.verticalLayout.addWidget(self.frame)
        self.frame_4 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.cumulativeLayout = QtWidgets.QHBoxLayout(self.frame_4)
        self.cumulativeLayout.setContentsMargins(0, 0, 0, 0)
        self.cumulativeLayout.setSpacing(0)
        self.cumulativeLayout.setObjectName("cumulativeLayout")
        self.verticalLayout.addWidget(self.frame_4)
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setMaximum(8192)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout.addWidget(self.horizontalSlider)
        self.horizontalSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_2.setMaximum(8192)
        self.horizontalSlider_2.setProperty("value", 8192)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.verticalLayout.addWidget(self.horizontalSlider_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.shaderCombo.currentIndexChanged['QString'].connect(MainWindow.setShader)
        self.heightEdit.textChanged['QString'].connect(MainWindow.setColormap)
        self.horizontalSlider.valueChanged['int'].connect(MainWindow.setPositionLeft)
        self.horizontalSlider_2.valueChanged['int'].connect(MainWindow.setPositionRight)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.frame.setProperty("class", _translate("MainWindow", "deep"))
        self.heightEdit.setText(_translate("MainWindow", "0.5, 2, 0.5, 0.2, 1, 1, 0.2, 0, 3"))

