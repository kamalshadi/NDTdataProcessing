import pylab as pl
import math
from geometry import *
import numpy as num
from scipy.optimize import minimize,fmin_cobyla
from myBasic import *

#Global variables
res=0.0001 #resolution (two point less than res distant are considered unique)
def order(v,w,q,mode=0):
	a=zip(v,w,q)
	if mode==0:
		a.sort()
	else:
		a.sort(reverse=True)
	l=zip(*a)
	v=list(l[0])
	w=list(l[1])
	q=list(l[2])
	return [v,w,q]


class cornerCases(Exception):
    def __init__(self, value):
        self.tag = value
    def __str__(self):
        return repr(self.tag)



def pdist(p1,p2):
	return ((p1.x-p2.x)**2+(p1.y-p2.y)**2)**.5

def is_in_cir(p,c):
	D=pdist(c.c,p)
	if D<=c.r:
		return True
	return False

def cirIntersections(c0,c1):
	D=pdist(c0.c,c1.c)
	if D>c1.r+c0.r:
		raise cornerCases,'Disjoint'
	elif D<abs(c1.r-c0.r):
		raise cornerCases,'Contained'
	elif c1==c0:
		raise cornerCases,'Identical'
	else:
		a=(c0.r**2-c1.r**2+D**2)/(2*D)
		h=(c0.r**2-a**2)**0.5
		P2=c0.c+(a/D)*(c1.c-c0.c)
		P3x=P2.x+(h/D)*(c1.c.y-c0.c.y)
		P3y=P2.y-(h/D)*(c1.c.x-c0.c.x)
		i1=point(P3x,P3y)
		P3x=P2.x-(h/D)*(c1.c.y-c0.c.y)
		P3y=P2.y+(h/D)*(c1.c.x-c0.c.x)
		i2=point(P3x,P3y)
		return(i1,i2)
		
def cirPatch(c):
	circ=pl.Circle((c.c.x,c.c.y), radius=c.r,fc='none',lw=2,ec='red')
	return circ
		
def multilat3(cA):
	#cA is the circle array(three circles currently)
	L=[]
	ccc=0
	for i,w in enumerate([(cA[1],cA[2]),(cA[0],cA[2]),(cA[0],cA[1])]):
		try:
			s0,s1=cirIntersections(w[0],w[1])
			D=pdist(s0,s1)
		except cornerCases as cc:
			kind=cc.tag
			if kind=='Disjoint':		# If circles are disjoint we raise "Disjoint" error and exit the function
				raise cornerCases, 'Disjoint'
			elif kind=='Contained':
				ccc=ccc+1
				if w[0].r < w[1].r:
					coc=w[0].c
				else:
					coc=w[1].c
				continue
			elif kind=='Identical':
				ccc=ccc+1
				continue
			else:
				'Check the code in "multilat" function'
		fg0=is_in_cir(s0,cA[i])
		fg1=is_in_cir(s1,cA[i])
		
		#tangent case
		if D<res:
			if fg0:
				return [s0]
			else:
				raise cornerCases, 'Disjoint'
				
		#two point intersection case
		else:
			if fg0:
				L.append(s0)
			if fg1:
				L.append(s1)
		#All contained or identical
	if ccc==3:
		raise cornerCases, 'trivialCase'
	elif ccc==2:
		return [coc]
	else:
		return L

		
def centroid(L):
	if len(L)==0:
		raise cornerCases, 'Disjoint'
	elif len(L)==1:
		return L[0]
	elif len(L)==2:
		return 0.5*(L[0]+L[1])
	elif len(L)==3:
		T=triangle(L)
		return T.centroid()
	elif len(L)==4:
		V=quad2tria(L)
		T1=triangle(V[0])
		T2=triangle(V[1])
		return cen_comp([(T1.centroid(),T1.A()),(T2.centroid(),T2.A())])
	else:
		raise cornerCases, 'unkown'
		
