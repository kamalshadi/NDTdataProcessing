import sqlite3 as sq
import os
from myBasic import order,CDF
import pylab as pl
import numpy as num
from eventD import eventDetection
from recur import recPlot
from tsTransform import *
import math

def bina(ts,val,h):
	a=min(ts)
	b=max(ts)
	bl=int(num.ceil(float((b-a))/h))
	unused,he=num.histogram(ts,bl)
	xax=[.5*(he[i]+he[i+1]) for i in range(bl)]
	Z=[0.0]*bl
	j=1
	part=he[j]
	z=[]
	for i,xx in enumerate(ts):
		if xx<=part:
			z.append(val[i])
		else:
			Z[j-1]=num.median(z)
			z=[val[i]]
			j=j+1
			part=he[j]
	return ([float(xx-a)/3600 for xx in xax],Z)
	
def ts2pdf(ta,val,res):
	a=min(ts)
	dn=[int(xx-a)%(24*60*60) for xx in ts]
	
def KL(z):
	l=len(z)
	#KL distance to uniform(a,b) PDF
	S=1.0/l
	p=z
	kl=0
	for k in range(l):
		if p[k]==0 : pass
		else : kl=kl+(p[k]*math.log(p[k]/S))
	return kl/math.log(1.0/S) 	
			
			
		
		
	
	



def tsA(fName):
	dF='CSV/'+fName+'.db'
	if not os.path.exists(dF):
		print 'Error: Database does not exist'
		return
	D=sq.connect(dF)
	cur=D.cursor()
	qq="""select cP,Community,SPD,lt,download_rate,cAS
	from meta
	where 
	SPD not null and Community not null and SPD!=-1 and cP not null"""
	cur.execute(qq)
	A=cur.fetchall()
	D={}
	SP={}
	for w in A:
		try:
			D[(w[0],w[1],w[2],w[-1])]=D[(w[0],w[1],w[2],w[-1])]+[(w[3],w[4])]
		except KeyError:
			D[(w[0],w[1],w[2],w[-1])]=[(w[3],w[4])]
	for w in D.keys():
		temp=D[w]
		if len(temp)<700:
			del D[w]
	#~ pref,com,sp=zip(*D.keys())
	#~ d={}
	#~ for k,p in enumerate(pref):
		#~ try:
			#~ d[p].append((com[k],sp[k]))
		#~ except KeyError:
			#~ d[p]=[(com[k],sp[k])]
	#~ for ww in d.items():
		#~ print ww
		#~ raw_input('=================>')	
	p=[]
	l=str(len(D.keys()))
	for j,w in enumerate(D.keys()):
		print str(j)+' '+l
		temp=D[w]
		cP='"'+w[0]+'"'
		C=str(w[1])
		qq="select lt,download_rate\n\
		from meta\n\
		where\n \
		SPD=-1 and Community="+C+" and cP="+cP+";"
		cur.execute(qq)
		A=cur.fetchall()
		lt2,r2=zip(*A)
		lt,r=zip(*temp)
		ts=lt+lt2
		at=min(ts)
		y=r+r2
		tsd,zd=diurnalPDF(ts,y,2*60*60)
		ew=KL(zd)
		p.append(ew)
		if ew<.3:
			continue
		
	#~ y,x=CDF(p)
	#~ pl.plot(x,y)
	#~ pl.show()
		print tsd
		print zd
		pl.plot(tsd,zd)
		pl.show()
		raw_input('============>')
		ts,y=order(ts,y)
		tsp=[float(xx-at)/(3600) for xx in ts]
		out=eventDetection(y,sigma=num.var(r),l=30,p=0.01)
		#~ if len(out)>0:
		if True:
			f,ax=pl.subplots(3,sharex=True)
			ax[0].plot(tsp,y)
			ax[0].set_ylabel('Download(Mbps)')
			for xx in out:
				if xx[1]>0:
					ax[1].plot([tsp[xx[0]],tsp[xx[0]]],[0,xx[1]],'b-',lw=3)
				if xx[1]<0:
					ax[1].plot([tsp[xx[0]],tsp[xx[0]]],[0,xx[1]],'r-',lw=3)
			ax[1].axhline(0,lw=2,color='black')
			xax,Z=bina(ts,y,4*60*60)
			ax[2].plot(xax,Z,'c--')
			ax[2].set_xlabel('Time in hour')
			pl.suptitle('AS'+str(w[-1]),fontsize=20)
			pl.show()
			recPlot(Z,2)
			pl.show()
			#~ 
			#~ 
				
			
		

if __name__=="__main__":
	fName="ndt201401"
	tsA(fName)
	
	
