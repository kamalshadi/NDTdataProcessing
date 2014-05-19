#!/usr/bin/env python

import os
import sys
import subprocess
import pylab as pl
from random import randint
import pickle as pk
from scipy.stats.mstats import mquantiles
from myBasic import PDF


def usage():
    return """
Summary:
PDF of Download/Upload Throughput for a given AS or prefix"""

def parse_args():
    from optparse import OptionParser
    parser = OptionParser(usage=usage())
    parser.add_option("-t", "--date", dest="date", default=None, 
                      help="Required: date for query in yyyy_mm format") 
    parser.add_option("-s", "--server", dest="sID", default=None, 
                      help="optional: three-letters mLab server ID") 
    parser.add_option("-p", "--prefix", dest="pr", default=None, 
                      help="optional: Client subnet") 
    parser.add_option("-a", "--asn", dest="asn", default=None, 
                      help="optional: AS number")
    parser.add_option("-f", "--bgp", dest="bf", default=None, 
                      help="optional: BGP file Name")                                        

    
                       
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()
    if options.date is None:
        print "Error: Please provide --date(-d) and --vbs (web100 variable names in comma seperated format) "
        sys.exit(1)
    if options.asn is None and	options.pr is None :
        print "Error: Please provide a prefix or AS"
        sys.exit(1)
    if options.asn is not None and options.bf is None :
        print "Error: BGP file name must be provided by AS number with -f option"
        sys.exit(1)        

    return (options, args)

if __name__=='__main__':
	#~ (options, args) = parse_args()
	#~ date=options.date
	#~ pr=options.pr
	#~ sID=options.sID
	#~ asn=options.asn
	#~ bf=options.bf
	#~ with open('MyQuery/mbps') as f:
		#~ q=f.read()
	#~ if pr is None:
		#~ with open('BGP/'+bf) as f:
			#~ pls=[]
			#~ for line in f:
				#~ w=line.split(' ')
				#~ if w[0].strip()==asn:
					#~ pls.append(w[1].strip())
		#~ where=[]
		#~ 
		#~ for pref in pls:
			#~ px,subl=pref.split('/')
			#~ dx=str(32-int(subl))
			#~ where.append('FORMAT_IP(PARSE_IP(web100_log_entry.connection_spec.remote_ip) & INTEGER(POW(2, 32)-1 - (POW(2,'+dx+\
			#~ ')-1)))=\''+px+"'")
		#~ i=0
		#~ ll=len(where)
		#~ while len(where)>0:
			#~ i=i+1
			#~ print str(i)+"'th 75 of "+str(ll)
			#~ temp=where[0:75]
			#~ del where[0:75]
			#~ cond='\n OR \n'.join(temp)
			#~ q1=q.replace('COND',cond)
			#~ q1=q1.replace("'",'"')
			#~ if i==1:
				#~ qq="bq -q --format=csv query --max_rows 100000 '" + q1.strip() + ";' > CSV/plotMbps"
			#~ else:
				#~ qq="bq -q --format=csv query --max_rows 100000 '" + q1.strip() + ";' |tail -n+2 >> CSV/plotMbps"
			#~ os.system(qq)
			
	with open('CSV/plotMbps-7922') as f:
		r=[]
		k=0
		for w in f:
			if k==0:
				k=1
				continue
			try:
				r.append([float(xx) for xx in w.split(',')])
			except:
				continue
	r1,r2,r3,r4=zip(*r)
	f,ax=pl.subplots(2,2)
	a1,a2=mquantiles(r1,[0.05,0.95])
	rr1=[xx for xx in r1 if a1<xx<a2]
	a1,a2=mquantiles(r2,[0.05,0.95])
	rr2=[xx for xx in r2 if a1<xx<a2]
	a1,a2=mquantiles(r3,[0.05,0.95])
	rr3=[xx for xx in r3 if a1<xx<a2]
	a1,a2=mquantiles(r4,[0.05,0.95])
	rr4=[xx for xx in r4 if a1<xx<a2]
	y1,x1=PDF(rr1)
	y2,x2=PDF(rr2)
	y3,x3=PDF(rr3)
	y4,x4=PDF(rr4)
	ax[0,0].plot(x1,y1)
	ax[0,0].set_title('Avg Throuput')
	ax[1,0].plot(x2,y2)
	ax[1,0].set_title('maxmin sender window throughput')
	ax[0,1].plot(x3,y3)
	ax[0,1].set_title('rwnd/rtt')
	ax[1,1].plot(x4,y4)
	ax[1,1].set_title('cwnd/rtt')
	pl.show()
			
		
