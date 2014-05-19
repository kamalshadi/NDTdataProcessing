import numpy as num
import pylab as pl
from random import shuffle
from myBasic import PDF,order


def cumsum(a):
	xbar=num.mean(a)
	s=[0]*(len(a)+1)
	for j in range(len(a)):
		s[j+1]=s[j]+a[j]-xbar
	return s
	
def sdiff(a):
	return max(a)-min(a)
	
def bootstrap(a,t,n=1000):
	y=[]
	p=0
	for i in range(n):
		b=a
		shuffle(b)
		s=cumsum(b)
		sv=sdiff(s)
		y.append(sv)
		if t>sv:
			p=p+1
	return float(p)/n
	
def MSE(x,m):
	c1=num.array(x[0:m])
	c2=num.array(x[m:])
	x1=num.mean(c1)
	x2=num.mean(c2)
	return sum((c1-x1)*(c1-x1))+sum((c2-x2)*(c2-x2))
	
def split(x,h=10):
	l=len(x)
	if l<2*h:
		return -1
	ms=float('inf')
	msp=-1
	for m in range(h,l-h):
		b=MSE(x,m)
		if ms>b:
			ms=b
			msp=m
			
	return msp
	
def evDetection(d,p,ofset=0):
	s=cumsum(d)
	s0=sdiff(s)
	th=bootstrap(a,s0)
	m=[]
	go=True
	if th>p:
		m0=split(d)
		if m0!=-1:
			return (m+[m0+ofset]+evDetection(d[0:m0],p,ofset)+evDetection(d[m0:],p,ofset+m0))
		else :
			return []
	else:
		return []
	
	
	
	
if __name__=='__main__':
	a=list(num.random.normal(0,1,(200,1)));
	b=list(num.random.normal(2,1,(40,1)));
	c=list(num.random.normal(0,1,(200,1)));
	e=list(num.random.normal(0,1,(200,1)));
	t=list(num.random.normal(6,1,(30,1)));
	d=a+b+c+t+e
	#~ r=range(len(d))
	#~ unused,ranks=order(d,r)
	#~ pl.plot(r,ranks)
	#~ pl.show()
	m=evDetection(d,.95)
	f,ax=pl.subplots(2,sharex=True)
	ax[0].plot(range(len(d)),d)
	for m0 in m:
		ax[0].axvline(m0,ls='--',c='r')
	#~ ax[1].plot(range(len(s)),s)
	pl.show()
	

	
	
	
	
