import sqlite3 as sq
import pickle as pk
import os
import SubnetTree

def ipInSub(ip,sub):
	pref,l1=sub.split('/')
	l=int(l1)
	ls=str(ip).split('.')
	temp1=[bin(int(x))[2:] for x in ls]
	temp2=['0'*(8-len(w))+w for w in temp1]
	binIP=''.join(temp2)
	prefIP=binIP[:l] + '0'*(32-l)
	ls=str(pref).split('.')
	temp1=[bin(int(x))[2:] for x in ls]
	temp2=['0'*(8-len(w))+w for w in temp1]
	binPref=''.join(temp2)
	return (binPref==prefIP)
	

def uosRetrieve(fName,net,ip):
	pF=os.getcwd()+'/Model/'+fName+'/'+net.replace('/','s')+'.uos'
	if os.path.exists(pF):
		with open(pF,'r') as f:
			uoss=eval(f.read())
		uosn=1
		for uos in uoss:
			for sub in [xx.strip() for xx in uos.split('U')]:
				if ipInSub(ip,sub):
					return uosn
			uosn=uosn+1
		return False
	else:
		return None
	
def mapS(z,model):
	for i,w in enumerate(model):
		br=w[1]
		if z>br[0] and z<br[1]:
			return str(i)
	return str(-1)

def makeDB(fName,bgpFile):
	dF='CSV/'+fName+'.db'
	mF='Model/'+fName+'.pk'
	if not os.path.exists(mF):
		print 'Error:Service plan model not found'
		return
	if os.path.exists(dF):
		print 'Error: Database already exists'
		return
	with open(mF,'r') as ftemp:
		spm=pk.load(ftemp)
	D=sq.connect(dF)
	cur=D.cursor()
	cur.execute("""Create table meta(test_id integer key,cIP text not null,lt integer not null,
	minRTT real not null,download_rate real not null,upload_rate real not null,
	sIP text not null,SPD integer,SPU integer,Community integer,cAS text,
	sAS text,cP text)""")
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

	print 'Parsing Raw Data...'
	i=0
	with open('CSV/'+fName) as f:
		for line in f:
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
				net=t[ip]
				asn=asDic[net]
				Comm=uosRetrieve(fName,net,ip)  # What happens to IPs with no UoS
				try:
					spd,spu=spm[asn]
					kd=mapS(d,spd)
					ku=mapS(u,spu)
					if Comm:
						cur.execute('''insert into meta (cIP,lt,minRTT,download_rate,
						upload_rate,sIP,SPD,SPU,cAS,cP,Community) values ("'''+ip+'",'+lt+','+rtt+','+str(d)+
						','+str(u)+','+'"'+sIP+'",'+kd+','+ku+',"'+asn+'","'+net+'",'+str(Comm)+')')
					else:
						cur.execute('''insert into meta (cIP,lt,minRTT,download_rate,
						upload_rate,sIP,SPD,SPU,cAS,cP) values ("'''+ip+'",'+lt+','+rtt+','+str(d)+
						','+str(u)+','+'"'+sIP+'",'+kd+','+ku+',"'+asn+'","'+net+'")')
				except KeyError:
					if Comm:
						cur.execute('''insert into meta (cIP,lt,minRTT,download_rate,
						upload_rate,sIP,cAS,cP,Community) values ("'''+ip+'",'+lt+','+rtt+','+str(d)+
						','+str(u)+','+'"'+sIP+'","'+asn+'","'+net+'",'+str(Comm)+')')
					else:
						cur.execute('''insert into meta (cIP,lt,minRTT,download_rate,
						upload_rate,sIP,cAS,cP) values ("'''+ip+'",'+lt+','+rtt+','+str(d)+
						','+str(u)+','+'"'+sIP+'","'+asn+'","'+net+'")')
			except KeyError:
				continue
	D.commit()
	D.close()
	
	
if __name__=='__main__':
	fName='ndt201401'
	bgpFile='01jan14'
	makeDB(fName,bgpFile)
	#~ print uosRetrieve(fName,'2.34.0.0/15','2.34.1.1')
