import numpy as num
from pylab import *
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.mlab import csd
from myParser import *
from CDF import order
from scipy import signal
import math
from signalSystem import *
from preprocess import *
from myDataMethods import *


    
def SCF(z,fs,a=0):
	# this implementation is based on cross spectrum between u and v
	N=len(z)
	m=range(-N/2,N/2)
	u=num.array([z[k]*num.exp(-1j*num.pi*a*m[k]/fs) for k in range(N)])
	v=num.array([z[k]*num.exp(1j*num.pi*a*m[k]/fs) for k in range(N)])
	scfuv,freq=csd(v,u)
	scfu,freq=csd(u,u)
	scfv,freq=csd(v,v)
	scf=abs(scfuv)/((abs(scfu))*(abs(scfv)))**.5
	return scf,freq
	
def timeSmooth(x,f0,a,fs):
	f1=f0-a/2
	f2=f0+a/2
	df=max(a/2,1.0/(24*10))
	l=len(x)
	r=num.array(range(l))-l/2
	e1=num.exp(-1j*num.pi*f2*fs*r)
	e2=num.exp(-1j*num.pi*f1*fs*r)
	h1=signal.firwin(1000, [f1-df, f1+df], pass_zero=False)
	h2=signal.firwin(1000, [f2-df, f2+df], pass_zero=False)
	x1=signal.lfilter(h1,1,x)*e1
	x2=signal.lfilter(h2,1,x)*e2
	z=x1*x2
	h3=signal.firwin(1000, 2.0/(l*fs))
	out1=signal.lfilter(h3,1,z)
	out=sigPower(out1)
	return out

def combteeth(x,fs,T0,m=1):
	l=len(x)
	U=num.array([0]*l+[1]*l+[0]*l)
	nts=(num.array(range(len(U)))-len(U)/2)/float(fs)
	g=num.exp(2j*num.pi*nts*m/float(T0))*U
	g=g/sigPower(g)
	out=num.convolve(g,x)
	return out
	
	
	
	
	#~ mfreqz(h1)
	#~ mfreqz(h2)
	#~ show()
def SCF_block(x,fs,a):
	ts=1.0/float(fs)
	l=len(x)
	n=num.array(range(l))
	u=num.exp(-1j*num.pi*a*n*ts)*x
	v=num.exp(1j*num.pi*a*n*ts)*x
	scf,f=csd(u,v)
	uu,f=csd(u,u)
	vv,f=csd(v,v)
	Saf=abs(scf)/(abs(uu)*abs(vv))**.5
	return max(Saf)
	
def syncAve(z,l):
	fg=True
	ind=l
	out=num.array([0.0]*l)
	z=num.array(z)
	i=0
	while fg:
		try:
			unused=z[ind-1]
			out=out+z[(i*l):ind]
			ind=ind+l
			i=i+1
		except IndexError:
			break
	return sigPower(out/i)
	
def eigAve(z,l):
	fg=True
	ind=l
	out=[]
	z=num.array(z)
	i=0
	while fg:
		try:
			unused=z[ind-1]
			out.append(z[(i*l):ind])
			ind=ind+l
			i=i+1
		except IndexError:
			break
	C=num.corrcoef(out)
	eig_vals, eig_vecs = np.linalg.eig(C)
	e=sorted(num.abs(eig_vals),reverse=True)
	pl.plot(e)
	pl.title(str(l))
	pl.show()
	return e[0]/e[1]
	
	

if __name__ == '__main__':
	fs=float(24)
	T=[0.2,.4,.5,.6,1,2,3,4,5,6,7,7.5,8,9,10,11,12]
	M=[0,1,2,3,4]
	f=open('csv/timeseriCSV','r')
	idd,t,v,s = parseCSV(f,2)
	z=[]
	for o,w in enumerate(list(set(idd))):
		l=len(idd)
		if type(t[0])!=list :
			tp=[float(t[x]) for x in range(l) if idd[x]==w]
			vp=[float(v[x]) for x in range(l) if idd[x]==w]
		else :
			tp=[float(t[o][x]) for x in range(len(t[o]))]
			vp=[float(v[o][x]) for x in range(len(t[o]))]
			tp,vp = order(tp,vp)
			tp,vp = makeUniform(tp,vp,1,0,24*30,-10)
			vp = missValueFill(vp,5,-10)
			z.append(vp)
	
	N=len(z[0])-1+(len(z[0])%2)
	#~ N=10000
	w=z[0][0:N]
	#~ nn=num.array(range(N))
	#~ w=.1*num.sin(2*math.pi*nn/fs)-.1*num.sin(.3*math.pi*nn/fs)+0.15+.1*num.random.normal(0,1,N)
	#~ w=.1*num.random.normal(0,1,N)
	#~ pl.plot(nn,w,'k')
	#~ pl.plot(nn,ww)
	#~ pl.show()
	th=[0]*len(T)
	the=[0]*len(T)
	noise=z[2][0:N]
	#~ noise=num.random.normal(0,1,N)
	for i,T0 in enumerate(T):
		yy=combteeth(dNorm(w),fs,T0,1)
		zz=combteeth(dNorm(noise),fs,T0,1)
		th[i]=sigPower(yy)
		the[i]=sigPower(zz)
	th=num.array(th)
	the=num.array(the)
	figure()
	subplot(2,2,1)
	plot(dNorm(w))
	ax=gca()
	ax.yaxis.set_visible(False)
	ax.xaxis.set_visible(False)
	title('Sample time series 1')
	subplot(2,2,2)
	plot(dNorm(noise))
	ax=gca()
	ax.yaxis.set_visible(False)
	ax.xaxis.set_visible(False)
	title('Sample time series 2')
	subplot(2,2,3)
	vlines(T,[0]*len(T),th/min(th))	
	#label='222.164.139.67'
	xlabel('Period in days')
	ylabel('Relative resonance for time series 1')
	subplot(2,2,4)
	vlines(T,[0]*len(T),the/min(the))
	ylabel('Relative resonance for time series 2')
	xlabel('Period in days')
	#label='222.164.139.67'
	show()
		
