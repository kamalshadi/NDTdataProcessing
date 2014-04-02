import os
import networkx as nx
from myBasic import list2dic,pickColor
from graphvisu import myDraw
def walktrapFile(fName):
	#Writing the graph edge as needed by walktrap
	grDir=os.getcwd()+'/CSV/Graphs/'+fName
	wDir=os.getcwd()+"/CSV/WalkTrap/"+fName
	if os.path.exists(wDir):
		print 'Directory: '+wDir+' Already exists'
		print 'please delete '+fName+' before rerun'
		return
	else:
		os.mkdir(wDir) 
	if os.path.exists(grDir):
		for un1,un2,u3 in os.walk(grDir):
			graphs=u3
			break
	print 'Preparing files for Walktrap from raw graphs...'
	for w in u3:
		G=nx.read_graphml(grDir+'/'+w)
		a=sorted(G.nodes())
		b=range(len(a))
		myDic=list2dic(a,b)
		f=open(wDir+'/'+w.replace('.G','.w'),'w')
		for edge in G.edges():
			w=G[edge[0]][edge[1]]['weight']
			ind1=myDic[edge[0]][0]
			ind2=myDic[edge[1]][0]
			s= str(ind1)+' '+str(ind2)+ ' ' + str(w) + '\n'
			f.write(s)
		f.close()
		
def communityGraph(fName):
	#for the name of the graph add .G
	# for the name of communities add .C
	gDir=os.getcwd()+'/CSV/Graphs/'+fName
	pDir=os.getcwd()+'/PIC/'+fName
	wDir=os.getcwd()+'/CSV/WalkTrap/'+fName
	if (not os.path.exists(gDir)) or (not os.path.exists(wDir)) or (not os.path.exists(pDir)):
		print 'Error: '+gDir+' or '+wDir+' not found'
		return
	else:
		for un1,un2,u3 in os.walk(gDir):
			graphs=u3
			break
	for w in u3:
		print '--------------------'
		print w.replace('.G','')
		G=nx.read_graphml(gDir+'/'+w)
		fn=wDir+'/'+w.replace('.G','.C')
		try:
			f=open(fn,'r')
		except IOError:
			continue
		a=sorted(G.nodes())
		b=[str(xx) for xx in range(len(a))]
		myDic=list2dic(b,a)
		C=0
		for k,line in enumerate(f):
			C=C+1
			t1=line.strip(' {}\t\n')
			t2=t1.split(',')
			cc = pickColor(k).strip()
			for ww in t2:
				n=myDic[ww.strip()]
				G.node[n[0].strip()]['color'] = cc
		print "Number of communities: "+str(C)
		myDraw(G,pDir+"/C_"+w.replace('.G','.png'))
		print '---------------------'

def rwcd(fName): #random walk community detection
	wDir=os.getcwd()+"/CSV/WalkTrap/"+fName
	if not os.path.exists(wDir):
		print 'Please prepare files for walktrap using walktrapFile(fName)'
		return
	else:
		for un1,un2,u3 in os.walk(wDir):
			wtf=[xx for xx in u3 if ('.w' in xx)]
			break
	tx='4'
	print 'Random walk length parameter: '+tx
	for w in wtf:
		qq = 'WalkTrap/walktrap '+wDir+'/'+w+ " -t"+tx+" -b -d1 -s |grep community| cut -d'=' -f2 > "+ wDir+'/'+w.replace('.w','.C')
		os.system(qq)
		communityGraph(fName)
		#~ C = UoSM_input(fName)
		#~ uos = cluster2sub(C,g)
		#~ with open('CSV/' + fName + '.uos', 'w') as f:
			#~ f.write(str(uos))
			
if __name__=='__main__':
	fName='ndt201401'
	rwcd(fName)
	
