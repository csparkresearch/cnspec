# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calibWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(424, 32)
        Form.setStyleSheet("")
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
        self.energy = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.energy.setStyleSheet("")
        self.energy.setMaximum(20000.0)
        self.energy.setObjectName("energy")
        self.gridLayout_3.addWidget(self.energy, 1, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/control/minus.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_3.addWidget(self.pushButton, 1, 2, 1, 1)
        self.channel = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.channel.setMinimum(1.0)
        self.channel.setMaximum(8192.0)
        self.channel.setObjectName("channel")
        self.gridLayout_3.addWidget(self.channel, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frame_2)

        self.retranslateUi(Form)
        self.energy.editingFinished.connect(Form.onFinish)
        self.pushButton.clicked.connect(Form.delete)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.energy.setSuffix(_translate("Form", " KeV"))
        self.pushButton.setToolTip(_translate("Form", "Delete this pair from the calibration"))
        self.pushButton.setText(_translate("Form", "REMOVE"))
        self.channel.setPrefix(_translate("Form", "Channel "))

from . import res_rc
