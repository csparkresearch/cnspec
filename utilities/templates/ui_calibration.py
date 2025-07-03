# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calibration.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName(_fromUtf8("Frame"))
        Frame.resize(700, 406)
        Frame.setStyleSheet(_fromUtf8("QSplitter::handle:vertical {\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"    stop:0 #eee, stop:1 #ccc);\n"
"border: 1px solid #777;\n"
"width: 13px;\n"
"margin-left: 2px;\n"
"margin-right: 2px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"#polyLabel {\n"
"color: rgb(25, 95, 42);\n"
"}\n"
"\n"
"color: rgb(57, 79, 99);\n"
""))
        Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.verticalLayout = QtGui.QVBoxLayout(Frame)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(Frame)
        self.splitter.setFrameShape(QtGui.QFrame.NoFrame)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(10)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.table = QtGui.QTableWidget(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table.sizePolicy().hasHeightForWidth())
        self.table.setSizePolicy(sizePolicy)
        self.table.setFrameShadow(QtGui.QFrame.Sunken)
        self.table.setAutoScrollMargin(10)
        self.table.setAlternatingRowColors(True)
        self.table.setRowCount(3)
        self.table.setColumnCount(5)
        self.table.setObjectName(_fromUtf8("table"))
        self.table.horizontalHeader().setDefaultSectionSize(120)
        self.table.horizontalHeader().setMinimumSectionSize(40)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setCascadingSectionResizes(True)
        self.table.verticalHeader().setDefaultSectionSize(20)
        self.table.verticalHeader().setHighlightSections(True)
        self.table.verticalHeader().setMinimumSectionSize(15)
        self.gridLayout_3.addWidget(self.table, 0, 0, 1, 1)
        self.frame = QtGui.QFrame(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setMargin(3)
        self.gridLayout_2.setHorizontalSpacing(10)
        self.gridLayout_2.setVerticalSpacing(3)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setStyleSheet(_fromUtf8("color: rgb(6, 52, 76);"))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 2, 2, 1)
        self.delims = QtGui.QComboBox(self.frame)
        self.delims.setMaximumSize(QtCore.QSize(200, 16777215))
        self.delims.setObjectName(_fromUtf8("delims"))
        self.delims.addItem(_fromUtf8(""))
        self.delims.addItem(_fromUtf8(""))
        self.delims.addItem(_fromUtf8(""))
        self.delims.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.delims, 0, 3, 2, 1)
        self.line_2 = QtGui.QFrame(self.frame)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_2.addWidget(self.line_2, 0, 1, 2, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 2, 1)
        self.plotSaveFrame = QtGui.QFrame(self.frame)
        self.plotSaveFrame.setEnabled(True)
        self.plotSaveFrame.setMinimumSize(QtCore.QSize(0, 0))
        self.plotSaveFrame.setFrameShape(QtGui.QFrame.NoFrame)
        self.plotSaveFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.plotSaveFrame.setObjectName(_fromUtf8("plotSaveFrame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.plotSaveFrame)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout_2.addWidget(self.plotSaveFrame, 2, 2, 1, 4)
        self.line = QtGui.QFrame(self.frame)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 0, 4, 2, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.gridLayout_2.addWidget(self.pushButton_4, 0, 5, 2, 1)
        self.gridLayout_3.addWidget(self.frame, 1, 0, 1, 1)
        self.calibframe = QtGui.QFrame(self.splitter)
        self.calibframe.setObjectName(_fromUtf8("calibframe"))
        self.gridLayout = QtGui.QGridLayout(self.calibframe)
        self.gridLayout.setContentsMargins(-1, -1, 1, -1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_2 = QtWidgets.QPushButton(self.calibframe)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 2, 3, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.calibframe)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 4, 2, 1, 2)
        self.polyLabel = QtGui.QLabel(self.calibframe)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.polyLabel.sizePolicy().hasHeightForWidth())
        self.polyLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.polyLabel.setFont(font)
        self.polyLabel.setTextFormat(QtCore.Qt.PlainText)
        self.polyLabel.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.polyLabel.setObjectName(_fromUtf8("polyLabel"))
        self.gridLayout.addWidget(self.polyLabel, 1, 0, 1, 4)
        self.frame_2 = QtGui.QFrame(self.calibframe)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 100))
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.widgetLayout = QtGui.QVBoxLayout(self.frame_2)
        self.widgetLayout.setMargin(0)
        self.widgetLayout.setSpacing(3)
        self.widgetLayout.setObjectName(_fromUtf8("widgetLayout"))
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 4)
        self.line_3 = QtGui.QFrame(self.calibframe)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 3, 1, 1, 3)
        self.pushButton = QtWidgets.QPushButton(self.calibframe)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 2, 2, 1, 1)
        self.logBrowser = QtGui.QTextBrowser(self.calibframe)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logBrowser.sizePolicy().hasHeightForWidth())
        self.logBrowser.setSizePolicy(sizePolicy)
        self.logBrowser.setMinimumSize(QtCore.QSize(350, 0))
        self.logBrowser.setStyleSheet(_fromUtf8(""))
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.gridLayout.addWidget(self.logBrowser, 0, 4, 5, 1)
        spacerItem1 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(Frame)
        self.delims.setCurrentIndex(2)
        QtCore.QObject.connect(self.pushButton_4, QtCore.SIGNAL(_fromUtf8("clicked()")), Frame.save)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), Frame.reloadCalibration)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Frame.addPoint)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), Frame.returnToSpectrum)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(_translate("Frame", "Frame", None))
        self.label.setText(_translate("Frame", "Separator:", None))
        self.delims.setItemText(0, _translate("Frame", "space", None))
        self.delims.setItemText(1, _translate("Frame", "tab", None))
        self.delims.setItemText(2, _translate("Frame", "comma", None))
        self.delims.setItemText(3, _translate("Frame", "semicolon", None))
        self.pushButton_4.setText(_translate("Frame", "Save Data", None))
        self.pushButton_2.setText(_translate("Frame", "Apply Calibration Polynomial", None))
        self.pushButton_3.setText(_translate("Frame", "<< Return to Spectrum", None))
        self.polyLabel.setText(_translate("Frame", "Calibration Polynomial:", None))
        self.pushButton.setText(_translate("Frame", "Add a point", None))
        self.logBrowser.setDocumentTitle(_translate("Frame", "Calibration Log", None))
        self.logBrowser.setHtml(_translate("Frame", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><title>Calibration Log</title><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Calibration Log:<br />=======================</p></body></html>", None))

