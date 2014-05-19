import numpy as num
from myBasic import order

def diurnalPDF(ts,val,bw,mode='median'):
	# ts is time in seconds
	# val are the values of time series
	# bw in bin size
	# mode is median or mean
	ts,val=order(ts,val)
	dl=86400
	nbc=lambda x: (x[0]/x[1] if (x[0]%x[1]==0) else x[0]/x[1]+1)
	nb=nbc((dl,bw))
	a=min(ts)
	b=max(ts)
	ts=[(xx-a)%dl for xx in ts]
	i=0
	d=num.array([-1.0]*nb)
	tm=num.array([-1.0]*nb)
	his=0
	for i in range(nb):
		b1=i*bw
		b2=(i+1)*bw
		for j in range(his,len(ts)):
			if ts[j]>=b2:
				break
		if j-his>0:
			if mode=='median':
				d[i]=num.median(val[his:j])
			elif mode=='mean':
				d[i]=num.mean(temp)
			else:
				return None
		tm[i]=b1
		i=i+1
		his=j
	ind=d>-1
	rv=d[ind]
	sp=sum(rv)
	return (tm[ind],rv/sp)
	
#~ if __name__=='__main__':
	#~ t=[1,2,4,5,3000,3601,4000,5555,86200]
	#~ u=[1,3,-1,4,111,50,60,30,0]
	#~ tm,v=diurnalPDF(t,u,1000)
	#~ print tm
	#~ print v
	
	 
	
		
		
	
