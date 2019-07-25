# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout_alpha.ui'
#
# Created: Thu May 11 09:02:50 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(897, 599)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setStyleSheet(_fromUtf8("*{outline:none;}\n"
"\n"
"QMainWindow{background: rgb(56, 102, 115);} \n"
"QMessageBox {background: #444544;} \n"
"\n"
"QTabBar{font:16px;} \n"
"QTabBar::tab{ padding:10px 50px; color:#CCCCCC;background: rgb(56, 102, 115);}\n"
"QTabBar::tab:selected{color:white; background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:.7 rgb(126, 197, 220) , stop:1 rgba(0,0,0,100) );} \n"
"QTabBar::tab:hover{color:white; background:qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(26, 177, 191,255), stop:1 rgba(100, 100, 200,255) );} \n"
"\n"
".deep,#widgets{ background: rgb(57, 79, 99); }\n"
"\n"
"QListWidget{background: rgb(26, 32, 35);color:#FFFFFF;} \n"
"QListWidget::item:hover{background: #223344;color:#FFFFFF;} \n"
"\n"
"QLabel,QRadioButton{color:#FFFFFF; margin:1px 2px;}\n"
"QCheckBox{color:#AAA;border:none; margin:3px 0px;}\n"
"\n"
"QSlider::groove:horizontal {margin:0px; padding:0px; border:none; background:#DDFDFE; color:#BB7777; height: 4px;}\n"
"QSlider::handle:horizontal {background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #eee, stop:1 #ccc);border: 2px solid #777;width: 13px;margin-top: -3px;margin-bottom: -3px;border-radius: 3px;}\n"
"\n"
"QPushButton{border:1px solid #424242; padding:5px;color:#000000;background:#AAAAAA;}\n"
"QPushButton:hover{background:rgb(26, 177, 191) ; color:white; border-color:#FFFFFF;}\n"
"QPushButton::disabled{background:#333333 ; color:black;}\n"
"#countLabel{border:1px solid green; padding:0px;color:#FFF;background:rgba(0,0,0,0);}\n"
"/*#calibrationButton{border:0px none; padding:0px;color:#FFF;background:rgba(0,0,0,0);}*/\n"
"\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    border-bottom: 5px solid white; margin:3px;\n"
"}\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    border-bottom: 5px solid black; margin:3px;\n"
"}\n"
"QPushButton{min-height24px; min-width:30px;}  \n"
"\n"
"QToolTip{\n"
"   background-color: rgb(191, 210, 214);\n"
"    border-bottom: 3px dotted blue;\n"
"    color:#000; \n"
"\n"
"    padding:4px; border:0px; margin:0px;\n"
"}\n"
"\n"
"QInputDialog {color: black;background-color: rgb(122, 122, 131);}\n"
"\n"
"\n"
".active{ border:2px solid #ABF9E7;}"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setToolTip(_fromUtf8(""))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(25, 25))
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.splitter = QtGui.QSplitter(self.tab)
        self.splitter.setFrameShadow(QtGui.QFrame.Raised)
        self.splitter.setLineWidth(0)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widgets = QtGui.QFrame(self.splitter)
        self.widgets.setMaximumSize(QtCore.QSize(200, 16777215))
        self.widgets.setAutoFillBackground(False)
        self.widgets.setFrameShape(QtGui.QFrame.NoFrame)
        self.widgets.setFrameShadow(QtGui.QFrame.Raised)
        self.widgets.setObjectName(_fromUtf8("widgets"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widgets)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.startButton = QtGui.QPushButton(self.widgets)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/control/play.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.startButton.setIcon(icon)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.verticalLayout.addWidget(self.startButton)
        self.pauseButton = QtGui.QPushButton(self.widgets)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/control/stop.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pauseButton.setIcon(icon1)
        self.pauseButton.setObjectName(_fromUtf8("pauseButton"))
        self.verticalLayout.addWidget(self.pauseButton)
        self.clearButton = QtGui.QPushButton(self.widgets)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/control/reset.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearButton.setIcon(icon2)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.verticalLayout.addWidget(self.clearButton)
        self.line_3 = QtGui.QFrame(self.widgets)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout.addWidget(self.line_3)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.updateButton = QtGui.QPushButton(self.widgets)
        self.updateButton.setEnabled(True)
        self.updateButton.setIcon(icon2)
        self.updateButton.setObjectName(_fromUtf8("updateButton"))
        self.horizontalLayout_3.addWidget(self.updateButton)
        self.checkBox = QtGui.QCheckBox(self.widgets)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.horizontalLayout_3.addWidget(self.checkBox)
        self.horizontalLayout_3.setStretch(0, 4)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.widgets)
        self.label.setMaximumSize(QtCore.QSize(16777215, 18))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.fitButton = QtGui.QPushButton(self.widgets)
        self.fitButton.setObjectName(_fromUtf8("fitButton"))
        self.gridLayout.addWidget(self.fitButton, 3, 0, 1, 2)
        self.summationButton = QtGui.QPushButton(self.widgets)
        self.summationButton.setObjectName(_fromUtf8("summationButton"))
        self.gridLayout.addWidget(self.summationButton, 4, 0, 1, 2)
        self.line = QtGui.QFrame(self.widgets)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 1, 0, 1, 2)
        self.logBox = QtGui.QCheckBox(self.widgets)
        self.logBox.setStyleSheet(_fromUtf8("QCheckBox{color:#FFF;}"))
        self.logBox.setObjectName(_fromUtf8("logBox"))
        self.gridLayout.addWidget(self.logBox, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setSpacing(3)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.calibrationButton = QtGui.QPushButton(self.widgets)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.calibrationButton.setFont(font)
        self.calibrationButton.setFlat(True)
        self.calibrationButton.setObjectName(_fromUtf8("calibrationButton"))
        self.gridLayout_2.addWidget(self.calibrationButton, 2, 0, 1, 2)
        self.label_2 = QtGui.QLabel(self.widgets)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 18))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.line_7 = QtGui.QFrame(self.widgets)
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        self.gridLayout_2.addWidget(self.line_7, 1, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.label_4 = QtGui.QLabel(self.widgets)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 18))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.line_2 = QtGui.QFrame(self.widgets)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.pushButton_6 = QtGui.QPushButton(self.widgets)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.verticalLayout.addWidget(self.pushButton_6)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 2)
        self.verticalLayout.setStretch(3, 2)
        self.verticalLayout.setStretch(4, 1)
        self.verticalLayout.setStretch(5, 2)
        self.verticalLayout.setStretch(6, 1)
        self.verticalLayout.setStretch(7, 1)
        self.verticalLayout.setStretch(10, 2)
        self.plots = QtGui.QFrame(self.splitter)
        self.plots.setMinimumSize(QtCore.QSize(600, 0))
        self.plots.setFrameShape(QtGui.QFrame.NoFrame)
        self.plots.setFrameShadow(QtGui.QFrame.Raised)
        self.plots.setObjectName(_fromUtf8("plots"))
        self.plot_area = QtGui.QVBoxLayout(self.plots)
        self.plot_area.setSpacing(0)
        self.plot_area.setMargin(0)
        self.plot_area.setObjectName(_fromUtf8("plot_area"))
        self.horizontalLayout_2.addWidget(self.splitter)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/control/plots.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab, icon3, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.saveLayout = QtGui.QVBoxLayout(self.tab_2)
        self.saveLayout.setMargin(0)
        self.saveLayout.setObjectName(_fromUtf8("saveLayout"))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/control/saved.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_2, icon4, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.fitButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.fit)
        QtCore.QObject.connect(self.updateButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.load)
        QtCore.QObject.connect(self.pushButton_6, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.save)
        QtCore.QObject.connect(self.pauseButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.pause)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), MainWindow.setAutoUpdate)
        QtCore.QObject.connect(self.startButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.start)
        QtCore.QObject.connect(self.clearButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.clear)
        QtCore.QObject.connect(self.summationButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.summation)
        QtCore.QObject.connect(self.logBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), MainWindow.toggleLog)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "CSpark Research : software for 512 bin MCA by IUAC", None))
        self.startButton.setToolTip(_translate("MainWindow", "Start acquiring and sorting pulses", None))
        self.startButton.setText(_translate("MainWindow", "START", None))
        self.pauseButton.setToolTip(_translate("MainWindow", "Pause data acquisition", None))
        self.pauseButton.setText(_translate("MainWindow", "STOP   ", None))
        self.clearButton.setToolTip(_translate("MainWindow", "Clear the histogram", None))
        self.clearButton.setText(_translate("MainWindow", "CLEAR", None))
        self.updateButton.setToolTip(_translate("MainWindow", "Load histogram onto the graph", None))
        self.updateButton.setText(_translate("MainWindow", "UPDATE", None))
        self.checkBox.setToolTip(_translate("MainWindow", "Auto update the graph", None))
        self.checkBox.setText(_translate("MainWindow", "Auto", None))
        self.label.setText(_translate("MainWindow", "Analyze", None))
        self.fitButton.setToolTip(_translate("MainWindow", "After selecting a region [either by dragging the region selector, or clicking on a peak arrow],\n"
"click to extract parameters from a gaussian fit.\n"
"\n"
"Also allows single point calibration if the actual value of the peak is known", None))
        self.fitButton.setText(_translate("MainWindow", "Gaussian Fit Region", None))
        self.summationButton.setToolTip(_translate("MainWindow", "After selecting a region [either by dragging the region selector, or clicking on a peak arrow],\n"
"click to extract parameters from a gaussian fit.\n"
"\n"
"Also allows single point calibration if the actual value of the peak is known", None))
        self.summationButton.setText(_translate("MainWindow", "Summation of Region", None))
        self.logBox.setText(_translate("MainWindow", "Enable Log Scale", None))
        self.calibrationButton.setToolTip(_translate("MainWindow", "Total Input Pulses. Click to clear the counter", None))
        self.calibrationButton.setText(_translate("MainWindow", "Calibration Menu", None))
        self.label_2.setText(_translate("MainWindow", "Calibrate", None))
        self.label_4.setText(_translate("MainWindow", "Save : Raw Data / Image", None))
        self.pushButton_6.setToolTip(_translate("MainWindow", "Save acquired data as well as fitted data if any.", None))
        self.pushButton_6.setText(_translate("MainWindow", "Save Data", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Acquisition", None))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Data Acquisition and controls", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Saved plots", None))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "View saved plots. Click on them to load them to the plot window for analysis", None))

import res_rc
