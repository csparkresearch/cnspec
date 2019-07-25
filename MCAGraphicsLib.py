class CustomViewBox(pg.ViewBox):
	"""
	Subclass of ViewBox
	"""
	signalShowT0 = QtCore.Signal()
	signalShowS0 = QtCore.Signal()

	def __init__(self, parent=None):
		"""
		Constructor of the CustomViewBox
		"""
		super(CustomViewBox, self).__init__(parent)
		self.setRectMode() # Set mouse mode to rect for convenient zooming
		self.menu = None # Override pyqtgraph ViewBoxMenu
		self.menu = self.getMenu() # Create the menu

	def raiseContextMenu(self, ev):
		"""
		Raise the context menu
		"""
		if not self.menuEnabled():
			return
		menu = self.getMenu()
		pos  = ev.screenPos()
		menu.popup(QtCore.QPoint(pos.x(), pos.y()))

	def getMenu(self):
		"""
		Create the menu
		"""
		if self.menu is None:
			self.menu = QtGui.QMenu()
			self.viewAll = QtGui.QAction("Vue d\'ensemble", self.menu)
			self.viewAll.triggered.connect(self.autoRange)
			self.menu.addAction(self.viewAll)
			self.leftMenu = QtGui.QMenu("Mode clic gauche")
			group = QtGui.QActionGroup(self)
			pan = QtGui.QAction(u'Déplacer', self.leftMenu)
			zoom = QtGui.QAction(u'Zoomer', self.leftMenu)
			self.leftMenu.addAction(pan)
			self.leftMenu.addAction(zoom)
			pan.triggered.connect(self.setPanMode)
			zoom.triggered.connect(self.setRectMode)
			pan.setCheckable(True)
			zoom.setCheckable(True)
			pan.setActionGroup(group)
			zoom.setActionGroup(group)
			self.menu.addMenu(self.leftMenu)
			self.menu.addSeparator()
			self.showT0 = QtGui.QAction(u'Afficher les marqueurs d\'amplitude', self.menu)
			self.showT0.triggered.connect(self.emitShowT0)
			self.showT0.setCheckable(True)
			self.showT0.setEnabled(False)
			self.menu.addAction(self.showT0)
			self.showS0 = QtGui.QAction(u'Afficher les marqueurs de Zone d\'intégration', self.menu)
			self.showS0.setCheckable(True)
			self.showS0.triggered.connect(self.emitShowS0)
			self.showS0.setEnabled(False)
			self.menu.addAction(self.showS0)
		return self.menu

	def emitShowT0(self):
		"""
		Emit signalShowT0
		"""
		self.signalShowT0.emit()

	def emitShowS0(self):
		"""
		Emit signalShowS0
		"""
		self.signalShowS0.emit()

	def setRectMode(self):
		"""
		Set mouse mode to rect
		"""
		self.setMouseMode(self.RectMode)

	def setPanMode(self):
		"""
		Set mouse mode to pan
		"""
		self.setMouseMode(self.PanMode)
