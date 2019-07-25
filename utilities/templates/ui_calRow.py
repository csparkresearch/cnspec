# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calRow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(372, 28)
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
        self.energy.setAlignment(QtCore.Qt.AlignCenter)
        self.energy.setSuffix("")
        self.energy.setMaximum(20000.0)
        self.energy.setObjectName("energy")
        self.gridLayout_3.addWidget(self.energy, 1, 2, 1, 1)
        self.channel = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.channel.setAlignment(QtCore.Qt.AlignCenter)
        self.channel.setPrefix("")
        self.channel.setMinimum(0.0)
        self.channel.setMaximum(8192.0)
        self.channel.setSingleStep(1.0)
        self.channel.setProperty("value", 0.0)
        self.channel.setObjectName("channel")
        self.gridLayout_3.addWidget(self.channel, 1, 1, 1, 1)
        self.enable = QtWidgets.QCheckBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enable.sizePolicy().hasHeightForWidth())
        self.enable.setSizePolicy(sizePolicy)
        self.enable.setObjectName("enable")
        self.gridLayout_3.addWidget(self.enable, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frame_2)

        self.retranslateUi(Form)
        self.enable.clicked.connect(Form.toggled)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.enable, self.channel)
        Form.setTabOrder(self.channel, self.energy)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.enable.setText(_translate("Form", "USE"))

from . import res_rc
