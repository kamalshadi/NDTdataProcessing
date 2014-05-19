import sys
import pylab as pl
import numpy as num
import math
import itertools
from preprocess import *
import scipy.stats
from sklearn import mixture

def CDF(a):
	nBins=100
	pdf,bins=num.histogram(a,nBins,density=True)
	cdf1=num.cumsum(pdf)
	g=bins[2]-bins[1]
	cdf=[x*g*100 for x in cdf1]
	x= bins[0:len(cdf)]
	return [cdf,x]
	

def pair(ts,val,res,fg):
	# pairing to form (X,Y) for correlation analysis 
	l=len(ts)
	a=[min(c1) for c1 in ts]
	b=[max(c1) for c1 in ts]
	tb=min(a)
	te=max(b)
	Chunk=int(math.floor((te-tb)/res))
	T=[tb+res*i for i in range(Chunk+1)]
	T[-1]=te
	tr=[0]*Chunk
	vr=[[]]*l
	for k in range(Chunk):
		tr[k]=0.5*(T[k]+T[k+1])
	for k in range(l):
		vr1=[[]]*Chunk
		hel=[]
		for i,w in enumerate(ts[k]):
			for j in range(Chunk):
				a=T[j]
				b=T[j+1]
				if (a <= w <b ):
					vr1[j]=vr1[j]+[val[k][i]]
					break
			if w==te:
				vr1[-1]=vr1[-1]+[val[k][i]]
		hel=[num.mean(x) if x!=[] else fg for x in vr1]			
		vr[k]=hel
	return [tr,vr]
	
def missing(v,f):
	l=len(v)
	for i,x in enumerate(v):
		if x==f :
			continue
		else:
			break
	if i>0:
		v[0:i]=[v[i]]*i
	for x in range(2,l):
		if v[x]==f:
			v[x]=v[x-1]
	return v

def missOmit(v1,w1,fg):
	v=list(v1)
	w=list(w1)
	lt=len(w1)
	l=len(v1)
	if l!=lt:
		print 'ERROR'
		return
	ind=[]
	for k in range(l):
		if (v[k]==fg or w[k]==fg):
			ind.append(k)
	for offset, index in enumerate(ind):
		index -= offset
		del v[index]
		del w[index]
	return [v,w]
				
def order(v,w):
	a=zip(v,w)
	a.sort()
	l=zip(*a)
	v=list(l[0])
	w=list(l[1])
	return [v,w]
			
def plotT(ts,vs,patch):
	fg=-1
	l=len(ts)
	tr=[0]*l
	vr=[0]*l
	vr1=[0]*l
	fig=pl.figure()
	ax=fig.add_subplot(111)
	axx=[0]*l
	for h1 in range(l):
		tr[h1],vr[h1]=order(ts[h1],vs[h1])
		tp,vp=dataClean(tr[h1],vr[h1])
		#~ tp,vp=[tr[h1],vr[h1]]
		axx[h1]=fig.add_subplot(l,1,h1+1)
		axx[h1].plot(tr[h1],vr[h1],'r')
		axx[h1].plot(tp,vp,label=patch[h1])
		pl.legend()
	ax.set_ylabel('Upload Throughput',fontsize=20)
	ax.set_xlabel('Time in hour',fontsize=20)
	ax.spines['top'].set_color('none')
	ax.spines['bottom'].set_color('none')
	ax.spines['left'].set_color('none')
	ax.spines['right'].set_color('none')
	ax.tick_params(labelcolor='#BFBFBF', top='off', bottom='off', left='off', right='off')
	
def PDF(a,nBins=100):
	pdf,bins=num.histogram(a,nBins,density=True)
	x= bins[0:len(pdf)]
	g=bins[2]-bins[1]
	return [[o*g for o in pdf],x]
	
def plotP(a,nBins,s):
	l=len(a)
	axx=[0]*l
	fig=pl.figure()
	ax=fig.add_subplot(111)
	for h1,w in  enumerate(a):
		b,c = PDF(w,nBins)
		axx[h1]=fig.add_subplot(l,1,h1+1)
		axx[h1].plot(c,b,label=s[h1])
		#~ pl.xlim(0.1,0.2)
		pl.legend()
	ax.set_ylabel('PDF',fontsize=20)
	ax.set_xlabel('Downloadload Throughput',fontsize=20)
	ax.spines['top'].set_color('none')
	ax.spines['bottom'].set_color('none')
	ax.spines['left'].set_color('none')
	ax.spines['right'].set_color('none')
	ax.tick_params(labelcolor='#BFBFBF', top='off', bottom='off', left='off', right='off')
	
	
def CC(x,z):
	x=[kk-num.mean(x) for kk in x]
	z=[kk-num.mean(z) for kk in z]
	l1=len(x)
	l2=len(z)
	if l1!=l2:
		print 'ERROR'
		return
	l=l1
	p=(l+1)/3
	c=x[p:(2*p)]
	w=[0]*(2*p+1)
	for q in range(2*p+1):
		temp=num.correlate(c,z[(0+q):(q+p)])
		w[q]=temp[0]
	t=[kk-p for kk in range(2*p+1)]
	return [t,w]

