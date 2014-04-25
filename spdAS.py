import numpy as num
import pickle as pk
import sqlite3 as sq
from myBasic import PDF
import os
from scipy.stats.mstats import mquantiles
import pylab as pl

colL=['green','blue','red','gray','yellow']

def kernel(v,mode='T'):
	if mode=='T':
		return [1-xx[0] if -1<xx[0]<1 else 0.0 for xx in v]
	else:
		return [(1/num.sqrt(2*num.pi))*(num.exp(-(xx[0]*xx[0])/2)) for xx in v]
		

def densityEst(a,x,p,knn=1,Mode='G'):
	""" This is a density estimation currently supporting
	 one-dimensional Data.
	 There are two modes of operation:
	 knn==0 (Default) use fixed bandwidth.
	 knn==1 use k nearest neigbors.
	 Tow types of kernel are supported:
	 Mode=='T' (Default) for triangular.
	 Mode=='G' for Gaussian.
	 a is a vector of samples.
	 p is the parameter of model (bandwidth when knn=0 of number of neighbors
	 otherwise.
	 x is  points of estimation
	"""
	N=len(x)
	x.resize(N,1)
	l=len(a)
	a=num.array(a)
	a.resize(l,1)
	if knn==0:
		try:
			from sklearn.neighbors.kde import KernelDensity
		except ImportError:
			print 'Error:Please install sklearn package...'
			return
		if Mode=='T':
			S='linear'
		elif Mode=='G':
			S='gaussian'
		else:
			print 'Currently only G(gaussian) and T(triangular) Modes are supported'
			return
		kde = KernelDensity(kernel=S, bandwidth=p).fit(a)
		return (x,num.exp(kde.score_samples(x)))
	elif knn==1:
		try:
			from sklearn.neighbors import NearestNeighbors
		except ImportError:
			print 'Error:Please install sklearn package...'
			return
		neigh = NearestNeighbors(n_neighbors=p)
		neigh.fit(a)
		dist,index=neigh.kneighbors(x)
		H=dist[:,-1]
		est=[0.0]*N
		for i,point_v in enumerate(x):
			point=point_v[0]
			h=H[i]
			est[i]=sum(kernel((a-point)/h,Mode))/(l*h)
		return (x,est)
	else:
		print 'knn must be 0 or 1'
		return

def peakDetection(seq,k,th):
	""" This function finds peaks in a ordered sequence
	seq is an input sequence
	k is the number of neighbor points
	th is the threshold for spikiness 
	Please look at the paper "Simple Algorithms for Peak Detection in Time-Series"
	output is list of indexes
	"""

	l=len(seq)
	output=[]
	if l<(2*k+1):
		return output
	his=-100
	hisI=-k-1
	for i in range(l):
		#S function number 3 in paper
		if i<k:
			if i==0:
				b1=float('-inf')
			else:
				b1=float(sum(seq[0:i]))/i
			b2=float(sum(seq[(i+1):(i+k+1)]))/k
			el=(seq[i]-b2)/seq[i]
			er=(seq[i]-b1)/seq[i]

		elif i>=(l-k):
			if i==l-1:
				b2=float('inf')
			else:
				b2=float(sum(seq[(i+1):]))/len(seq[(i+1):])
			b1=float(sum(seq[(i-k):i]))/k
			er=(seq[i]-b1)/seq[i]
			el=(seq[i]-b2)/seq[i]
		else:
			b1=float(sum(seq[(i-k):i]))/k
			b2=float(sum(seq[(i+1):(i+k+1)]))/k
			el=(seq[i]-b1)/seq[i]
			er=(seq[i]-b2)/seq[i]
#		if el>th and er>th: #ORiginal
		if (el>th and er>th):
				if i-hisI > k:
					output.append(i)
					his=seq[i]
					hisI=i
				else:
					if seq[i]>his:
						output[-1]=i
						his=seq[i]
						hisI=i


	return output
	

