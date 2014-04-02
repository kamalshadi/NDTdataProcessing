import networkx as nx
import pylab as pl

def order(v,w):
	a=zip(v,w)
	a.sort()
	l=zip(*a)
	v=list(l[0])
	w=list(l[1])
	return [v,w]
	
def myDraw(G,fName,labels=None):
	#It will draw a graph considering following parameters
	# weight for edge
	# label/color/size for nodes
	# Note all these parameters are optional
	dS=600
	dC='blue'
	Ew=3
	for w in G.nodes(True):
		if 'color' not in w[1].keys():
			G.node[w[0]]['color']=dC
		if 'size' not in w[1].keys():
			G.node[w[0]]['size']=dS
	pos=nx.spring_layout(G)
	N=nx.get_node_attributes(G,'color')
	nC=N.values()
	z=N.keys()
	z,nC=order(z,nC)
	N=nx.get_node_attributes(G,'size')
	nS=N.values()
	z=N.keys()
	z,nS=order(z,nS)
	nx.draw_networkx_nodes(G, pos,nodelist=z,node_size=nS,node_color=nC)
	if labels:
		t=G.nodes(True)
		a1=[w[0] for w in t ]
		a2=[w[1][labels] if labels in w[1].keys() else w[0] for w in t]
		nx.draw_networkx_labels(G,pos, dict(zip(a1,a2)))
	elist=[]
	ew=[]
	for w in G.edges_iter():
		elist.append(w)
		if 'weight' not in G[w[0]][w[1]]:
			ew.append(Ew)
		else:
			ew.append(G[w[0]][w[1]]['weight'])
			
	nx.draw_networkx_edges(G, pos, edgelist=elist, width=ew)
	ax=pl.gca()
	ax.yaxis.set_visible(False)
	ax.xaxis.set_visible(False)
	pl.savefig(fName)
	
	
