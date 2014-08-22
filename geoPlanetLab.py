# This python file tries to use ground truth data 
# from planetlab to quantifies errors in multilateration algorithms

from multiLateration import *
import sqlite3 as sq
import pylab as pl
from mpl_toolkits.basemap import Basemap
import numpy as num
from math import radians, cos, sin, asin, sqrt
from myBasic import *

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

def queryData(dF='dannyFull.db',cluster=1):
	Dc={}
	D=sq.connect(dF)
	cur=D.cursor()
	A=cur.execute("""select cIP,sID,min(minRTT),\
	min(slg),min(slat),min(clg),min(clat)
	from meta
	where cluster="""+str(cluster)+"""
	group by cIP,sID""")
	geoS={}
	gt={}
	for w in A:
		cIP=str(w[0])
		sID=str(w[1])
		try:
			Dc[cIP]=Dc[cIP]+[(str(w[1]),w[2])]
		except KeyError:
			Dc[cIP]=[(str(w[1]),w[2])]
		gt[cIP]=(w[5],w[6])
		geoS[sID]=(w[3],w[4])
	return (gt,geoS,Dc)

def visBg(ax):
	#~ m = Basemap(projection='cyl',llcrnrlat=23,urcrnrlat=50,\
				#~ llcrnrlon=-125,urcrnrlon=-60,resolution='c')
	m = Basemap(projection='cyl',llcrnrlat=10,urcrnrlat=70,\
				llcrnrlon=-160,urcrnrlon=-10,resolution='c')
	#~ m = Basemap(projection='merc',llcrnrlat=23,urcrnrlat=50,\
			#~ llcrnrlon=-125,urcrnrlon=-50,lat_ts=28,resolution='c')

	m.drawcoastlines(ax=ax,linewidth=2)
	m.drawstates(ax=ax)
	m.drawcountries(color='black',linewidth=2,ax=ax)
	m.fillcontinents(color='white',lake_color='aqua',ax=ax)
	m.drawparallels(num.arange(-90.,91.,30.),ax=ax)
	m.drawmeridians(num.arange(-180.,181.,60.),ax=ax)
	m.drawmapboundary(fill_color='aqua',ax=ax)
	return m
	
def visData(dF='dannyFull.db'):
	f,ax=pl.subplots()
	m=visBg(ax)
	D=sq.connect(dF)
	cur=D.cursor()
	A=cur.execute("""select clg,clat,cluster
	from meta
	group by clg,clat,cluster""")
	for w in A:
		clg=w[0]
		clat=w[1]
		x,y=m(clg,clat)
		cluster=w[2]
		ax.plot(x,y,'s',ms=10,color=pickColor(cluster))
	A=cur.execute("""select slg,slat
	from meta
	group by slg,slat""")
	for w in A:
		slg=w[0]
		slat=w[1]
		x,y=m(slg,slat)
		ax.plot(x,y,'b*',ms=20)
	ax.plot(-float('inf'),-float('inf'),'b*',label='Servers')
	ax.plot(-float('inf'),-float('inf'),'bs',label='Clients')
	ax.legend(loc=4)
	pl.show()
	

def rtt2dis(v):
	c=299792.458
	return v*c*2.0/3.0
	
