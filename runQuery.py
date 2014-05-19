import os
from myBasic import PDF
import pylab as pl
from scipy.stats.mstats import mquantiles

def runQuery():
	with open('MyQuery/runQuery') as f:
		qstr=f.read()
	qstr=qstr.replace("'",'"').strip()
	qq="bq -q --format=csv query --max_rows 100000 '" + qstr + ";' > CSV/runQuery"
	os.system(qq)
	
if __name__=='__main__':
	print 'Running Query...'
	runQuery()
	print 'Analyzing...'
	i=0
	r1=[]
	r2=[]
	r3=[]
	r4=[]
	with open('CSV/runQuery') as f:
		for line in f:
			if i==0:
				i=1
				continue
			w=line.split(',')
			try:
				r1.append(float(w[0]))
				r2.append(float(w[1]))
				r3.append(float(w[2]))
				r4.append(float(w[3]))
			except:
				continue
	f,ax=pl.subplots(4)
	a1,a2=mquantiles(r1,[0.05,0.95])
	rr1=[xx for xx in r1 if a1<xx<a2]
	a1,a2=mquantiles(r2,[0.05,0.95])
	rr2=[xx for xx in r2 if a1<xx<a2]
	a1,a2=mquantiles(r3,[0.05,0.95])
	rr3=[xx for xx in r3 if a1<xx<a2]
	a1,a2=mquantiles(r4,[0.05,0.95])
	rr4=[xx for xx in r4 if a1<xx<a2]
	y1,x1=PDF(rr1)
	y2,x2=PDF(rr2)
	y3,x3=PDF(rr3)
	y4,x4=PDF(rr4)
	ax[0].plot(x1,y1)
	ax[1].plot(x2,y2)
	ax[2].plot(x3,y3)
	ax[3].plot(x4,y4)
	pl.show()
	
			
			
			

