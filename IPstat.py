# This function is to see the analyze the statistics of 
# MLAB NDT test within a specific month
import os 
from ip2net import ip2net
from myBasic import list2dic,order
import pickle as pk
if __name__=='__main__':
	th=4000
	fName='ndt201401'
	bgpFile='01jan14'
	ipl=[]
	with open('CSV/'+fName) as f:
		for line in f:
			ip=line.split(',')[0].strip()
			ipl.append(ip)
		del ipl[0]
	A=ip2net(bgpFile,ipl)
	print 'Obtaining Stats...'
	asn=[xx[0] for xx in A if xx]
	pref=[xx[1] for xx in A if xx]
	o=list2dic(asn)
	asp1=[(o[w],w) for w in o.keys() if o[w]>4000]
	unused,asp=order(*zip(*asp1),mode=1)
	f=open('Prolific/asn','w')
	pk.dump(asp,f)
	f.close()
	
	
