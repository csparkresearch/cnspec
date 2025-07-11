'''
Code snippet for reading data from the 1024 bin MCA

'''
import serial, struct, time,platform,os,sys,inspect, re
import numpy as np
if 'inux' in platform.system(): #Linux based system
	import fcntl

Byte =     struct.Struct("B") # size 1
ShortInt = struct.Struct("H") # size 2
Integer=   struct.Struct("I") # size 4
unpacker = {1:Byte, 2:ShortInt, 4:Integer}
#ListMode1 = struct.Struct("IHH") # size (4+2)+2      #time(6) + adc(2)
#ListMode2 = struct.Struct("IHHH") # size (4+2)+2+2   #time(6) + adc(2) + adc(2)
ListMode1 = struct.Struct("IH") # size (4)+2      #time(4) + adc(2)
ListMode2 = struct.Struct("IHH") # size (4)+2+2   #time(4) + adc(2) + adc(2)

def _bv(x):
	return 1<<x

def connect(**kwargs):
	return MCA(**kwargs)


def listPorts():
	'''
	Make a list of available serial ports. For auto scanning and connecting
	'''
	import glob
	system_name = platform.system()
	if system_name == "Windows":
		# Scan for available ports.
		available = []
		for i in range(256):
			try:
				s = serial.Serial('COM%d'%i)
				available.append('COM%d'%i)
				s.close()
			except serial.SerialException:
				pass
		return available
	elif system_name == "Darwin":
		# Mac
		return glob.glob('/dev/tty*') + glob.glob('/dev/cu*')
	else:
		# Assume Linux or something else
		return glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyUSB*')

