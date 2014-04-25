import numpy as num
import pickle as pk
import pylab as pl
from myBasic import CDF,PDF,list2dic
import sqlite3 as sq

def asso(a,b):
	r=[]
	asm=list(set(a))
	bsm=list(set(b))
	dic={}
	for v,w in zip(a,b):
		try:
			dic[v][w]=dic[v][w]+1
		except KeyError:
			dic[v]=[0]*len(bsm)
	for spu in asm:
		spd=dic[spu].index(max(dic[spu]))
		r.append((spd,spu))
	dic={}
	for v,w in zip(b,a):
		try:
			dic[v][w]=dic[v][w]+1
		except KeyError:
			dic[v]=[0]*len(asm)
	for spd in bsm:
		spu=dic[spd].index(max(dic[spd]))
		r.append((spd,spu))
	return list(set(r))
		
		
		
		
		
fName='ndt201401'
pd=[]
pu=[]
with open('Model/'+fName+'.pk') as f:
	asd=pk.load(f)
asn=asd.keys()
dF='CSV/'+fName+'.db'
with open(dF) as f:
	D=sq.connect(dF)
cur=D.cursor()
for w in asn:
	print w
	spd,spu=asd[w]
	qq='''select spd  , spu
	from meta
	where SPD not null and spu not null and spd!=-1 and spu !=-1 and cAS="'''+w+'"'
	cur.execute(qq)
	A=cur.fetchall()
	B=zip(*A)
	dn=list(B[0])
	un=list(B[1])
	r=asso(dn,un)
	for tup in r:
		ds=tup[0]
		us=tup[1]
		try:
			print spd[ds]
			print spu[us]
		except:
			print '!!!!!!!!!!1'
			print spd
			print ds
		raw_input()
	


