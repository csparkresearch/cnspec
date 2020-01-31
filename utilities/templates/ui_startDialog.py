# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'startDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(436, 202)
        Dialog.setStyleSheet("color: rgb(46, 52, 54);")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.message_2 = QtWidgets.QLabel(Dialog)
        self.message_2.setObjectName("message_2")
        self.gridLayout.addWidget(self.message_2, 3, 0, 2, 1)
        self.stopBox = QtWidgets.QSpinBox(Dialog)
        self.stopBox.setObjectName("stopBox")
        self.gridLayout.addWidget(self.stopBox, 2, 1, 1, 3)
        self.message = QtWidgets.QLabel(Dialog)
        self.message.setObjectName("message")
        self.gridLayout.addWidget(self.message, 0, 0, 1, 4)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 3, 1, 1)
        self.message_3 = QtWidgets.QLabel(Dialog)
        self.message_3.setObjectName("message_3")
        self.gridLayout.addWidget(self.message_3, 2, 0, 1, 1)
        self.refreshBox = QtWidgets.QSpinBox(Dialog)
        self.refreshBox.setObjectName("refreshBox")
        self.gridLayout.addWidget(self.refreshBox, 5, 1, 1, 3)
        self.thresholdBox = QtWidgets.QSpinBox(Dialog)
        self.thresholdBox.setObjectName("thresholdBox")
        self.gridLayout.addWidget(self.thresholdBox, 3, 1, 1, 3)
        self.message_4 = QtWidgets.QLabel(Dialog)
        self.message_4.setObjectName("message_4")
        self.gridLayout.addWidget(self.message_4, 5, 0, 1, 1)
        self.clearBox = QtWidgets.QCheckBox(Dialog)
        self.clearBox.setChecked(True)
        self.clearBox.setObjectName("clearBox")
        self.gridLayout.addWidget(self.clearBox, 6, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Start Acquisition"))
        self.message_2.setText(_translate("Dialog", "Threshold (channels)"))
        self.message.setText(_translate("Dialog", "Set parameters and start acquiring data (clears previous data)"))
        self.message_3.setText(_translate("Dialog", "Stop automatically after(seconds)"))
        self.message_4.setText(_translate("Dialog", "Auto-refresh histogram(seconds)"))
        self.clearBox.setText(_translate("Dialog", "Clear Old Spectrum"))

