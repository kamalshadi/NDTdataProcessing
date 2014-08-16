import numpy as num
import networkx as nx
from myBasic import *
import math 
from itertools import combinations
import os
import pickle as pk
import sqlite3 as sq
import pylab as pl
from graphvisu import myDraw
fName='danny'


def ng(lS,lIP,minRTT,eps=0.01):	
	myDic=list2dic(lS,zip(lIP,minRTT))
	ll=len(myDic)
	sim={}
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
	return G

def sqPars(fName='DannyFull.db'):
	qq='''select cIP,sID,min(minRTT),cluster
	from meta
	group by cIP,sID'''
	dF='dannyFull.db'
	D=sq.connect(dF)
	cur=D.cursor()
	cur.execute(qq)
	A=cur.fetchall()
	lIP,sIP,rtt,C=zip(*A)
	D=list2dic(lIP,C)
	return (D,ng(sIP,lIP,rtt,eps=0.01))
	
def walktrapFile(G):
	wDir=os.getcwd()+"/CSV/WalkTrap/"
	a=sorted(G.nodes())
	f=open(wDir+'/'+fName+'.w','w')
	maxx=0
	for edge in G.edges():
		w=G[edge[0]][edge[1]]['weight']
		ind1=a.index(edge[0])
		ind2=a.index(edge[1])
		s= str(ind1)+' '+str(ind2)+ ' ' + str(w) + '\n'
		f.write(s)
	f.close()

def rwcd(tx='6'): #random walk community detection
	print 'Walktrap walk length: '+tx
	wDir=os.getcwd()+"/CSV/WalkTrap/"+fName+".w"
	qq = 'WalkTrap/walktrap '+wDir+ " -t"+tx+" -b -d1 -s |grep community| cut -d'=' -f2 > "+ wDir.replace('.w','.C')
	os.system(qq)
	#~ communityGraph(fName,w.replace('.w',''))
		
def communityGraph(fName,G,pos=None,ax=None,lbs=None):
	#for the name of the graph add .G
	# for the name of communities add .C
	wFile=os.getcwd()+'/CSV/WalkTrap/'+fName+'.C'
	wFile2=os.getcwd()+'/CSV/WalkTrap/'+fName+'.Clabel'
	ff=open(wFile2,'w')
	fn=wFile
	try:
		f=open(fn,'r')
	except IOError:
		print 'Could not open '+fn
		return
	a=sorted(G.nodes())
	C=0
	for k,line in enumerate(f):
		C=C+1
		t1=line.strip(' {}\t\n')
		t2=t1.split(',')
		cc = pickColor(k).strip()
		for ww in t2:
			n=a[int(ww)]
			ff.write(' '+n+' ')
			G.node[n]['color'] = cc
		ff.write('\n')
	print "Number of communities: "+str(C)
	if C<1:
		lab=str(C)+' community'
	else:
		lab=str(C)+' communities'
	myDraw(G,s=0,pos=pos,tit=lab,ax=ax,labels=lbs)
	print '---------------------'
	f.close()
	return pos

if __name__=='__main__':
	f,ax=pl.subplots(1)
	D,G=sqPars()
	for w in G.nodes():
		if D[w][0]==1:
			G.node[w]['label']='1'
		else:
			G.node[w]['label']='0'
	#~ pos=myDraw(G,labels='label',ax=ax)
	walktrapFile(G)
	rwcd(tx='6')
	communityGraph(fName,G,ax=ax,lbs='label')
	pl.show()
	#~ myDraw(G,labels='label')
	#~ pl.show()
	

	
