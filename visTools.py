from graphvisu import myDraw
import networkx as nx
import pylab as pl
import os
from myBasic import pickColor


def communityGraph(fName,w,pos=None,s=1):
	#for the name of the graph add .G
	# for the name of communities add .C
	tit=w.replace('.G','').replace('s','/')
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
	if C<1:
		lab=str(C)+' community'
	else:
		lab=str(C)+' communities'
	if pos is None:
		myDraw(G,pDir+"/"+w+".png",s)
	else:
		myDraw(G,pDir+"/"+w+".png",s,pos=pos,tit=tit+'\n'+lab)
	print '---------------------'
	f.close()
	#~ raw_input('=============>')
	
if __name__=='__main__':
	fName='ndt201311'
	pD='PIC/'+fName
	if os.path.exists(pD):
		print 'Remove '+pD+' for PIC/ then rerun'
	else:
		os.mkdir(pD)
	fn=[]
	if fn==[]:
		for u1,u2,u3 in os.walk('CSV/WalkTrap/'+fName+'/'):
			fn=[xx.replace('.w','') for xx in u3 if ('.w' in xx)]
			break
	for w in fn:
		gF='CSV/Graphs/'+fName+'/'+w.replace('/','s')+'.G'
		pl.figure()
		pl.subplot(121)
		G=nx.read_graphml(gF)
		pos=myDraw(G)
		pl.subplot(122)
		communityGraph(fName,w,pos)
		raw_input('====================>')
