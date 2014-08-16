print 'hi'
du=0
dd=0
md=0
mu=0
fu=0
fd=0
td=0
tu=0
print 'hi'
with open('Files/roc') as f:
	i=0
	for line in f:
		print line
		if i==0:
			i=1
			continue
		else:
			d,u=line.split(',')
			md=md+int(d[0])
			fd=fd+int(d[1])
			dd=dd+int(d[2])
			td=td-int(d[0])+int(d[2])+int(d[1])
			mu=mu+int(u[0])
			fu=fu+int(u[1])
			du=du+int(u[2])
			tu=tu-int(u[0])+int(u[2])+int(u[1])
	fad=float(fd)/td
	mid=float(md)/dd
	fau=float(fu)/tu
	miu=float(mu)/du
	print fad
	print mid
	print fau
	print miu
