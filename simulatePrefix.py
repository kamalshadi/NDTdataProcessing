import os
from spd import spDump
from formGraph import csv2gml
from formCom import walktrapFile,rwcd,UoSM_input,cluster2sub

bgpFile='01jan14'
date='2014_01'
tx='9' # random walk length
g='/24' #subnet resolution
prefix='94.0.0.0/12'
ASS=0 # if 1 run for all AS of prefix otherwise only the prefix
fName='6ndtrun'

def prefixRun():
	bf=os.listdir('BGP')
	if bgpFile not in bf:
		qq="./bgpTable.sh"
		os.system(qq)
	else:
		print 'Warning: Already existed bgp File used.'
	found=[]
	dic={}
	with open('BGP/'+bgpFile,'r') as f:
		fg=0
		for line in f:
			if fg==0:
				fg=1
				continue
			w=line.split(' ')
			asn=w[0].strip()
			pref=w[1].strip()
			try:
				dic[asn].append(pref)
			except KeyError:
				dic[asn]=[pref]
			if pref==prefix:
				found=1
				AS=asn
	if found==0:
		print 'Input Error: Prefix not found in BGP table'
		return 0
	else:
		print 'The prefix is in AS'+AS
		ps=dic[AS]
	print 'Query Data for AS...'
	l=len(ps)
	if l<=100:
		qq="./bqP.py -f "+fName+" -p "+",".join(ps)+" -d "+date
		os.system(qq)
	else:
		fg=0
		j=1
		while len(ps)>0:
			if (l%100==0):
				print 'Qurey '+str(j)+' of '+str(l/100)
			else:
				print 'Qurey '+str(j)+' of '+str(l/100+1)
			j=j+1
			if fg==0:
				fg=1
				qq="./bqP.py -f "+fName+" -p "+",".join(ps[0:100])+" -d "+date
				os.system(qq)
				del ps[0:100]
			else:
				qq="./bqP.py -f "+fName+" -p "+",".join(ps[0:100])+" -d "+date+" -a 1"
				os.system(qq)
				del ps[0:100]
				
				
			
			
	
if __name__=='__main__':
	if os.path.exists('CSV/'+fName):
		print fName+' Warning: Data for already exists.'
	else:
		prefixRun()
	if fName+'.pk' not in os.listdir('Model'):
		spDump(fName,bgpFile)
	else:
		print 'Use already existing service plan models'
	if os.path.exists('CSV/Graphs/'+fName):
		print fName+' Warning: NG already exists.'
	else:
		if os.path.exists('CSV/PrefixData/'+fName):
			csv2gml(fName)
		else:
			csv2gml(fName,bgpFile=bgpFile)
	#~ walktrapFile(fName)
	#~ print 'Walktrap .....'
	rwcd(fName,tx,g)
