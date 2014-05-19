import numpy as num
import pylab as pl
from scipy.spatial.distance import pdist,squareform
from scipy.stats.mstats import mquantiles

def recMat(u,m):
	# This function returns recurrence matrix from univariate time series
	# u is the time series
	# m is the dimension for reconstruction phase
	l=len(u)
	nv=l-m+1
	d=num.zeros((nv,m))
	for i in range(nv):
		d[i,:]=u[i:(i+m)]
	return pdist(d)
	
def recBinary(d,method='RR',param=.1):
	# This will convert d1 matrix to binary
	# two methods are implemented fixed recursion rate(RR) and number of neighbors=NN
	# param is the parameter of each method
	if method=='RR':
		rr=mquantiles(d,param)
		d1=num.sign(d-rr)
		d1[d1>=-0.1]=1
	else:
		d1=None
	return d1
		
		
def recPlot(u,m):
	d1=recMat(u,m)
	d2=recBinary(d1)
	d=squareform(d2)
	print d
	#~ vmin=min(d1)
	#~ vmax=max(d1)
	d=squareform(d1)
	nb=num.shape(d)[0]
	y,x=num.mgrid[1:nb,1:nb]
	#~ pl.pcolor(d,vmin=vmin, vmax=vmax)
	#~ pl.colorbar()
	pl.imshow(d>.5,cmap='Greys', interpolation='nearest')
	
#~ if __name__=='__main__':
	#~ t=num.array(range(1000))
	#~ u=num.sin(2*num.pi*.05*t)
	u=[1,3,2,4,5,1,0,-1,2,3,-1,2.3]
	#~ recPlot(u,2)
	#~ pl.colorbar()
	#~ pl.show()
	
	
	
