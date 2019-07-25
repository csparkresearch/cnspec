# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'regionWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(343, 29)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 10))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.regionStart = QtWidgets.QSpinBox(self.frame_2)
        self.regionStart.setMaximum(20000)
        self.regionStart.setObjectName("regionStart")
        self.gridLayout_3.addWidget(self.regionStart, 1, 1, 1, 1)
        self.regionStop = QtWidgets.QSpinBox(self.frame_2)
        self.regionStop.setMinimum(10)
        self.regionStop.setMaximum(20000)
        self.regionStop.setObjectName("regionStop")
        self.gridLayout_3.addWidget(self.regionStop, 1, 2, 1, 1)
        self.toolButton = QtWidgets.QToolButton(self.frame_2)
        self.toolButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/control/close.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout_3.addWidget(self.toolButton, 1, 3, 1, 1)
        self.viewButton = QtWidgets.QPushButton(self.frame_2)
        self.viewButton.setObjectName("viewButton")
        self.gridLayout_3.addWidget(self.viewButton, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frame_2)

        self.retranslateUi(Form)
        self.toolButton.clicked.connect(Form.delete)
        self.regionStop.editingFinished.connect(Form.regionChanged)
        self.regionStart.editingFinished.connect(Form.regionChanged)
        self.viewButton.clicked.connect(Form.viewData)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.regionStart.setPrefix(_translate("Form", "Start: "))
        self.regionStop.setPrefix(_translate("Form", "Stop: "))
        self.viewButton.setText(_translate("Form", "View"))

from . import res_rc
