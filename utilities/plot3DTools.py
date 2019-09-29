from .Qt import QtGui,QtCore,QtWidgets
import sys,os,time
import pyqtgraph as pg
import numpy as np
from . templates import ui_view3d as view3d
from . templates import ui_viewSurface as viewSurface


try:
	import pyqtgraph.opengl as gl
	GL_ENABLED = True
except:
	GL_ENABLED = False


class surface3d(QtGui.QMainWindow, viewSurface.Ui_MainWindow):
	pointList=[]
	shaders = ['balloon','shaded','normalColor','heightColor','viewNormalColor','edgeHilight']
	def __init__(self, parent=None,data_2d=None,BINS=None):
		super(surface3d, self).__init__(parent)
		self.setupUi(self)
		global GL_ENABLED
		self.GL_ENABLED = GL_ENABLED
		self.BINS = BINS
		self.plotView.setCameraPosition(distance=50)
		self.plot = gl.GLSurfacePlotItem(z=data_2d, shader='shaded', color=(0.5, 0.5, 1, 1))
		#self.plot.scale(BINS/49., BINS/49., .1)
		self.plot.translate(-1*BINS/2, -1*BINS/2, 0)
		self.plotView.addItem(self.plot)
		self.lastZStep = 0

	def setData(self,data_2d):
		self.plot.setData(z=data_2d)

	def scaleZ(self,z):
		delta = z - self.lastZStep
		self.lastZStep = z
		if not delta: return
		self.plot.scale(1., 1., 1+delta/100.)


