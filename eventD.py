import Queue as qx
import numpy as num
from scipy.stats import t
import math
import pylab as pl

def sigDiff(s,l,p=.01):
	#calculate significant change for x with confidance p
	tval=abs(t.ppf(p/2,2*l-2))
	return tval*math.sqrt(2.0*s/l)

def eventDetection(a,sigma=1,l=30,p=0.01):
	"""a is the time series.
	sigma is the variance.
	l,p are algorithm parameters(see the paper:
					"A sequential algorithm for testing climate regime shifts".
	The program returns the index of events with its power in a list of tuples.
	"""
	N=len(a)
	diff=sigDiff(sigma,l)
	print 'Band: '+str(diff)
	q=qx.Queue(N)
	#loading
	for w in a:
		q.put(w,False)
	V=[0.0]*l
	for i in range(l):
		V[i]=q.get(False)
	ev=qx.Queue(l)
	i=l-1
	inp=qx.Queue(N)
	out=[]
	while ((not q.empty()) or (not inp.empty())) :
		if V[-1] is not None:
			if len(V)==l:
				m=num.mean(V)
			else:
				pass
			try:
				v=inp.get(False)
			except qx.Empty:
				v=q.get(False)
			i=i+1
			if abs(v-m) <= diff:
				if len(V) < l:
					V=V+[v]
				else:
					V[:]=V[1:]+[v]
				continue
			else:
				ep=1
				if v-m < 0: #Downward shift
					RSI=(m-v-diff)/(l*num.sqrt(sigma))
					for j in range(0,l-1):
						try:
							can=inp.get(False)
						except qx.Empty:
							try:
								can=q.get(False)
							except qx.Empty:
								ep=0
								break
						ev.put(can,False)
						RSI=RSI+(-can+m-diff)/(l*num.sqrt(sigma))
						if RSI <= 0:
							while not ev.empty():
								inp.put(ev.get(False),False)
							if len(V) < l :
								V=V+[v]
							elif len(V)==l:
								V=V[1:]+[v]
							else:
								print 'ERROR in V vector'
							ep=0
							break
					if ep==1:
						temp=list(ev.queue)
						V=[v]
						m=num.mean(V+temp)
						for w in temp:
							inp.put(w,False)
						#~ pl.plot(i,v,'r*')
						ev=qx.Queue(l)
						out.append((i,-RSI))

				else:						 #upward shift
					RSI=(v-m-diff)/(l*num.sqrt(sigma))
					for j in range(0,l-1):
						try:
							can=inp.get(False)
						except qx.Empty:
							try:
								can=q.get(False)
							except qx.Empty:
								ep=0
								break
						ev.put(can,False)
						RSI=RSI+(can-m-diff)/(l*num.sqrt(sigma))
						if RSI <= 0:
							while not ev.empty():
								inp.put(ev.get(False),False)
							if len(V) < l :
								V=V+[v]
							elif len(V)==l:
								V=V[1:]+[v]
							else:
								print 'ERROR in V vector'
							ep=0
							break
					if ep==1:
						temp=list(ev.queue)
						V=[v]
						m=num.mean(V+temp)
						for w in temp:
							inp.put(w,False)
						#~ pl.plot(i,v,'r*')
						ev=qx.Queue(l)
						out.append((i,RSI))
		else:
			try:
				V[V.index(None)]=inp.get(False)
			except qx.Empty:
				try:
					V[V.index(None)]=q.get(False)
				except qx.Empty:
					continue
			i=i+1
	return out
