#!/bin/bash

#Will get only the date anf hour
#download BGP routing table and extract "AS# prefix" logged in output file

if [ -d 'BGP' ]
then
if [ -f 'BGP/bgpdump' ]
then
:
else
echo 'Please install bgpdump in BGP directory from url: "http://www.ris.ripe.net/source/bgpdump/"'
exit 100
fi
else
echo 'Please install bgpdump in BGP directory from url: "http://www.ris.ripe.net/source/bgpdump/"'
exit 100
fi



printf 'You must provide input for reqired fields.\n
                 date is in yyyymmdd format and time in hh format\n
                 Note that even hours are available only\n'
echo '---------------------------------'
arg=''
# Entering Project name
read -p "Enter date (yyyymmdd) : "  date
read -p "Eneter time (hh) : " hr
yr=`echo $date|cut -c1-4`
mo=`echo $date|cut -c5-6`
url="http://archive.routeviews.org/bgpdata/$yr.$mo/RIBS/rib.$date.${hr}00.bz2"
echo $url
saving='./BGP'
echo 'Downloading.......'
wget -P $saving $url
echo 'Unzipping.........'
bzip2 -d "$saving/rib.$date.${hr}00.bz2"
fName="rib.$date.${hr}00"
echo 'Converting to text......'
BGP/bgpdump "BGP/$fName" > "BGP/$fName.txt"
echo 'Parsing......'
./parseBGP.py -f "$fName.txt"

