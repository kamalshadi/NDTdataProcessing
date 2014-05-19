from myParser import *
from myDataMethods import *
import pylab
from signalSystem import *
from preprocess import *

if __name__ == '__main__':
	
	pl.figure()
	f=open('csv/timeseriCSV','r')
	idd,t,pV,patch = parseCSV(f,2)
	z=[float(x) for x in pV[1]]
	tp=[float(x) for x in t[1]]
	t1,z1=makeUniform(tp,z,1,0,max(tp),-10)
	z2=missValueFill(z1,5,-10)
	noise = list(num.random.normal(0,1,len(z2)))
	ax=pl.subplot(211)
	combf(dNorm(z2),24*10)
	combf(noise,24*10,'r')
	#~ spectrum(z2,1,True)
	pl.legend(["upload Time series", "white noise Time series"],loc=2,shadow=True, fancybox=True)
	pl.title("Client IP = 222.164.139.67")
	pl.xlabel('Periodicity in hour',fontsize=20)
	pl.ylabel('Synchronized average',fontsize=20)
	z=[float(x) for x in pV[3]]
	tp=[float(x) for x in t[3]]
	t1,z1=makeUniform(tp,z,1,0,max(tp),-10)
	z2=missValueFill(z1,5,-10)
	ax=pl.subplot(212)
	combf(dNorm(z2),24*10)
	combf(noise,24*10,'r')
	pl.legend(["upload Time series", "white noise Time series"],loc=2,shadow=True, fancybox=True)
	pl.title("Client IP = 58.182.185.215")
	pl.xlabel('Periodicity in hour',fontsize=20)
	pl.ylabel('Synchronized average',fontsize=20)
	pl.show()
