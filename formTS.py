import os
import sqlite3 as sq
import pylab as pl
# Read AS database and for a time series (considering only one SP,Uos abd prefix could be set by flags)


fName=''
def TS(fName,SPn=None,Prefixn=None,UoSn=None):
	dbF=os.getcwd()+'/CSV/PrefixData/'+fName+'.db'
	if os.path.exists(dbF):
		D=sq.connect(dbF)
		cur=D.cursor()
	else:
		print 'Error:Databse does not exist'
		return 101
	if (Prefixn is None and UoSn is None and SPn is None):
		query='select l_time,dr from meta order by l_time'
	elif (Prefixn is None and UoSn is not None and SPn is None):
		query='select l_time,dr from meta where (uos="'+UoSn+'") order by l_time'
	elif (Prefixn is not None and UoSn is None and SPn is None):
		query='select l_time,dr from meta where (prefix="'+Prefixn+'") order by l_time'
	elif (Prefixn is None and UoSn is None and SPn is not None):
		query='select l_time,dr from meta where (sp="'+SPn+'" or sp="-1") order by l_time'
	elif (Prefixn is not None and UoSn is not None and SPn is None):
		query='select l_time,dr from meta where (prefix="'+Prefixn+'" and \
		uos="'+UoSn+'") order by l_time'
	elif (Prefixn is not None and UoSn is None and SPn is not None):
		query='select l_time,dr from meta where (prefix="'+Prefixn+'" and \
		(sp="'+SPn+'" or sp="-1")) order by l_time'
	elif (Prefixn is None and UoSn is not None and SPn is not None):
		query='select l_time,dr from meta where ((sp="'+SPn+'" or sp="-1") and uos="'+UoSn+'") order by l_time'
	else:
		query='select l_time,dr from meta where (prefix="'+Prefixn+'" and \
		(sp="'+SPn+'" or sp="-1") and uos="'+UoSn+'") order by l_time'
	R=cur.execute(query)
	ts,dr=zip(*R.fetchall())
	D.close()
	return (list(ts),list(dr))

if __name__=='__main__':
	TS('UK5607',Prefixn='94.0.0.0/12.uo/')
	
		
	


