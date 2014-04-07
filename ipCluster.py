import ipaddress as ix
from myBasic import *
from subnet import *
from ipClass import *
#~ import numpy as num
#~ from random import randint
#~ import datetime
#~ import re as regx
#~ from random import shuffle
#~ from graphvisu import myDraw
#~ import csv
#~ from itertools import combinations
#~ import networkx as nx
#~ import pylab as pl
#~ import Queue as qx


def IPread(fName):
	# return unicode string of IP addresses
	s=[]
	i=0
	f=open('csv/'+fName,'r')
	for line in f:
		line=line.strip('"\'\n')
		temp=line.split(',')
		iplist=[ix.ip_address(unicode(x)) for x in temp]
		s.append(iplist)
	f.close()
	return s

def IPnet(s,slash='/24'):
	#this function assign IP to slash network
	# returning a dictionary

	dslash={}
	lslash=[]
	l=len(s)
	ld=[0]*l
	for i,day in enumerate(s):
		for ad in day:
			ince=ix.IPv4Interface(unicode(str(ad)+slash))
			net=str(ince.network)
			ipad=str(ince.ip)
			if net not in dslash.keys():
				dslash[net]=[ipad]
			else:
				dslash[net].append(ipad)
		ld[i]=dslash
		dslash={}
	return ld

def IPprune(diclist,th,mode=0):
	l=len(diclist)
	ld=[0]*l
	for i,dic in enumerate(diclist):
		for h,val in dic.items():
			if mode==1 :
				if len(val)>=th:
					del dic[h]
			if mode==0 :
				if len(val)<th:
					del dic[h]
		ld[i]=dic
	return ld

def IPquant(ld,client=False):
	l=len(ld)
	q=[[]]*l
	for i,dic in enumerate(ld):
		for j,val in enumerate(dic.values()):
			if not client: q[i]=q[i]+[len(val)]
			else : q[i]=q[i]+[len(set(val))]
	return q

def proNet(ll,th):
	l=len(ll)
	c=[0]*l
	for i,val in enumerate(ll):
		for x in val:
			if x>th :
				c[i]=c[i]+1
	return c

def netStat(ll):
	l=len(ll)
	c=[0]*l
	for i,val in enumerate(ll):
		c[i]=float(len(val))
	return [c,float(num.mean(c)),float(num.std(c))]
	
def slashIP(ipL,s):
	# conver a list of IP to desired slash ip net
	if type(ipL)==list:
		l=len(ipL)
		ipn=[0]*l
		for i,w in enumerate(ipL):
				try:
					ince=ix.IPv4Interface(unicode(w+s))
				except:
					print i
					print w
				temp=str(ince.network)
				ltemp=temp.split('/')
				ipn[i]=ltemp[0]
	else :
		ince=ix.IPv4Interface(unicode(ipL+s))
		temp=str(ince.network)
		ltemp=temp.split('/')
		ipn=ltemp[0]
		
	return ipn
	
def IP2int(ipL):
	# the inpot is list of ip in string format
	w=[int(ix.ip_address(unicode(it))) for it in ipL]
	return w
		
def IPvis(fName):
	cIP=IPread(fName)
	med=[str(xx) for xx in flatten(cIP)]
	slash=['/24','/23','/22','/21','/20','/19','/18','/17','/16']
	l=len(slash)
	m=[0]*l
	s=[0]*l
	for i,w in enumerate(slash):
		ld=IPnet(cIP,w)
		#~ ld=IPprune(ld,2)
		v=IPquant(ld)
		st,m[i],s[i]=netStat(v)
	wid=.3
	ind=range(l)
	pl.bar(ind,m,color='b',yerr=s,label='213.87.0.0',width=wid,align='center')
	pl.xlabel('Subnet',fontsize=20)
	pl.ylabel('Number of existing subnets',fontsize=20)
	pl.xticks(ind, slash)
	pl.title('/16 network subnets',fontsize=20)
	q1='Total number of uniqe IPs :'+str(len(set(med)))
	q2='Total number of tests :'+str(len(med))
	pl.text(l/3,max(m)-(max(m)-min(m))/10,q1)
	pl.text(l/3,max(m)-(max(m)-min(m))/7,q2)
	pl.legend()
	pl.show()
	
