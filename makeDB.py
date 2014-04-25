import sqlite3 as sq
import os
import SubnetTree
import pickle as pk

	

def makeDB(fName,bgpFile):
	dF='CSV/'+fName+'.db'
	if os.path.exists(dF):
		print 'Error: Database already exists'
		return
	D=sq.connect(dF)
	cur=D.cursor()
	cur.execute("""Create table meta(cIP text not null,lt integer not null,
	minRTT real not null,download_rate real not null,upload_rate real not null,
	sIP text not null,SPD integer,SPU integer,Community integer,cAS integer not null,cP text not null,sID text)""")
	i=0
	bf=open('BGP/'+bgpFile,'r')
	t = SubnetTree.SubnetTree()
	print 'Building subnet network from BGP table'
	asDic={}
	ASdic={}
	for lines in bf:
		if i==0:
			i=1
			continue
		net=lines.strip().split()[-1].strip()
		asn=lines.strip().split()[0].strip()
		asDic[net]=asn
		t[net]=net
	
	with open('Files/serverMap.pk') as f:
		sMap=pk.load(f)
	print 'Parsing Raw Data...'
	i=0
	with open('CSV/'+fName) as f:
		iw=1
		for rowid,line in enumerate(f):
			if i==0:
				i=1
				continue
			w=line.split(',')
			ip=w[0].strip()
			lt=w[1]
			d=float(w[3].strip())
			u=float(w[4].strip())
			rtt=w[2]
			sIP=w[-1].strip()
			try:
				try:
					sID=sMap[sIP]
				except KeyError:
					sID='?'
				net=t[ip]
				asn=asDic[net]
				qq='''insert into meta (cIP,lt,minRTT,download_rate,
				upload_rate,cAS,cP,sIP,sID) values ("'''+ip+'",'+lt+','+rtt+','+str(d)+\
				','+str(u)+','+asn+',"'+net+'","'+sIP+'","'+sID+'")'
				try:
					cur.execute(qq)
				except:
					print 'Warning(makeDB.py) '+str(iw)+':Row '+str(rowid)+' not compatible(not inserted)'
					iw=iw+1
			except KeyError:
				continue
	D.commit()
	D.close()
	
	
if __name__=='__main__':
	fName='ndt201311'
	bgpFile='01nov13'
	makeDB(fName,bgpFile)
	#~ print uosRetrieve(fName,'2.34.0.0/15','2.34.1.1')

