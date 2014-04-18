import numpy as num
import pickle as pk
from sqliteDB import makeDB

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
			b2=float(sum(seq[(i+1):(i+k+1)]))/k
			el=(seq[i]-b2)/seq[i]
			er=th+1
		elif i>=(l-k):
			b1=float(sum(seq[(i-k):i]))/k
			er=(seq[i]-b1)/seq[i]
			el=th+1
		else:
			b1=float(sum(seq[(i-k):i]))/k
			b2=float(sum(seq[(i+1):(i+k+1)]))/k
			el=(seq[i]-b1)/seq[i]
			er=(seq[i]-b2)/seq[i]
		if el>th and er>th:
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
	

def modePars(a,pN=.1,k=20,th=.01,np=1000):
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
	ind=peakDetection(est,k,th)
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
	
def spDump(fName,bgpFile,the=4320):
	try:
		from scipy.stats.mstats import mquantiles
	except ImportError:
		print 'Error:Please install scipy package...'
		return
	try:
		import SubnetTree
	except ImportError:
		print 'Error:Please install SubnetTree package...'
		return

	i=0
	bf=open('BGP/'+bgpFile,'r')
	t = SubnetTree.SubnetTree()
	print 'Building subnet network from BGP table'
	asDic={}
	ASdic={}
	for lines in bf:
		if i==0:
			i=1
			continue
		net=lines.strip().split()[-1].strip()
		asn=lines.strip().split()[0].strip()
		asDic[net]=asn
		t[net]=net

	print 'Parsing Raw Data...'
	i=0
	with open('CSV/'+fName) as f:
		for line in f:
			if i==0:
				i=1
				continue
			w=line.split(',')
			ip=w[0].strip()
			d=float(w[3].strip())
			u=float(w[4].strip())
			try:
				net=t[ip]
				asn=asDic[net]
				output=(d,u)
			except KeyError:
				continue
			try:
				ASdic[asn].append(output)
			except KeyError:
				ASdic[asn]=[output]
	k=ASdic.keys()
	model={}
	i=0
	lsp=[w for w in ASdic.keys() if len(ASdic[w])>the]
	ll=len(lsp)
	for w in lsp:
		a=ASdic[w]
		bd=list(zip(*a)[0])
		ad1,ad2=mquantiles(bd,[0.05,.95])
		zd=[xx for xx in bd if ad1<xx<ad2]
		bu=list(zip(*a)[1])
		au1,au2=mquantiles(bu,[0.05,.95])
		zu=[xx for xx in bu if au1<xx<au2]
		i=i+1
		print str(i)+' / '+str(ll)+':AS-SP-Model for AS'+w+ '(#points: '+str(len(a))+')'
		spmd=modePars(zd)
		spmu=modePars(zu)
		model[w]=(spmd,spmu)
	print 'Saving Service Plan Model'
	f=open('Model/'+fName+'.pk','w')
	pk.dump(model,f)

#~ if __name__=='__main__':
	#~ spDump('ndt201401','01jan14')	
	#~ print 'Making Database....'
	#~ makeDB(fName,bgpFile)
		
		
