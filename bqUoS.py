import os
def uosQ(fName,date):
	mD=os.getcwd()+'/Model/'+fName
	if not os.path.exists(mD):
		print 'Error: UoSM model for '+fName+' not found'
		return 101
	for u1,u2,u3 in os.walk(mD):
		lu=[xx for xx in u3 if ('.uos' in xx)]
		break
	for w in lu:
		try:
			dirS=os.getcwd()+'/CSV/PrefixData/'+fName+'/'+w.replace('.uos','')
			os.mkdir(dirS)
		except OSError:
			print 'UoS Prefix data already exist'
			return 101
		print 'Querying UoS Data for '+w.replace('.uos','')+' ...'
		with open(mD+'/'+w,'r') as f:
			uos_t=f.read()
			uosL=eval(uos_t)
			uosn=-1
			for i,uos in enumerate(uosL):
				uosn=uosn+1
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
				co=0
				while len(tID)>0:
					co=co+1
					cond='\n OR \n'.join(tID[0:100])
					with open('MyQuery/ndtUoS','r') as f:
						qStr=f.read()
					qStr = qStr.replace('DATE',date)
					qStr = qStr.replace('COND',cond)
					qStr = qStr.replace("'", '"')
					if co==0:
						qq = "bq -q --format=csv query --max_rows 100000 '" + qStr.strip() + ";' >" +dirS+'/'+str(uosn)
					else:
						qq = "bq -q --format=csv query --max_rows 100000 '" + qStr.strip() + ";' |tail -n+2 >>" +dirS+'/'+str(uosn)
					print 'Query '+ str(co) +' of '+ str((len(tID)/100)+1)
					r = os.system(qq)
					del tID[0:100]
				
	
#~ if __name__=='__main__':
	#~ uosQ('6ndtrun','2014_01')
	
	
