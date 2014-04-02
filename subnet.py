import ipaddress as ix
class subnet:
	def __init__(self,sub):
		self.sub = ix.ip_network(unicode(sub))
	def bin(self):
		ip=self.string().split('/')[0]
		ls=str(ip).split('.')
		temp1=[bin(int(x))[2:] for x in ls]
		temp2=['0'*(8-len(w))+w for w in temp1]
		return ''.join(temp2)
	def prefix(self):
		l=int(str(self.sub).split('/')[1])
		ip=str(self.sub).split('/')[0]
		temp1=[bin(int(w))[2:] for w in ip.split('.')]
		temp=['0'*(8-len(w))+w for w in temp1]
		p=''.join(temp)
		return [p,l]
	def split(self):
		p,l=self.prefix()
		if l<31:
			pr=str(ix.ip_address(int(p,2)))
			pl=str(ix.ip_address(int(p[0:l]+'1'+'0'*(32-l-1),2)))
			subr=subnet(unicode(pr+'/'+str(l+1)))
			subl=subnet(unicode(pl+'/'+str(l+1)))
			return [subl,subr]
		if l==31:
			subr=subnet(str(ix.ip_address(int(list(self.sub.hosts())[0])))+'/32')
			subl=subnet(str(ix.ip_address(int(list(self.sub.hosts())[-1])))+'/32')
			return [subl,subr]
		else:
			return [None,None]
	def last(self):
		p,l=self.prefix()
		pp=p[0:l]+'1'*(32-l)
		if l<31 and l!=32:
			return str(ix.ip_address(int(pp,2)))
		elif l==31:
			return str(ix.ip_address(int(list(self.sub.hosts())[-1])))
		else:
			return self.string().split('/')[0]
	def first(self):
		p,l=self.prefix()
		if l<31 and l!=32:
			return str(ix.ip_address(int(p,2)))
		elif l==31:
			return str(ix.ip_address(int(list(self.sub.hosts())[0])))
		else:
			return self.string().split('/')[0]
	def string(self):
		return str(self.sub)
	def grow(self):
		p,l = self.prefix()
		p_n=int(p[0:(l-1)]+'0'*(32-l+1),2)
		return subnet(str(ix.ip_address(p_n))+'/'+str(l-1))
		
		
	