def isPortFree(portname):
	try:
		fd = serial.Serial(portname, MCA.BAUD, stopbits=1, timeout = 1.0)
		if fd.isOpen():
			if 'inux' in platform.system(): #Linux based system
				try:
					fcntl.flock(fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
					fd.close()
					return True #Port is available
				except IOError:
					fd.close()
					return False #Port is not available

			else:
				fd.close()
				return True #Port is available
		else:
			fd.close()
			return False #Port is not available

	except serial.SerialException as ex:
		return False #Port is not available

def getFreePorts(openPort=None):
	'''
	Find out which ports are currently free 
	'''
	portlist={}
	for a in listPorts():
		if a != openPort:
			portlist[a] = isPortFree(a)
		else:
			portlist[a] = False
	return portlist




class spectrum:
	datatype = 'histogram'
	offline = False
	def __init__(self,bins,channelSize,**kwargs):
		self.bins = bins
		self.channelSize = channelSize
		self.calPoly = np.poly1d([1,0])
		self.calPolyInv = np.poly1d([1,0])
		self.offline = False
		self.log = False
		self.clearData()
		self.xlabel = 'Channel Number'
		self.ylabel = 'counts'
		if 'filename' in kwargs:
			self.loadFile(kwargs.get('filename'))

	def get_xlabel(self,**kwargs):
		return self.xlabel

	def hasData(self):
		return self.data.any()

	def clearData(self):
		self.overFlow=0
		self.data = np.zeros(self.bins)

	def addRawData(self,data,**kwargs):
		try:
			for a in range(self.bins): self.data[a] = unpacker[self.channelSize].unpack(data[a*self.channelSize:a*self.channelSize+self.channelSize])[0]

		except Exception as ex:
			msg = "Incorrect Number of Bytes Received\n"+ex.message
			raise RuntimeError(msg)
		self.overFlow = self.data[self.bins-1] #store info about last channel
		self.data[self.bins-1] = 0 #Make last channel 0
		if 'threshold' in kwargs:
			self.data[:kwargs.get('threshold')+5] = 0 # force 0 for values below threshold

	def setCalibration(self,points,**kwargs):
		'''
		Prepares a calibration polynomial from channel numbers and corresponding energies
		[ [a1,b1] , [a2,b2] ...]
		a1,a2 ...  = channels
		b1,b2 ...  = energies
		'''

		try:
			self.calPoly = np.poly1d(np.polyfit(points[:,0],points[:,1],len(points)-1))
			self.calPolyInv = np.poly1d(np.polyfit(points[:,1],points[:,0],len(points)-1))
			print('calibration range:',self.getCalibratedRange())
			self.xlabel = 'keV'
		except Exception as e:
			print(e)
			print('Failed to calibrate')
			self.xlabel = 'Channel Number'

	def getCalibratedRange(self,**kwargs):
		return [self.calPoly(0),self.calPoly(self.bins)]
			
	def clearCalibration(self):
		self.calPoly = np.poly1d([1,0])
		self.calPolyInv = np.poly1d([1,0])
		self.xlabel = 'Channel Number'

	def setLog(self,log):
		self.log = log
		if log: self.ylabel = 'log(counts)'
		else: self.ylabel = 'counts'

	def getHistogram(self,**kwargs):
		if self.log: return np.log10(self.data)
		else: return self.data*1.1

	def xaxis(self,calibrate=True,**kwargs):
		if calibrate: return self.calPoly(np.array(range(self.bins)))
		else: return np.array(range(self.bins))

	def loadFile(self,filename):
		with open(filename) as f:
			comments=''
			delim = ','
			while True:
				header = f.readline()
				if header[0]=='#':
					comments+=header[1:]
					continue
				data1 = header.strip()
				if ',' in data1:
					delim = ','
				elif '  ' in data1:
					delim = '  '
				elif '\t' in data1:
					delim = '\t'
				else:
					delim = ' '
				break
			print ('Loading : %s\n------\nComment: %s\n------\n\n'%(filename,comments))
			if re.search('[a-df-zA-DF-Z]', header): #Header has letters
				ar = np.loadtxt(filename,skiprows=1,delimiter=delim)
			else:
				try:
					ar = np.loadtxt(filename,delimiter=delim)
				except Exception as e:
					logging.exception(e)					
					print('error loading:',filename,delim,e)
					return False


		self.data =ar[:,1]
		self.bins = len(self.data)
		slope = (ar[:,0][-1] - ar[:,0][0] )/float(self.bins)
		self.calPoly = np.poly1d([slope , ar[:,0][0]]) #slope, intercept
		self.calPolyInv = np.poly1d([1/slope,-ar[:,0][0]/slope])
		self.offline = True

		return True

	def selectDataset(self,trace):
		pass




class listSpectrum:
	offline = False
	datatype = 'list'
	def __init__(self,bins,channelSize,parameters=2,**kwargs):
		self.bins = bins
		self.totalCoincidences=0
		self.BINS2D = kwargs.get('BINS2D',64)
		self.SCALE2D = int(self.bins/self.BINS2D)
		self.channelSize = channelSize
		self.parameters = parameters
		self.saveFilename = None#os.path.join(os.path.expanduser('~'),'MCA_thumbnails',str(time.time())+'.csv')
		self.listFile = None
		self.spectra = [spectrum(bins,channelSize) for a in range(parameters)]
		self.activeDataset = 0 #default is first trace.
		self.offline = False
		self.xlabel = 'Channel Number'
		self.ylabel = 'counts'
		self.lastTime = 0
		self.clearData()

		if 'filename' in kwargs:
			self.loadFile(kwargs.get('filename'))

	def setOutputFilename(self,fname):
		self.saveFilename = fname
		self.listFile = open(fname,'wt')

	def selectDataset(self,trace):
		if trace>=self.parameters:
			print('exceeded parameter range. Max:',self.parameters)
			return False
		self.activeDataset = trace

	def calPoly(self,v):
		return self.spectra[self.activeDataset].calPoly(v)
	def calPolyInv(self,v):
		return self.spectra[self.activeDataset].calPolyInv(v)

	def get_xlabel(self,**kwargs):
		activeDataset = kwargs.get('trace',self.activeDataset)
		self.spectra[activeDataset].get_xlabel()

	def hasData(self):
		for a in self.spectra:
			if a.hasData(): return True
		return False

	def clearData(self):
		self.overFlow=0
		self.totalCoincidences = 0
		self.HISTOGRAM2D,_,_ = np.histogram2d([],[],bins=self.BINS2D)
		#self.list = [[] for a in range(self.parameters+1)]
		self.lastTime = 0
		for a in self.spectra:
			a.clearData()
		if self.saveFilename:
			self.listFile = open(self.saveFilename,'wt')

	def addRawData(self,data):
		width = 2*(self.parameters+2)
		for a in range(int(len(data)/width)):
			start = a*width
			if self.parameters==1:
				t,adc = ListMode1.unpack(data[start:start+width]) #IH
				self.spectra[0].data[adc] +=1
				self.spectra[0].data[0] = 0
				
			elif self.parameters==2:
				t,adc1,adc2 = ListMode2.unpack(data[start:start+width]) #IHH
				
				#### HACKS
				#adc2 = int(np.round(adc2*450/490.))
				#if 160<adc1<200 and adc2>0:
				#	print('Coincide: ',adc1, adc2)
				#	self.data[0][adc1]+=1  #Count only non-zero elements
				#	self.data[1][adc2]+=1  #Count only non-zero elements
				#####

				if adc1:
					self.spectra[0].data[adc1] +=1
					self.spectra[0].data[0] = 0
				if adc2: 
					self.spectra[1].data[adc2] +=1
					self.spectra[1].data[0] = 0
				#if 150<adc1<205 and 170<adc2<225:
				if adc1 and adc2:
					self.totalCoincidences +=1
					self.HISTOGRAM2D[int(adc1/self.SCALE2D)][int(adc2/self.SCALE2D)]+=1

				#self.list[1].append(adc1)
				#self.list[2].append(adc2)
			tm = ( t )/64.e3 #Convert to mseconds
			if self.listFile: #Dump to file if it is open
				self.listFile.write('%.3f %d %d\n'%(tm+self.lastTime,adc1,adc2))
			self.lastTime = tm
			#if len(self.list[0]): #not the first element
			#	self.list[0].append(tm+self.list[0][-1]) #Add the timestamp of the previous value
			#	#self.listFile.write('%.3f %d %d\n'%(tm+self.list[0][-1],adc1,adc2))
			#else:
			#	self.list[0].append(tm)
			#	#self.listFile.write('%.3f %d %d\n'%(tm,adc1,adc2))

	def setCalibration(self,points,**kwargs):
		activeDataset = kwargs.get('trace',self.activeDataset)
		self.spectra[activeDataset].setCalibration(points)

	def getCalibratedRange(self,**kwargs):
		activeDataset = kwargs.get('trace',self.activeDataset)
		return self.spectra[activeDataset].getCalibratedRange()
			
	def clearCalibration(self,**kwargs):
		activeDataset = kwargs.get('trace',self.activeDataset)
		self.spectra[activeDataset].clearCalibration()

	def setLog(self,log):
		for a in self.spectra: a.setLog(log)
		self.log = log
		if log: self.ylabel = 'log(counts)'
		else: self.ylabel = 'counts'

	def getHistogram(self,**kwargs):
		activeDataset = kwargs.get('trace',self.activeDataset)
		return self.spectra[activeDataset].getHistogram()

	def xaxis(self,calibrate=True,**kwargs):
		activeDataset = kwargs.get('trace',self.activeDataset)
		return self.spectra[activeDataset].xaxis(calibrate)

	def loadFile(self,filename):
		data = np.loadtxt(filename)
		for a in range(len(data[0])-1): #iterate over total-1 columns. first col is time.
			self.spectra[a].data,_ = np.histogram(data[:,1+a],bins = self.bins,range=(0,self.bins-1))
			self.spectra[a].data[0] = 0
		self.rawdata = data
		self.activeDataset = 0
		data = data[ data[:,1]*data[:,2] >0] #Only coincident data.
		data_2d,_,_ = np.histogram2d(data[:,1],data[:,2],bins=self.BINS2D,range=[(0,self.bins-1),(0,self.bins-1)])
		self.HISTOGRAM2D = data_2d
		self.totalCoincidences = data_2d.sum()
		self.filename = filename

	def cut(self,start,end,**kwargs):
		'''
		checks a true condition on the second parameter and modifies the first.
		activeDataset [keyword trace = 0 or 1] can be passed optionally, but will not modify global selction of active dataset
		'''
		activeDataset = kwargs.get('trace',self.activeDataset) #optional. trace=0 will select the first channel. 1 for second.
		this_one = activeDataset
		other_one = (activeDataset+1)%2
		start_channel = int(self.spectra[other_one].calPolyInv(start))
		end_channel = int(self.spectra[other_one].calPolyInv(end))
		print('Gating trace %d with [trace %d from channel:%d to channel:%d]'%(this_one,other_one,start_channel,end_channel))	
		d1 = self.rawdata[:,this_one+1] #current spectrometer
		d2 = self.rawdata[:,other_one+1] #other spectrometer
		if start or end: # at least one should be non-zero. otherwise dont apply gate
			d1 = d1[(start_channel<d2) & (d2<end_channel)] #apply a cut around second
			print('gate applied')
		self.spectra[this_one].data,_ = np.histogram(d1,bins = self.bins,range=(0,self.bins-1))
		self.spectra[other_one].data,_ = np.histogram(d2,bins = self.bins,range=(0,self.bins-1))
		self.spectra[this_one].data[0] = 0
		self.spectra[other_one].data[0] = 0

class MCA:	
	GET_VERSION = Byte.pack(1)
	START_COUNT =   Byte.pack(2)
	GET_COUNT =   Byte.pack(3)
	
	SET_SQR1 =    Byte.pack(9)
	GET_CCS_VOLTAGE =Byte.pack(11)

	START_HISTOGRAM =Byte.pack(12)
	STOP_HISTOGRAM =Byte.pack(13)
	CLEAR_HISTOGRAM =Byte.pack(14)
	GET_HISTOGRAM =Byte.pack(15)

	SET_THRESHOLD =Byte.pack(16)

	READ_BULK_FLASH =Byte.pack(17)
	WRITE_BULK_FLASH =Byte.pack(18)
	SET_DAC =Byte.pack(20)

	I2C_SCAN =Byte.pack(21)
	I2C_READ =Byte.pack(22)
	I2C_WRITE =Byte.pack(23)
	#PILEUP_REJECT =Byte.pack(22)
	EXTERNAL_TRIGGER =Byte.pack(23)

	GET_VOLTAGE =Byte.pack(24)
	
	CAPTURE_DMASPEED =Byte.pack(31)
	GET_SCOPE_TRACE = Byte.pack(32)

	GET_LIST = Byte.pack(101)

	SET_PARAMETER = Byte.pack(30)
	PARAMETER_OPTIONS={
	'ADRC': 1,
	'SAMC': 2,
	'ADCS': 3,
	'DELAY': 4,
	'10BIT': 5,
	}

	BAUD = 500000
	version_len = 5
	name = 'Multi Channel Analyzer'
	histogram_version = 'CSMCA'
	list_mode_version = 'CSLM'
	portname = None
	traces = {}
	def __init__(self,**kwargs):
		self.buff=np.zeros(10000)
		self.name = 'Multi Channel Analyzer'
		self.listMode = 0 #No List mode parameters. 1= single param, 2=dual param ...

		self.occupiedPorts=set()
		self.blockingSocket = None
		self.connected=False
		self.DAC_ENABLED = False
		#self.PILEUP_REJECT_ENABLED = False
		self.EXTERNAL_TRIGGER_ENABLED = False
		self.VOLTMETER_ENABLED = False
		self.external_trigger_width = 2
		self.threshold = 65
		self.version=''
		self.version_number = 0
		self.total_bins = 1024
		self.bytes_per_bin = 4
		self.overflow = 0
		self.activeSpectrum = spectrum(1024,4)
		self.timebase = 1.
		self.samples = 500
		self.calPoly12 = np.poly1d([0, 3.3 / 4095, 0.])
		self.calPoly10 = np.poly1d([0, 3.3 / 1023, 0.])


		if 'port' in kwargs:
			try:
				self.connected=self.connectToPort(kwargs.get('port',None))
				if self.connected:
					return
			except Exception as ex:
				print('Failed to connect to ',self.portname,ex.message)
				
		elif kwargs.get('autoscan',False):	#Scan and pick a port	
			portList = getFreePorts()
			for a in portList:
				if portList[a]:
					try:
						self.connected=self.connectToPort(a)
						if self.connected:
							return
					except Exception as e:
						print (e)
				else:
					print(a,' is busy')



	def getSpectrum(self,**kwargs):
		'''
		Fetch spectrum by name, or last active spectrum. (self.activeSpectrum)
		'''
		name = kwargs.get('name',False)
		if not name: # No argument supplied
			if self.activeSpectrum:
				return self.activeSpectrum
			else:
				print("No offline data found, and  Device connection Status:",self.connected)
				return False
		return self.traces.get(name,None)

	def setCalibration(self,points,**kwargs):
		'''
		Prepares a calibration polynomial from channel numbers and corresponding energies
		[ [a1,b1] , [a2,b2] ...]
		a1,a2 ...  = channels
		b1,b2 ...  = energies
		'''
		spec = self.getSpectrum(**kwargs)
		if not spec:
			return False

		spec.setCalibration(points)

	def loadFile(self,filename,removeCal = False):
		self.traces[filename] = spectrum(1024,4,filename = filename) #Trace is an empty 1K histogram on init
		self.activeSpectrum = self.traces[filename]

	def loadListFile(self,filename,removeCal = False):
		self.traces[filename] = listSpectrum(1024,4,2,filename = filename, BINS2D=128)#empty dual list spectrum
		self.activeSpectrum = self.traces[filename]

	def __sendInt__(self,val):
		"""
		transmits an integer packaged as two characters
		:params int val: int to send
		"""
		self.fd.write(ShortInt.pack(int(val)))

	def __sendByte__(self,val):
		"""
		transmits a BYTE
		val - byte to send
		"""
		#print (val)
		if(type(val)==int):
			self.fd.write(Byte.pack(val))
		else:
			self.fd.write(val)

	def __getByte__(self):
		"""
		reads a byte from the serial port and returns it
		"""
		try:
			ss=self.fd.read(1)
			if len(ss): return Byte.unpack(ss)[0]
			else:
				print('byte communication error.',time.ctime())
				return 0
		except:
			return 0
	def __getInt__(self):
		"""
		reads two bytes from the serial port and
		returns an integer after combining them
		"""
		try:
			ss = self.fd.read(2)
			if len(ss)==2: return ShortInt.unpack(ss)[0]
			else:
				print('int communication error.',time.ctime())
				return 0
		except:
			return 0
	def __getLong__(self):
		"""
		reads four bytes.
		returns long
		"""
		try:
			ss = self.fd.read(4)
			if len(ss)==4: return Integer.unpack(ss)[0]
			else:
				print('long communication error.',time.ctime())
				return 0
		except:
			pass
	def __waitForData__(self,timeout=0.2):
		start_time = time.time()
		while (time.time()-start_time)<timeout:
			if self.fd.inWaiting():return True
		return False
	def __get_ack__(self):
		"""
		fetches the response byte
		1 SUCCESS
		2 ARGUMENT_ERROR
		3 FAILED
		used as a handshake
		"""
		x=self.fd.read(1)
		#print('pending',self.fd.read(10))
		try:return Byte.unpack(x)[0]
		except: return 3
	def connectToPort(self,portname):
		'''
		connect to a port, and check for the right version
		'''

		try:
			fd = serial.Serial(portname, self.BAUD, stopbits=1, timeout = 1.0)
			if fd.isOpen():
				#try to lock down the serial port
				if 'inux' in platform.system(): #Linux based system
					import fcntl
					try:
						fcntl.flock(fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
						#print ('locked access to ',portname,fd.fileno())
					except IOError:
						#print ('Port {0} is busy'.format(portname))
						return False

				else:
					pass
					#print ('not on linux',platform.system())

				if(fd.inWaiting()):
					fd.setTimeout(0.1)
					fd.read(1000)
					fd.flush()
					fd.setTimeout(1.0)

			else:
				#print('unable to open',portname)
				return False

		except serial.SerialException as ex:
			print ('Port {0} is unavailable: {1}'.format(portname, ex) )
			return False

		version= self.__get_version__(fd)
		version = version.decode() #Bytes to string
		subversion = ''
		version_number = 0

		self.CCS_ENABLED = False
		self.DAC_ENABLED = False
		self.SCOPE_ENABLED = False

		### Check Validity of the version
		if not version.startswith( (self.histogram_version,self.list_mode_version) ):
			print ('version check failed',len(version),version)
			self.version = ''
			self.fd = None
			return False
		
		self.name = version
		version_number = float(version[-3:])

		# HISTOGRAM MODE MCA
		if version.startswith(self.histogram_version):
			vercopy = version.split(self.histogram_version)[1] # remove version prefix CSMCA
			subversion = vercopy[:2]
			self.listMode = 0

		if version_number>=2.1:
			self.SCOPE_ENABLED = True
		# LIST MODE MCA
		elif version.startswith(self.list_mode_version):
			vercopy = version.split(self.list_mode_version)[1] # remove version prefix CSLM

			self.listMode = int(vercopy[0]) # e.g. 18K => 1 parameter. 8K bins.
			subversion = vercopy[1:3]

			self.CCS_ENABLED = False

		#print('MCA: ',subversion, version_number, self.listMode)

		if '-G-' in version or '-D-' in version: #In gamma spectrometers. Or if explicitly specified
			self.DAC_ENABLED = True
			print('DAC available for threshold setting')
			self.VOLTMETER_ENABLED = True
		if '-C-' in version: #Coincidence Gate
			print('Coincidence gate setting enabled. Voltmeter enabled.')
			self.EXTERNAL_TRIGGER_ENABLED = True
			self.VOLTMETER_ENABLED = True

		if subversion == '8K':
			print('version 8K')
			self.total_bins = 8192						
			self.bytes_per_bin = 2
			self.threshold = 65*8
			self.VOLTMETER_ENABLED = False
			self.CCS_ENABLED = False
		elif subversion == '4K':
			print('version 4K')
			self.total_bins = 4096						
			self.bytes_per_bin = 2
			self.threshold = 65*4
			self.VOLTMETER_ENABLED = False
			self.CCS_ENABLED = False
		elif subversion == '1K':
			self.total_bins = 1024
			self.threshold = 75
			self.bytes_per_bin = 4
			self.CCS_ENABLED = True




		self.version = version
		self.fd = fd
		self.version_number = version_number
		self.portname = portname
		if self.listMode: self.traces[self.portname] = listSpectrum(self.total_bins,self.bytes_per_bin,self.listMode)
		else:
			print('histogram mode MCA detected')
			self.traces[self.portname] = spectrum(self.total_bins,self.bytes_per_bin)
		self.activeSpectrum = self.traces[self.portname]

		return True

	def __get_version__(self,fd):
		fd.write(self.GET_VERSION)
		x=fd.readline()
		#print('remaining',[ord(a) for a in fd.read(10)])
		if len(x):
			x=x[:-1]
		return x

	def get_version(self):
		return self.__get_version__(self.fd)

	##### MAIN FEATURES FOR HISTOGRAM MCAs ########

	def startHistogram(self):
		'''
		Start sampling pulsesand sorting them into a hardware contained histogram.
		'''
		try:
			self.__sendByte__(self.START_HISTOGRAM)
			self.__get_ack__()

		except Exception as ex:
			print(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def stopHistogram(self):
		'''
		Stop sampling pulses
		'''
		print('stop invoked')
		try:
			self.__sendByte__(self.STOP_HISTOGRAM)
			self.__get_ack__()

		except Exception as ex:
			print(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def clearHistogram(self):
		'''
		Clear the histogram
		
		'''
		self.traces[self.portname].clearData()

		try:
			self.__sendByte__(self.CLEAR_HISTOGRAM)
			self.__sendInt__(0)
			self.__sendInt__(self.total_bins)
			self.__get_ack__()
			self.startCount() # Also clear the counter

		except Exception as ex:
			print(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)


	def startCount(self):
		'''
		Resets total even counter to 0
		'''
		try:
			self.__sendByte__(self.START_COUNT)
			self.__get_ack__()

		except Exception as ex:
			print(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def sync(self):
		'''
		START : Starting position . [0,1024]
		STOP : Ending position [START,1024]
		'''
		if not self.listMode : ##### HISTOGRAM DATA. FULL REFRESH.
			samples = self.total_bins
			splitting = 200
			data=b''
			try:
				for i in range(int(samples/splitting)):
					self.__sendByte__(self.GET_HISTOGRAM)
					self.__sendInt__(i*splitting)
					self.__sendInt__(splitting)
					data+= self.fd.read(int(splitting*self.bytes_per_bin))
					self.__get_ack__()

				if samples%splitting:
					self.__sendByte__(self.GET_HISTOGRAM)
					self.__sendInt__(samples-samples%splitting)
					self.__sendInt__(samples%splitting)
					data += self.fd.read(int(self.bytes_per_bin*(samples%splitting)))        
					self.__get_ack__()

				self.traces[self.portname].addRawData(data,threshold=self.threshold)
				self.activeSpectrum = self.traces[self.portname]
			except Exception as ex:
				print(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

		else: ### LIST MODE DATA . update with latest
			data_size = 2 #Values are 2 byte long short ints
			try:
				self.__sendByte__(self.GET_LIST)
				param_total = self.__getByte__()
				total = self.__getInt__()
				data = self.fd.read(total*data_size*param_total)
				self.__get_ack__()
				if len(data)>2:
					self.traces[self.portname].addRawData(data)
					self.activeSpectrum = self.traces[self.portname]
			except Exception as ex:
				print(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
				return


	def getHistogram(self,**kwargs):
		spec = self.getSpectrum(**kwargs)
		if not spec:
			return False

		return spec.getHistogram()

	def setParameter(self,param,value):
		reg = self.PARAMETER_OPTIONS.get(param)
		if reg is None:
			print('invalid option [%s]. try:'%param,self.PARAMETER_OPTIONS.keys())
			return
		self.__sendByte__(self.SET_PARAMETER)
		self.__sendByte__(reg)
		self.__sendByte__(value)
		print('param ack', self.__get_ack__())
		print(param, value)
		

	def setThreshold(self,thres, softwareThresholdAlso = False):
		'''
		Set number of bins to reject (Starting from 0)
		Max-value : 4095
		'''
		self.threshold = thres
		if self.DAC_ENABLED: #Hardware threshold control available. more efficient at rejecting pulses.
			chan = int(2*(thres-5)*4095/self.total_bins)
			if chan<0 : chan =0
			if chan>4095:
				print (chan,'exceeded HW threshold capability')
				chan = 4095
			self.setHWThreshold(chan)
			if self.listMode==2: #set 2nd channel with identical value also
				self.setHWThreshold(chan,2)
		
		#Software control implemented in firmware which rejects low value spikes
		if softwareThresholdAlso:
			self.setSWThreshold(thres)
	def scanI2C(self):
		'''
		scan for I2C devices : Threshold DAC uses I2C . Use this to check for its presence.
		'''
		self.__sendByte__(self.I2C_SCAN)
		x=[self.__getByte__() for a in range(16)]
		self.__get_ack__()
		return x

	def I2CWriteBulk(self,address,bytestream): 
		self.__sendByte__(self.I2C_WRITE)
		self.__sendByte__(address) #address
		self.__sendByte__(len(bytestream)) #Total bytes to write. <=255
		for a in bytestream:
			self.__sendByte__(Byte.pack(a))
		tmt = self.__getByte__()		
		self.__get_ack__()
		if tmt: return True #Hasn't Timed out.
		else: return False   #Timeout occured

	def I2CReadBulk(self,address,register,total): 
		self.__sendByte__(self.I2C_READ)
		self.__sendByte__(address) #address
		self.__sendByte__(register) #device register address
		self.__sendByte__(total) #Total bytes to read. <=255
		data = []
		for a in range(total):
			val = self.__getByte__()
			data.append(val)
		tmt = self.__getByte__()		
		return data,True if not tmt else False


	####### BMP280 ###################
	# https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf
	## Partly from https://github.com/farmerkeith/BMP280-library/blob/master/farmerkeith_BMP280.cpp
	BMP280_ADDRESS = 118
	BMP280_REG_CONTROL = 0xF4
	BMP280_REG_RESULT = 0xF6
	BMP280_HUMIDITY_ENABLED = False
	_BMP280_humidity_calib = [0]*6
	BMP280_oversampling = 0
	_BMP280_PRESSURE_MIN_HPA = 0
	_BMP280_PRESSURE_MAX_HPA = 1600
	_BMP280_sea_level_pressure = 1013.25 #for calibration.. from circuitpython library

	def BMP280_init(self):
		b = self.I2CWriteBulk(self.BMP280_ADDRESS,[0xE0,0xB6]) #reset
		time.sleep(0.1)
		self.BMP280_HUMIDITY_ENABLED = False
		b,tmt = self.I2CReadBulk(self.BMP280_ADDRESS, 0xD0 ,1)
		print(b)
		if b is None:return None
		b = b[0]
		if b in [0x58,0x56,0x57]:
			print('BMP280. ID:',b)
		elif b==0x60:
			self.BMP280_HUMIDITY_ENABLED = True
			print('BME280 . includes humidity')
		else:
			print('ID unknown',b)
		# get calibration data
		b,tmt = self.I2CReadBulk(self.BMP280_ADDRESS, 0x88 ,24) #24 bytes containing calibration data
		coeff = list(struct.unpack('<HhhHhhhhhhhh', bytes(b)))
		coeff = [float(i) for i in coeff]
		self._BMP280_temp_calib = coeff[:3]
		self._BMP280_pressure_calib = coeff[3:]
		self._BMP280_t_fine = 0.


		if self.BMP280_HUMIDITY_ENABLED:
			self.I2CWriteBulk(self.BMP280_ADDRESS, [0xF2,0b101]) #ctrl_hum. oversampling x 16
			#humidity calibration read 
			self._BMP280_humidity_calib = [0]*6
			val,tmt = self.I2CReadBulk(self.BMP280_ADDRESS,0xA1,1)
			self._BMP280_humidity_calib[0] = val[0]#H1
			coeff,tmt = self.I2CReadBulk(self.BMP280_ADDRESS,0xE1, 7) 
			coeff = list(struct.unpack('<hBbBbb', bytes(coeff)))
			self._BMP280_humidity_calib[1] = float(coeff[0])
			self._BMP280_humidity_calib[2] = float(coeff[1])
			self._BMP280_humidity_calib[3] = float((coeff[2] << 4) |  (coeff[3] & 0xF))
			self._BMP280_humidity_calib[4] = float((coeff[4] << 4) | (coeff[3] >> 4))
			self._BMP280_humidity_calib[5] = float(coeff[5])
			print('calibration data: ',self._BMP280_temp_calib,self._BMP280_humidity_calib)



		self.I2CWriteBulk(self.BMP280_ADDRESS, [0xF4,0xFF]) # ctrl_meas (oversampling of pressure, temperature)



	def _BMP280_calcTemperature(self,adc_t):
		v1 = (adc_t / 16384.0 - self._BMP280_temp_calib[0] / 1024.0) * self._BMP280_temp_calib[1]
		v2 = ((adc_t / 131072.0 - self._BMP280_temp_calib[0] / 8192.0) * ( adc_t / 131072.0 - self._BMP280_temp_calib[0] / 8192.0)) * self._BMP280_temp_calib[2]
		self._BMP280_t_fine = int(v1+v2)
		return (v1+v2) / 5120.0  #actual temperature. 

	def _BMP280_calcPressure(self,adc_p,adc_t):
		self._BMP280_calcTemperature(adc_t) #t_fine has been set now.
		# Algorithm from the BMP280 driver. adapted from adafruit adaptation
		# https://github.com/BoschSensortec/BMP280_driver/blob/master/bmp280.c
		var1 = self._BMP280_t_fine / 2.0 - 64000.0
		var2 = var1 * var1 * self._BMP280_pressure_calib[5] / 32768.0
		var2 = var2 + var1 * self._BMP280_pressure_calib[4] * 2.0
		var2 = var2 / 4.0 + self._BMP280_pressure_calib[3] * 65536.0
		var3 = self._BMP280_pressure_calib[2] * var1 * var1 / 524288.0
		var1 = (var3 + self._BMP280_pressure_calib[1] * var1) / 524288.0
		var1 = (1.0 + var1 / 32768.0) * self._BMP280_pressure_calib[0]
		if not var1:
			return _BMP280_PRESSURE_MIN_HPA
		pressure = 1048576.0 - adc_p
		pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
		var1 = self._BMP280_pressure_calib[8] * pressure * pressure / 2147483648.0
		var2 = pressure * self._BMP280_pressure_calib[7] / 32768.0
		pressure = pressure + (var1 + var2 + self._BMP280_pressure_calib[6]) / 16.0
		pressure /= 100
		if pressure < self._BMP280_PRESSURE_MIN_HPA:
			return self._BMP280_PRESSURE_MIN_HPA
		if pressure > self._BMP280_PRESSURE_MAX_HPA:
			return self._BMP280_PRESSURE_MAX_HPA
		return pressure


	def _BMP280_calcHumidity(self,adc_h,adc_t):
		self._BMP280_calcTemperature(adc_t) #t fine set.
		var1 = float(self._BMP280_t_fine) - 76800.0
		var2 = (self._BMP280_humidity_calib[3] * 64.0 + (self._BMP280_humidity_calib[4] / 16384.0) * var1)
		var3 = adc_h - var2
		var4 = self._BMP280_humidity_calib[1] / 65536.0
		var5 = (1.0 + (self._BMP280_humidity_calib[2] / 67108864.0) * var1)
		var6 = 1.0 + (self._BMP280_humidity_calib[5] / 67108864.0) * var1 * var5
		var6 = var3 * var4 * (var5 * var6)
		humidity = var6 * (1.0 - self._BMP280_humidity_calib[0] * var6 / 524288.0)
		if humidity > 100:
			return 100
		if humidity < 0:
			return 0

		return humidity

	def BMP280_all(self):
		if self.BMP280_HUMIDITY_ENABLED:
			data,tmt = self.I2CReadBulk(self.BMP280_ADDRESS, 0xF7,8)
		else:
			data,tmt = self.I2CReadBulk(self.BMP280_ADDRESS, 0xF7,6)
		#os = [0x34,0x74,0xb4,0xf4]
		#delays=[0.005,0.008,0.014,0.026]
		#self.I2CWriteBulk(self.BMP280_ADDRESS,[self.BMP280_REG_CONTROL,os[self.BMP280_oversampling] ])
		#time.sleep(delays[self.BMP280_oversampling])
		if tmt:return None
		if data is None:return None
		if None not in data:
			# Convert pressure and temperature data to 19-bits
			adc_p = (((data[0] & 0xFF) * 65536.) + ((data[1] & 0xFF) * 256.) + (data[2] & 0xF0)) / 16.
			adc_t = (((data[3] & 0xFF) * 65536.) + ((data[4] & 0xFF) * 256.) + (data[5] & 0xF0)) / 16.
			if self.BMP280_HUMIDITY_ENABLED:
				adc_h = (data[6] * 256.) + data[7]
				return [self._BMP280_calcPressure(adc_p,adc_t), self._BMP280_calcTemperature(adc_t), self._BMP280_calcHumidity(adc_h,adc_t)]
			else:
				return [self._BMP280_calcPressure(adc_p,adc_t), self._BMP280_calcTemperature(adc_t), 0]

		return None


	def setHWThreshold(self,thres,channel=1):
		'''
		Set number of bins to reject using DAC if available (Starting from 0)
		Max-value : 4095
		'''
		#self.threshold = thres
		if self.DAC_ENABLED: #Hardware threshold control available. more efficient at rejecting pulses.
			self.__sendByte__(self.SET_DAC)
			if self.listMode==2: #Specify channel also
				self.__sendByte__(channel-1)
			#print('DAC SET',channel,thres)
			self.__sendInt__(thres)
			self.__get_ack__()

		else:  
			return False

	def setSWThreshold(self,thres):
		'''
		Set number of bins to reject via the firmware interrupt (Starting from 0)
		Max-value : 512

		Software control implemented in firmware which rejects low value spikes
		'''
		if(thres>512):thres=512

		self.__sendByte__(self.SET_THRESHOLD)
		self.__sendInt__(thres)
		self.__get_ack__()

	def getStatus(self):
		'''
		Return running state , number of points acquired
		'''
		try:
			self.__sendByte__(self.GET_COUNT)
			C = self.__getLong__()
			S = True if self.__getByte__() else False
			self.__get_ack__()
			return S,C

		except Exception as ex:
			self.connected=False
			print(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)





	def getCCS(self):
		'''
		Return voltage at CCS
		'''
		try:
			self.__sendByte__(self.GET_CCS_VOLTAGE)
			V = self.__getInt__()
			self.__get_ack__()
			return 3.3*V/4095/16.

		except Exception as ex:
			print(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)


	def __getVoltage__(self,chan):
		'''
		Return voltage from CH0SA (chan)
		'''
		if self.VOLTMETER_ENABLED:
			self.__sendByte__(self.GET_VOLTAGE)
			self.__sendByte__(chan)
			V = self.__getInt__()
			self.__get_ack__()
			return 3.3*V/4095/16
		else:
			return False


	def getVoltage(self,chan):
		'''
		Return voltage . 'VM','THR','LM35','AN0'
		'''
		if self.VOLTMETER_ENABLED:
			chans = {'AN0':0,'THR':3,'LM35':5,'VMON':4,'CCS':6}
			if chan not in chans:
				print('invalid channel')
				return
			return self.__getVoltage__(chans[chan])
		else:
			return False

	def getTemperature(self):
		return self.getVoltage('LM35')*100





	#####FLASH READ/WRITE

	def readBulkFlash(self,numbytes):
		"""
		Read n(max 2k) BYTES from the flash
		"""
		try:
			self.__sendByte__(self.READ_BULK_FLASH)
			bytes_to_read = numbytes
			if numbytes%2: bytes_to_read+=1     #bytes+1 . stuff is stored as integers (byte+byte) in the hardware
			self.__sendInt__(bytes_to_read)   
			ss=self.fd.read(int(bytes_to_read))
			self.__get_ack__()
			if numbytes%2: return ss[:-1]   #Kill the extra character we read. Don't surprise the user with extra data
			return ss
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def writeBulkFlash(self,data):
		"""
		write a byte array to the entire flash page. Erases any other data

		data           Array to dump onto flash. Max size 2048 bytes
		"""
		if(len(data)>2048):
			print('length>2048 . trimming')
			data = data[:2048]
		if(type(data)==str):data = [ord(a) for a in data]
		if len(data)%2==1:data.append(0)
		try:
			self.__sendByte__(self.WRITE_BULK_FLASH)   #indicate a flash write coming through
			self.__sendInt__(len(data))  #send the length
			#self.__sendByte__(0) #Deprecated. Not used.
			for n in range(len(data)):
				self.__sendByte__(data[n])
				#Printer('Bytes written: %d'%(n+1))
			self.__get_ack__()
		except Exception as ex:
			print('write failed',ex)
			return

		#verification by readback
		tmp=[a for a in self.readBulkFlash(len(data))]
		print ('Verification done: ',tmp == data)
		if tmp!=data: print('Verification by readback failed')
	
	## MISCELLANEOUS OUTPUT FEATURES : SQUARE WAVE
	def setSqr1(self,freq,duty_cycle=50):
		if freq==0 or duty_cycle==0 : #Switch off SQR1
			print('disabled sqr1')
			self.__sendByte__(self.SET_SQR1)
			self.__sendInt__(0)
			self.__sendInt__(0)
			self.__sendByte__(4) #Disable
			self.__get_ack__()
			return
			
		if freq>100e3:
			print ('Frequency is greater than 100KHz. Not allowed')
			return 0
		p=[1,8,64,256]
		prescaler=0
		while prescaler<=3:
			wavelength = int(64e6/freq/p[prescaler])
			if wavelength<65525: break
			prescaler+=1
		if prescaler==4 or wavelength==0:
			return 0
		high_time = wavelength*duty_cycle/100.
		print ('set square wave[F:%d, DC:%.2f %%  | W:%d, HT:%d , PS: %d]'%(freq,duty_cycle,wavelength,high_time,prescaler))
		self.__sendByte__(self.SET_SQR1)
		self.__sendInt__(int(round(wavelength)))
		self.__sendInt__(int(round(high_time)))
		self.__sendByte__(prescaler)
		self.__get_ack__()

		return 64e6/wavelength/p[prescaler&0x3]

	def externalGate(self,state):
		'''
		Beta feature: An external trigger input is available on some variants to reject/accept pulses
		'''
		if self.EXTERNAL_TRIGGER_ENABLED:
			if state: state = 1
			else: state  = 0
			self.__sendByte__(self.EXTERNAL_TRIGGER)
			self.__sendByte__(self.external_trigger_width if state else 0)
			self.__get_ack__()
		else:
			print('External low-true gate for coincidence is only available for gamma spectrometer')


	def capture_init(self, chan, samples, tg, autoclear):
		if(self.version_number < 2.1):
			print('scope unavailable')
			return
		MAX_SCOPE_SAMPLES = 5000
		tg = int(tg * 8) / 8.  # Round off the timescale to 1/8uS units
		if (tg < 0.5): tg = int(0.5 * 8) / 8.
		if (samples >MAX_SCOPE_SAMPLES):
			self.__print__(f'Sample limit exceeded. {MAX_SCOPE_SAMPLES} max')
			samples = MAX_SCOPE_SAMPLES

		self.timebase = int(tg * 8) / 8.
		self.samples = samples
		CHOSA = chan
		try:
			self.__sendByte__(self.CAPTURE_DMASPEED)
			self.__sendByte__(CHOSA | (0x80 if autoclear else 0x00))  # |0x80 for autoclear
			self.__sendInt__(samples)  # total number of samples to record
			self.__sendInt__(int(tg * 8))  # Timegap between samples.  8MHz timer clock
			self.__get_ack__()

		except Exception as ex:
			print(ex, 'communication error')

	def get_pulse(self,chan, samples, tg, autoclear):
		if(self.version_number < 2.1):
			print('scope unavailable')
			return
		self.capture_init(chan, samples, tg, autoclear)
		time.sleep(1e-6 * self.samples * self.timebase + 0.1)
		y = self.__retrieveBufferData__(0, self.samples)

		return np.linspace(0, 1e-3 * self.timebase * (self.samples - 1), self.samples), self.calPoly10(y)  # time in mS


	def get_filtered_pulse(self, y, width):
		samples = len(y)
		ind = np.argmax(y)
		startindex=0
		endindex=0		
		if(ind<width/2):
			startindex=0
			endindex = width
		elif(ind > samples - width/2):
			startindex=samples - width
			endindex = samples
		else:
			startindex = ind-width/2
			endindex = ind+width/2
		startindex = int(startindex)
		endindex = int(endindex)
		return y[startindex:endindex]


	def __retrieveBufferData__(self, chan, samples):
		if(self.version_number < 2.1):
			print('scope unavailable')
			return
		data = b''
		self.data_splitting=500
		try:
			for i in range(int(samples / self.data_splitting)):
				self.__sendByte__(self.GET_SCOPE_TRACE)
				self.__sendInt__(self.data_splitting)
				self.__sendInt__(i * self.data_splitting)
				data += self.fd.read(
					int(self.data_splitting * 2))  # reading int by int sometimes causes a communication error. this works better.
				self.__get_ack__()

			if samples % self.data_splitting:
				self.__sendByte__(self.GET_SCOPE_TRACE)
				self.__sendByte__(chan)  # channel number starts with A0 on PIC
				self.__sendInt__(samples % self.data_splitting)
				self.__sendInt__(samples - samples % self.data_splitting)
				data += self.fd.read(int(2 * (
						samples % self.data_splitting)))  # reading int by int may cause packets to be dropped. this works better.
				self.__get_ack__()

		except Exception as ex:
			print(ex)

		try:
			for a in range(int(samples)): self.buff[a] = ShortInt.unpack(data[a * 2:a * 2 + 2])[0]
		except Exception as ex:
			msg = "Incorrect Number of Bytes Received\n"
			raise RuntimeError(msg)

		return self.buff[:int(samples)]



	############################ FITTING ROUTINES #####################################
	#-------------GAUSSIAN--------

	def gauss_erf(self,p,x,y):#p = [height, mean, sigma]
		return y - p[0] * np.exp(-(x-p[1])**2 /(2.0 * p[2]**2))

	def gauss_eval(self,x,p):
		return p[0] * np.exp(-(x-p[1])**2 /(2.0 * p[2]**2))

	def gaussianFit(self,region,**kwargs):
		try:
			from scipy.optimize import leastsq
		except:
			print('scipy module not found. aborting least square fit.')
			return None

		spec = self.getSpectrum(**kwargs)
		if not spec:
			return None

		Y = spec.getHistogram()
		if len(Y) == 2: #Dual parameter MCA
			Y = Y[kwargs.get('parameter',1) - 1] # Select the first trace by default
		X = spec.xaxis()

		FIT = {}
		start,end= region
		FIT['region'] = '%.1f - %.1f'%(start,end)
		start = (np.abs(X-start)).argmin() #Find closest index
		end = (np.abs(X-end)).argmin()
		X = np.array(X[start:end])
		Y = np.array(Y[start:end])
		
		#X+=(X[1]-X[0])/2.0  #Move the center to the center of the bins

		size = len(X)
		maxy = max(Y)
		halfmaxy = maxy / 2.0
		mean = sum(X*Y)/sum(Y)
		
		halfmaxima = X[int(len(X)/2)]
		for k in range(size):
			if abs(Y[k] - halfmaxy) < halfmaxy/10:
				halfmaxima = X[k]
				break
		sigma = mean - halfmaxima
		par = [maxy, mean, sigma] # Amplitude, mean, sigma				
		try:
			plsq = leastsq(self.gauss_erf, par,args=(X,Y))
		except:
			return None
		if plsq[1] > 4:
			print('fit failed')
			return None

		par = plsq[0]
		Xmore = np.linspace(X[0],X[-1],1000)
		par[1] += (X[1]-X[0])/2.0 #Move centroid to the center of the bins.
		Y = self.gauss_eval(Xmore, par)

		FIT['area'] = np.trapz(Y,dx = (Xmore[1]-Xmore[0]) )
		FIT['amplitude'] = par[0]; FIT['centroid'] = par[1];
		FIT['fwhm'] = abs(par[2]*2.355) #FWHM = sigma*2.355				
		FIT['type'] = 'gaussian'
		FIT['X'] = Xmore
		FIT['Y'] = Y
		return FIT
		
	#-------------GAUSSIAN WITH TAIL--------

	def gausstail_erf(self,p,x,y):#p = [height, mean, sigma,gamma]
		res = (y - p[0]*p[3]**2/(p[3]**2 + (x-p[1])**2))*(x<p[1]) + (y - p[0] * np.exp(-(x-p[1])**2 /(2.0 * p[2]**2)))*(x>p[1])
		return res 		


	def gausstail_eval(self,x,p):
		return (p[0]*p[3]**2/(p[3]**2 + (x-p[1])**2))*(x<p[1]) + (p[0] * np.exp(-(x-p[1])**2 /(2.0 * p[2]**2)))*(x>p[1])

		
	def gaussianTailFit(self,region,**kwargs):
		try:
			from scipy.optimize import leastsq
		except:
			print('scipy module not found. aborting least square fit.')
			return None

		spec = self.getSpectrum(**kwargs)
		if not spec:
			return None

		Y = spec.getHistogram()
		if len(Y) == 2: #Dual parameter MCA
			Y = Y[kwargs.get('parameter',1) - 1] # Select the first trace by default
		X = spec.xaxis()
		FIT = {}

		start,end= region
		FIT['region'] = '%.1f - %.1f'%(start,end)
		start = (np.abs(X-start)).argmin() #Find closest index
		end = (np.abs(X-end)).argmin()
		X = np.array(X[start:end])
		Y = np.array(Y[start:end])

		size = len(X)
		maxy = max(Y)
		halfmaxy = maxy / 2.0
		mean = sum(X*Y)/sum(Y)
		
		halfmaxima = X[int(len(X)/2)]
		for k in range(size):
			if abs(Y[k] - halfmaxy) < halfmaxy/10:
				halfmaxima = X[k]
				break
		sigma = mean - halfmaxima
		gamma = 2 # Lorentzian
		par = [maxy, mean, sigma,gamma] # Amplitude, mean, sigma				
		try:
			plsq = leastsq(self.gausstail_erf, par,args=(X,Y))
		except:
			return None
		if plsq[1] > 4:
			print('fit failed')
			return None

		par = plsq[0]
		Xmore = np.linspace(X[0],X[-1],1000)
		par[1] += (X[1]-X[0])/2.0 #Move centroid to the center of the bins.
		Y = self.gausstail_eval(Xmore, par)

		FIT['area'] = np.trapz(Y,dx = (Xmore[1]-Xmore[0]) )
		FIT['amplitude'] = par[0]; FIT['centroid'] = par[1];
		FIT['fwhm'] = abs(par[2]*1.17741 + par[3]) #FWHM = sigma*1.17741+gamma				
		FIT['gamma'] = par[3]
		FIT['type'] = 'gaussiantail'
		FIT['X'] = Xmore
		FIT['Y'] = Y
		return FIT




if __name__ == '__main__':
	a=connect(autoscan=True)
	#print ('version' , a.get_version() ,a.version)
	#print ('------------')
	#a.writeBulkFlash('Gammaspec1K 23 Sep 19\n511keV @ 82chan , @35degrees')
	#a.setThreshold(150)
	print(a.getVoltage('THR'))
	#for x in range(10,500):
	#	print(a.getVoltage('THR'),a.setThreshold(x))
	#	time.sleep(0.01)
	#a.startHistogram()
	#while 1:
	#	a.updateListBuffer()
	#	time.sleep(0.2)
	print(a.scanI2C())
	a.setSqr1(200,50)
	a.setThreshold(100)
	x,y = a.get_pulse(0,1000,0.5,False)
	print(y, max(y))
	#while 1:
	#	print(a.__getVoltage__(0))
	#for x in range(50,int(a.total_bins/3)):
	#	a.setThreshold(x)
	#	print(x)
	#	time.sleep(0.01)
	#a.startHistogram()
	#a.stopHistogram()
	#a.clearHistogram()
	#a.startCount()
	#for x in range(100):
	#	print a.getCCS(),a.getHistogram(),a.getStatus()
	#	time.sleep(0.1)