def modePars(a,pN=.1,k=20,th=.01,np=1000,nf=1):
	""" This function detect service plans based on the peaks and valleys
	using KNN kernel estimation"""
	N=len(a)
	kern='G' #Gaussian kernel
	#pN Percent of neighbors
	# peak detection parameters
	# k,th are peak detection parameters
	#np number of points in kernel estimation
	x=num.linspace(min(a),max(a),np)
	x,est=densityEst(a,x,int(pN*N),knn=1,Mode=kern)
	mest=max(est)
	pl.plot(x,[xx*nf/mest for xx in est],'k',linewidth=2,label='KNN')
	ind=peakDetection(est,k,th)
	for j,i in enumerate(ind):
		pl.plot(x[i],est[i]*nf/mest,'*',mfc=colL[j],mec=colL[j],ms=20)
	nS=len(ind)
	if nS<2:
		if nS==0:
			spm=[(1.0,[float(x[0]),float(x[-1])],-1)]
		else:
			spm=[(1.0,[float(x[0]),float(x[-1])],float(x[ind[0]]))]
	else:
		spm=[0]*nS
		brp=-1
		for i in range(nS):
			brpO=brp
			if i<nS-1:
				brp=est.index(min(est[ind[i]:ind[i+1]]))
			if i==0:
				spp=len([xx for xx in a if xx<x[brp]])
				per=float(spp)/N
				spm[0]=(per,[float(x[0]),float(x[brp])],float(x[ind[i]]))
			elif i==nS-1:
				spp=len([xx for xx in a if xx>x[brp]])
				per=float(spp)/N
				spm[-1]=(per,[float(x[brp]),float(x[-1])],float(x[ind[i]]))
			else:
				spp=len([xx for xx in a if x[brpO]<xx<x[brp]])
				per=float(spp)/N
				spm[i]=(per,[float(x[brpO]),float(x[brp])],float(x[ind[i]]))
	return spm
	


if __name__=='__main__':
	#~ asn='9829'
	s=[]
	i=0
	with open('Files/pAS') as f:
		for line in f:
			if i==0:
				i=1
				continue
			s.append(line.strip('" \n'))
	s=['17813']
	fName='ndt201401'
	dateL='January 2014'
	dF='CSV/'+fName+'.db'
	asname='Mahanagar Telephone Nigam'
	if not os.path.exists(dF):
		print 'Error: Database not exists'
	else:
		D=sq.connect(dF)
		cur=D.cursor()
		for asn in s:
			AS='"'+str(asn)+'"'
			qq='''select download_rate,upload_rate
			from meta
			where
			cAS='''+AS
			cur.execute(qq)
			dR,uR=zip(*cur.fetchall())
			print 'Number of tests: '+str(len(dR))
			
			# Download data
			
			print 'Download rate analysis...'
			ad1,ad2=mquantiles(dR,[0.05,.95])
			zd=[xx for xx in dR if ad1<xx<ad2]
			yd,xd=PDF(zd)
			fig1=pl.figure()
			pl.subplot(121)
			pl.plot(xd,yd,'k--',label='Histogram')
			spm=modePars(zd,pN=.1,k=20,th=.01,np=1000,nf=max(yd))
			for i,w in enumerate(spm):
				a=w[1][0]
				if i==0:
					xlim1=a
				b=w[1][1]
				pl.axvspan(a, b, facecolor=colL[i], alpha=0.4,ec='none')
			pl.yticks([])
			pl.xlim([xlim1,b])
			pl.legend()
			pl.xlabel('Mbps (Download)',fontsize=20)
			pl.ylabel('PDF',fontsize=20)
			# upload data
			
			print 'Upload rate analysis...'
			ad1,ad2=mquantiles(uR,[0.05,.95])
			zd=[xx for xx in uR if ad1<xx<ad2]
			yd,xd=PDF(zd)
			pl.subplot(122)
			pl.plot(xd,yd,'k--',label='Histogram')
			spm=modePars(zd,pN=.1,k=20,th=.01,np=1000,nf=max(yd))
			for i,w in enumerate(spm):
				a=w[1][0]
				if i==0:
					xlim1=a
				b=w[1][1]
				pl.axvspan(a, b, facecolor=colL[i], alpha=0.4,ec='none')
			pl.legend()
			pl.xlim([xlim1,b])
			pl.xlabel('Mbps (Upload)',fontsize=20)
			pl.ylabel('PDF',fontsize=20)
			pl.yticks([])
			pl.suptitle('AS'+asn+' ('+dateL+')\n'+asname,fontsize=20)
			#~ pl.savefig('PIC/201401/'+asn, bbox_inches='tight')
			pl.show()
			print '-------------------------------------------------'

		
		
