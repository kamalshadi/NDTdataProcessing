import os
from spd import spDump
from formGraph import csv2gml
from formCom import walktrapFile,rwcd,UoSM_input,cluster2sub

bgpFile='01dec13'
date='2013_12'
fName='ndt201312'
tx='6' # random walk length
g='/24' #subnet resolution

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
		spDump(fName,bgpFile)
	else:
		print 'Use already existing service plan models'
	csv2gml(fName,bgpFile=bgpFile)
	walktrapFile(fName)
	rwcd(fName,tx)
