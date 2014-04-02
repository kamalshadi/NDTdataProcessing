import ipaddress as ix
from subnet import *
class ipClass:
	def __init__(self,ip):
		if type(ip)==str :
			self.ip = ix.ip_address(unicode(ip))
		elif type(ip)==int :
			self.ip = ix.ip_address(ip)
		else:
			print 'IP should be an integer or string'
			return None
	def bin(self):
		ls=str(self.ip).split('.')
		temp1=[bin(int(x))[2:] for x in ls]
		temp2=['0'*(8-len(w))+w for w in temp1]
		return ''.join(temp2)
		
	def prefix(self,l):
		temp1=self.bin()[:l] + '0'*(32-l)
		return temp1
		
	def string(self):
		return str(self.ip)
		
	def next(self,slash='/32'):
		subString=str(ix.ip_address(int(self.prefix(int(slash.strip('/'))),2)))
		ipSub=subnet(subString+slash)
		last_ip=ipSub.last()
		if last_ip=='255.255.255.255':
			return None
		next_ip=str(ix.ip_address((int(ix.ip_address(unicode(last_ip)))+1)))
		return next_ip
		
	def prev(self,slash='/32'):
		subString=str(ix.ip_address(int(self.prefix(int(slash.strip('/'))),2)))
		ipSub=subnet(subString+slash)
		first_ip=ipSub.first()
		if first_ip=='0.0.0.0':
			return None
		prev_ip=str(ix.ip_address((int(ix.ip_address(unicode(first_ip)))-1)))
		return prev_ip
	
	def first(self,slash='/32'):
		subString=str(ix.ip_address(int(self.prefix(int(slash.strip('/'))),2)))
		ipSub=subnet(subString+slash)
		first_ip=ipSub.first()
		return first_ip
		
	def last(self,slash='/32'):
		subString=str(ix.ip_address(int(self.prefix(int(slash.strip('/'))),2)))
		ipSub=subnet(subString+slash)
		last_ip=ipSub.last()
		return last_ip
	def int(self):
		a=self.bin()
		return int(a,2)
		
	def sub(self,g):
		l=int(g.split('/')[1])
		temp=int(self.prefix(l),2)
		ip=str(ix.ip_address(temp))
		return subnet(ip+g)
