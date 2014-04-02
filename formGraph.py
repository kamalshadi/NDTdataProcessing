from myBasic import *
import networkx as nx
from graphvisu import myDraw
from ipClass import *
import numpy as num
import math 
from itertools import combinations
import os
import pickle as pk

def prefixDic(fName,bgpFile):
	"""This function reads raw CSV file and save each prefix as a dictionary"""
	directory=os.getcwd()+'/CSV/PrefixData/'+fName
	if os.path.exists(directory):
		print 'Directory:'+os.getcwd()+'/CSV/PrefixData/'+fName+' already exists'
		print 'Please remove '+fName+' directory then rerun'
		return
	try:
		import SubnetTree
	except ImportError:
		print 'Error:Please install SubnetTree package...'
		return
	i=0
	bf=open('BGP/'+bgpFile,'r')
	t = SubnetTree.SubnetTree()
	print 'Building subnet network from BGP table...'
	asDic={}
	for lines in bf:
		if i==0:
			i=1
			continue
		net=lines.strip().split()[-1].strip()
		asn=lines.strip().split()[0].strip()
		asDic[net]=asn
		t[net]=net
	print 'Parse and LPM on raw data to build prefix dictionary...'
	prefDic={}
	with open('CSV/'+fName,'r') as f:
		i=0
		for line in f:
			if i==0:
				i=1
				continue
			w=line.split(',')
			ip=w[0].strip()
			server=w[-1].strip()
			rtt=float(w[2].strip())
			try:
				net=t[ip]
			except KeyError:
				continue
			asn=asDic[net]
			try:
				prefDic[net][1].append((ip,server,rtt))
			except KeyError:
				try:
					asn=asDic[net]
				except KeyError:
					asn='Unknown'
				prefDic[net]=(asn,[(ip,server,rtt)])
	for w in prefDic.keys():
		if len(prefDic[w][1])<500:
			del prefDic[w]
	os.mkdir(directory)
	for w in prefDic.keys():
		with open(directory+'/'+w.replace('/','s')+'.pk','w') as f:
			pk.dump(prefDic[w],f)
			
			
