import os
import sqlite3 as sq
import pickle as pk


if __name__=='__main__':
	with open('Files/silver.pk') as f:
		sMap=pk.load(f)
	sC={}
	with open('Files/geoPlanetlab') as f:
		for line in f:
			w=[xx.strip() for xx in line.split(' ')]
			ip=w[-1]
			clg=w[1]
			clat=w[2]
			sC[ip]=(clg,clat)
	geoS={}
	with open('Files/geoServers') as f:
		for line in f:
			w=line.split(' ')
			sID=w[0].strip()
			geoS[sID]=(w[1],w[2])
	west='Planetlab/data-west/'
	east='Planetlab/data-east/'
	dF='dannyFull.db'
	D=sq.connect(dF)
	cur=D.cursor()
	cur.execute("""Create table meta(cIP text not null,
	minRTT real not null,cluster integer,Community integer,sID text,flag integer default 0,sIP text not null,slg real not null,\
	slat real not null,clg real not null,clat real not null)""")
	r=0
	iw=0
	for f1,f2,f3 in os.walk(west):
		print f1
		for fn in f3:
			if '.csv' in fn:
				print fn
				with open(west+fn) as f:
					for line in f:
						try:
							cIP,sIP,rtt=[xx.strip() for xx in line.split(',')]
						except ValueError:
							pass
						try:
							sID=sMap[sIP]
							slg=geoS[sID][0]
							slat=geoS[sID][1]
							clat=sC[cIP][1]
							clg=sC[cIP][0]
						except KeyError:
							sID='?'
							r=r+1
						cluster='0'
						qq='''insert into meta (cIP,minRTT,cluster,sID,sIP,slg,slat,clg,clat) values ("'''+cIP+'",'+rtt+','+cluster+','+'"'+sID+'","'+sIP+'","'\
						+slg+'","'+slat+'","'+clg+'","'+clat+'"'+')'
						try:
							cur.execute(qq)
						except:
							print 'Warning(makeDB.py) '+str(iw)+':Row '+str(rowid)+' not compatible(not inserted)'
							iw=iw+1
	for f1,f2,f3 in os.walk(east):
		print f1
		for fn in f3:
			if '.csv' in fn:
				with open(east+fn) as f:
					for line in f:
						try:
							cIP,sIP,rtt=[xx.strip() for xx in line.split(',')]
						except ValueError:
							pass
						try:
							sID=sMap[sIP]
							slg=geoS[sID][0]
							slat=geoS[sID][1]
							clat=sC[cIP][1]
							clg=sC[cIP][0]
						except KeyError:
							sID='?'
							r=r+1
						cluster='1'
						qq='''insert into meta (cIP,minRTT,cluster,sID,sIP,slg,slat,clg,clat) values ("'''+cIP+'",'+rtt+','+cluster+','+'"'+sID+'","'+sIP+'","'\
						+slg+'","'+slat+'","'+clg+'","'+clat+'"'+')'
						try:
							cur.execute(qq)
						except:
							print 'Warning(makeDB.py) '+str(iw)+':Row '+str(rowid)+' not compatible(not inserted)'
							iw=iw+1
	D.commit()
	D.close()
	print r
	print '------------'
	print iw
