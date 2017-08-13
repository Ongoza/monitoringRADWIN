#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""testDrive.py
 
 TODO:

CHANGELOG:
 DONE --> Added status_only options resulting only True or False result (Script mode without any output)
 DONE --> bugfix from Filip Van Raemdonck mechanix debian org
 DONE --> add more support for modules (raise instead of sys.exit)
 DONE --> locale func names
 DONE --> package def
 DONE --> some code cleanup
 rwGPS_
  $str = "$timeStart, $lat, $lng, $rss, $myPing, $linkName, $linkStatus";
  
"""
from pysnmp.entity.rfc3413.oneliner import cmdgen
import sys
import os
import time
import string
import subprocess

# ##########################################################################################
# ###########################################################################################
__program__   = 'Loco TestSpeedLocal'
__version__   = '0.8'
__date__      = '2013/1/9'
__author__    = 'O Skuybida'
__licence__   = 'Comercial'
__copyright__ = 'Copyright (C) 2013 Oleg Skuibida'

def getODU2(myHost):
   try:	
	#errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('test-agent', 'NSMX-RO', 1), cmdgen.UdpTransportTarget((myHost, 161)),(1,3,6,1,2,1,2,2,1,10,1),)
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('test-agent', 'public', 0), cmdgen.UdpTransportTarget((myHost, 161)),
	(1,3,6,1,2,1,2,2,1,10,1), # downlink
	(1,3,6,1,2,1,2,2,1,16,1), #uplink
	(1,3,6,1,4,1,4458,1000,2,2,14,0), # radio speed
	(1,3,6,1,4,1,4458,1000,1,5,9,1,0), # rss
	(1,3,6,1,4,1,4458,1000,1,1,19,0), # bs name
	(1,3,6,1,4,1,4458,1000,1,5,5,0)) # link status
	if errorIndication:
		data = [-1,-1,-1,-1,'N',-1]
	else:
		if errorStatus:
			data = [-1,-1,-1,-1,'N',-1]
		else:
			data = []
			for name, val in varBinds:
				data.append(val.prettyPrint())
   except:
	   data = [-1,-1,-1,-1,'N',-1]
   return(data)
	
def getODU(myHost):
   try:
	#errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('test-agent', 'NSMX-RO', 1), cmdgen.UdpTransportTarget((myHost, 161)),(1,3,6,1,2,1,2,2,1,10,1),)
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('test-agent', 'public', 0), cmdgen.UdpTransportTarget((myHost, 161)),
	(1,3,6,1,2,1,2,2,1,10,1),
	(1,3,6,1,2,1,2,2,1,16,1))
	if errorIndication:
		data = [-1,-1]
	else:
		if errorStatus:
			data = [-1,-1]
		else:
			data = []
			for name, val in varBinds:
				data.append(val.prettyPrint())
   except:
	   data = [-1,-1]
   return(data)
	
def getGPS(myHost):
   try:
	data = []
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
	cmdgen.CommunityData('test-agent', 'public', 0), cmdgen.UdpTransportTarget((myHost, 161)),
	(1,3,6,1,4,1,4458,1000,1,5,40,11,0),
	(1,3,6,1,4,1,4458,1000,1,5,40,13,0))
	if errorIndication:
		data = [-1,-1]
	else:
		if errorStatus:
			data = [-1,-1]
		else:
			data = []
			for name, val in varBinds:
				data.append(val.prettyPrint())
   except:
	   data = [-1,-1]
   return(data)

def pingNode(ip):
   try:
	str22 = "ping -c1 -w1 " + ip
	proc = subprocess.Popen(str22, shell=True, stdout=subprocess.PIPE)
	out = proc.stdout.readlines()
	ss = out[1].split(' ')
	ms = 0
	if (len(ss)>1):
		try:
			ms = float(ss[6][5:])
		except:
			ms = 0
   except:
	   ms = 0
   return ms
  
def _error(err):
    """Exit if running standalone, else raise an exception
    """

    if __name__ == '__main__':
        print "%s: %s" % (os.path.basename(sys.argv[0]), str(err))
        print "Try `%s --help' for more information." % os.path.basename(sys.argv[0])
        sys.exit(1)
    else:
        raise Exception, str(err)



def _usage():
    """Print usage if run as a standalone program
    """
    print """usage: %s [OPTIONS] IP-ODU IP-GPS IP-for ping
    Loco TestDrive script.
   Mandatory arguments to long options are mandatory for short options too.
   -h, --help       Display this help and exit

    Report bugs to Oleg [at] loco com ua""" % os.path.basename(sys.argv[0])
    sys.exit(0)

if __name__ == '__main__':
	"""Main loop
	"""	
	train_str = sys.argv[1]
	train = int(train_str)-1
	#print "start", train
	nodeList = ['100.200.200.1','100.200.200.2','100.200.200.3','100.200.200.4','100.200.200.5','100.200.200.6','100.200.200.7','100.200.200.8','100.200.200.9','100.200.200.10']
	nodeListGPS = ['100.200.200.21','100.200.200.22','100.200.200.23','100.200.200.24','100.200.200.25','100.200.200.26','100.200.200.27','100.200.200.28','100.200.200.29','100.200.200.20']
	dt = time.strftime('%y.%m.%d %X')
	nodeODU= nodeList[train]# адрес ODU
	nodeGPS = nodeListGPS[train] # адрес GPS
	#nodeODU='100.100.105.1'
	#nodeGPS='100.100.105.4'
	node = "100.254.254.254" # ping host
	#print 'd0'
	#node = "192.168.200.15" # ping host
	myFile = "/home/drive/data/__"+train_str
	while (1>0):
		try:
			#print "s0"
			sd1, su1 = getODU(nodeODU)
			#print "s1"
			t1 = time.time()
			#print "s2"
			time.sleep(0.5)
			#print "s3"
			sd2, su2, sA, rss, sN, status = getODU2(nodeODU)
			#print "s4"
			t = int((time.time() - t1)*1000)
			#print "s5"
			sd1 = int(sd1)
			sd2 = int(sd2)
			su1 = int(su1)
			su2 = int(su2)
			#print sd1, sd2
			if (sd1>0 and sd2>0):
				#print sd1, "=="
				sDown = int(((int(sd2) - int(sd1))*8)/t)
			else:
				sDown = 0
			if (su1>0 and su2>0):	
				sUp = int(((int(su2)- int(su1))*8)/t)
			else:
				sUp = 0
			#print sA
			sA= int(sA)/1000
			ping = pingNode(node)
			#print "ddd"
			GPSln, GPSlt = getGPS(nodeGPS)
			#print GPSln, GPSlt
			tm1 = time.strftime('%y-%m-%d')
			tm2 = time.strftime('%X')
			myStr = tm1+' '+tm2+' '+str(GPSln)+' '+str(GPSlt)+' '+str(ping)+' '+str(rss)+' '+str(sN)+' '+str(status)+' '+str(sDown)+' '+str(sUp)+' '+str(sA)
			#print train_str+' '+myStr
			if os.path.exists(myFile):
				if (os.path.getsize(myFile)>200000):
					os.rename(myFile, myFile+"_"+time.strftime('_%y-%m-%d_%X'))
			Filehandle = open (myFile, 'a+')
			Filehandle.write (myStr+"\n")  
			Filehandle.close ()
			time.sleep(5)	
		except:
			print "error"