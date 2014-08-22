import geoInterface as gx
import multiLateration as ml
import geometry as gm


Eligible={'2D':['LSE','LSE_GC','Centroid'],'3D':['LSE','LSE_GC','Centroid'],\
			'Sphere':['LSE','LSE_GC','Centroid'],'Earth1':['LSE','LSE_GC','Centroid'],\
			'Earth2':['LSE','LSE_GC','Centroid']}
class Project:
	np=0
	def __init__(self,res=1e-6,mode='2D',disp='True',solver='LSE',apt=3):
		Project.np=Project.np+1
		self.res=res
		self.mode=mode
		self.disp=disp
		self.solver=solver
		self.apt=apt

	def add_anchor(self,ID,loc,IP=None):
		try:
			gx.AnchorDic[ID]
			print str(ID)+':Anchor with same ID already exists'
			return
		except KeyError:
			a=gx.Anchor(ID,gm.point(loc),IP=IP)
			gx.AnchorDic[ID]=a
		return a
			
	def add_target(self,ID,loc=None,IP=None):
		try:
			gx.TargetDic[ID]
			print 'Target with same ID already exists'
			return
		except:
			if loc is not None:
				t=gx.Target(ID,gm.point(loc),IP)
			else:
				t=gx.Target(ID,None,IP=IP)
			gx.TargetDic[ID]=t
		return t
			
	def add_measures(self,m):
		for w in m:
			a=w[0]
			t=w[1]
			d=w[2]
			try:
				weight=w[3]
			except IndexError:
				weight=1.0
			try:
				gx.AnchorDic[a]
			except KeyError:
				print a+':Anchor not found'
				continue
			try:
				gx.TargetDic[t]
			except KeyError:
				print t+':Target not found'
				continue
			cur=gx.TargetDic[t]
			cur.add_measures([(a,d,weight)])
			
	def info(self):
		na=len(gx.AnchorDic)
		nt=len(gx.TargetDic)
		print '---------Setup--------------'
		print 'Number of anchors:'+str(na)
		print 'Number of targets:'+str(nt)

		lt=0
		gt=0
		lgt=0
		pgt=0
		nt=gx.Target.count
		nm=gx.nm
		e=[]
		for t in gx.TargetDic.values():
			if t.status:
				lt=lt+1
				if t.loc is not None:
					lgt=lgt+1
					gt=gt+1
					pgt=pgt+t.nm
					e.append(t.loc.dist(t.eloc))
			else:
				if t.loc is not None:
					pgt=pgt+t.nm
					gt=gt+1
		try:
			print 'Percentage of GT targets:'+str(float(gt*100)/nt)+'%'
		except ZeroDivisionError:
			print 'Percentage of GT targets:'+'0.0%'
		print 'Number of measurements:'+str(nm)
		try:
			print 'Percentage of GT measurements:'+str(float(pgt*100)/nm)+'%'
		except ZeroDivisionError:
			print 'Percentage of GT measurements'+'0.0%'
		print '---------Results--------------'
		print 'Number of targets localized:'+str(lt)
		try:
			print 'Percentage of ground truth targets localized:'+str(lgt*100/gt)+'%'
		except ZeroDivisionError:
			print 'Percentage of ground truth targets localized:0.0%'
		if len(e)>0:
			me=sum(e)/lgt
			print 'Mean of error:'+str(me)
			if len(e)>1:
				ve=sum([(xx-me)**2 for xx in e])/lgt 
				print 'Variance of error:'+str(me)
		print '==============================='
		print 'GT: Ground Truth'
		
	def solve(self,**kwargs):
		try:
			if self.solver not in Eligible[self.mode]:
				print 'Error:'+self.solver+' solver not found for '+self.mode
				return
		except KeyError:
			print 'Error: Mode '+self.mode+' not supported'
			return
		if self.mode=='2D':
			for tID in gx.TargetDic.keys():
				tar=gx.TargetDic[tID]
				if len(tar.measures)<self.apt:
					continue
				cA=[]
				for tup in tar.measures.items():
					landmark=tup[0]
					c=gx.AnchorDic[landmark].loc
					ms=[xx[0] for xx in tup[1]]
					ws=[xx[1] for xx in tup[1]]
					# considering all measurements
					for xx in ms:
						cA.append(gm.circle(c,xx))
				if self.solver=='LSE':
					try:
						tar.eloc = ml.lse(cA,cons=False)
						tar.status=1
					except:
						tar.status=-1
				elif self.solver=='LSE_GC':
					try:
						tar.eloc = ml.lse(cA)
					except cornerCases:
						self.status=-1
						
					
					
						
					
					
#~ if __name__=='__main__':
	#~ P=Project()
	#~ print P.res
	#~ P.add_anchor('a',(2,3))
	#~ P.add_anchor('b',(0,0))
	#~ P.add_anchor('c',(0,5))
	#~ t1=P.add_target('t1')
	#~ t2=P.add_target('t2',[-1,-1])
	#~ t1.add_measures([('a',3),('b',1),('c',3)])
	#~ P.solve()
	#~ P.info()
					
					
		
		