def localizationDemo(dF='dannyFull.db'):
	D=sq.connect(dF)
	cur=D.cursor()
	geoS={}
	gt={}
	A=cur.execute("""select sID,min(slg),max(slat)
	from meta
	group by sID""")
	for w in A:
		geoS[w[0]]=(w[1],w[2])
	
	A=cur.execute("""select cIP,min(clg),max(clat)
	from meta
	group by cIP""")
	for w in A:
		gt[w[0]]=(w[1],w[2])
	Dc={}
	A=cur.execute("""select cIP,sID,min(minRTT)
	from meta
	group by cIP,sID""")
	for w in A:
		cIP=str(w[0])
		try:
			Dc[cIP]=Dc[cIP]+[(str(w[1]),w[-1])]
		except KeyError:
			Dc[cIP]=[(str(w[1]),w[-1])]

	col=['red','green','yellow']
	for key in Dc.iterkeys():
		if len(Dc[key])<3:
			continue
		ll=len(Dc[key])
		clg,clat=gt[key]
		f,ax=pl.subplots()
		m=visBg(ax)
		cx,cy=m(clg,clat)
		ax.plot(cx,cy,'r*',ms=20,label='Client')
		print key
		print '------------'
		cA=[]
		for q,tup in enumerate(Dc[key]):
			rtt=tup[1]
			dis=rtt2dis(rtt/2)
			slg,slat=geoS[tup[0]]
			sx,sy=m(slg,slat)
			dis=(dis/E.R)*(180/math.pi)
			cA.append(circle(point(sx,sy),dis))
			if q==ll-1:
				ax.plot(sx,sy,'bo',ms=15,label='Server')
			else:
				ax.plot(sx,sy,'bo',ms=15)
		try:
			p1=lse(cA,cons=True)
			p2=lse(cA,cons=False)
			ax.plot(p1.x,p1.y,'rd',ms=15,label='LSE-GC')
			ax.plot(p2.x,p2.y,'cd',ms=15,label='LSE')
		except cornerCases as hc:
			if hc.tag=='Disjoint':
				ax.set_title('Disjoint')
		ax.legend(loc=4)
		drawC(cA,ax)
		pl.show()

def localizationError(dF='dannyFull.db'):
	D=sq.connect(dF)
	cur=D.cursor()
	geoS={}
	gt={}
	A=cur.execute("""select sID,min(slg),max(slat)
	from meta
	group by sID""")
	for w in A:
		geoS[w[0]]=(w[1],w[2])
	
	A=cur.execute("""select cIP,min(clg),max(clat)
	from meta
	group by cIP""")
	for w in A:
		gt[w[0]]=(w[1],w[2])
	Dc={}
	A=cur.execute("""select cIP,sID,min(minRTT)
	from meta
	group by cIP,sID""")
	for w in A:
		cIP=str(w[0])
		try:
			Dc[cIP]=Dc[cIP]+[(str(w[1]),w[-1])]
		except KeyError:
			Dc[cIP]=[(str(w[1]),w[-1])]

	col=['red','green','yellow']
	e1=[]
	e2=[]
	f,ax=pl.subplots()
	m=visBg(ax)
	pl.close()
	for key in Dc.iterkeys():
		if len(Dc[key])<3:
			continue
		ll=len(Dc[key])
		clg,clat=gt[key]
		cx,cy=m(clg,clat)
		pc=point(cx,cy)
		cA=[]
		for q,tup in enumerate(Dc[key]):
			rtt=tup[1]
			dis=rtt2dis(rtt/2)
			slg,slat=geoS[tup[0]]
			sx,sy=m(slg,slat)
			dis=(dis/E.R)*(180/math.pi)
			cA.append(cir(point(sx,sy),dis))

		try:
			p1=lse(cA,cons=True)
			p2=lse(cA,cons=False)
			e1.append(p1.dist(pc)*math.pi*E.R/180000)
			e2.append(p2.dist(pc)*math.pi*E.R/180000)
		except cornerCases as hc:
			if hc.tag=='Disjoint':
				continue
	#in Kilometers
	return (e1,e2)

def errorVis(e,t):
	f,ax=pl.subplots(1)
	ax.boxplot(e, widths = 0.15)
	ax.set_xticks([1,2])
	ax.set_xticklabels(t)
	ax.set_ylabel('Error in km',fontsize=20)
	pl.show()
	
def disDelay(dF='dannyFull.db'):
	D=sq.connect(dF)
	cur=D.cursor()
	geoS={}
	gt={}
	A=cur.execute("""select sx,sy,cx,cy,delay
	from
	(
	select cIP,sID,min(minRTT) as delay,min(slg) as sx,min(slat) as sy,min(clg) as cx,min(clat) as cy
	from meta
	group by cIP,sID
	)""")
	d=[]
	dr=[]
	for w in A:
		sx=w[0]
		sy=w[1]
		cx=w[2]
		cy=w[3]
		rtt=w[4]
		d.append(rtt2dis(rtt/2))
		dr.append(geoDis(cx,cy,sx,sy))
	l=len(d)
	pl.plot(dr,[d[i]/(1000*dr[i]) for i in range(l)],'r*')
	pl.xlabel('d',fontsize=20)
	pl.ylabel(r'$\hat{d}/d$',fontsize=20)
	pl.show()
	

