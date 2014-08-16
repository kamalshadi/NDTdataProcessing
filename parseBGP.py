#!/usr/bin/env python

import os
import sys
import subprocess


def usage():
    return """
Summary:
Parsing ASCII bgp file created by bgpdump and log in format:
ASNumber Prefix
"""
		

def parse_args():
    from optparse import OptionParser
    parser = OptionParser(usage=usage())
    parser.add_option("-f", "--fileName", dest="fName", default=None, 
                      help="Required: filename") 
    parser.add_option("-r", "--results", dest="rf", default=None, 
                      help="Required: filename for saving results")     
        
    
                       
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()
    if options.fName is None or options.rf is None:
        print "Error: Please provide --filename to parse BGP data\n "
        print "and provide --results tas a filename to save results\n "
        sys.exit(1)

    return (options, args)
		

def parseBGP1(fName,rf):
	f=open("BGP/"+fName,'r')
	fw=open("BGP/"+rf,'w')
	fw.write('AS PREFIX\n')
	prefix=""
	asp=""
	pf=False
	pa=False
	prev=-1
	for line in f:
		if line.strip()=="":
			pf=False
			pa=False
		elif "PREFIX" in line:
			prefix=line.split()[-1].strip()
			pf=True
		elif "ASPATH" in line:
			asp=line.split()[-1].strip()
			pa=True
		else:
			pass
		if pa and pf:
			if prefix != prev:
				fw.write(asp.strip('{"\' \n()\t}').strip()+" "+prefix.strip('{"\'\n()}').strip()+"\n")
				prev=prefix
			pf=False
			pa=False
	f.close()
	fw.close()
	
if __name__=='__main__':
	(options, args) = parse_args()
	fName=options.fName
	rf=options.rf
	parseBGP1(fName,rf)
