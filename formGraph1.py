from myBasic import *
import networkx as nx
from ipClass import *
import numpy as num
import math 
from itertools import combinations
import os
import pickle as pk
import re
import sqlite3 as sq
import os

def ppf(fName,th):
	dF=os.getcwd()+'/CSV/'+fName+'.db'
	if os.path.exists(dF):
		D=sq.connect(dF)
		cur=D.cursor()
		qq='''select cP
		from meta
		group by (cP)
		having count(cIP)>'''+str(th)
		cur.execute(qq)
		A=[str(xx[0]) for xx in cur.fetchall()]
		return A
	else:
		return -1
		
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

			
def csv2gml(fName,eps=0):
	th=600 ### parameter for prolific prefix
	print 'Finding prolific Prefixes with more than '+str(th)+' tests...'
	prolificPrefix=ppf(fName,th)
	if prolificPrefix==-1:
		print 'Error(csv2gml): Database not found'
		return -1
	grDir=os.getcwd()+"/CSV/Graphs/"+fName

	if os.path.exists(grDir):
		print 'Directory:'+grDir+' already exists'
		print 'Please remove '+fName+' directory and rerun'
		return -1
	else:
		os.mkdir(grDir)

	lll=len(prolificPrefix)
	ippat=re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
	for qqq,prefixOn in enumerate(prolificPrefix):
		print '|||||||||||||||||||||||||||||||||||||||||||||'
		print '=================> '+str(qqq+1)+' / '+str(lll)+' <==================='
		print 'Graph formation for prefix: '+prefixOn
		lIP1,minRTT1,lS=prefQuery(fName,prefixOn)
		N=len(lIP1)
		lIP=['0']*N
		minRTT=[0.0]*N
		sim={}
		E=[]
		axial={}
		uds=0
		to_del=[]
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
			continue
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
			continue

		if not nx.is_connected(G):
			print "Graph is not connected, Largest component is used\n"
			G=nx.connected_component_subgraphs(G)[0]
		nx.write_graphml(G,grDir+'/'+prefixOn.replace('/','s')+'.G')
		#~ myDraw(G,picDir+'/Raw_'+prefixOn.replace('/','s')+'.png')
		print prefixOn+' Specs:'
		print 'Size of Graph: '+str(G.size())
		print 'Order of Graph: '+str(G.order())		
	
#~ if __name__=='__main__':
	#~ fName='ndt201311'
	#~ csv2gml(fName,0)