def commonPrefix(lIP):
	a=[]
	for ip in lIP:
		t1=ip.split('.')
		t2=[bin(int(xx))[2:] for xx in t1]
		t3=['0'*(8-len(xx))+xx for xx in t2]
		a.append(''.join(t3))
	for i in range(32):
		r=[xx[i] for xx in a]
		if len(set(r))>1:break
		if i==31 : i=i+1
	return [str(ix.ip_address(int(a[0][0:i]+'0'*(32-i),2)))+'/'+str(i),i]

		
	
	
	
		
def IPax(lIP,C):
	# create 1-D IP plot, lIP is the list of IPs and C is the labels
	l=len(lIP)
	colors1=[]
	if len(C) != l :
		print 'ERROR, length of IPs and C are different'
		return
	temp1=[int(ix.ip_address(unicode(xx))) for xx in lIP]
	ipL,C=order(ipL,C)
	a=list(set(C))
	for i in range(len(a)):
		colors1.append('%06X' % randint(0, 0xFFFFFF))
	colors=dict(a,colors1)
	pl.figure()
	endIP=ipL[-1]
	sIP=ipL[0]
	prevC=C[0]

	pl.show()

def testVector(suffle=False):
	g='/20'
	net1=ix.ip_network(unicode('0.0.0.0'+g))
	lIP=list(net1.hosts())
	lIP=[ix.ip_address(unicode(subnet(str(net1)).first()))]+lIP+[ix.ip_address(unicode(subnet(str(net1)).last()))]
	l=len(lIP)
	C=['0.0.0.0/20']*l
	net2=ix.ip_network(u'0.0.4.0/22')
	net3=ix.ip_network(u'0.0.6.0/24')
	net4=ix.ip_network(u'0.0.14.0/23')
	net5=ix.ip_network(u'0.0.8.0/24')
	net6=ix.ip_network(u'0.0.9.0/24')
	for i,w in enumerate(lIP):
		if w in net2:
			C[i]='0.0.4.0/22'
		if w in net3:
			C[i]='0.0.6.0/24'
		if w in net4:
			C[i]='0.0.14.0/23'
		if w in net5:
			C[i]='0.0.8.0/24'
		if w in net6:
			C[i]='0.0.9.0/24'
	if shuffle:
		x=range(l)
		shuffle(x)
		E=int((99.0/100.0)*l)
		ind=x[0:E]
		C = del_indices(C,ind)
		lIP= del_indices(lIP,ind)
	dic=list2dic(C,[str(xx) for xx in lIP])
	return dic.values()
	
def IPaxVis(b,c,y=1,anot=True):
	#b is ip bracket
	#c is ip cluster
	bb=list(b)
	for i in range(len(b)):
		bb[i]=[ipClass(xx).int() for xx in b[i]]
	cc=['#999999','#FF3300','#99CC00','#FFFF00','#996666','#003300',
	'#3399FF','#000000','#FF00CC','#333333']
	colors=dict(zip(sorted(list(set(c))),cc))
	mark=[]
	mM=[]
	for i,w in enumerate(bb):
		if w[0]==w[1]:
			mark.append(w[0])
			mM.append(c[i])
			line=pl.plot(w[0],y,'*')
			if anot:
				pl.annotate(str(c[i]), xy=(w[0], y), xytext=(w[0], y+.1),rotation=90,
				size=20,arrowprops=dict(facecolor=colors[c[i]], shrink=0.05,ec="none")
				)
		else:
			line=pl.plot(w,[y,y])
			if anot:
				pl.annotate(str(c[i]), xy=(0.5*(w[0]+w[1]), y), xytext=(0.5*(w[0]+w[1]), y+.1),rotation=90,
				size=20,arrowprops=dict(facecolor=colors[c[i]], shrink=0.05,ec="none"),
				)
		if i==32:
			print 'Go'
		pl.setp(line,lw=10,ms=15,c=colors[c[i]],mfc=colors[c[i]],mew=0)
		frame1=pl.gca()
		#~ frame1.axes.get_xaxis().set_visible(False)
	lm=len(mark)
	if lm>0:
		for i,w in enumerate(mark):
			line=pl.plot(w,y,'*')
			if anot:
				pl.annotate(str(mM[i]), xy=(w, y), xytext=(w, y+.1),rotation=90,
				size=20,arrowprops=dict(facecolor=colors[mM[i]], shrink=0.05,ec="none")
				)
			pl.setp(line,ms=15,mfc=colors[mM[i]],mew=0)
	frame1.axes.get_yaxis().set_visible(False)
	#~ pl.ylim(y-.1,y+.15)
	#~ pl.show()
	
