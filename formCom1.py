import os
import networkx as nx
from myBasic import list2dic,pickColor
from ipCluster import cluster2sub
import pickle as pk

def walktrapFile(fName):
	#Writing the graph edge as needed by walktrap
	grDir=os.getcwd()+'/CSV/Graphs/'+fName
	wDir=os.getcwd()+"/CSV/WalkTrap/"+fName
	if os.path.exists(wDir):
		print 'Directory: '+wDir+' Already exists'
		print 'please delete '+fName+' before rerun'
		return -1
	else:
		os.mkdir(wDir) 
	if os.path.exists(grDir):
		for un1,un2,u3 in os.walk(grDir):
			graphs=u3
			break
	else:
		print 'Error in walktrapFile function:'
		print grDir+' Do not exists'
		return -1
	print 'Preparing files for Walktrap from raw graphs...'
	for w in u3:
		print '---------------------------------------------'
		print 'Prefix: '+w.replace('.G','').replace('s','/')
		G=nx.read_graphml(grDir+'/'+w)
		a=sorted(G.nodes())
		f=open(wDir+'/'+w.replace('.G','.w'),'w')
		maxx=0
		for edge in G.edges():
			w=G[edge[0]][edge[1]]['weight']
			ind1=a.index(edge[0])
			ind2=a.index(edge[1])
			maxx=max(max(ind1,ind2),maxx)
			s= str(ind1)+' '+str(ind2)+ ' ' + str(w) + '\n'
			f.write(s)
		f.close()
		
def UoSM_input(fName,w):
	#for the name of the graph add .G
	#for the name of communities add .C
	gFile=os.getcwd()+'/CSV/Graphs/'+fName+'/'+w+'.G'
	wFile=os.getcwd()+'/CSV/WalkTrap/'+fName+'/'+w+'.C'
	if (not os.path.exists(gFile)) or (not os.path.exists(wFile)):
		print 'Error: '+gFile+' or '+wFile+' not found'
		return
	G=nx.read_graphml(gFile)
	try:
		f=open(wFile,'r')
	except IOError:
		return
	a=sorted(G.nodes())
	#~ b=[str(xx) for xx in range(len(a))]
	#~ myDic=list2dic(b,a)
	C=[]
	for k,line in enumerate(f):
		for line in f:
			t1=line.strip(' {}\t\n')
			t2=t1.split(',')
			t=[xx.strip() for xx in t2]
			#~ ll=[myDic[xx][0] for xx in t]
			ll=[a[int(xx)] for xx in t]
			C.append(ll)
	return C

def rwcd(fName,tx='6',g='/24'): #random walk community detection
	print 'Walktrap walk length: '+tx
	wDir=os.getcwd()+"/CSV/WalkTrap/"+fName
	if not os.path.exists(wDir):
		print 'Please prepare files for walktrap using walktrapFile(fName)'
		return
	else:
		for un1,un2,u3 in os.walk(wDir):
			wtf=[xx for xx in u3 if ('.w' in xx)]
			break
	print 'Random walk length parameter: '+tx
	if os.path.exists(os.getcwd()+"/Model/uos-"+fName+'.pk'):
		print 'Error: ' +fName+' Model already exists, delete to rerun'
		return
	lll=len(wtf)
	A={}
	for j,w in enumerate(wtf):
		print '---------------- '+str(j+1) +' / '+str(lll) +'  -----------------------'
		prefix=w.replace('.w','').replace('s','/')
		print 'Prefix: '+prefix
		qq = 'WalkTrap/walktrap '+wDir+'/'+w+ " -t"+tx+" -b -d1 -s |grep community| cut -d'=' -f2 > "+ wDir+'/'+w.replace('.w','.C')
		os.system(qq)
		#~ communityGraph(fName,w.replace('.w',''))
		C = UoSM_input(fName,w.replace('.w',''))
		print 'No. of Clusters: '+str(len(C))
		print 'Cluster to subnet conversion...'
		if len(C)>0:
			uos = cluster2sub(C,g)
		A[prefix]=uos
	with open('Model/uos-' + fName+'.pk','w') as f:
		pk.dump(A,f)
			
			
#~ if __name__=='__main__':
	#~ fName='ndt201311'
	#~ walktrapFile(fName)
	#~ rwcd(fName,tx='6')
	
