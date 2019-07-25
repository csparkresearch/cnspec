from .Qt import QtGui,QtCore,QtWidgets
from .templates import ui_tracesRow as tracesRow

import sys
import re

	
class AnimatedLabel(QtWidgets.QLabel):
    def __init__(self,args):
        QtWidgets.QLabel.__init__(self)

        color1 = QtGui.QColor(255, 0, 0)
        color2 = QtGui.QColor(255, 144, 0)
        color3 = QtGui.QColor(255, 255, 0)
        color4 = QtGui.QColor(0,0,0,0)

        self.co_get = 0
        self.co_set = 0

        byar = QtCore.QByteArray()
        byar.append('zcolor')
        self.color_anim = QtCore.QPropertyAnimation(self, byar)
        self.color_anim.setStartValue(color4)
        self.color_anim.setKeyValueAt(0.25, color1)
        self.color_anim.setKeyValueAt(0.4, color2)
        self.color_anim.setKeyValueAt(0.6, color3)
        self.color_anim.setKeyValueAt(0.8, color2)
        self.color_anim.setEndValue(color4)
        self.color_anim.setDuration(1500)
        self.color_anim.setLoopCount(1)

        self.custom_anim = QtCore.QPropertyAnimation(self, byar)

    def parseStyleSheet(self):
        ss = str(self.styleSheet())
        sts = [s.strip() for s in ss.split(';') if len(s.strip())]
        return sts

    def getBackColor(self):
        self.co_get += 1
        # print(fuin(), self.co_get)
        return self.palette().color(self.pal_ele)

    def setBackColor(self, color):
        self.co_set += 1
        sss = self.parseStyleSheet()
        bg_new = 'background-color: rgba(%d,%d,%d,%d);' % (color.red(), color.green(), color.blue(), color.alpha())

        for k, sty in enumerate(sss):
            if re.search('\Abackground-color:', sty):
                sss[k] = bg_new
                break
        else:
            sss.append(bg_new)

        self.setStyleSheet('; '.join(sss))

    pal_ele = QtGui.QPalette.Window
    zcolor = QtCore.pyqtProperty(QtGui.QColor, getBackColor, setBackColor)


class AnimatedFrame(QtWidgets.QFrame):
    def __init__(self,args):
        QtWidgets.QFrame.__init__(self)

        color1 = QtGui.QColor(255, 0, 0)
        color2 = QtGui.QColor(0, 255, 255)
        color3 = QtGui.QColor(255, 0, 255)
        color4 = QtGui.QColor(0,0,0)

        self.co_get = 0
        self.co_set = 0

        byar = QtCore.QByteArray()
        byar.append('zcolor')
        self.color_anim = QtCore.QPropertyAnimation(self, byar)
        self.color_anim.setStartValue(color4)
        self.color_anim.setKeyValueAt(0.25, color1)
        self.color_anim.setKeyValueAt(0.4, color2)
        self.color_anim.setKeyValueAt(0.6, color3)
        self.color_anim.setKeyValueAt(0.8, color2)
        self.color_anim.setEndValue(color4)
        self.color_anim.setDuration(1500)
        self.color_anim.setLoopCount(1)

        self.custom_anim = QtCore.QPropertyAnimation(self, byar)

    def parseStyleSheet(self):
        ss = self.styleSheet()
        sts = [s.strip() for s in ss.split(';') if len(s.strip())]
        return sts

    def getBackColor(self):
        self.co_get += 1
        # print(fuin(), self.co_get)
        return self.palette().color(self.pal_ele)

    def setBackColor(self, color):
        self.co_set += 1
        sss = self.parseStyleSheet()
        bg_new = 'color: rgba(%d,%d,%d,%d);' % (color.red(), color.green(), color.blue(), color.alpha())

        for k, sty in enumerate(sss):
            if re.search('\Acolor:', sty):
                sss[k] = bg_new
                break
        else:
            sss.append(bg_new)

        self.setStyleSheet('; '.join(sss))

    pal_ele = QtGui.QPalette.Window
    zcolor = QtCore.pyqtProperty(QtGui.QColor, getBackColor, setBackColor)


class traceRowWidget(QtWidgets.QWidget,tracesRow.Ui_Form):
	def __init__(self,curve):
		super(traceRowWidget, self).__init__()
		self.setupUi(self)
		self.curve = curve
		self.penStyle = {'color':curve.opts['pen'].color(),'width':curve.opts['pen'].width(),'style':curve.opts['pen'].style()}
		self.lineStyles = {"solid":QtCore.Qt.SolidLine,"Dashed":QtCore.Qt.DashLine,"Dotted":QtCore.Qt.DotLine,"Dash-Dot":QtCore.Qt.DashDotLine,"Dash-Dot-Dot":QtCore.Qt.DashDotDotLine}

		#Fill
		self.colorDialog = QtGui.QColorDialog()
		self.colorDialog.setOptions(QtGui.QColorDialog.ShowAlphaChannel|QtGui.QColorDialog.DontUseNativeDialog|QtGui.QColorDialog.NoButtons)
		self.colorDialog.setWindowFlags(QtCore.Qt.Popup)
		self.colorDialog.setOption(QtGui.QColorDialog.DontUseNativeDialog, True)

		#Outline
		self.colorDialog2 = QtGui.QColorDialog()
		self.colorDialog2.setOptions(QtGui.QColorDialog.ShowAlphaChannel|QtGui.QColorDialog.DontUseNativeDialog|QtGui.QColorDialog.NoButtons)
		self.colorDialog2.setWindowFlags(QtCore.Qt.Popup)
		self.colorDialog2.setOption(QtGui.QColorDialog.DontUseNativeDialog, True)


		#self.colorButton.clicked.connect(self.displayColorDialog)
		#self.fillButton.setStyleSheet('background-color: %s;'%self.curve.opts['brush'].color().name())
		#self.outlineButton.setStyleSheet('background-color: %s;'%self.curve.opts['pen'].color().name())

		self.colorDialog.currentColorChanged.connect(self.changeFill)
		self.colorDialog2.currentColorChanged.connect(self.changeOutline)

	def displayFillDialog(self):
		self.colorDialog.show()

	def displayOutlineDialog(self):
		self.colorDialog2.show()

	def editLineStyle(self):
		item,ok = QtGui.QInputDialog.getItem(self,_translate("ewn","Select Line Style"),"", list(self.lineStyles.keys()), 0, False)
		if (ok and not item.isEmpty()):
			self.changeStyle(self.lineStyles[str(item)])

	def changeFill(self,btn):
		self.curve.opts['brush'].setColor(btn)
		col=str(self.curve.opts['brush'].color().name())
		self.fillButton.setStyleSheet('background-color: %s;'%col)

	def changeOutline(self,btn):
		self.curve.opts['pen'].setColor(btn)
		col=str(self.curve.opts['pen'].color().name())
		self.outlineButton.setStyleSheet('background-color: %s;'%col)


	def changeStyle(self,style):
		self.curve.opts['pen'].setStyle(style)

	def changeWidth(self,W):
		self.curve.opts['pen'].setWidth(W)