def bracketIP(V,b,g='/24'):
	# Boundry IPs must be revisited e.g. 255.255.255.xxx and 0.0.0.xxx
	# V is value list (IP string) and 'b' is cluster labels
	# output is a list of list and a list of clusters
	# g is maximum gap allowed in subnet
	a=[int(ix.ip_address(unicode(xx))) for xx in V]
	V=[ipClass(xx) for xx in V]
	l=len(a)
	if l!=len(b):
		print 'length error in input of bracketing'
		return
	if l==0:
		print 'IP set is empty'
		return [None,None]
	unused,b=order(a,b)
	a,V=order(a,V)
	prev=b[0]
	p=V[0].string()
	prevV=V[0].next(g)
	if prevV is not None:
		prevV_int=int(ix.ip_address(unicode(prevV)))
	else:
		prevV_int=2**32
	outB=[]
	outC=[]
	s=V[0].string()
	bb=0
	for i in range(len(a)):
		curV=V[i].first(g)
		curV_int=int(ix.ip_address(unicode(curV)))
		if (b[i]!=prev or ((curV_int) > prevV_int)):
			outB.append(temp)
			outC.append(prev)
			s=V[i].string()
			prevV=V[i].next(g)
			p=V[i].string()
			prevV_int=int(ix.ip_address(unicode(prevV)))
			prev=b[i]
			temp=[s,p]
			bb=1
			if i==len(a)-1:
				outB.append([s,p])
				outC.append(prev)
		else:
			bb=0
			prevV=V[i].next(g)
			p=V[i].string()
			prevV_int=int(ix.ip_address(unicode(prevV)))
			prev=b[i]
			temp=[s,p]
	if bb==0:
		outB.append([s,p])
		outC.append(prev)
	else:
		pass

	return [outB,outC]
	
def growSub(br,g='/24'):
	if br is None:
		return None
	ll=len(br)
	brr=[['0.0.0.0','0.0.0.0']]*ll
	for i,w in enumerate(br):
		temp=list(w)
		pref,l=commonPrefix(w)
		if l <= int(g.strip('/')):
			brr[i]=w
		else:
			subg=subnet(pref)
			while (l > int(g.strip('/'))):
				subg=subg.grow()
				l=l-1
				net=ix.ip_network(unicode(subg.string()))
				if (ll==1):
					temp=[subg.first(),subg.last()]
				elif (i==0 and (ix.ip_address(unicode(ipClass(br[i+1][0]).first(g))) not in net)):
					temp=[subg.first(),subg.last()]
				elif(i==(ll-1) and (ix.ip_address(unicode(ipClass(br[i-1][1]).last(g))) not in net)):
					temp=[subg.first(),subg.last()]
				elif ((ix.ip_address(unicode(ipClass(br[i-1][1]).last(g))) not in net) and (ix.ip_address(unicode(ipClass(br[i+1][0]).first(g))) not in net)):
					temp=[subg.first(),subg.last()]
				else : break				
				brr[i]=temp
	return brr

