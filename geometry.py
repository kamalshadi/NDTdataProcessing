import math
import numpy as num


# Global
res=0.0001
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
			self.x=argv[0]
			self.y=argv[1]
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
	
	def dist(self,other):
		return ((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2)**0.5
		
	def std(self):
		if self.dim==2:
			return [self.x,self.y]
		return [self.x,self.y,self.z]
		

class vec:
	def __init__(self,*argv):
		if isinstance(argv[0],point) and isinstance(argv[1],point) :
			p=argv[1]-argv[0]
			self.dx=p.x
			self.dy=p.y
			self.dz=p.z
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
			
		
	
class circle:
	def __init__(self,p,r):
		self.c=p
		self.r=r
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

class triangle:
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
		
E=sphere(point(0,0,0),6371000)
		
	
	
#~ if __name__=='__main__':
	#~ p=point((1,2))
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