def rot(p,phi):
	s=math.sin(phi)
	c=math.cos(phi)
	x=p.x*c-p.y*s
	y=s*p.x+c*p.y
	return point(x,y)

def cen_cirSeg(c,v,w):
	#Centroid and area of segment of a circle "c"
	#v and w are to points on a circle(secant endpoints)
	#fg True for small segment and false for big one
	amb=0
	#finding the angle of rotation
	m=vec(c.c,0.5*(v+w))
	mp=0.5*(v+w)
	if pdist(mp,c.c)<res:
		amb=1
		phi=math.pi/2+vec(c.c,v).angle()
	else:
		phi=m.angle()
	print 'phi '+str(phi*180/math.pi)
	#calculating centroid
	ow=vec(c.c,w)
	ov=vec(c.c,v)
	t=ow.angle(ov)
	r=c.r
	A=0.5*(t-math.sin(t))*r**2
	h=4*r*((math.sin(t/2))**3)/(3*(t-math.sin(t)))
	ans=point(h,0)
	
	#rotating and transformation
	pp=rot(ans,phi)+c.c
	
	Ap=math.pi*(r**2)-A
	ratio=A/Ap
	o=c.c
	return [(pp,A),(ratio*(o-pp)+o,Ap)]
		
def cen_comp(L):
	#L is the list of (centroid,area) tuples
	num=point(0,0)
	denum=0
	for w in L:
		num=num+w[1]*w[0]
		denum=denum+w[1]
	return num/denum
	
def cen_triangle(V):
	# P is the vertices of polygon
	V01=0.5*(V[0]+V[1])
	V12=0.5*(V[2]+V[1])
	L1=line(V01,V[2])
	L2=line(V12,V[0])
	return L1.intersect(L2)
	
def quad2tria(V):
	l=len(V)
	for j in range(l):
		for i in range(l):
			if i==j:
				continue
			L1=line(V[j],V[i])
			S=list({0,1,2,3}-{i,j})
			if (L1.side(V[S[0]])*L1.side(V[S[1]]))==-1:
				return [(V[i],V[j],V[S[0]]),(V[i],V[j],V[S[1]])]
	raise cornerCases, 'Degenerate'


	
def trilat(sA,s0=None):
	# trilateration according to wikipedia page
	# if s0 is given the nearest point to s0 is returned

	#Checking disjoint case
	if (sA[0].c.dist(sA[1].c) >  (sA[0].R+sA[1].R)) or (sA[2].c.dist(sA[1].c) >  (sA[2].R+sA[1].R)) or (sA[2].c.dist(sA[0].c) >  (sA[2].R+sA[0].R)):
		raise cornerCases, 'Disjoint'
	P01=vec(sA[0].c,sA[1].c)
	ex=P01/P01.mag()
	P02=vec(sA[0].c,sA[2].c)
	i=P02.dot(ex)
	temp=P02-i*ex
	ey=temp/temp.mag()
	ez=ex*ey
	d=(sA[0].c).dist(sA[1].c)
	j=ey.dot(P02)
	r0=sA[0].R
	r1=sA[1].R
	r2=sA[2].R
	x=(r0**2-r1**2+d**2)/(2*d)
	y=(r0**2-r2**2+i**2+j**2)/(2*j)-x*i/j
	try:
		z=(r0**2-x**2-y**2)**0.5
	except ValueError:
		raise cornerCases, 'methodFailure'
	l1=sA[0].c+x*ex+y*ey+z*ez
	l2=sA[0].c+x*ex+y*ey-z*ez
	if s0 is None:
		return (l1,l2)
	else:
		if s0.dist(l1) > s0.dist(l2):
			return l2
		return l1
	
	
#centroid method
def CCA(cA):
	#centroid of common area
	#this method return the centroid of common area
	try:
		L=multilat3(cA)
	except cornerCases as cc:
		if cc.tag=='Disjoint':
			return
		elif cc.tag=='trivialCase':
			return cA[0].c
	return centroid(L)
	