def joinBrIP(br,lb):
	b=list(br)
	ll=len(br)
	for i in range(ll):
		b[i]=[ipClass(xx).int() for xx in br[i]]
	temp,lbr=joinBr(b,lb)
	l=len(temp)
	brr=[['0.0.0.0','0.0.0.0']]*l
	for i,w in enumerate(temp):
		brr[i]=[str(ix.ip_address(w[0])),str(ix.ip_address(w[1]))]
	return [brr,lbr]
	
def cluster2sub(C,g_in='/24',g_out=None):
	if g_out is None:
		g_out=g_in
	print 'Subnet resolution: '+g_in
	#C is a list of lists, each item being a cluster
	labels1=[[str(i)]*len(w) for i,w in enumerate(C)]
	labels=flatten(labels1)
	V=flatten(C)
	N1,pN = commonPrefix(V) #tentative
	N=subnet(N1) #tentative
	br,lb=bracketIP(V,labels,g_in)
	br=growSub(br,g_out)
	sub1=['0']*len(br)
	sub=['0']*len(set(lb))
	for i,w in enumerate(br):
		abr=ipClass(w[0])
		bbr=ipClass(w[1])
		a1=abr.prev(g_out)
		b1=bbr.next(g_out)
		if i==0:
			a_p = ipClass(N.first()).prev('/32') #tentative
		else :
			a_p = br[i-1][1]
		if i==len(br)-1:
			b_n = ipClass(N.last()).next('/32') #tentative
		else:
			b_n = br[i+1][0]
		if ((a1 is not None) and (a_p is not None)):
			if ipClass(a1).int() > ipClass(a_p).int() :
				a = a1
			else:
				a = a_p
		elif ((a1 is None) and (a_p is not None)):
			a=a_p
		elif ((a1 is not None) and (a_p is None)):
			a=a1
		else:
			a=None
		if ((b1 is not None) and (b_n is not None)):
			if ipClass(b1).int() > ipClass(b_n).int() :
				b = b_n
			else :
				b = b1
		elif ((b1 is None) and (b_n is not None)):
			b=b_n
		elif ((b1 is not None) and (b_n is None)):
			b=b1
		else:
			b=None
		sub1[i]=bracket2sub(w,a,b,g_out)
	dic=list2dic(lb,sub1)
	fl=['0']*len(dic.keys())
	for i,w in enumerate(dic.keys()):
		temp1=list(dic[w])
		to_del=[]
		for j in range(len(temp1)):
			if temp1[j].find('/')==-1:
				to_del.append(j)
		temp1=del_indices(temp1,to_del)
		sub[i]=' U '.join(temp1)
		fl[i]=w
	fl,sub=order(fl,sub)
	sub=prune(sub,g_in) 
	return sub
	
def bracket2sub(bracket,a1,b1,g):
	gi=int(g.strip('/'))
	# all IPs should be in form of strings
	out=''
	if a1 is None:
		a=-1
	else:
		a=int(ix.ip_address(unicode(a1)))
	if b1 is None:
		b=2**33
	else:
		b=int(ix.ip_address(unicode(b1)))
	sub,pl=commonPrefix(bracket)
	rootsub=subnet(sub)
	re=ipClass(rootsub.first()).int()
	le=ipClass(rootsub.last()).int()
	root=ix.ip_network(unicode(sub))
	if ((re <= a) or (le >= b)):
		if pl < gi :
			L,R=rootsub.split()
			brL=[L.first(),L.last()]
			brR=[R.first(),R.last()]
			out=(out+' U '+bracket2sub(brL,a1,b1,g)).strip('U ')
			out=(out+' U '+bracket2sub(brR,a1,b1,g)).strip('U ')
		else:
			return out
	else:
		return rootsub.string()
	out=out.strip('U ')
	return out

def uos2bracket(uos):
	l=len(uos)
	br=[]
	lb=[]
	for i,w in enumerate(uos):
		if w=='':continue
		subs=[xx.strip(' ') for xx in w.split('U')]
		for v in subs:
			br.append([subnet(v).first(),subnet(v).last()])
			lb.append(str(i))
	return [br,lb]
	
def cardinal(br):
	a=0
	for w in br:
		a=a+ipClass(w[1]).int()-ipClass(w[0]).int()+1
	return a



