# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout_alpha.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(897, 599)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setStyleSheet("*{outline:none;}\n"
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
".active{ border:2px solid #ABF9E7;}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setToolTip("")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(25, 25))
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.splitter = QtWidgets.QSplitter(self.tab)
        self.splitter.setFrameShadow(QtWidgets.QFrame.Raised)
        self.splitter.setLineWidth(0)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setObjectName("splitter")
        self.widgets = QtWidgets.QFrame(self.splitter)
        self.widgets.setMaximumSize(QtCore.QSize(200, 16777215))
        self.widgets.setAutoFillBackground(False)
        self.widgets.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.widgets.setFrameShadow(QtWidgets.QFrame.Raised)
        self.widgets.setObjectName("widgets")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widgets)
        self.verticalLayout.setObjectName("verticalLayout")
        self.startButton = QtWidgets.QPushButton(self.widgets)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/control/play.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.startButton.setIcon(icon)
        self.startButton.setObjectName("startButton")
        self.verticalLayout.addWidget(self.startButton)
        self.pauseButton = QtWidgets.QPushButton(self.widgets)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/control/stop.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pauseButton.setIcon(icon1)
        self.pauseButton.setObjectName("pauseButton")
        self.verticalLayout.addWidget(self.pauseButton)
        self.clearButton = QtWidgets.QPushButton(self.widgets)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/control/reset.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearButton.setIcon(icon2)
        self.clearButton.setObjectName("clearButton")
        self.verticalLayout.addWidget(self.clearButton)
        self.line_3 = QtWidgets.QFrame(self.widgets)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.updateButton = QtWidgets.QPushButton(self.widgets)
        self.updateButton.setEnabled(True)
        self.updateButton.setIcon(icon2)
        self.updateButton.setObjectName("updateButton")
        self.horizontalLayout_3.addWidget(self.updateButton)
        self.checkBox = QtWidgets.QCheckBox(self.widgets)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_3.addWidget(self.checkBox)
        self.horizontalLayout_3.setStretch(0, 4)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widgets)
        self.label.setMaximumSize(QtCore.QSize(16777215, 18))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.fitButton = QtWidgets.QPushButton(self.widgets)
        self.fitButton.setObjectName("fitButton")
        self.gridLayout.addWidget(self.fitButton, 3, 0, 1, 2)
        self.summationButton = QtWidgets.QPushButton(self.widgets)
        self.summationButton.setObjectName("summationButton")
        self.gridLayout.addWidget(self.summationButton, 4, 0, 1, 2)
        self.line = QtWidgets.QFrame(self.widgets)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 2)
        self.logBox = QtWidgets.QCheckBox(self.widgets)
        self.logBox.setStyleSheet("QCheckBox{color:#FFF;}")
        self.logBox.setObjectName("logBox")
        self.gridLayout.addWidget(self.logBox, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.calibrationButton = QtWidgets.QPushButton(self.widgets)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.calibrationButton.setFont(font)
        self.calibrationButton.setFlat(True)
        self.calibrationButton.setObjectName("calibrationButton")
        self.gridLayout_2.addWidget(self.calibrationButton, 2, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.widgets)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 18))
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.line_7 = QtWidgets.QFrame(self.widgets)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridLayout_2.addWidget(self.line_7, 1, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.label_4 = QtWidgets.QLabel(self.widgets)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 18))
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.line_2 = QtWidgets.QFrame(self.widgets)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.pushButton_6 = QtWidgets.QPushButton(self.widgets)
        self.pushButton_6.setObjectName("pushButton_6")
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
        self.plots = QtWidgets.QFrame(self.splitter)
        self.plots.setMinimumSize(QtCore.QSize(600, 0))
        self.plots.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.plots.setFrameShadow(QtWidgets.QFrame.Raised)
        self.plots.setObjectName("plots")
        self.plot_area = QtWidgets.QVBoxLayout(self.plots)
        self.plot_area.setContentsMargins(0, 0, 0, 0)
        self.plot_area.setSpacing(0)
        self.plot_area.setObjectName("plot_area")
        self.horizontalLayout_2.addWidget(self.splitter)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/control/plots.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab, icon3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.saveLayout = QtWidgets.QVBoxLayout(self.tab_2)
        self.saveLayout.setContentsMargins(0, 0, 0, 0)
        self.saveLayout.setObjectName("saveLayout")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/control/saved.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_2, icon4, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.fitButton.clicked.connect(MainWindow.fit)
        self.updateButton.clicked.connect(MainWindow.load)
        self.pushButton_6.clicked.connect(MainWindow.save)
        self.pauseButton.clicked.connect(MainWindow.pause)
        self.checkBox.toggled['bool'].connect(MainWindow.setAutoUpdate)
        self.startButton.clicked.connect(MainWindow.start)
        self.clearButton.clicked.connect(MainWindow.clear)
        self.summationButton.clicked.connect(MainWindow.summation)
        self.logBox.clicked['bool'].connect(MainWindow.toggleLog)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CSpark Research : software for 512 bin MCA by IUAC"))
        self.startButton.setToolTip(_translate("MainWindow", "Start acquiring and sorting pulses"))
        self.startButton.setText(_translate("MainWindow", "START"))
        self.pauseButton.setToolTip(_translate("MainWindow", "Pause data acquisition"))
        self.pauseButton.setText(_translate("MainWindow", "STOP   "))
        self.clearButton.setToolTip(_translate("MainWindow", "Clear the histogram"))
        self.clearButton.setText(_translate("MainWindow", "CLEAR"))
        self.updateButton.setToolTip(_translate("MainWindow", "Load histogram onto the graph"))
        self.updateButton.setText(_translate("MainWindow", "UPDATE"))
        self.checkBox.setToolTip(_translate("MainWindow", "Auto update the graph"))
        self.checkBox.setText(_translate("MainWindow", "Auto"))
        self.label.setText(_translate("MainWindow", "Analyze"))
        self.fitButton.setToolTip(_translate("MainWindow", "After selecting a region [either by dragging the region selector, or clicking on a peak arrow],\n"
"click to extract parameters from a gaussian fit.\n"
"\n"
"Also allows single point calibration if the actual value of the peak is known"))
        self.fitButton.setText(_translate("MainWindow", "Gaussian Fit Region"))
        self.summationButton.setToolTip(_translate("MainWindow", "After selecting a region [either by dragging the region selector, or clicking on a peak arrow],\n"
"click to extract parameters from a gaussian fit.\n"
"\n"
"Also allows single point calibration if the actual value of the peak is known"))
        self.summationButton.setText(_translate("MainWindow", "Summation of Region"))
        self.logBox.setText(_translate("MainWindow", "Enable Log Scale"))
        self.calibrationButton.setToolTip(_translate("MainWindow", "Total Input Pulses. Click to clear the counter"))
        self.calibrationButton.setText(_translate("MainWindow", "Calibration Menu"))
        self.label_2.setText(_translate("MainWindow", "Calibrate"))
        self.label_4.setText(_translate("MainWindow", "Save : Raw Data / Image"))
        self.pushButton_6.setToolTip(_translate("MainWindow", "Save acquired data as well as fitted data if any."))
        self.pushButton_6.setText(_translate("MainWindow", "Save Data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Acquisition"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Data Acquisition and controls"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Saved plots"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "View saved plots. Click on them to load them to the plot window for analysis"))

from . import res_rc
