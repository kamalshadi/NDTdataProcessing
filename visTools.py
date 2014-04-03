from graphvisu import myDraw
import networkx as nx
import pylab as pl
import os
from myBasic import pickColor


def communityGraph(fName,w):
	#for the name of the graph add .G
	# for the name of communities add .C
	gFile=os.getcwd()+'/CSV/Graphs/'+fName+'/'+w+'.G'
	pDir=os.getcwd()+'/PIC/'+fName
	wFile=os.getcwd()+'/CSV/WalkTrap/'+fName+'/'+w+'.C'
	if (not os.path.exists(gFile)) or (not os.path.exists(wFile)):
		print 'Error: '+gFile+' or '+wFile+' not found'
		return 101
		
	if (not os.path.exists(pDir)):
		os.mkdir(pDir)

	print '--------------------'
	G=nx.read_graphml(gFile)
	fn=wFile
	try:
		f=open(fn,'r')
	except IOError:
		print 'Could not open '+fn
		return
	a=sorted(G.nodes())
	#~ b=[str(xx) for xx in range(len(a))]
	#~ myDic=list2dic(b,a)
	C=0
	for k,line in enumerate(f):
		C=C+1
		t1=line.strip(' {}\t\n')
		t2=t1.split(',')
		cc = pickColor(k).strip()
		for ww in t2:
			#~ n=myDic[ww.strip()]
			n=a[int(ww)]
			#~ G.node[n[0].strip()]['color'] = cc
			G.node[n]['color'] = cc
	print w
	print "Number of communities: "+str(C)
	myDraw(G,pDir+"/C_"+w+".png")
	print '---------------------'
	f.close()
	#~ raw_input('=============>')
	
if __name__=='__main__':
	fName='6ndtrun'
	w='90.192.0.0s11'
	gF='CSV/Graphs/'+fName+'/'+w.replace('/','s')+'.G'
	G=nx.read_graphml(gF)
	pl.subplot(121)
	nx.draw(G)
	pl.subplot(122)
	communityGraph(fName,w)
	pl.show()
	