def formCluster(fName,eps,draw=False):	
	epsilon=.5
	S=4
	minRTT=[]
	lIP=[]
	lS=[]
	sim={}
	E=[]
	city={}
	with open('csv/'+fName,'r') as f:
		val=csv.reader(f)
		i=0
		for row in val:
			if i==0:
				i=1
				continue
			if test_id_2_ip(row[0]) is None:
				continue
			lIP.append(test_id_2_ip(row[0]))
			lS.append(ipClass(row[-1]).sub('/24').string())
			minRTT.append(int(row[1]))
			city[test_id_2_ip(row[0])]=row[2]
	myDic=list2dic(lS,zip(lIP,minRTT))
	for i,w in enumerate(myDic.keys()):
		occur={}
		l=len(myDic[w])
		print '\n loop:'
		print l*(l-1)/2
		if l>500: 
			print 'Jumped'
			continue
		v=[ww[1] for ww in myDic[w]]
		sigma=num.std(v)
		print sigma
		for comb in combinations(myDic[w],2):
			a=comb[0][0]
			b=comb[1][0]
			delta=abs(comb[0][1]-comb[1][1])
			link=(a,b)
			if link in occur.keys():
				occur[link]=occur[link]+1
			else:
				occur[link]=0
			if link not in sim.keys():
				sim[link]=[math.exp(-delta/sigma)]
			elif (link in sim.keys() and occur[link]==0):
				sim[link]=sim[link]+[math.exp(-delta/sigma)]
			else:
				pass  # This definitely has to be changed
	G=nx.Graph()
	for w in sim.keys():
		G.add_node(w[0],labels=city[w[0]])
		G.add_node(w[1],labels=city[w[1]])
		weight=combSum(sim[w])
		if weight > epsilon:
			G.add_edge(w[0],w[1],width=weight)
	G=s_core(G,S)
	if draw:
		myDraw(G,'labels')
	Gn=nx.connected_components(G)
	return Gn
		
	
def countAxial(fName):
	lIP=clientRead(fName)
	sIP1=serverRead(fName)
	sIP=[ipClass(xx).sub('/24') for xx in sIP1]
	myDic=list2dic(lIP,sIP)
	nIP=len(myDic)
	val=myDic.values()
	temp=[1 for w in val if len(set(w))>1]
	nA=len(temp)
	return [nIP,nA]
	
def scatterValue(fName,C={}):
	lS1=serverRead(fName)
	lS=[ipClass(xx).sub('/24').string() for xx in lS1]
	myDic=list2dic(lS)
	dim1=''
	dim2=''
	n1=0
	n2=0
	for w in myDic.keys():
		if myDic[w]>n1:
			dim1=w
			n1=myDic[w]
		elif myDic[w]>n2:
			dim2=w
			n2=myDic[w]
		else:
			pass
	lIP={}
	h=0
	with open('csv/'+fName,'r') as f:
		val=csv.reader(f)
		for row in val:
			if h==0:
				h=1
				continue
			if ipClass(row[-1]).sub('/24').string()==dim1:
				ip=test_id_2_ip(row[0])
				if ip is None : continue
				if ip not in lIP.keys():
					lIP[ip]=[int(row[1]),None]
				else:
					lIP[ip][0]=int(row[1])
			elif ipClass(row[-1]).sub('/24').string()==dim2:
				ip=test_id_2_ip(row[0])
				if ip is None : continue
				if ip not in lIP.keys():
					lIP[ip]=[None,int(row[1])]
				else:
					lIP[ip][1]=int(row[1])
			else:
				pass
	x=[]
	y=[]
	lab=[]
	cc=['#999999','#FF3300','#99CC00','#FFFF00','#996666','#003300',
	'#3399FF','#000000','#FF00CC','#333333']
	pl.figure()
	for u in lIP.keys():
		found=False
		w=lIP[u]
		if (w[0] is None or w[1] is None): continue
		if C!={}:
			for k,li in enumerate(C):
				if u in li:
					co=cc[k]
					found=True
					break
			if found:
				pl.plot(w[0],w[1],'o',color=co)
			else:
				pl.plot(w[0],w[1],'*',color='black')
		else:
			x.append(w[0])
			y.append(w[1])
			lab.append(u)
	if C=={}:
		pl.scatter(x,y)
		#~ pl.annotate(lab, xy=(x, y), xytext=(-20,20))
	pl.show()
	
