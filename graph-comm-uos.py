import sqlite3 as sq
import math
import numpy as num
import pylab as pl
import os
import re
from ipClass import *
from myBasic import *
import networkx as nx
from ipCluster import cluster2sub

def prefQuery(fName,pref):
	dF=os.getcwd()+'/CSV/'+fName+'.db'
	qq='''select cIP,minRTT,sID
	from meta
	where sID!="?" and cP="'''+pref+'"'
	D=sq.connect(dF)
	cur=D.cursor()
	cur.execute(qq)
	A=cur.fetchall()
	ips=[str(xx[0]) for xx in A]
	sIDs=[str(xx[-1]) for xx in A]
	rtts=[xx[1] for xx in A]
	return (ips,rtts,sIDs)
	
def NG(fName,prefix,eps=.4):
	lIP1,minRTT1,lS=prefQuery(fName,prefix)
	N=len(lIP1)
	lIP=['0']*N
	minRTT=[0.0]*N
	sim={}
	E=[]
	axial={}
	uds=0
	to_del=[]
	ippat=re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
	for i in range(N):
		ip=lIP1[i]
		rtt=minRTT1[i]
		m=re.search(ippat,ip)
		if m is None:
			to_del.append(i)
			continue
		try:
			lIP[i] = ipClass(ip.strip()).sub('/24').string().split('/')[0].strip()
			minRTT[i]=rtt
		except ValueError:
			print 'Value Error for ip: '+ip
			to_del.append(i)
			continue
		try:
			axial[lIP[i]]=[lS[i]]+axial[lIP[i]]
		except KeyError:
			axial[lIP[i]]=[lS[i]]
	invalid=len(to_del)
	for i in range(N):
		try:
			if len(set(axial[lIP[i]])) < 2:
				to_del.append(i)
		except KeyError:
			invalid=invalid+1
			to_del.append(i)
	lS=del_indices(lS,to_del)
	lIP=del_indices(lIP,to_del)
	minRTT=del_indices(minRTT,to_del)
	myDic=list2dic(lS,zip(lIP,minRTT))
	ll=len(myDic)
	print 'No.  invalid tests: '+str(invalid)
	print 'ratio of axial tests: '+str(len(lIP))+' / '+str(len(lIP1)-invalid)
	print 'Number of servers : '+ str(ll)
	if ll<2:
		print 'Not enough servers'
		print '|||||||||||||||||||||||||||||||||||||||'
		return None
	for i,w in enumerate(myDic.keys()):
		print '--------------------------------'
		print 'Server: '+w
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
		if weight > eps:
			G.add_edge(w[0],w[1],weight=weight)
	if G.size()==0 or G.order()==0:
		print 'Graph could not be formed.'
		print '||||||||||||||||||||||||||||||||||'
		return None

	if not nx.is_connected(G):
		print "Graph is not connected, Largest component is used\n"
		G=nx.connected_component_subgraphs(G)[0]
	nx.write_graphml(G,'Debug/'+prefix.replace('/','s')+'.G')
	#~ myDraw(G,picDir+'/Raw_'+prefixOn.replace('/','s')+'.png')
	print prefix+' Specs:'
	print 'Size of Graph: '+str(G.size())
	print 'Order of Graph: '+str(G.order())		
	
def walktrapFile(prefix):
	w=prefix.replace('/','s')
	print 'Preparing files for Walktrap from raw graphs...'
	print '---------------------------------------------'
	print 'Prefix: '+prefix
	G=nx.read_graphml('Debug/'+w+'.G')
	a=sorted(G.nodes())
	f=open('Debug/'+w+'.w','w')
	maxx=0
	for edge in G.edges():
		w=G[edge[0]][edge[1]]['weight']
		ind1=a.index(edge[0])
		ind2=a.index(edge[1])
		maxx=max(max(ind1,ind2),maxx)
		s= str(ind1)+' '+str(ind2)+ ' ' + str(w) + '\n'
		f.write(s)
	f.close()
		
def UoSM_input(prefix):
	w=prefix.replace('/','s')
	#for the name of the graph add .G
	#for the name of communities add .C
	gFile='Debug/'+w+'.G'
	wFile='Debug/'+w+'.C'
	G=nx.read_graphml(gFile)
	f=open(wFile,'r')
	a=sorted(G.nodes())
	C=[]
	for k,line in enumerate(f):
		for line in f:
			t1=line.strip(' {}\t\n')
			t2=t1.split(',')
			t=[xx.strip() for xx in t2]
			ll=[a[int(xx)] for xx in t]
			C.append(ll)
	return C

def rwcd(prefix,tx='4',g='/24'): #random walk community detection
		w=prefix.replace('/','s')
		f=open('Debug/'+w+'.uos','w')
		print 'Prefix: '+prefix
		fn='Debug/'+w+'.w'
		qq = 'WalkTrap/walktrap '+fn+ " -t"+tx+" -b -d1 -s |grep community| cut -d'=' -f2 > Debug/"+w+'.C'
		os.system(qq)
		#~ communityGraph(fName,w.replace('.w',''))
		C = UoSM_input(prefix)
		print 'No. of Clusters: '+str(len(C))
		print 'Cluster to subnet conversion...'
		if len(C)>0:
			uos = cluster2sub(C,g)
		with open('Debug/'+w+'.uos', 'w') as f:
			f.write(str(uos))
		print '-------------------------------------------------'
			



if __name__=='__main__':
	fName='ndt201311'
	prefix='67.160.0.0/11'
	NG(fName,prefix,eps=0)
	walktrapFile(prefix)
	rwcd(prefix,tx='6')
