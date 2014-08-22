import math
import numpy as num
import pylab as pl
from myBasic import pickColor

# Global
res=0.0001

def solve2p(a,b,c):
	d=float(b**2-4*a*c)
	if d<0:
		return []
	else:
		d=d**.5
		x1=(-b+d)/(2*a)
		x2=(-b-d)/(2*a)
	return [x1,x2]
	
def angleMap(a):
	a1=a%(2*math.pi)
	if a1>math.pi:
		return -2*math.pi+a1
	else:
		return a1

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


def order(v,w,mode=0):
	a=zip(v,w)
	if mode==0:
		a.sort()
	else:
		a.sort(reverse=True)
	l=zip(*a)
	v=list(l[0])
	w=list(l[1])
	return [v,w]
	

class geoError(Exception):
    def __init__(self, value):
        self.tag = value
    def __str__(self):
        return repr(self.tag)
 
class point:
	def __init__(self,*argv):
		l=len(argv)
		if l==1:
			self.dim=len(argv[0])
		else:
			self.dim=l
		if l==1:
			self.x=argv[0][0]
			self.y=argv[0][1]
			try:
				self.z=argv[0][2]
			except IndexError:
				self.z=0.0
		else:
			if l==2:
				z=0
			elif l==3:
				z=argv[2]
			else:
				raise geoError, 'Input'
			self.x=float(argv[0])
			self.y=float(argv[1])
			self.z=z
	def __str__(self):
		return 'p('+str(self.x)+','+str(self.y)+','+str(self.z)+')'

	def __eq__(self, other): 
		return self.__dict__ == other.__dict__

	def __sub__(self, other):
		if isinstance(other, point):
			tx=self.x-other.x
			ty=self.y-other.y
			tz=self.z-other.z
		else:
			tx=self.x-other.dx
			ty=self.y-other.dy
			tz=self.z-other.dz
		return point(tx,ty,tz)

	def __add__(self, other):
		if isinstance(other, point):
			tx=self.x+other.x
			ty=self.y+other.y
			tz=self.z+other.z
		else:
			tx=self.x+other.dx
			ty=self.y+other.dy
			tz=self.z+other.dz
		return point(tx,ty,tz)

	def __mul__(self, other):
		return point(other*self.x,other*self.y,other*self.z)

	def __rmul__(self, other):
		return point(other*self.x,other*self.y,other*self.z)
		
	def __div__(self, other):
		return point(self.x/other,self.y/other,self.z/other)
	
	def __neg__(self):
		x=-self.x
		y=-self.y
		z=-self.z
		return point(x,y,z)

	def dist(self,other):
		return ((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2)**0.5
		
	def std(self):
		if self.dim==2:
			return [self.x,self.y]
		return [self.x,self.y,self.z]
		
	#~ def transform(self,p1,p2):
		#~ if isinstance(p2,point):
			#~ v=vec(p1,p2)
			#~ rot=v.angle()
			#~ return self.transform(p1,rot)
		#~ else:
			#~ temp=self-p1
			#~ rot=p2
			#~ px=math.cos(rot)*temp.x+math.sin(rot)*temp.y
			#~ py=-math.sin(rot)*temp.x+math.cos(rot)*temp.y
			#~ return point(px,py)
	def transform(self,p,rot):
			px=math.cos(rot)*self.x+math.sin(rot)*self.y
			py=-math.sin(rot)*self.x+math.cos(rot)*self.y
			p_t=point(px,py)
			return p_t-p
	
	def angle(self,p):
		v=vec(self,p)
		return v.angle()
		
		

class vec:
	def __init__(self,*argv):
		if isinstance(argv[0],point) and isinstance(argv[1],point) :
			p=argv[1]-argv[0]
			self.dx=float(p.x)
			self.dy=float(p.y)
			self.dz=float(p.z)
		else:
			self.dx=float(argv[0])
			self.dy=float(argv[1])
			try:
				self.dz=float(argv[2])
			except IndexError:
				self.dz=0.0

	def __str__(self):
		return 'vec('+str(self.dx)+','+str(self.dy)+','+str(self.dz)+')'

	def __eq__(self, other): 
		return self.__dict__ == other.__dict__
		
	def __sub__(self, other):
		if isinstance(other, vec):
			tx=self.dx-other.dx
			ty=self.dy-other.dy
			tz=self.dz-other.dz
			return vec(tx,ty,tz)
		else:
			tx=self.dx-other.x
			ty=self.dy-other.y
			tz=self.dz-other.z
			return point(tx,ty,tz)

	def __add__(self, other):
		if isinstance(other, vec):
			tx=self.dx+other.dx
			ty=self.dy+other.dy
			tz=self.dz+other.dz
			return vec(tx,ty,tz)
		else:
			tx=self.dx+other.x
			ty=self.dy+other.y
			tz=self.dz+other.z
			return point(tx,ty,tz)

	def __mul__(self, other):
		if isinstance(other, vec):
			return self.cross(other)
		return vec(other*self.dx,other*self.dy,other*self.dz)

	def __rmul__(self, other):
		if isinstance(other, vec):
			return other.cross(self)
		return vec(other*self.dx,other*self.dy,other*self.dz)

	def __div__(self, other):
		return vec(self.dx/other,self.dy/other,self.dz/other)


	def dot(self,v):
		return self.dx*v.dx+self.dy*v.dy+self.dz*v.dz
	
	def cross(self,v):
		z=self.dx*v.dy-self.dy*v.dx
		x=self.dy*v.dz-self.dz*v.dy
		y=self.dz*v.dx-self.dx*v.dz
		return vec(x,y,z)

	def mag(self):
		return (self.dx**2+self.dy**2+self.dz**2)**0.5

	def angle(self,*args):
		x=self.dx
		y=self.dy
		z=self.dz

		if len(args)==0:
			if self.mag()<res:
				return 0.0
			if x>=0 and y>=0:
				try:
					return math.atan(y/x)
				except ZeroDivisionError:
					return math.pi/2
			elif x<0 and y>=0:
				return math.pi-math.atan(y/abs(x))
			elif x>=0 and y<0:
				try:
					return -math.atan(abs(y)/x)
				except ZeroDivisionError:
					return -math.pi/2
			else:
				return math.atan(abs(y)/abs(x))-math.pi
		elif len(args)==1:
			b=args[0]
			try:
				rv=math.acos(self.dot(b)/(self.mag()*b.mag()))
				return rv
			except ZeroDivisionError:
				return 0.0
				
	def rot(self,a):
		dx=self.dx
		dy=self.dy
		dx_t=self.dx*math.cos(a)-self.dy*math.sin(a)
		dy_t=self.dx*math.sin(a)+self.dy*math.cos(a)
		return vec(dx_t,dy_t)
			
		
	
class circle:
	def __init__(self,p,r):
		self.c=p
		self.r=float(r)
	def __str__(self):
		return 'Circle['+self.c.__str__()+','+str(self.r)+']'

	def __eq__(self, other): 
		return self.__dict__ == other.__dict__

	def touch(self,o):
		d=self.c.dist(o.c)
		met=self.r+o.r
		if d<met+res:
			return True
		else:
			return False
			
	def side(self,p):
		d=p.dist(self.c)
		r=self.r
		if d<r:
			return 1
		elif d<r+res:
			return 0
		else:
			return -1
		
		
		
class line:
	def __init__(self,x,y):
		if isinstance(x,point) and isinstance(y,point):
			if x==y:
				raise geoError, 'Degenerate'
			try:
				temp=(x.y-y.y)/(x.x-y.x)
				if temp==0:
					self.kind='Horizental'
					self.b=x.y
				else:
					self.kind='Normal'
					self.b=x.y-temp*x.x
			except ZeroDivisionError:
				temp=float('inf')
				self.kind='Vertical'
				self.b=x.x
			self.m=temp
		elif (not isinstance(x,point)) and isinstance(y,point) :
			self.m=float(x)
			if x==0:
				self.kind='Horizental'
				self.b=y.y
			elif x==float('inf'):
				self.kind='Vertical'
				self.b=y.x
			else:
				self.kind='Normal'
				self.b=y.y-x*y.x
		else:
			self.m=float(x)
			if x==0:
				self.kind='Horizental'
			elif x==float('inf'):
				self.kind='Vertical'
			else:
				self.kind='Normal'
			self.b=float(y)

	def __str__(self):
		if self.kind=='Vertical':
			return 'Line(x='+str(self.b)+')'
		elif self.kind=='Horizental':
			return 'Line(y='+str(self.b)+')'
		else:
			return 'Line('+str(self.m)+'x+'+str(self.b)+')'
			
	def intersect(self,L):
		if isinstance(L,line):
			if self.m==L.m:
				raise geoError,'parellel'
			else:
				if self.kind=='Normal' and L.kind=='Normal':
					x=(self.b-L.b)/(L.m-self.m)
					y=L.m*x+L.b
					return point(x,y)
				elif self.kind=='Horizental' and L.kind=='Normal':
					x=(self.b-L.b)/L.m
					return point(x,self.b)
				elif self.kind=='Vertical' and L.kind=='Normal':
					y=L.m*self.b+L.b
					return point(self.b,y)
				elif L.kind=='Horizental' and self.kind=='Normal':
					x=(L.b-self.b)/self.m
					return point(x,L.b)
				elif L.kind=='Vertical' and self.kind=='Normal':
					y=self.m*L.b+self.b
					return point(L.b,y)
				elif self.kind=='Horizental' and L.kind=='Vertical':
					return point(L.b,self.b)
				elif self.kind=='Vertical' and L.kind=='Horizental':
					return point(self.b,L.b)
				else:
					raise geoError,'Unknown'
		else:
			p=L.c
			x0=p.x
			y0=p.y
			r=L.r
			m=self.m
			b=self.b
			c0=b-y0
			if self.kind=='Vertical':
				x=self.b
				sol=solve2p(1,-2*y0,(x-x0)**2-r**2+y0**2)
				w=[]
				for yy in sol:
					w.append(point(x,yy))
				return w
			else:
				sol=solve2p(1+m**2, -2*x0+2*m*c0 , x0**2+c0**2-r**2)
				w=[]
				for x in sol:
					w.append(point(x,m*x+b))
				return w
			
				

	def side(self,p):
		if self.kind=='Vertical':
			if p.x==self.b:
				return 0
			elif p.x>self.b:
				return -1
			else:
				return 1
		else:
			met=p.y-(self.m*p.x+self.b)
		if met<0:
			return -1
		elif met>0:
			return 1
		else:
			return 0

class Triangle:
	def __init__(self,L):
		x=L[0]
		y=L[1]
		z=L[-1]
		L=line(x,y)
		if L.side(z)==0:
			raise geoError, 'Degenerate'
		self.a=x
		self.b=y
		self.c=z
	def __str__(self):
		return 'Triangle{'+self.a.__str__().strip('p')+','+self.b.__str__().strip('p')+','+self.c.__str__().strip('p')+'}'

	def centroid(self):
		V01=0.5*(self.a+self.b)
		V12=0.5*(self.c+self.b)
		L1=line(V01,self.c)
		L2=line(V12,self.a)
		return L1.intersect(L2)

	def A(self):
		v1=vec(self.a,self.b)
		v2=vec(self.a,self.c)
		return 0.5*abs(v1.cross(v2))

class sphere:
	def __init__(self,c,R):
		self.c=c
		self.R=R
	def dist(self,p):
		return abs(p.dist(self.c)-self.R)

	def s2c(self,lon,lat):
		x=self.R*math.cos(lat)*math.cos(lon)
		y=self.R*math.cos(lat)*math.sin(lon)
		z=self.R*math.sin(lat)
		return self.c+point(x,y,z)

	def gcd(self,lon1, lat1, lon2, lat2):
		dlon = lon2 - lon1 
		dlat = lat2 - lat1 
		a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
		temp = 2 * math.asin(math.sqrt(a)) 
		dd = self.R * temp
		return dd

	def gcd2l(self,d):
		#great circle distance to straight line distance
		theta=d/self.R
		return (2*(self.R**2)*(1-math.cos(theta)))**0.5
		
	def map(self,point):
		a=vec(self.c,p)
		e=a/a.mag()
		return self.c+self.R*e

	def side(self,p):
		d=pdist(self.c,p)
		if d>R-res and d<R+res:
			return 0
		if d<R:
			return -1
		else:
			return 1
	#~ def rand(self):
		#~ r1=num.random.rand()
		#~ r2=num.random.rand()
		#~ lat=(r1-.5)*math.pi
		#~ lon=2*(r2-0.5)*math.pi
		#~ return (lon,lat)
		
class Polygon:
	def __init__(self,L):
		#L is the list of points on the polygon
		#L[-1]==L[0] Closed polygon
		if L[-1]==L[0]:
			self.L=L
			self.n=len(L)
		else:
			raise geoError, 'open'

	def area(self):
		s=0
		for i in range(self.n-1):
			p1=self.L[i]
			p2=self.L[i+1]
			s=s+p1.x*p2.y-p2.x*p1.y
		return 0.5*s
	
	def centroid(self):
		sx=0
		sy=0
		for i in range(self.n-1):
			p1=self.L[i]
			p2=self.L[i+1]
			sx=sx+(p1.x*p2.y-p2.x*p1.y)*(p1.x+p2.x)
			sy=sy+(p1.x*p2.y-p2.x*p1.y)*(p1.y+p2.y)
		p=point(sx,sy)
		return p/(6.0*self.area())
		
class Ray:
	def __init__(self,p,a):
		self.c=p
		self.a=angleMap(a)
	def side(self,p):
		ba=p.angle(self.c)
		da=abs(ba-a)/(2*math.pi)
		if da % (2*math.pi) < res:
			return 1
		else:
			return 1
			
	def to_line(self):
		if (abs(self.a-math.pi/2) < res) or (abs(self.a+math.pi/2) < res):
			m=float('inf')
			b=self.c.x
			return line(m,b)
		m=math.tan(self.a)
		return line(m,self.c)
			
	def intersect(self,c):
		if isinstance(c,circle):
			L=self.to_line()
			p=L.intersect(c)
			if len(p)==0:
				return
			else:
				a1=self.c.angle(p[0])
				a2=self.c.angle(p[1])
				if abs(a1-a2) < res:
					print 'hey'
					if p[0].dist(self.c)> p[1].dist(self.c):
						return [p[1],p[0]]
					else:
						return [p[0],p[1]]
				elif abs(a1-self.a) > abs(a2-self.a):
					return [p[1]]
				else:
					return [p[0]]
			
class ndisc:
	def __init__(self,cA):
		self.cA=cA
		self.n=len(cA)
	def is_disjoint(self):
		l=len(self.cA)
		for i in range(l):
			for j in range(i+1,l):
				if not self.cA[j].touch(self.cA[i]):
					return True
		return False
	def sort(self):
		r=[xx.r for xx in self.cA]
		r,self.cA=order(r,self.cA)
		
	#~ def remove_ins(self):
		#~ self.sort()
		#~ if cA[
	def side(self,p):
		counter=[0,0,0] #[#inside,#on,#outside]
		for cir in self.cA:
			fg=cir.side(p)
			if fg==1:
				counter[0]=counter[0]+1
			elif fg==0:
				counter[1]=counter[1]+1
			else:
				counter[2]=counter[2]+1
		return counter
		
	def get_x0(self,weighted=True):
		l=self.n
		r=[w.r for w in self.cA]
		c=[w.c for w in self.cA]
		S=sum(r)
		W=[(S-w)/((l-1)*S) for w in r]
		p0=point(0,0)	#Initialized point
		for i in range(l):
			p0=p0+W[i]*c[i]
		return p0
		
	def intersect(self,obj):
		l=self.n
		d=[0.0]*l
		pl=[point(0,0)]*l
		if isinstance(obj,Ray):
			for i,cir in enumerate(self.cA):
				pl[i]=obj.intersect(cir)[0]
				d[i]=pl[i].dist(obj.c)
		usd,pn=order(d,pl)
		return pn[0]
				
			
		
	def poly(self,step):
		# step is the radian resolution
		cA=self.cA
		self.sort()
		st=False
		fin=False
		cdi=0
		alpha=0
		x0=self.cA[0].c+point(self.cA[0].r,0)
		xc=x0
		pl=[]
		while (alpha<(2*math.pi)):
			if self.side(xc)[-1]==0:
				pl.append(xc)
				st=True
				break
			else:
				xx=num.cos(step)*cA[cdi].r
				yy=num.sin(step)*cA[cdi].r
				xc_t=point(xx,yy)
				xc=xc_t.transform(-cA[cdi].c,-alpha)
				alpha=alpha+step
		if not st:
			return pl
		# pivoting
		pv0=self.get_x0()
		pv=point(pv0.x,pv0.y)
		v0=vec(xc,pv)
		vc=vec(xc,pv)
		spin=0.0
		pv_found=False
		while spin<(2*math.pi):
			if self.side(pv)[0]==self.n:
				pv_found=True
				break
			else:
				vc=vc/2
				if vc.mag()<10*res:
					spin=spin+10*step
					vc=v0.rot(spin)
				pv=xc+vc
		# pivoting finished
		if not pv_found:
			return [xc]
		alpha=num.linspace(0,2*math.pi,int(2*math.pi/step))
		alpha[-1]=math.pi*2
		for a in alpha:
			ray=Ray(pv,a)
			try:
				pc=self.intersect(ray)
				pl.append(pc)
			except geoError:
				print 'Unknown Error in ray-ndisc intersection'
				raise geoError, 'Unknown'
		pl[-1]=pl[0]
		return pl
		
		
			
		
			
			
			
			
			
		
		
		
		
		
		
		
		
	
		
E=sphere(point(0,0,0),6371000)
		

f,ax=pl.subplots(1)

if __name__=='__main__':
	p1=point(0,0)
	p2=point(2,1)
	p3=point(0,-3.89)
	r1=1
	r2=2.9
	r3=2.9
	c11=circle(p1,r1)
	c22=circle(p2,r2)
	c33=circle(p3,r3)
	cA=[c11,c22,c33]
	drawC(cA,ax)

	nd=ndisc(cA)
	p=nd.poly(math.pi/180)

	pg=Polygon(p)
	pp=pg.centroid()
	ax.plot(pp.x,pp.y,'ks',ms=20)
	for w in p:
		ax.plot(w.x,w.y,'ko')
	pl.show()
	#~ ax.plot([xx.x for xx in p],[xx.y for xx in p],'c-',lw=2)
	#~ print len(p)
	#~ ax.plot(p1.x,p1.y,'rs')
	#~ ax.plot(p2.x,p2.y,'bd')
	#~ ax.plot(p3.x,p3.y,'k^')
	#~ pl.show()
	
	#~ print -c
	#~ print p.transform(-c,-45.0*math.pi/180)
	
	#~ c=point(-1,-1)
	#~ d=point(-1,1)
	#~ k=p.transform(c,p)
	#~ print k
	#~ L=[point(0,0),point(1,1),point(-7,9),point(0,0)]
	#~ P=Polygon(L)
	#~ T=Triangle(L[0:3])
	#~ print T.centroid()
	#~ print P.centroid()
	#~ p=point((1,2))
	#~ print p
	#~ print p
	#~ print p
	#~ a=point(3,6,-1)
	#~ s=sphere(a,2)
	#~ i1=s.rand()
	#~ i2=s.rand()
	#~ p1=s.s2c(i1[0],i1[1])
	#~ p2=s.s2c(i2[0],i2[1])
	#~ print p1.dist(p2)
	#~ dd=s.gcd(i1[0],i1[1],i2[0],i2[1])
	#~ print dd
	#~ print s.gcd2l(dd)
	#~ p1=
	#~ b=point(2,4,1)
	#~ c=point(1,4,2)
	#~ d=vec(1,-1,3)
	#~ print a-d
	#~ e=vec(5,1,9)
	#~ print e
	#~ print d
	#~ print e.angle(d)
