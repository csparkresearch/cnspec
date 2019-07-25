import numpy as np
from scipy.optimize import leastsq

############################ FITTING ROUTINES #####################################
def closestIndex(arr,val):
	return (np.abs(arr-val)).argmin()

#-------------GAUSSIAN--------

def gauss_erf(p,x,y):#p = [height, mean, sigma]
	return y - p[0] * np.exp(-(x-p[1])**2 /(2.0 * p[2]**2))

def gauss_eval(x,p):
	return p[0] * np.exp(-(x-p[1])**2 /(2.0 * p[2]**2))

def gaussfit(x,y,region):
	FIT = {}
	start,end= region
	FIT['region'] = '%.1f - %.1f'%(start,end)
	start = closestIndex(x,start)
	end = closestIndex(x,end)
	X = np.array(x[start:end])
	Y = np.array(y[start:end])
	
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
		plsq = leastsq(gauss_erf, par,args=(X,Y))
	except:
		return None
	if plsq[1] > 4:
		print('fit failed')
		return None

	par = plsq[0]
	Xmore = np.linspace(X[0],X[-1],1000)
	par[1] += (X[1]-X[0])/2.0 #Move centroid to the center of the bins.
	Y = gauss_eval(Xmore, par)

	FIT['area'] = np.trapz(Y,dx = (Xmore[1]-Xmore[0]) )
	FIT['amplitude'] = par[0]; FIT['centroid'] = par[1];
	FIT['fwhm'] = abs(par[2]*2.355) #FWHM = sigma*2.355				
	FIT['type'] = 'gaussian'

	return Xmore,Y,par,FIT

#-------------GAUSSIAN WITH TAIL--------

def gausstail_erf(p,x,y):#p = [height, mean, sigma,gamma]
	res = (y - p[0]*p[3]**2/(p[3]**2 + (x-p[1])**2))*(x<p[1]) + (y - p[0] * np.exp(-(x-p[1])**2 /(2.0 * p[2]**2)))*(x>p[1])
	return res 		


def gausstail_eval(x,p):
	return (p[0]*p[3]**2/(p[3]**2 + (x-p[1])**2))*(x<p[1]) + (p[0] * np.exp(-(x-p[1])**2 /(2.0 * p[2]**2)))*(x>p[1])

	
def gausstailfit(x,y,region):
	FIT = {}
	start,end= region
	FIT['region'] = '%.1f - %.1f'%(start,end)
	start = closestIndex(x,start)
	end = closestIndex(x,end)
	X = np.array(x[start:end])
	Y = np.array(y[start:end])

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
		plsq = leastsq(gausstail_erf, par,args=(X,Y))
	except:
		return None
	if plsq[1] > 4:
		print('fit failed')
		return None

	par = plsq[0]
	Xmore = np.linspace(X[0],X[-1],1000)
	par[1] += (X[1]-X[0])/2.0 #Move centroid to the center of the bins.
	Y = gausstail_eval(Xmore, par)

	FIT['area'] = np.trapz(Y,dx = (Xmore[1]-Xmore[0]) )
	FIT['amplitude'] = par[0]; FIT['centroid'] = par[1];
	FIT['fwhm'] = abs(par[2]*1.17741 + par[3]) #FWHM = sigma*1.17741+gamma				
	FIT['gamma'] = par[3]
	FIT['type'] = 'gaussiantail'

	return Xmore,Y,par,FIT
