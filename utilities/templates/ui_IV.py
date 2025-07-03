# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'IV.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(245, 56)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.currentLabel = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.currentLabel.sizePolicy().hasHeightForWidth())
        self.currentLabel.setSizePolicy(sizePolicy)
        self.currentLabel.setMinimumSize(QtCore.QSize(60, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.currentLabel.setFont(font)
        self.currentLabel.setObjectName("currentLabel")
        self.verticalLayout.addWidget(self.currentLabel)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "Constant Current Source"))
        self.currentLabel.setToolTip(_translate("Form", "Constant Current Source output voltage.\n"
"Colour changes to green for valid loads"))
        self.currentLabel.setText(_translate("Form", "Source Preparation:"))

