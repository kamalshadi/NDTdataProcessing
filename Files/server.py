import pickle as pk
f=open('silver2','r')
g=open('silver.pk','w')
d={}
for line in f:
	w=line.split(' ')
	sID=w[0].strip()[0:3]
	ip=w[1].strip()
	try:
		d[ip]=sID
	except KeyError:
		print 'Error: '+ip
pk.dump(d,g)
f.close()
g.close()

		
