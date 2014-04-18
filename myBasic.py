from itertools import combinations
import random
from math import radians, cos, sin, asin, sqrt
import numpy as num


def order(v,w,mode=0):
	a=zip(v,w)
	if mode==0:
		a.sort()
	else:
		a.sort(reverse=True)
	l=zip(*a)
	v=list(l[0])
	w=list(l[1])
	return [v,w]
	
def del_indices(ls,ind):
	w=[i for j, i in enumerate(ls) if j not in ind]
	return w
def makeOneLineCSV(fName):
	w=[]
	with open('csv/'+fName,'r') as f:
		for line in f:
			w.append(line.strip())
		s=','.join(w)
	f=open('csv/'+fName,'w')
	f.write(s)
	f.close()
	
def flatten(ls):
	return [item for sublist in ls for item in sublist]
	
def list2dic(ls,zs=None,ts=None):
	if zs is None:
		d={}
		for w in ls:
			try:
				d[w]=d[w]+1
			except KeyError:
				d[w]=1
		return d
	else:
		d={}
		for i,w in enumerate(ls):
			try:
				if ts is None:
					d[w]=d[w]+[zs[i]]
				else:
					d[w][1]=d[w][1]+[zs[i]]
					d[w][0]=d[w][0]+[ts[i]]
			except KeyError:
				if ts is None:
					d[w]=[zs[i]]
				else:
					d[w]=[[ts[i]],[zs[i]]]
		return d

def bracket(a,b,g):
	# 'a' is value list and 'b' is cluster labels
	# output is a list of list and a list of clusters
	# g is maximum gap allowed
	l=len(a)
	if l!=len(b):
		print 'length error in input of bracketing'
		return
	a,b=order(a,b)
	prev=b[0]
	prevV=a[0]
	outB=[]
	outC=[]
	s=a[0]
	for i in range(len(a)):
		if (b[i]!=prev or (a[i]-prevV)>g):
			outB.append([s,prevV])
			outC.append(prev)
			s=a[i]
			prevV=a[i]
			prev=b[i]
		else:
			prevV=a[i]
			prev=b[i]
	outB.append([s,prevV])
	outC.append(prev)
	return [outB,outC]
	
def joinBr(B,C):
	l=len(B)
	p=B[0]
	c=C[0]
	Br=[]
	Cr=[]
	bb=0
	jump=0
	for i in range(l):
		if i==0 : continue
		if (B[i][0]-p[1]<2) and (C[i]==c):
			p=[p[0],B[i][1]]
			bb=1
		else:
			Br.append(p)
			Cr.append(c)
			bb=0
			p=B[i]
			c=C[i]
	if bb==1:
		Br.append(p)
		Cr.append(c)
	else:
		Br.append(B[-1])
		Cr.append(C[-1])		
	return [Br,Cr]
	
def combSum(v,q=2):
	l=len(v)
	s=0.0
	if l < q:
		return 0
	for comb in combinations(v,2):
		s=s+comb[0]*comb[1]
	return 2*s / (l*(l-1))
	

def randColor():
	x = random.randint(0, 16777215)
	s= "#%x" % x
	return s

def pickColor(m):
	n=int(m)
	c=[	"#f00f00","#b00200","#000f10","#100100",
	"#ffffcc","#ff5400","#a7bf42","#ffff00",
	"#9937d2","#feb8c6","#780909","#cde312",
	"#19bac1","#fbfbfb","#195839","#514fad",
	"#0f0e1c","#9e143f","#0bf01c","#779679",
	"#0f1e11","#0e103f","#00001c","#779fff",
	"#f44f00","#b2b200","#0f0f10","#1b2100",
	"#044f0f","#02b20f","#0f0f1f","#0b210f",
	"#f00fc4","#f00404","#a00f44","#f00f04"]
	if n >= len(c):
		print "Color index exceeded. 'blue' was returned as default"
		return '#0000ff'
	return c[n]
	
def header2id(fName,key):
	#add id to each line showing the number of headers starting with key
	i=0
	m=0
	with open(fName,'r') as f:
		for line in f:
			if m==0:
				p=line.strip()+',Community,Quantity\n'
			t=line.split(',')
			if t[0]==key:
				if m!=0:
					for w in dic.keys():
						p=p+w+','+str(dic[w])+'\n'
				i=i+1
				dic={}
			else:
				w=line.strip()+','+str(i)
				if w not in dic.keys():
					dic[w]=1
				else:
					dic[w]=dic[w]+1
			m=1
	for w in dic.keys():
		p=p+w+','+str(dic[w])+'\n'
	return p

def geoDis(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km
    
#~ def peakDetection(seq,k,th):
	#~ """ This function finds peaks in a ordered sequence
	#~ seq is an input sequence
	#~ k is the number of neighbor points
	#~ th is the threshold for spikiness 
	#~ Please look at the paper "Simple Algorithms for Peak Detection in Time-Series"
	#~ output is list of indexes
	#~ """
	#~ l=len(seq)
	#~ output=[]
	#~ if l<(2*k+1):
		#~ return output
	#~ his=-100
	#~ hisI=-k-1
	#~ for i in range(l):
		#~ #S function number 3 in paper
		#~ if i<k:
			#~ b2=float(sum(seq[(i+1):(i+k+1)]))/k
			#~ e=(seq[i]-b2)/seq[i]
		#~ elif i>=(l-k):
			#~ b1=float(sum(seq[(i-k):i]))/k
			#~ e=(seq[i]-b1)/seq[i]
		#~ else:
			#~ b1=float(sum(seq[(i-k):i]))/k
			#~ b2=float(sum(seq[(i+1):(i+k+1)]))/k
			#~ b=(b1+b2)/2
			#~ e=(seq[i]-b)/seq[i]
		#~ print e
		#~ if e>th:
			#~ if i-hisI > k:
				#~ output.append(i)
				#~ his=seq[i]
				#~ hisI=i
			#~ else:
				#~ if seq[i]>his:
					#~ output[-1]=i
					#~ his=seq[i]
					#~ hisI=i
	#~ return output
	#~ 

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
	
def catX(a,r):
	"""return label for element of a
	based on resolution of r
	element (i*r)<a_i<(i+1)*r are labeled i and so on..."""
	L=[-1]*len(a)
	a1=sorted(enumerate(a),key=lambda pair:pair[1])
	b=zip(*a1)[1]
	I=zip(*a1)[0]
	minb=b[0]
	j=0
	for i,w in enumerate(b):
		if minb+(j*r)<= w < (j+1)*r+minb:
			L[I[i]]=j
		else:
			j=j+1
			L[I[i]]=j
	return L
	
def CDF(a,nBins=100):
	pdf,bins=num.histogram(a,nBins,density=True)
	cdf1=num.cumsum(pdf)
	g=bins[2]-bins[1]
	cdf=[x*g*100 for x in cdf1]
	x= bins[0:len(cdf)]
	return [cdf,x]

def PDF(a,nBins=100):
	pdf,bins=num.histogram(a,nBins,density=True)
	x= bins[0:len(pdf)]
	g=bins[2]-bins[1]
	return [[o*g for o in pdf],x]
	
#~ def avgDis(C):
	#~ """C is the list of the cities"""
	#~ with open('Files/latLong','r') as f:
		#~ for i,line in enumerate(f):
			#~ if i==0:
				#~ continue
			#~ city.append
			
#~ if __name__=='__main__':
	#~ seq=[10,8,5,1,4,8,9,6,3,7,12,13,15,20,210]
	#~ print catX(seq,4)
			