def bracketDiff(a,b):
	# a-b
	# b is list of brackets
	c=[a]
	for w in b:
		pass
	
def bracketOverlapp(a,b):
	if ((a[0] < b[0] and a[1] < b[1]) or (a[0] > b[0] and a[1] > b[1])):
		return True
	else:
		return False
	
def prune(sub,g_in):
	out=[]
	for w in sub:
		t=[xx.strip() for xx in w.split('U')]
		q=[]
		for h in t:
			try: #????????????????????????????????????????????????
				temp,l1=h.split('/')
			except ValueError:
				print 'Warning raised in ip prune function'
				print h
			if int(l1) <= int(g_in.strip('/ ')):
				q.append(h)
		if len(q)>0:
			out.append(' U '.join(q))
	return out
				
			
	
def prefix_break(P):
	# P is list of prefixes
	S=[(ipClass(subnet(xx).first()).int(),0) for xx in list(set(P))]
	E=[(ipClass(subnet(xx).last()).int(),1) for xx in list(set(P))]
	A=sorted(S+E)
	ipx,fg=zip(*A)
	ipB=[]
	q=list2Queue(list(ipx),list(fg))
	j=-1
	ns=0
	while not q.empty():
		j=j+1
		x=q.get()
		if j==0:
			S=x[-1]
			a=x[0]
			l=x[1]
			ns=ns+l
			j=j+1
			continue
		Sn=x[-1]
		an=x[0]
		l=x[1]
		if S==0 and Sn==0:
			ipB.append([a,an-1])
			ns=ns+l
			a=an
		elif S==0 and Sn==1:
			ipB.append([a,an])
			ns=ns-l
			if ns>0:
				a=an+1
			else:
				a=None
			S=Sn
		elif S==1 and Sn==1:
			ipB.append([a,an])
			ns=ns-l
			if ns>0 :
				a=an+1
			else:
				a=None
		else:
			if ns > 0:
				if a is None :
					print 'ip Break code has a bug:Report'
				else:
					ipB.append([a,an-1])
					a=an
					ns=ns+l
			else:
				ns=ns+l
				a=an
			S=0
	ipR=[]
	for w in ipB:
		b1=ipClass(w[0]).string()
		b2=ipClass(w[1]).string()
		bw=[b1,b2]
		if w[0]==0:
			a=None
		else:
			a=ipClass(w[0]-1).string()
		if w[1]==2*32-1:
			b=None
		else:
			b=ipClass(w[1]+1).string()
		ipR=ipR+[xx.strip() for xx in bracket2sub(bw,a,b,'/24').split('U')]
	return ipR
			
def list2Queue(x,fg=None):
	# this progrram fragments lists and return as queue with each elements
	# containing a tuple (element,repetition)
	q=qx.Queue()
	lx=len(x)
	if fg is None:
		for i,w in enumerate(x):
			if i==0:
				p=w
				l=1
			else:
				if p==w :
					l=l+1
					if i==lx-1:
						q.put((p,l))
						break
				else:
					q.put((p,l))
					p=w
					l=1
		return q
	else:
		if len(fg)!=lx:
			print 'Error; fg (flag) must be the same size with input vector'
			return None
		else:
			for i,w in enumerate(x):
				if i==0:
					p=w
					t=fg[0]
					l=1
				else:
					if p==w and t==fg[i] :
						l=l+1
						if i==lx-1:
							q.put((p,l,t))
					else:
						q.put((p,l,t))
						p=w
						t=fg[i]
						l=1
						if i==lx-1:
							q.put((p,l,t))
			return q
			
				
			
		
		 
		
	
	
