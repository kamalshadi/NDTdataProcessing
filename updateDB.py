import sqlite3 as sq
import os
import pickle as pk

class Median:
    def __init__(self):
		self.vl=[]
    def step(self, value):
        self.vl.append(value)

    def finalize(self):
		a=len(self.vl)
		if a==0:
			return None
		b=sorted(self.vl)
		ind=a/2
		if a%2==0:
			return 0.5*(b[ind]+b[ind-1])
		else:
			return b[ind]

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


def uosM(ip,uoss):
	uosn=0
	for uos in uoss:
		for sub in [xx.strip() for xx in uos.split('U')]:
			if ipInSub(ip,sub):
				return uosn
		uosn=uosn+1
	return -1
	
def mapS(z,model):
	l=len(model)
	for i,w in enumerate(model):
		br=w[1]
		if (z>br[0] and z<br[1]):
			return str(i)
		elif (i==l-1 and z>br[1]):
			return str(i)
		else:
			pass
	return str(-1)

def updateDB(fName,extra=1):
	dF='CSV/'+fName+'.db'
	uosD='Model/uos-'+fName+'.pk'
	sD='Model/'+fName+'.pk'
	try:
		fu=open(uosD)
		fs=open(sD)
		spm=pk.load(fs)
		pref=pk.load(fu)
	except IOError:
		print 'Service Plan and UoS models must exist'
		return -1
	if not os.path.exists(dF):
		print 'Error: Database does not exist (updateDB)'
		return -1
	D=sq.connect(dF)
	D.create_aggregate("median", 1, Median)
	cur=D.cursor()
	cur2=D.cursor()
	qq='''select rowid,cIP,cAS,cP,download_rate,upload_rate,sID,minRTT from meta'''
	cur.execute(qq)
	A=cur.fetchall()
	ll=len(A)
	for j,row in enumerate(A):
		if j%100==0:
			print 'Percentage: '+str(round(float(j)*10000/ll)/100)
		pf=1
		sf=1
		uf=1
		rowid=row[0]
		cIP=str(row[1])
		cAS=str(row[2])
		cP=str(row[3])
		d=row[4]
		u=row[5]
		sID=row[6]
		rtt=row[-1]
		try:
			spd,spu=spm[cAS]
		except KeyError:
			sf=0
		try:
			uos=pref[cP]
		except KeyError:
			pf=0
		if sf:
			dsp=mapS(d,spd)
			usp=mapS(u,spu)
		else:
			dsp='null'
			usp='null'
		if pf:
			C=uosM(cIP,uos)
			if C==-1 and extra==1:
				qqq="select Community,median(minRTT)\
				from meta \
				where\
				sID='"+sID+"' and cP='"+cP+"' and Community not null\
				group by Community"
				cur2.execute(qqq)
				B=cur2.fetchall()
				minc=9999
				for w in B:
					if abs(w[1]-rtt)<minc:
						C=w[0]
						minc=abs(w[1]-rtt)
		else:
			C='null'
		if C!='null' or sf:
			qq='update meta set SPD='+str(usp) +',SPU='+str(dsp) +', Community='+str(C) +' where rowid='+str(rowid)
			cur.execute(qq)
		
		
		#~ raw_input('================>')
	D.commit()
	D.close()
		
if __name__=='__main__':
	updateDB('ndt201311')