class AppWindow(QtGui.QMainWindow, view3d.Ui_MainWindow):
	pointList=[]
	shaders = ['balloon','shaded','normalColor','heightColor','viewNormalColor','edgeHilight']
	def __init__(self, parent=None):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		global GL_ENABLED
		self.GL_ENABLED = GL_ENABLED

		self.width = 20.
		self.maxDataSets = 40
		#self.scaling = self.width/10.
		self.curves = []
		self.data = []

		self.add3DPlot(self.cumulativeLayout)
		self.shaderCombo.addItems(self.shaders)
		self.setShader('heightColor')



	def setShader(self,shade):
		#shade = self.shaders[val]
		if shade == 'shaded':
			self.plot2.setShader('shaded')
			self.plot2.opts['computeNormals'] = True
			self.plot2.setGLOptions('opaque')

		elif shade == 'balloon':
			self.plot2.opts['color'] = (.3, .1, .3, 0.3)
			self.plot2.setShader('balloon')
			self.plot2.setGLOptions('additive')
			self.plot2.opts['computeNormals'] = True

		elif shade == 'normalColor':
			self.plot2.opts['color'] = (0, 1, .5, 0.2)
			self.plot2.setShader('normalColor')
			self.plot2.setGLOptions('additive')
			self.plot2.opts['computeNormals'] = True

		elif shade == 'viewNormalColor':
			self.plot2.setShader('viewNormalColor')
			self.plot2.setGLOptions('opaque')
			self.plot2.opts['computeNormals'] = True

		elif shade == 'edgeHilight':
			self.plot2.setShader('edgeHilight')
			self.plot2.setGLOptions('additive')
			self.plot2.opts['computeNormals'] = True

		elif shade == 'heightColor':
			self.plot2.setShader('heightColor')
			self.plot2.setGLOptions('additive')
			self.plot2.opts['computeNormals'] = False
			self.plot2.shader()['colorMap'] = np.array([0.01,0.4,0.37,0.05,2,2,1,0.2])

	def setColormap(self,steps):
		steps = str(steps)
		try:
			cmap = [float(a) for a in steps.split(',')]
			self.plot2.shader()['colorMap'] = cmap
			self.plot2.setShader('heightColor')
		except:
			pass

	def add3DPlot(self,layout):
		
		if not self.GL_ENABLED:
			print ('OpenGL not available')
			return False
		'''
		try:
			w = gl.GLViewWidget()
		except:
			self.GL_ENABLED = False
			return
		w.opts['distance'] = 40
		layout.addWidget(w)
		w.setWindowTitle('3D line Spectra')

		gz = gl.GLGridItem()
		gz.translate(0, 0, -self.width/2)
		w.addItem(gz)
		self.plot = w
		'''

		try:
			w2 = gl.GLViewWidget()
		except:
			self.GL_ENABLED = False
			return
		w2.opts['distance'] = 80
		layout.addWidget(w2)
		w2.setWindowTitle('3D surface Spectra')

		gz = gl.GLGridItem()
		gz.translate(0, 0, -self.width/2)
		w2.addItem(gz)

		self.plot2 = gl.GLSurfacePlotItem(color=(.2, .1, 0, 0.5), computeNormals=False, smooth=False)
		#plt.shader()['colorMap'] = np.array([0.2, 2, 0.5, 0.2, 1, 1, 0.2, 0, 2])
		#plt.translate(10, 10, 0)
		w2.addItem(self.plot2)
		self.plot2.translate(-self.width/2,-self.width/2,-self.width/2)


		self.start_time = time.time()

		verts = np.array([[
			[0, 0, 0],
			[0, self.width, -self.width/5],
			[0, self.width, self.width/5],
		]
		])
		self.m2colors = [[[ 0.11650455,0.11115034,0.64362394,0.82398102],
						[ 0.63367245 , 0.8738815  , 0.95143971 , 0.18921984],
						[ 0.3180938  , 0.81616747 , 0.6948056  , 0.19030863]]]
		self.m2edgeColor = (1,1,0,1)
		self.m2 = gl.GLMeshItem(vertexes=verts,  vertexColors=self.m2colors, smooth=False, shader='balloon', drawEdges=True, edgeColor=self.m2edgeColor)
		self.m2.translate(-self.width/2,-self.width/2,-self.width/2)
		self.m2.setGLOptions('additive')
		w2.addItem(self.m2)


		verts = np.array([[
			[self.width, 0, 0],
			[self.width, self.width, -self.width/5],
			[self.width, self.width, self.width/5],
		]
		])
		self.m3 = gl.GLMeshItem(vertexes=verts,  vertexColors=self.m2colors, smooth=False, shader='balloon', drawEdges=True, edgeColor=self.m2edgeColor)
		self.m3.translate(-self.width/2,-self.width/2,-self.width/2)
		self.m3.setGLOptions('additive')

		w2.addItem(self.m3)



	def setPositionLeft(self,val):
		val = 8192-val
		val = self.width*val/8192.
		verts = np.array([[
			[val, 0, 0],
			[val, self.width, -self.width/5],
			[val, self.width, self.width/5],
		]
		])
		self.m3.setMeshData(vertexes=verts,  vertexColors=self.m2colors, smooth=False, shader='balloon', drawEdges=True, edgeColor=self.m2edgeColor)


	def setPositionRight(self,val):
		val = 8192-val
		val = self.width*val/8192.
		verts = np.array([[
			[val, 0, 0],
			[val, self.width, -self.width/5],
			[val, self.width, self.width/5],
		]
		])
		self.m2.setMeshData(vertexes=verts,  vertexColors=self.m2colors, smooth=False, shader='balloon', drawEdges=True, edgeColor=self.m2edgeColor)


	def clear(self):
		self.start_time = time.time()
		self.data = []

	def addCurveFromFile(self,filename):
		data = np.loadtxt(filename,delimiter=',')
		t = float(filename.split('data_')[1][:-8])
		self.addCurve(data[:,0],data[:,1],t)

	def addCurve(self,x,y,Z=None):
		if not self.GL_ENABLED: return None
		if Z is None:Z = time.time() - self.start_time
		print ('time = ',Z)
		self.data.append([np.array(x),np.array(y),Z])
		datasets = len(self.data)
		#z = [datasets*self.scaling]*len(x)
		hmax = max([max(a[1]) for a in self.data])
		ymax = max([a[2] for a in self.data])

		'''
		pts = np.vstack([z,self.width*x/max(x),self.width*y/hmax]).transpose()
		plt = gl.GLLinePlotItem(pos=pts, color=pg.glColor((200,100,50)), width=1., antialias=True)
		plt.translate(-self.width/2, -self.width/2, -self.width/2)
		self.plot.addItem(plt)
		self.curves.append(plt)
		'''
		
		x = self.width*self.data[0][0]/max(x)
		y = np.array([self.width*a[2]/ymax for a in self.data])
		z = np.array([self.width*(a[1])/hmax for a in self.data])

		self.plot2.setData(x = x, y=y, z=z.T )
		#if self.scaling*datasets>=self.width:
		#	self.replotAll()
		'''
		vec = np.vstack([x-self.width/2 , self.width*(self.data[0][1])/hmax-self.width/2 , np.ones(len(x)) ])
		verts = np.array([vec.T])
		print (verts,verts.shape)
		colors = np.random.random(size=(verts.shape[0], 3, 4))
		self.m2.setMeshData(vertexes = verts , vertexColors=colors, smooth=False, shader='balloon', drawEdges=True, edgeColor=(1, 1, 0, 1))
		'''
		#print len(self.curves),len(self.data)
		if datasets>self.maxDataSets:
			self.data = self.data[::2]
			#for a in self.curves[len(self.data):]:
			#	self.plot.removeItem(a)
			#self.curves = self.curves[:len(self.data)]
			#self.replotAll()
		#return plt

	'''
	def replotAll(self):
		datasets = len(self.data)
		self.scaling = self.width/(datasets*2)
		for a in range(datasets):
			print (a)
			pts = np.vstack([[a*self.scaling]*self.data[a][2],self.width*self.data[a][0]/max(self.data[a][0]),self.width*self.data[a][1]/max(self.data[a][1]) ]).transpose()
			self.curves[a].setData(pos=pts, width=1., antialias=True)

		#self.plot2.setData(x = self.width*self.data[0][0]/max(x), y = np.linspace(0,self.width,len(self.data)), z=np.array([self.width*a[1]/max(a[1]) for a in self.data]).T  )
	'''
