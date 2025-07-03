# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gate.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(365, 101)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.b1 = QtWidgets.QRadioButton(Dialog)
        self.b1.setObjectName("b1")
        self.options = QtWidgets.QButtonGroup(Dialog)
        self.options.setObjectName("options")
        self.options.addButton(self.b1)
        self.verticalLayout.addWidget(self.b1)
        self.b2 = QtWidgets.QRadioButton(Dialog)
        self.b2.setObjectName("b2")
        self.options.addButton(self.b2)
        self.verticalLayout.addWidget(self.b2)
        self.b3 = QtWidgets.QRadioButton(Dialog)
        self.b3.setObjectName("b3")
        self.options.addButton(self.b3)
        self.verticalLayout.addWidget(self.b3)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Apply Gate"))
        self.b1.setText(_translate("Dialog", "RadioButton"))
        self.b2.setText(_translate("Dialog", "RadioButton"))
        self.b3.setText(_translate("Dialog", "Reset All Gates"))

