from eventD import eventDetection
import pylab as pl
import numpy as num

if __name__=='__main__':
	a=num.random.normal(10,3,100)
	b=num.random.normal(7,3,33)
	c=num.random.normal(10.2,3,67)
	d=list(a)+list(b)+list(c)
	f,ax=pl.subplots(2,sharex=True)
	ax[0].plot(d)
	out=eventDetection(d,sigma=9,l=30,p=0.05)
	for xx in out:
		if xx[1]>0:
			ax[1].plot([xx[0],xx[0]],[0,xx[1]],'b-',lw=3)
		if xx[1]<0:
			ax[1].plot([xx[0],xx[0]],[0,xx[1]],'r-',lw=3)
	ax[1].axhline(0,lw=2,color='black')
	pl.show()