def csv2gml(fName,eps=.4,bgpFile=None):
	""" this function reads pickle file:
	dictionary of prefixes in form
	A[prefix]=(AS,ip,time,rtt,server)"""
	if bgpFile is not None:
		print 'Parsing Data...'
		prefixDic(fName,bgpFile)
	directory=os.getcwd()+'/CSV/PrefixData/'+fName
	grDir=os.getcwd()+"/CSV/Graphs/"+fName
	picDir=os.getcwd()+"/PIC/"+fName
	if not os.path.exists(directory):
		print 'Directory:'+os.getcwd()+'/CSV/PrefixData/'+fName+' do not exists'
		print 'Please provide bgpFile as an argument to catogarize data by prefixes'
		return
	if os.path.exists(grDir):
		print 'Directory:'+grDir+' already exists'
		print 'Please remove '+fName+' directory and rerun'
		return
	else:
		os.mkdir(grDir)
	if os.path.exists(picDir):
		print 'Directory:'+picDir+' already exists'
		print 'Please remove '+fName+' directory and rerun'
		return
	else:
		os.mkdir(picDir)
	for un1,un2,prefixes in os.walk(directory):
		simul=prefixes
		break
	lll=str(len(simul))
	for qqq,prefixOn1 in enumerate(simul):
		prefixOn=prefixOn1.replace('.pk','')
		pathf=directory+'/'+prefixOn
		with open(pathf,'r') as f:
			mL=pk.load(f)
		print '|||||||||||||||||||||||||||||||||||||||||||||'
		print '=================> '+str(qqq)+' / '+lll+' <==================='
		print 'Graph formation for prefix: '+prefixOn
		print 'Number of tests:'+str(len(mL[1]))
		lIP1,lS1,minRTT1=[list(xx) for xx in zip(*mL[1])]
		N=len(lIP1)
		lIP=['0']*N
		lS=['0']*N
		minRTT=[0.0]*N
		sim={}
		E=[]
		axial={}
		with open('Files/serverMap','r') as f:
			st=f.read()
		serverMap=eval(st)
		uds=0
		to_del=[]
		for i in range(N):
			ip=lIP1[i]
			ser=lS1[i]
			rtt=minRTT1[i]
			try:
				lIP[i] = ipClass(ip.strip()).sub('/24').string().split('/')[0].strip()
				#~ lIP[i] = xx[0].strip()
				lS[i]=serverMap[ser][0]
				minRTT[i]=rtt
			except ValueError:
				to_del.append(i)
				continue
			except KeyError:
				to_del.append(i)
				uds=uds+1
				continue
			try:
				axial[lIP[i]]=[lS[i]]+axial[lIP[i]]
			except KeyError:
				axial[lIP[i]]=[lS[i]]
		print 'Unrecognized test (no server info):'+str(uds)
		for i in range(N):
			try:
				if len(set(axial[lIP[i]])) < 2:
					to_del.append(i)
			except KeyError:
				to_del.append(i)
		lS=del_indices(lS,to_del)
		lIP=del_indices(lIP,to_del)
		minRTT=del_indices(minRTT,to_del)
		myDic=list2dic(lS,zip(lIP,minRTT))
		ll=len(myDic)
		print 'Number of servers : '+ str(ll)
		if ll<2:
			print 'Not enough servers'
			print '|||||||||||||||||||||||||||||||||||||||'
			continue
		for i,w in enumerate(myDic.keys()):
			print '--------------------------------'
			print w
			occur={}
			l=len(myDic[w])
			print 'loop '+str(i+1)+' of '+str(ll)+' :'
			print '          '+str(l)+' clients -> '+str(l*(l-1)/2)+' loops'
			print '--------------------------------'
			print '\n\n'
			v=[ww[1] for ww in myDic[w]]
			sigma=num.std(v)
			if sigma < 1:
				continue
			for comb in combinations(myDic[w],2):
				a=comb[0][0]
				b=comb[1][0]
				if a==b:
					continue
				delta=abs(comb[0][1]-comb[1][1])
				if a > b :
					link=(a,b)
				else:
					link=(b,a)
				#~ if link in occur.keys():
					#~ occur[link]=occur[link]+1
				#~ else:
					#~ occur[link]=0
				#~ if link not in sim.keys():
					#~ sim[link]=[math.exp(-delta/sigma)]
				#~ elif (link in sim.keys() and occur[link]==0):
					#~ sim[link]=sim[link]+[math.exp(-delta/sigma)]
				#~ else:
					#~ pass  # This definitely has to be changed
				try:
					occur[link]=occur[link]+1
				except KeyError:
					occur[link]=0
				try:
					if occur[link]==0:
						sim[link]=sim[link]+[math.exp(-delta/sigma)]
					else:
						sim[link][-1]=max(sim[link][-1],math.exp(-delta/sigma))
				except KeyError:
					sim[link]=[math.exp(-delta/sigma)]
		G=nx.Graph()
		print 'Parameter eps in building Graph: '+str(eps)
		for w in sim.keys():
			weight=combSum(sim[w])   # weighting function 1
			#~ if len(sim[w]) < 2:			# weighting function 2
				#~ weight=0
			#~ else:
				#~ weight=float(num.mean(sim[w]))
			if weight > eps:
				G.add_edge(w[0],w[1],weight=weight)
		if G.size()==0 or G.order()==0:
			print 'Graph could not be formed.'
			print '||||||||||||||||||||||||||||||||||'
			continue
		#~ G=score(G,1)  # Added robustness
		#~ if G.size()==0 or G.order()==0:
			#~ print 'SCORE Nullification'
			#~ return 0
		if not nx.is_connected(G):
			print "Graph is not connected, Largest component is used\n"
			G=nx.connected_component_subgraphs(G)[0]
		nx.write_graphml(G,grDir+'/'+prefixOn.replace('/','s')+'.G')
		myDraw(G,picDir+'/Raw_'+prefixOn.replace('/','s')+'.png')
		print 'Size of Graph: '+str(G.size())
	
if __name__=='__main__':
	fName='ndt201401'
	bgpFile='xrib.20140115.0000.txt'
	csv2gml(fName)
	