def Norm(x,c):
	return ((x[0]-c[0])**2+(x[1]-c[1])**2)**0.5


def sum_error(x,c,r):
	l=len(c)
	e=0
	for i in range(l):
		e=e+(Norm(x,c[i].std()) - r[i])**2
	return e
	
def cost(e,p):
	if e<0:
		return abs(p*e)
	else:
		return abs(e)
		
		
		
def cost_model(x,c,r,p):
	l=len(c)
	e=0
	for i in range(l):
		e=e+cost((Norm(x,c[i].std()) - r[i])/r[i],p)
	return e
	
	
#~ def sum_error_der(x,c,r):
	#~ l=len(c)
	#~ ex=0
	#~ ey=0
	#~ for i in range(l):
		#~ dn=Norm(x,[c[i].x,c[i].y])
		#~ ex=ex+(x[0]-c[i].x)/dn
		#~ ey=ey+(x[1]-c[i].y)/dn
	#~ return num.array([ex,ey])
	
	
def is_disjoint(cA):
	l=len(cA)
	for i in range(l):
		for j in range(i+1,l):
			if not cA[j].touch(cA[i]):
				return True
	return False
				
	
def lse(cA,cons=True):
	l=len(cA)
	r=[w.r for w in cA]
	c=[w.c for w in cA]
	S=sum(r)
	W=[(S-w)/((l-1)*S) for w in r]
	p0=point(0,0)	#Initialized point
	for i in range(l):
		p0=p0+W[i]*c[i]
	x0=num.array([p0.x,p0.y])
	if cons:
		print 'GC-LSE'
		if not is_disjoint(cA):
			cL=[]
			for q in range(l):
				def ff(x,q=q):
					return r[q]-Norm(x,c[q].std())
				cL.append(ff)
			res = fmin_cobyla(sum_error, x0,cL,args=(c,r),consargs=(),rhoend = 1e-5)
			ans=res
		else:
			raise geoError, 'Disjoint'
	else:
		print 'LSE'
		res = minimize(sum_error, x0, args=(c,r), method='BFGS')
		ans=res.x
	return point(ans)
	
def myWay(cA,p):
	l=len(cA)
	r=[w.r for w in cA]
	c=[w.c for w in cA]
	S=sum(r)
	W=[(S-w)/((l-1)*S) for w in r]
	p0=point(0,0)	#Initialized point
	for i in range(l):
		p0=p0+W[i]*c[i]
	x0=num.array([p0.x,p0.y])
	res = minimize(cost_model, x0, args=(c,r,p), method='BFGS')
	ans=res.x
	return point(ans)
	

	
	
#LEAST SQUARE ERROR
#CONSTRAINED GEOMETRICAL OPTIMIZATION
#RTT2DISTANCE
#GENEREALIZE FOR MORE THAN 3 LANDMARK
#VISULAZATION
		
def test_cirSeg():
	q=1.0/(2**0.5)
	p0=point(-2,1)
	#~ p1=point(-1,0)
	#~ p2=point(0,3)
	c0=cir(p0,2)
	p1=point(0,1)
	p2=point(-4,1)
	pa1,pa2=cen_cirSeg(c0,p1,p2)
	cen1=pa1[0]
	cen2=pa2[0]
	f,ax=pl.subplots(1)
	a1=cirPatch(c0)
	ax.add_artist(a1)
	ax.plot(cen1.x,cen1.y,'k*')
	ax.plot(cen2.x,cen2.y,'bs')
	ax.plot(c0.c.x,c0.c.y,'ro')
	ax.plot([p1.x,p2.x],[p1.y,p2.y])
	ax.set_xlim([c0.c.x-c0.r-1,c0.c.x+c0.r+1])
	ax.set_ylim([c0.c.y-c0.r-1,c0.c.y+c0.r+1])

	pl.show()
	