def dia(x,z):
	x0=num.mean(x)
	z0=num.mean(z)
	l=len(x)
	d=[]
	for j in range(l):
		d.append(math.sqrt((x[j]-x0)**2+(z[j]-z0)**2))
	B=sum(d)
	A=(max(x)-min(x))*(max(z)-min(z))
	return B/(float(l)*A)

def outlierOmit(x,z,r):
	l=len(x)
	i=0
	d=[]
	for ll in itertools.combinations([j for j in range(l)],2):
		d.append(math.sqrt((x[ll[0]]-x[ll[1]])**2+(z[ll[0]]-z[ll[1]])**2))
		i=i+1
	Th=sum(d)/float(i)
	ind=[]
	x0=num.mean(x)
	z0=num.mean(z)
	for k in range(l):
		dd=math.sqrt((x[k]-x0)**2+(z[k]-z0)**2)
		if (dd>(r*Th)):
			ind.append(k)
	for offset, index in enumerate(ind):
		index -= offset
		del x[index]
		del z[index]
	return [x,z]
	
def nTHist(ts,endt,r,patch):
	l=len(ts)
	nBins=(endt)/r
	fig=pl.figure()
	ax=fig.add_subplot(111)
	axx=[0]*l
	his=[[]]*l
	for k in range(l):
		his[k],p = num.histogram(ts[k],nBins)
		axx[k]=fig.add_subplot(l,1,k+1)
		axx[k].plot(p[0:len(his[k])],his[k],label=patch[k])
		pl.legend()
		pl.xlim(0,72)
	ax.set_ylabel('Number of test',fontsize=20)
	ax.set_xlabel('Time in hour',fontsize=20)
	ax.spines['top'].set_color('none')
	ax.spines['bottom'].set_color('none')
	ax.spines['left'].set_color('none')
	ax.spines['right'].set_color('none')
	ax.tick_params(labelcolor='#BFBFBF', top='off', bottom='off', left='off', right='off')
	
def bhatt(x,z,nBins):
	#~ x0=dNorm(x,1)
	#~ z0=dNorm(z,1)
	x0=x
	z0=z
	a1=min(x0)
	a2=min(z0)
	a=min(a1,a2)
	b1=max(x0)
	b2=max(z0)
	b=max(b1,b2)
	res=(b-a)/nBins
	bins=[a+res*j for j in range(nBins+1)]
	bins[-1]=b
	xp0,unused =PDF(x,bins)
	zp0,unused =PDF(z,bins)
	a=sum([math.sqrt(xp0[k]*zp0[k]) for k in range(nBins)])
	b=-100*math.log(a)
	
	return b
	
def KL(z,a=0,b=24,r=1):
	#KL distance to uniform(a,b) PDF
	D=float(b-a)
	S=1.0/D
	nBins=[a+i*r for i in range(int(D/r))]+[b]
	p,b = PDF(z,nBins)
	g=b[1]-b[0]
	u=g*S
	l=len(b)
	kl=0
	for k in range(l):
		if p[k]==0 : pass
		else : kl=kl+(p[k]*math.log(p[k]/u))
	return kl/math.log(1.0/u) 
	

def moment(z,i,Central='True'):
	if i==1:
		r=num.mean(z)
	else:
		if Central :
			a=num.std(z)
			if (i<3): a=1
			w=(num.array(z)-num.mean(z))/a
			r=num.mean(w**i)
		else :
			w=num.array(z)
			r=num.mean(w**i)
	return r
		
			
def bicMetric(X,plot=False):
	if type(X[0])!=list :
		X=num.array([[xx] for xx in X])
		cv_types = ['full']
	else:
		cv_types = ['spherical', 'tied', 'diag', 'full']
	lowest_bic = num.infty
	bic = []
	n_components_range = range(1, 7)
	for cv_type in cv_types:
		for n_components in n_components_range:
			# Fit a mixture of gaussians with EM
			gmm = mixture.GMM(n_components=n_components, covariance_type=cv_type)
			gmm.fit(X)
			bic.append(gmm.bic(X))
			if bic[-1] < lowest_bic:
				lowest_bic = bic[-1]
				best_gmm = gmm
	if plot:
		bic = num.array(bic)
		color_iter = itertools.cycle(['k', 'r', 'g', 'b', 'c', 'm', 'y'])
		clf = best_gmm
		bars = []
		# Plot the BIC scores
		spl = pl.subplot(2, 1, 1)
		for i, (cv_type, color) in enumerate(zip(cv_types, color_iter)):
			xpos = num.array(n_components_range) + .2 * (i - 2)
			bars.append(pl.bar(xpos, bic[i * len(n_components_range):
										 (i + 1) * len(n_components_range)],
							   width=.2, color=color))
		pl.xticks(n_components_range)
		pl.ylim([bic.min() * 1.01 - .01 * bic.max(), bic.max()])
		pl.title('BIC score per model')
		xpos = num.mod(bic.argmin(), len(n_components_range)) + .65 +\
			.2 * num.floor(bic.argmin() / len(n_components_range))
		pl.text(xpos, bic.min() * 0.97 + .03 * bic.max(), '*', fontsize=14)
		spl.set_xlabel('Number of components')
		spl.legend([b[0] for b in bars], cv_types)
	return best_gmm
		
# End of CDF.py
