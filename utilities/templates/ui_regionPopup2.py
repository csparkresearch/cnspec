# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'regionPopup2.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.setWindowModality(QtCore.Qt.NonModal)
        DockWidget.resize(263, 425)
        DockWidget.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        DockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_3 = QtWidgets.QFrame(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMaximumSize(QtCore.QSize(280, 16777215))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.frame_3)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.commandLinkButton = QtWidgets.QCommandLinkButton(self.frame)
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.horizontalLayout.addWidget(self.commandLinkButton)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 100))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.widgetLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.widgetLayout.setContentsMargins(0, 0, 0, 0)
        self.widgetLayout.setSpacing(3)
        self.widgetLayout.setObjectName("widgetLayout")
        self.verticalLayout.addWidget(self.frame_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.dirChange = QtWidgets.QPushButton(self.frame_3)
        self.dirChange.setMinimumSize(QtCore.QSize(0, 0))
        self.dirChange.setMaximumSize(QtCore.QSize(150, 30))
        self.dirChange.setObjectName("dirChange")
        self.gridLayout.addWidget(self.dirChange, 3, 1, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.saveAllCheckbox = QtWidgets.QCheckBox(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveAllCheckbox.sizePolicy().hasHeightForWidth())
        self.saveAllCheckbox.setSizePolicy(sizePolicy)
        self.saveAllCheckbox.setObjectName("saveAllCheckbox")
        self.gridLayout.addWidget(self.saveAllCheckbox, 2, 0, 1, 1)
        self.decayInterval = QtWidgets.QDoubleSpinBox(self.frame_3)
        self.decayInterval.setMinimum(0.01)
        self.decayInterval.setMaximum(1000.0)
        self.decayInterval.setProperty("value", 30.0)
        self.decayInterval.setObjectName("decayInterval")
        self.gridLayout.addWidget(self.decayInterval, 1, 1, 1, 2)
        self.saveAllInterval = QtWidgets.QSpinBox(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveAllInterval.sizePolicy().hasHeightForWidth())
        self.saveAllInterval.setSizePolicy(sizePolicy)
        self.saveAllInterval.setMinimum(1)
        self.saveAllInterval.setMaximum(60)
        self.saveAllInterval.setObjectName("saveAllInterval")
        self.gridLayout.addWidget(self.saveAllInterval, 2, 1, 1, 1)
        self.savedSpectraCounter = QtWidgets.QSpinBox(self.frame_3)
        self.savedSpectraCounter.setMaximumSize(QtCore.QSize(40, 16777215))
        self.savedSpectraCounter.setFrame(True)
        self.savedSpectraCounter.setAlignment(QtCore.Qt.AlignCenter)
        self.savedSpectraCounter.setReadOnly(True)
        self.savedSpectraCounter.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.savedSpectraCounter.setKeyboardTracking(False)
        self.savedSpectraCounter.setMaximum(99999)
        self.savedSpectraCounter.setObjectName("savedSpectraCounter")
        self.gridLayout.addWidget(self.savedSpectraCounter, 2, 2, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.frame_3)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 0, 0, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)
        self.textBrowser = QtWidgets.QTextBrowser(self.frame_3)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 150))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.statusBar = QtWidgets.QLabel(self.frame_3)
        self.statusBar.setText("")
        self.statusBar.setObjectName("statusBar")
        self.verticalLayout.addWidget(self.statusBar)
        self.horizontalLayout_2.addWidget(self.frame_3)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        self.dirChange.clicked.connect(DockWidget.changeDirectory)
        self.decayInterval.editingFinished.connect(DockWidget.halflifeTime)
        self.commandLinkButton.clicked.connect(DockWidget.insertRegion)
        self.saveAllCheckbox.clicked.connect(DockWidget.enablePeriodicSpectrumSaving)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setWindowTitle(_translate("DockWidget", "Analyze Graph"))
        self.commandLinkButton.setText(_translate("DockWidget", "Insert New Graph Selector"))
        self.dirChange.setText(_translate("DockWidget", "Select Directory"))
        self.label_5.setText(_translate("DockWidget", "Sum Record Interval"))
        self.saveAllCheckbox.setText(_translate("DockWidget", "Save Interval"))
        self.decayInterval.setSuffix(_translate("DockWidget", " Sec"))
        self.saveAllInterval.setSuffix(_translate("DockWidget", " Min"))