def test_CCA():
	r0=2
	r1=2
	r2=2
	p0=point(-1,0)
	p1=point(-1,0)
	p2=point(-1,0)
	c0=cir(p0,r0)
	c1=cir(p1,r1)
	c2=cir(p2,r2)
	p=CCA([c0,c1,c2])
	f,ax=pl.subplots(1)
	a0=cirPatch(c0)
	a1=cirPatch(c1)
	a2=cirPatch(c2)
	ax.add_artist(a0)
	ax.add_artist(a1)
	ax.add_artist(a2)
	ax.plot(p.x,p.y,'k*')
	ax.set_xlim([-4,4])
	ax.set_ylim([-4,4])

	pl.show()
		
def lsLocalization(cA):
	#cA is the arrays of circles
	l=len(cA)
	sx=[cA[i].c.x for i in range(l)]
	sy=[cA[i].c.y for i in range(l)]
	r=[cA[i].r for i in range(l)]
	#sx is the landmark x coordinates
	#sy iss the landmark y coordinates
	#r is corresponding disstances from the mobile node
	l=len(sx)
	if len(sy)==len(r)==l:
		if l<3:
			print 'At least three landmarks are needed' 
			return
	else:
		print 'Size of inputs do not match'
		return
	r,sx,sy=order(r,sx,sy)
	sxt=[xx-sx[0] for xx in sx]
	syt=[xx-sy[0] for xx in sy]
	H=num.matrix([sxt[1:],syt[1:]]).transpose()
	b=num.matrix(num.zeros((l-1,1)))
	for k in range(1,l):
		kk=sxt[k]**2+syt[k]**2
		d=r[0]**2-r[k]**2
		b[k-1,0]=0.5*(kk+d)
	S=((H.T*H).I)*H.T*b
	#~ print sx
	#~ return S[1,0]
	return point(S[0,0]+sx[0],S[1,0]+sy[0])

def drawC(cA,ax):
	xmin=float('inf')
	xmax=-xmin
	ymin=float('inf')
	ymax=-ymin
	for q,w in enumerate(cA):
		t1=w.c.x-w.r
		t2=w.c.x+w.r
		if t1<xmin:
			xmin=t1
		if t2>xmax:
			xmax=t2
		t1=w.c.y-w.r
		t2=w.c.y+w.r
		if t1<ymin:
			ymin=t1
		if t2>ymax: 
			ymax=t2
		circ=pl.Circle((w.c.x,w.c.y), radius=w.r,fc='none',lw=2,ec=pickColor(q))
		ax.add_artist(circ)
	ax.set_xlim([xmin,xmax])
	ax.set_ylim([ymin,ymax])
		
	
#~ if __name__=='__main__':
	#~ px=point(1,-2,0)
	#~ p0=point(6.5,3,0)
	#~ p1=point(-5,6)
	#~ p2=point(2,7)
	#~ s0=cir(p0,4)
	#~ s1=cir(p1,p1.dist(px)+1)
	#~ s2=cir(p2,p2.dist(px)+1)
	#~ cA=[s0,s1,s2]
	#~ a=lse(cA,True)
	#~ f,ax=pl.subplots(1)
	#~ drawC(cA,ax)
	#~ ax.plot(a.x,a.y,'r*',ms=20)
	#~ ax.plot(px.x,px.y,'ks',ms=10)
	#~ r=[w.r for w in cA]
	#~ c=[w.c for w in cA]
	#~ f1=lambda x: r[0]-Norm(x,[c[0].x,c[0].y])
	#~ f2=lambda x: r[1]-Norm(x,[c[1].x,c[1].y])
	#~ f3=lambda x: r[2]-Norm(x,[c[2].x,c[2].y])
	#~ print '-----------------'
	#~ print f1([a.x,a.y])
	#~ print f2([a.x,a.y])
	#~ print f3([a.x,a.y])
	#~ pl.show()
	#~ print a
	

		
