#!/usr/bin/env python

import os
import sys
import subprocess


def usage():
    return """
Summary:
This function query NDT data in month specified by -d options using bigquery API.
the output is logged in CSV file with format:
Client IP, Time, RTT, Download Mbps, Upload Mbps, Server IP

Look at options for specifications
"""
		

def parse_args():
    from optparse import OptionParser
    parser = OptionParser(usage=usage())
    parser.add_option("-d", "--date", dest="date", default=None, 
                      help="Required: date for query in yyyy_mm format")     
    parser.add_option("-f", "--fileName", dest="fName", default=None, 
                      help="optional: output filename for data") 
    parser.add_option("-q", "--query", dest="qs", default='ndtQ', 
                      help="Optional: query string file")  
    parser.add_option("-r", "--res", dest="res", default=12, type='int',
                      help="optional: resolution to run query(hours)")
    parser.add_option("-n", "--days", dest="nd", default=31, type='int', 
                      help="optional: Number of days to query") 
    parser.add_option("-o", "--odays", dest="off", default='01',
                      help="optional: Number of days to offset(inter 0x for x days if 0<x<10 ") 
    
                       
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()
    if options.date is None:
        print "Error: Please provide --date(-d) to download data "
        sys.exit(1)

    return (options, args)
		

if __name__=='__main__':
	(options, args) = parse_args()
	qq=open('MyQuery/'+options.qs,'r')
	qstr1=qq.read()
	date=options.date
	res=options.res
	nd=options.nd
	off=options.off
	count=max(nd*24/res,1)
	temp=qstr1.replace('DATE1',date)
	if options.fName is None:
		fName='ndt'+date.replace('_','')
	else:
		fName=options.fName
	for j in range(count):
		print 'LOOP '+str(j+1)+'/'+str(count)
		temp2=temp.replace('RES',str(res))
		temp3=temp2.replace('DATE2',date.replace('_','-')+'-'+off)
		qstr=temp3.replace('COUNT',str(j+1))
		if j==0:
			qc = "bq -q --format=csv query --max_rows 100000 '" + qstr.strip() + ";' > CSV/" + fName
		else:
			qc = "bq -q --format=csv query --max_rows 100000 '" + qstr.strip() + ";' |tail -n+2 >> CSV/" + fName
		r = os.system(qc)