def clusterCen(method='LSE',prune=0,cluster=0,fg=False,ax=None):
	
	#Methods 'LSE' 'LSE-GC' 'ACF' 'CEN'
	#Prune 0 (To consider all data) 1 (To consider only minRTTs)
	
	gt,gs,D=queryData(cluster = cluster)
	l=len(D)
	cA=[]
	for w in D.items():
		cIP=w[0]
		sL=[x[0] for x in w[1]]
		cen=[point(gs[x]) for x in sL]
		rtt=[x[1] for x in w[1]]
		d=[rtt2dis(x/2) for x in rtt]
		dis=[(x/E.R)*(180/math.pi) for x in d]
		lc=len(cen)
		for i in range(lc):
			if sL[i]=='?':
				continue
			cA.append(circle(cen[i],dis[i]))
	if ax:
		dataVis(gt,gs,ax)
		drawC(cA,ax)
	p1=myWay(cA,p=.1)
	p2=myWay(cA,p=1)
	p3=lse(cA,cons=True)
	return (p1,p2,p3)
	
def dataVis(gt,gs,ax):
	for w in gt.values():
		ax.plot(w[0],w[1],'b*',ms=10)
	for w in gs.values():
		ax.plot(w[0],w[1],'rs',ms=5)
		
def clusterCen2(cluster=0,ax=None):
	gt,gs,D=queryData(cluster=cluster)
	S={}
	for w in D.values():
		for tup in w:
			ser=tup[0]
			if ser=='?':
				continue
			rtt=tup[1]
			try:
				if S[ser] > rtt:
					S[ser]=rtt
			except KeyError:
				S[ser]=rtt
	cA=[]
	for w in S.items():
		ser=w[0]
		rtt=w[1]
		cen=point(gs[ser])
		d=rtt2dis(rtt/2)
		dis=(d/E.R)*(180/math.pi)
		cA.append(circle(cen,dis))
	if ax:
		dataVis(gt,gs,ax)
		drawC(cA,ax)
	p1=myWay(cA,p=.1)
	p2=myWay(cA,p=1)
	p3=lse(cA,cons=True)
	return (p1,p2,p3)
	
def clusterCen3(cluster=0,ax=None):
	gt,gs,D=queryData(cluster=cluster)
	S={}
	for w in D.values():
		for tup in w:
			ser=tup[0]
			if ser=='?':
				continue
			rtt=tup[1]
			try:
				if S[ser] > rtt:
					S[ser]=rtt
			except KeyError:
				S[ser]=rtt
	cA=[]
	for w in S.items():
		ser=w[0]
		rtt=w[1]
		cen=point(gs[ser])
		d=rtt2dis(rtt/2)
		dis=(d/E.R)*(180/math.pi)
		cA.append(circle(cen,dis))
	if ax:
		dataVis(gt,gs,ax)
		drawC(cA,ax)
	nd=ndisc(cA)
	pp=nd.poly(math.pi/180)
	for p in pp:
		ax.plot(p.x,p.y,'ko')
	P=Polygon(pp)
	return P.centroid()

		
		
	
	
#~ if __name__=='__main__':
	#~ f,ax=pl.subplots(1)
	#~ p1=clusterCen3(ax=ax,cluster=1)
	#~ ax.plot(p1.x,p1.y,'cd',ms=20)
	#~ pl.title('East Cluster, Utilizing minimum measurements, Centroid',fontsize=20)
	#~ pl.show()
	#~ disDelay()
	#~ localizationDemo()
	#~ cluster=0
	#~ f,ax=pl.subplots()
	#~ visBg(ax)
	#~ p1,p2,p3=clusterCen(cluster=cluster,fg=False,ax=ax)
	#~ ax.plot(p1.x,p1.y,'ro',ms=20)
	#~ ax.plot(p2.x,p2.y,'bo',ms=20)
	#~ ax.plot(p3.x,p3.y,'ko',ms=20)
	#~ pl.show()
	

	
