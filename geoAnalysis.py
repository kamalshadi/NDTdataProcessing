import numpy as num
from ipClass import *
import sqlite3 as sq
import pickle as pk
from itertools import combinations
from math import radians, cos, sin, asin, sqrt
import pylab as pl

def bini(ip):
	ls=str(ip).split('.')
	temp1=[bin(int(x))[2:] for x in ls]
	temp2=['0'*(8-len(w))+w for w in temp1]
	return ''.join(temp2)

def ip2sub(ip,s):
	b=bini(ip)
	temp1=b[:s] + '0'*(32-s)
	return temp1

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
    
    
def idis(a):
	d=[]
	for w in a:
		l=len(w)
		if l<2:
			continue
		for comb in combinations(w,2):
			g1=comb[0]
			g2=comb[1]
			d.append(geoDis(g1[1],g1[0],g2[1],g2[0]))
	return d

def uosM(ip,uosm):
	C=-1
	for k,w in enumerate(uosm):
		for sub1 in w.split('U'):
			sub=sub1.strip()
			P,S=sub.split('/')
			if ip2sub(ip,int(S))==bini(str(P)):
				C=k
				break
		if C!=-1:
			break
	return C

if __name__=='__main__':
	asnL=[]
	cpL=[]
	geoF='CSV/geo2014_01'
	db='CSV/ndt201401.db'
	mod='Model/uos-ndt201401.pk'
	D={}
	cPgeo={}
	uosgeo={}
	print 'Building Dictionary...'
	with open(geoF) as f:
		for i,line in enumerate(f):
			if i==0:
				continue
			ip1,lat,lg=line.split(',')
			cIP=ip1.strip()
			D[cIP]=(float(lat),float(lg))
	print 'Query Data ...'
	Db=sq.connect(db)
	cur=Db.cursor()
	qq='''select cIP,cP,cAS
	from meta
	where SPU not null'''
	cur.execute(qq)
	print 'Loading the UoS model'
	with open(mod) as f:
		M=pk.load(f)
	F=True
	count=0
	err=0
	while F:
		ro=cur.fetchone()
		if ro is None:
			break
		ip=ro[0].strip()
		try:
			geo=D[ip]
		except KeyError:
			continue
		cP=ro[1].strip()
		asn=ro[2]
		try:
			uosm=M[cP]
		except KeyError:
			continue
		C=uosM(str(ip),uosm)
		if C==-1:
			continue
		try:
			uosgeo[(cP,C)]=uosgeo[(cP,C)]+[geo]
		except KeyError:
			uosgeo[(cP,C)]=[geo]
		try:
			cPgeo[cP]=cPgeo[cP]+[geo]
		except KeyError:
			cPgeo[cP]=[geo]
		asnL.append(asn)
		cpL.append(cP)
	duos1=num.array(idis(uosgeo.values()))
	duos=list(duos1[duos1<1000])
	print len(duos)
	dcp1=num.array(idis(cPgeo.values()))
	dcp=list(dcp1[dcp1<1000])
	print len(dcp)
	y1,x1=CDF(duos)
	y2,x2=CDF(dcp)
	pl.plot(x1,y1,'r',label='UoS')
	pl.plot(x2,y2,'b',label='BGP Prefixes')
	pl.xlabel('Distance in km',fontsize=20)
	pl.ylabel('CDF',fontsize=20)
	pl.legend()
	pl.show()
	
	
		

		
		
		
		
