import os
from spd import spDump
from formGraph import csv2gml
from formCom import walktrapFile,rwcd,UoSM_input,cluster2sub

bgpFile='01Nov13'
date='2013_11'
fName='ndt201311'
tx='6' # random walk length
g='/24' #subnet resolution
the=3000 # minimum number of tests for ASes

if __name__=='__main__':
	bf=os.listdir('BGP')
	if bgpFile not in bf:
		qq="./bgpTable.sh"
		os.system(qq)
	else:
		print 'Warning: Already existed bgp File used.'
	if fName not in os.listdir('CSV'):
		qq="./bq.py -d "+date+" -f "+fName
		os.system(qq)
	else:
		print 'Warning: Already existed NDT data File used.'
	if fName+'.pk' not in os.listdir('Model'):
		spDump(fName,bgpFile,the)
	else:
		print 'Use already existing service plan models'
	#~ grD=os.getcwd()+'CSV/Graphs/fName'
	#~ if os.path.exists(grD):
		#~ print 'Warning: already existing Graphs are utilized.'
	#~ else:
		#~ csv2gml(fName,bgpFile=bgpFile)
	#~ wD=os.getcwd()+'CSV/Graphs/fName'
	#~ if os.path.exists(wD):
		#~ print 'Warning: already existing WalkTrap files are utilized.'
	#~ else:
		#~ walktrapFile(fName)
		#~ rwcd(fName,tx)
