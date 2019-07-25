# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tracesRow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(173, 27)
        Form.setStyleSheet("QPushButton{\n"
"padding:1px;\n"
"border : 1px solid gray;\n"
"}\n"
"QSpinBox{\n"
"padding:0px;\n"
"}\n"
"QCheckBox{\n"
"padding:1px;\n"
"}\n"
"QLabel{\n"
"color:#000;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widgetLayout = QtWidgets.QHBoxLayout()
        self.widgetLayout.setContentsMargins(-1, 0, -1, -1)
        self.widgetLayout.setSpacing(3)
        self.widgetLayout.setObjectName("widgetLayout")
        self.widthBox = QtWidgets.QSpinBox(Form)
        self.widthBox.setMinimumSize(QtCore.QSize(60, 0))
        self.widthBox.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setKerning(True)
        self.widthBox.setFont(font)
        self.widthBox.setWrapping(False)
        self.widthBox.setFrame(True)
        self.widthBox.setAlignment(QtCore.Qt.AlignCenter)
        self.widthBox.setPrefix("")
        self.widthBox.setMinimum(1)
        self.widthBox.setMaximum(7)
        self.widthBox.setObjectName("widthBox")
        self.widgetLayout.addWidget(self.widthBox)
        self.fillButton = QtWidgets.QPushButton(Form)
        self.fillButton.setMinimumSize(QtCore.QSize(50, 0))
        self.fillButton.setMaximumSize(QtCore.QSize(35, 16777215))
        self.fillButton.setObjectName("fillButton")
        self.widgetLayout.addWidget(self.fillButton)
        self.outlineButton = QtWidgets.QPushButton(Form)
        self.outlineButton.setMinimumSize(QtCore.QSize(50, 0))
        self.outlineButton.setMaximumSize(QtCore.QSize(35, 16777215))
        self.outlineButton.setObjectName("outlineButton")
        self.widgetLayout.addWidget(self.outlineButton)
        self.verticalLayout.addLayout(self.widgetLayout)

        self.retranslateUi(Form)
        self.widthBox.valueChanged['int'].connect(Form.changeWidth)
        self.outlineButton.clicked.connect(Form.displayOutlineDialog)
        self.fillButton.clicked.connect(Form.displayFillDialog)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.widthBox.setToolTip(_translate("Form", "Set the width of the trace"))
        self.widthBox.setSuffix(_translate("Form", " px"))
        self.fillButton.setToolTip(_translate("Form", "Change the color of the trace"))
        self.fillButton.setText(_translate("Form", "fill"))
        self.outlineButton.setToolTip(_translate("Form", "Change the color of the trace"))
        self.outlineButton.setText(_translate("Form", "outline"))

