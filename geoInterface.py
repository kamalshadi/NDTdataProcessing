# This is the intrinsic data model used by the localization package "localization"

#D
AnchorDic={}
TargetDic={}
nm=0

class Anchor:
	count=0
	def __init__(self,ID,loc,IP):
		self.ind=Anchor.count
		Anchor.count=Anchor.count+1
		self.loc=loc
		self.ID=str(ID)
		self.IP=IP
		self.measures={}
		self.nm=0 # number of measurements
	def __str__(self):
		return 'Anchor '+self.ID+' @ '+self.loc.__str__()
	def add_measures(self,m):
		global nm
		for w in m:
			try:
				t=TargetDic[w[0]]
			except KeyError:
				print w[0]+':Target not found'
				continue
			self.nm=self.nm+1
			nm=nm+1
			try:
				if len(w)==2:
					self.measures[w[0]].append(w[1],1)
				else:
					self.measures[w[0]].append(w[1],w[2])
			except KeyError:
				if len(w)==2:
					self.measures[w[0]]=[(w[1],1)]
				else:
					self.measures[w[0]]=[(w[1],w[2])]
			a=self.ID
			try:
				if len(w)==2:
					t.measures[a].append((w[1],1))
				else:
					t.measures[a].append((w[1],w[2]))
			except KeyError:
				if len(w)==2:
					t.measures[a]=[(w[1],1)]
				else:
					t.measures[a]=[(w[1],w[2])]
			
				
				
		
				


class Target:
	count=0
	def __init__(self,ID,loc,IP):
		self.ind=Target.count
		Target.count=Target.count+1
		self.loc=loc
		self.eloc=None
		self.ID=str(ID)
		self.IP=IP
		self.status=0	#0 means not yet localized\
						#1 localized
						#2 Attempt of localization failed
		self.measures={}
		self.nm=0 #Number of measurements
	def __str__(self):
		if self.loc is None:
			if self.status:
				return 'Target '+self.ID+' @ Estimated location: '+self.eloc.__str__()
			else:
				return 'Target '+self.ID
		else:
			if self.status:
				return 'Target '+self.ID+' @ Real Location:'+self.loc.__str__()+\
										+' @ Estimated Location:'+self.eloc.__str__()
			else:
				return 'Target '+self.ID+' @ Real Location:'+self.loc.__str__()

	def add_measures(self,m):
		global nm
		for w in m:
			try:
				a=AnchorDic[w[0]]
			except KeyError:
				print w[0]+':Anchor not found'
				continue
			self.nm=self.nm+1
			nm=nm+1
			try:
				if len(w)==2:
					self.measures[w[0]].append((w[1],1))
				else:
					self.measures[w[0]].append((w[1],w[2]))
			except KeyError:
				if len(w)==2:
					self.measures[w[0]]=[(w[1],1)]
				else:
					self.measures[w[0]]=[(w[1],w[2])]
			t=self.ID
			a=AnchorDic[w[0]]
			try:
				if len(w)==2:
					a.measures[t].append((w[1],1))
				else:
					a.measures[t].append((w[1],w[2]))
			except KeyError:
				if len(w)==2:
					a.measures[t]=[(w[1],1)]
				else:
					a.measures[t]=[(w[1],w[2])]


# 0 Empty project
# 1 Setup compiled with no measurements
# 2 Setup and measurement Compiles
# 3 Failure in solution
# 4 Solved


	
			
		

#~ if __name__=='__main__':
	#~ p=(3,4)
	#~ add_anchor('a1',p)
	#~ add_anchor('a2',(0,1))
	#~ add_target('t1',(0,0))
	#~ add_target('t2',(0.1,-0.2))
	#~ add_target('t3')
	#~ add_measures([('a1','t1',22),('a1','t3',12,4),('a1','t3',13.1),('a2','t3',1)])
	#~ print AnchorDic['a1'].measures
	#~ print TargetDic['t3'].measures
	#~ info()

