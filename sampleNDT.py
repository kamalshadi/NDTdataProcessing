#!/usr/bin/env python

import os
import sys
import subprocess
import pylab as pl
from random import randint
import pickle as pk
from scipy.stats.mstats import mquantiles

def cp(v):
	ind=[]
	hs=v[0]
	for j,w in enumerate(v):
		if w!=hs:
			hs=w
			ind.append(j)
	return ind
	
def acp(v):
	ini=v[0]
	k=0
	tup=[]
	for j,w in enumerate(v[1:]):
		if w!=ini:
			ini=w
			if j==len(v)-2:
				tup.append((k,j+1))
		else:
			a=k
			b=j+1
			if b-a>1:
				tup.append((k,b-1))
			k=j+1
	tupf=tup
	#~ tupf=[]
	#~ if len(tup)>1:
		#~ tupf.append(tup[0])
		#~ for k,w in enumerate(tup[1:]):
			#~ if w[0]-tupf[-1][1]<20:
				#~ tupf[-1]=(tupf[-1][0],w[1])
			#~ else:
				#~ tupf.append(w)	
	#~ else:
		#~ tupf=tup
	return tupf
		

def slow_start(t,v):
	ini=v[0]
	l=len(t)
	k=-1
	for j,w in enumerate(v):
		if w!=ini:
			k=j
			break
	return k
	

def usage():
    return """
Summary:
Sampling randomly NDT test for chosen web100 variables
"""

def parse_args():
    from optparse import OptionParser
    parser = OptionParser(usage=usage())
    parser.add_option("-t", "--date", dest="date", default=None, 
                      help="Required: date for query in yyyy_mm format") 
    parser.add_option("-n", "--number", dest="nt", default='4', 
                      help="optional: Number of tests to query") 
    parser.add_option("-d", "--direction", dest="d", default='1', 
                      help="optional: Download(1) is default and upload(0)") 
    parser.add_option("-s", "--server", dest="sID", default=None, 
                      help="optional: three-letters mLab server ID") 
    parser.add_option("-p", "--prefix", dest="pr", default=None, 
                      help="optional: Client subnet") 

    
                       
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()
    if options.date is None:
        print "Error: Please provide --date(-d) and --vbs (web100 variable names in comma seperated format) "
        sys.exit(1)

    return (options, args)

