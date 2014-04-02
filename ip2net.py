def ip2net(bgpFile,ipList):
	""" ip2net gets as an input --->
	bgpFile: The name of the file containing the parsed BGP table
	ipList: string list of ipv4
	and it returns --->
	output: list of (AS_number,prefix) for each ip in ipList.
	bgpFile='xrib.20140115.0000.txt'
	"""
	try:
		import SubnetTree
	except ImportError:
		print 'Error:Please install SubnetTree package...'
		return
	l=len(ipList)
	output=[None]*l
	bf=open('BGP/'+bgpFile,'r')
	t = SubnetTree.SubnetTree()
	print 'Building subnet network from BGP table'
	i=0
	asDic={}
	for lines in bf:
		if i==0:
			i=1
			continue
		net=lines.strip().split()[-1].strip()
		asn=lines.strip().split()[0].strip()
		asDic[net]=asn
		t[net]=net

	print 'Longest Prefix Matching ....'
	for i,ip in enumerate(ipList):
		try:
			net=t[ip]
			asn=asDic[net]
			output[i]=(asn,net)
		except KeyError:
			pass
	return output
			
			
			
