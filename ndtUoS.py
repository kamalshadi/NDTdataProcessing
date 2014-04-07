import os
import sqlite3 as sq
import pickle as pk


def ndtUoS(fName,date,asn=None):
	if asn is None:
		for i in range(len(fName)):
			try:
				asn=str(int(fName[i:]))
				break
			except ValueError:
				asn=-1
				continue
	if asn==-1:
		print 'Error: you should provide AS# for ndtUoS function'
		return 101
	spD=os.getcwd()+'/Model/'+fName+'.pk'
	if not os.path.exists(spD):
		print 'SP model not found'
	else:
		with open(spD) as f:
			dic=pk.load(f)
			sp=dic[asn]
	uosQ(fName,date,sp)

def spd(v,sp):
	M='-1'
	for k,s in enumerate(sp):
		br=s[1]
		if v<br[1][0] and v>br[0][0]:
			return str(k)
	return M

def uosQ(fName,date,sp):
	print 'Enter'
	mD=os.getcwd()+'/Model/'+fName
	sD=os.getcwd()+'/CSV/PrefixData/'+fName+'.db'
	if os.path.exists(sD):
		print 'Error: data already exists for this project, look at /PrefixData directory.'
		return 101
	if not os.path.exists(mD):
		print 'Error: UoSM model for '+fName+' not found'
		return 101
	for u1,u2,u3 in os.walk(mD):
		lu=[xx for xx in u3 if ('.uos' in xx)]
		break
	T=sq.connect(sD)
	cur=T.cursor()
	cur.execute('''create table meta
	(ip text not null,
	l_time integer not null,
	rtt real,
	dr real,
	ur real,
	prefix text,
	sp integer,
	uos integer,
	server text not null,
	primary key(ip,l_time,server)
	)''')
	for w in lu:
		curPrefix='"'+w.replace('.uos','').replace('s','/')+'"'
		print 'Querying UoS Data for '+w.replace('.uos','')+' ...'
		with open(mD+'/'+w,'r') as f:
			uos_t=f.read()
			uosL=eval(uos_t)
			uosn=-1
			
			for i,uos in enumerate(uosL):
				uosn=uosn+1
				print 'UoS #'+str(uosn)
				tID=[]
				for pref in uos.split('U'):
					w1=pref.strip()
					try:
						sub,l1=w1.split('/')
					except ValueError:
						continue
					l=int(l1)
					mask=int('1'*l+'0'*(32-l),2)
					tID.append('format_ip(parse_ip(web100_log_entry.connection_spec.remote_ip) & ' + str(mask) + ')="'+sub.strip()+'"')
				co=-1
				while len(tID)>0:
					co=co+1
					cond='\n OR \n'.join(tID[0:100])
					with open('MyQuery/ndtUoS','r') as f:
						qStr=f.read()
					qStr = qStr.replace('DATE',date)
					qStr = qStr.replace('COND',cond)
					qStr = qStr.replace("'", '"')
					if co==0:
						qq = "bq -q --format=csv query --max_rows 100000 '" + qStr.strip() + ";' >temp"
					else:
						qq = "bq -q --format=csv query --max_rows 100000 '" + qStr.strip() + ";' |tail -n+2 >>temp"
					print 'Query '+ str(co+1) +' of '+ str((len(tID)/100)+1)
					r = os.system(qq)
					del tID[0:100]
				ct=0
				with open('temp','r') as f:
					for line in f:
						if ct==0:
							ct=1
							continue
						it=line.split(',')
						ip='"'+it[0]+'"'
						l_time=it[1]
						rtt=it[2]
						dr=it[3]
						ur=it[4]
						serv='"'+it[5].strip(' \n')+'"'
						sepl=spd(float(dr),sp)
						qst='insert into meta values('+ip+','+l_time+','+rtt+','+dr+','+ur+','+curPrefix+','+sepl+','+str(uosn)+','+serv+')'
						try:
							cur.execute(qst)
						except sq.IntegrityError:
							print qst
	T.commit()
	T.close()
	
	#~ 
#~ if __name__=='__main__':
	#~ fName='Us10887'
	#~ ndtUoS(fName,'2014_01','10887')
	

