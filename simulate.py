import os
from spd import spDump
from formGraph1 import csv2gml
from formCom1 import walktrapFile,rwcd
from updateDB import updateDB
from makeDB import makeDB

bgpFile='01jan14'
date='2014_01'
fName='ndt201401'
tx='6' # random walk length
g='/24' #subnet resolution
the=1000 # minimum number of tests for ASes

if __name__=='__main__':
	if not os.path.exists('BGP/'+bgpFile):
		qq="./bgpTable.sh"
		os.system(qq)
	else:
		print 'Warning: Already existed bgp File used.'
	if not os.path.exists('CSV/'+fName):
		qq="./bq.py -d "+date+" -f "+fName
		os.system(qq)
	else:
		print 'Warning: Already existed NDT data File used.'
	if not os.path.exists('CSV/'+fName+'.db'):
		makeDB(fName,bgpFile)
	else:
		print 'Warning: Already existed NDT database  used.'
	if not os.path.exists('Model/'+fName+'.pk'):
		spDump(fName,the)
	else:
		print 'Use already existing service plan models'

	online_C=False
	if not os.path.exists('CSV/Graphs/'+fName):
		csv2gml(fName,0)
		walktrapFile(fName)
		rwcd(fName,tx='6')
		online_C=True
	else:
		print 'Use already existing graphs are used'
	if not online_C:
		if not os.path.exists('CSV/Walktrap/'+fName):
			walktrapFile(fName)
			rwcd(fName,tx='6')
	else:
		pass
	print 'Updating database...'
	updateDB(fName)
		
