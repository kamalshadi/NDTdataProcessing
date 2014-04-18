import pylab as pl
import numpy as num
import sqlite3 as sq
import pickle as pk
import os
from spd import densityEst
from scipy.stats.mstats import mquantiles
from myBasic import PDF

fName='ndt201401'
dF='CSV/'+fName+'.db'
sF='Model/'+fName+'.pk'
fg=0
if not os.path.exists(dF) or not os.path.exists(sF):
	fg=1

D=sq.connect(dF)
cur=D.cursor()

def visSP(asn):
	with open(sF) as f:
		asd=pk.load(f)
		spd,spu=asd[str(asn)]
	print 'Detected Download SP: '+str(len(spd))
	print 'Detected Upload SP: '+str(len(spu))
	# AS is Autonomous number
	AS='"'+str(asn)+'"'
	qq='''select download_rate,upload_rate
	from meta
	where
	cAS='''+AS
	cur.execute(qq)
	dR,uR=zip(*cur.fetchall())
	np=1000
	
	# calculating Download Data
	
	ad1,ad2=mquantiles(dR,[0.05,.95])
	zd=[xx for xx in dR if ad1<xx<ad2]
	xd=num.linspace(min(zd),max(zd),np)
	N=len(zd)
	xd,estd=densityEst(zd,xd,int(.05*N),knn=1,Mode='G')
	ypd,xpd=PDF(zd)
	nf1d=max(ypd)
	nf2d=max(estd)
	yed=[xx*nf1d/nf2d for xx in estd]
	
	# calculating Upload Data
	
	au1,au2=mquantiles(uR,[0.05,.95])
	zu=[xx for xx in uR if au1<xx<au2]
	xu=num.linspace(min(zu),max(zu),np)
	N=len(zu)
	xu,estu=densityEst(zu,xu,int(.05*N),knn=1,Mode='G')
	ypu,xpu=PDF(zu)
	nf1u=max(ypu)
	nf2u=max(estu)
	yeu=[xx*nf1u/nf2u for xx in estu]
	
	# Plotting
	colL=['red','blue','black','green']
	fig=pl.figure()
	
	# Plotting Download data
	
	ax1=pl.subplot(121)
	pl.plot(xd,yed,'b',label='KNN estimation',linewidth=2)
	pl.plot(xpd,ypd,'r--',label='Histogram')
	pl.xlabel('Download Throuput(Mbps)',fontsize=20)
	pl.ylabel('PDF',fontsize=20)
	for i,w in enumerate(spd):
		a=w[1][0]
		b=w[1][1]
		mod=w[2]
		pl.plot([a,b],[0,0],linewidth=5,color=colL[i])
		if mod!=-1:
			temp=[abs(xx-mod) for xx in xd]
			mintemp=min(temp)
			It=temp.index(mintemp)
			ymod=estd[It]
			print 'SPD detected at: '+str(mod)
			pl.plot(mod,ymod*nf1d/nf2d,'*',mfc=colL[i],mec=colL[i],ms=20)
	pl.ylim([-.01,nf1d+.01])
	pl.legend()
	pl.title('AS'+asn)
	
	# Plotting Upload data
	
	ax1=pl.subplot(122)
	pl.plot(xu,yeu,'b',label='KNN estimation',linewidth=2)
	pl.plot(xpu,ypu,'r--',label='Histogram')
	pl.xlabel('Upload Throuput(Mbps)',fontsize=20)
	pl.ylabel('PDF',fontsize=20)
	for i,w in enumerate(spu):
		a=w[1][0]
		b=w[1][1]
		mod=w[2]
		pl.plot([a,b],[0,0],linewidth=5,color=colL[i],mec=colL[i])
		if mod!=-1:
			temp=[abs(xx-mod) for xx in xu]
			mintemp=min(temp)
			It=temp.index(mintemp)
			ymod=estu[It]
			print 'SPU detected at: '+str(mod)
			pl.plot(mod,ymod*nf1u/nf2u,'*',mfc=colL[i],mec=colL[i],ms=20)
	pl.ylim([-.01,nf1u+.01])
	pl.legend()
	pl.title('AS'+asn)
	
	
	
if __name__=='__main__':
	asn='25490'
	if fg==0:
		visSP(asn)
		pl.legend()
		pl.title('AS'+asn)
		pl.show()
	else:
		print 'Model or database not exists'