if __name__=='__main__':
	(options, args) = parse_args()
	date=options.date
	number=options.nt
	DD=options.d
	seed=randint(1,10)
	sID=options.sID
	pref=options.pr
	serD=pk.load(open('Files/silver.pk'))
	with open('MyQuery/sampleNDT','r') as f:
		q1=f.read()
	if DD=='0':
		with open('MyQuery/queryTestID-U','r') as f:
			q2=f.read()
	else:
		with open('MyQuery/queryTestID-D','r') as f:
			q2=f.read()
	if sID is not None:
		with open('Files/silverInv.pk','r') as f:
			sIDm=pk.load(f)
		try:
			list_ser=sIDm[sID]
			temp1=['web100_log_entry.connection_spec.local_ip="'+xx+'"' for xx in list_ser]
			server1=' or '.join(temp1)
			q1=q1.replace('SERVER',server1)
		except KeyError:
			q1=q1.replace('(SERVER) AND','')
	else:
		q1=q1.replace('(SERVER) AND','')
	if pref is not None:
		px,subl=pref.split('/')
		subl=str(32-int(subl))
		ipNet='FORMAT_IP(PARSE_IP(web100_log_entry.connection_spec.remote_ip) & INTEGER(POW(2, 32)-1 - (POW(2,'+subl+')-1)))="'+px+'"'
		q1=q1.replace('PREFIX',ipNet)
	else:
		q1=q1.replace('(PREFIX) AND','')
	q1=q1.replace('DATE',date)
	q1=q1.replace('NUMBER',str(number))
	q1=q1.replace('DD',str(DD))
	q1=q1.replace('SEED',str(seed))
	print 'Selecting Random tests...'
	qq="bq -q --format=csv query --max_rows 100 '" + q1.strip() + ";' > CSV/tempTestID"
	r = os.system(qq)
	print 'Downloading the tests\' data...'
	q2=q2.replace('DATE',date)
	g=open('CSV/tempTests','w')
	Q=min(100,int(number))
	with open('CSV/tempTestID','r') as f:
		for i,line in enumerate(f):
			if i==0:
				continue
			print '------------------------------------'
			print 'Test '+str(i)+' of '+str(Q)
			testid=line.split(',')[0].strip()
			ip=line.split(',')[2].strip()
			serip=line.split(',')[1].strip()
			q3=q2.replace('TEST_ID','"'+testid+'"')
			qq="bq -q --format=csv query --max_rows 10000 '" + q3.strip() + ";' > CSV/Temp/"+line.replace('/','-').replace('.gz','').strip()
			r=os.system(qq)
			print 'Parsing...'
			with open('CSV/Temp/'+line.replace('/','-').replace('.gz','').strip()) as hf:
				for k,linet in enumerate(hf):
					if k==0:
						continue
					if k==1:
						L=[[float(xx) for xx in linet.split(',')]]
					else:
						L.append([float(xx) for xx in linet.split(',')])
			print '\n\n\n'
			print line
			if DD=='1':
				f,ax=pl.subplots(5, sharex=True)
				du,rt,ct,st,rtt,dataout,datasegout,segout,dataretran,segretran,cong,datasent,cwnd,rwnd,ss,ssth,srtt=zip(*L)
				ll=len(du)
				
				# throughputs
				throu=datasent[-1]*8/du[-1]
				throuIns=[min(cwnd[xx],rwnd[xx])*8/(rtt[xx]*1e3) if rtt[xx]>0 else 0 for xx in range(ll)]
				d1=mquantiles([min(cwnd[xx],rwnd[xx])*8/(srtt[xx]*1e3) if rtt[xx]>0 else 0 for xx in range(ll)],.9)[0]
				
				
				#Latency
				minRTT=min([xx for xx in rtt if xx>2])
				
				#loss
				ls=float(int(round((segretran[-1]/segout[-1])*1e4)))/100
				lb=float(int(round(((dataretran[-1])/dataout[-1])*1e4)))/100
				
				#limited ratios
				rtr=[xx[0]/xx[1]  if xx[1]>0 else 0 for xx in zip(rt,du)]
				ctr=[xx[0]/xx[1]   if xx[1]>0 else 0 for xx in zip(ct,du)]
				strr=[xx[0]/xx[1] if xx[1]>0 else 0 for xx in zip(st,du) ]
				
				# converting time to secs
				du=[xx/1e6 for xx in du]
				
				#plot Latency
				ax[0].plot(du,rtt,label='RTT')
				ax[0].set_ylabel('ms',fontsize=20)
				ax[0].axhline(minRTT,c='cyan',lw=2,label='minRTT')
				ax[0].legend()
				
				
				# plot windows
				tup=acp(ss)
				if len(tup)>0:
					for ind in tup:
						ax[1].axvspan(du[ind[0]],du[ind[1]],facecolor='gray',alpha=0.3,ec='none')
				k=slow_start(du,ssth)
				if k!=-1:
					ax[1].plot(du[k:],[xx/1e3 for xx in ssth[k:]],ls='-',c='k',lw=1,label='SSthreshold')
				ax[1].plot(du,[xx/1e3 for xx in cwnd],'blue',linewidth=2,label='Congestion Window')
				axa1=ax[1].twinx()
				axa1.plot(du,[xx/1e3 for xx in rwnd],'red',linewidth=1,label='Receiver Window')
				axa1.set_ylabel('KB',fontsize=20)
				ax[1].set_ylabel('KB',fontsize=20)
				ax[1].legend(loc=4)
				axa1.legend(loc=1)
				
				
				#plot limited ratios
				ax[2].plot(du,rtr,'r',label='Receiver-Limited Time Ratio')
				ax[2].plot(du,ctr,'k',label='Network-Limited Time Ratio')
				ax[2].plot(du,strr,'b',label='Sender-Limited Time Ratio')
				ax[2].set_ylabel('Ratio',fontsize=20)
				ax[2].legend()
				
				#loss info
				ax[3].plot(du,segretran,'r--',label='Retransmitted segments',lw=2)
				axa3=ax[3].twinx()
				axa3.plot(du,[xx/1e3 for xx in dataretran],'b',label='Retransmitted bytes')
				axa3.set_ylabel('KB',fontsize=20)
				ax[3].set_ylabel('Number',fontsize=20)
				ax[3].annotate('loss percentage (KB): '+str(lb) , xy=(0.5, 0.5),  xycoords='axes fraction',ha='center', va='center')
				ax[3].annotate('loss percentage (Segments): '+str(ls) , xy=(0.5, 0.4),  xycoords='axes fraction',ha='center', va='center')
				ax[3].legend(loc=4)
				axa3.legend(loc=1)
				
				#plot throughputs
				ax[4].plot(du,throuIns,label='Instantaneous')
				ax[4].axhline(throu,c='cyan',lw=2,label='Avg')
				ax[4].axhline(d1,c='black',lw=1,ls='--',label='D1')
				ax[4].legend(loc=1)
				ax[4].set_xlabel('Time elapsed(sec)',fontsize=20)
				ax[4].set_ylabel('Mbps',fontsize=20)
				ax[4].legend(loc=1)
				ind=cp(cong)
				for j in ind:
					ax[0].axvline(du[j],ls='--',c='black',lw=2)
					ax[1].axvline(du[j],ls='--',c='black',lw=2)
					ax[2].axvline(du[j],ls='--',c='black',lw=2)
					ax[3].axvline(du[j],ls='--',c='black',lw=2)
					ax[4].axvline(du[j],ls='--',c='black',lw=2)
				try:
					sID=serD[serip.strip()]
				except KeyError:
					sID=serip
				pl.suptitle(ip+' -> '+sID,fontsize=15)
				pl.show()
			elif DD=='0':
				du,rec=zip(*L)
				f,ax=pl.subplots(1)
				ax.set_xlabel('Elapsed Time (Mbps)')
				
				#throughput
				ll=len(du)
				throu=rec[-1]/du[-1]
				ax.plot(du,rec)
				pl.show()
			else:
				print '-d could only be set to 0 for upload and 1 for download'

		
		
