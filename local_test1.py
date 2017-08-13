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
import re
import threading
#import demjson
global numTrain
# ##########################################################################################
numTrain = 9  # number of train
# ###########################################################################################
__program__   = 'Loco TestSpeedLocal'
__version__   = '0.6'
__date__      = '2012/12/23'
__author__    = 'O Skuybida'
__licence__   = 'Comercial'
__copyright__ = 'Copyright (C) 2012 Oleg Skuibida'

lat = 0 
long = 0
num = 2
myip = '100.100.191.1'



def getLink(myHost):
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('test-agent', 'public', 0), cmdgen.UdpTransportTarget((myHost, 161)),(1,3,6,1,4,1,4458,1000,1,5,9,1,0),(1,3,6,1,4,1,4458,1000,1,1,19,0),(1,3,6,1,4,1,4458,1000,1,5,5,0),)
	myStr = ''
	if errorIndication:
		return(" -1 -1 -1")
	else:
		if errorStatus:
			myStr = errorStatus.prettyPrint()
		else:
			for name, val in varBinds:
				myStr +=' '+val.prettyPrint()
		return(myStr)
	
def getGPS1(myHost):
		data = -1
		errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('test-agent', 'public', 0), cmdgen.UdpTransportTarget((myHost, 161)),(1,3,6,1,4,1,4458,1000,1,5,40,11,0),)
		if errorIndication:
			data = -1
		else:
			if errorStatus:
				data = - 1
			else:
				for name, val in varBinds:
					data = val
					#str = float(val)
					#print str 
		return(data)

def getGPS2(myHost):
		data = -1
		errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('test-agent', 'public', 0), cmdgen.UdpTransportTarget((myHost, 161)),(1,3,6,1,4,1,4458,1000,1,5,40,13,0),)
		if errorIndication:
			data = -1
		else:
			if errorStatus:
				data = - 1
			else:
				for name, val in varBinds:
					data = val
		return(data)
		
def getDist(myHost):
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('test-agent', 'public', 0), cmdgen.UdpTransportTarget((myHost, 161)),(1,3,6,1,4,1,4458,1000,1,5,29,0),)
	myStr = -1
	if errorIndication:
		myStr = -1
	else:
		if errorStatus:
			myStr = -1
		else:
			for name, val in varBinds:
				myStr = val
		return(myStr)

def getAspeed(myHost):
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('test-agent', 'public', 0), cmdgen.UdpTransportTarget((myHost, 161)),(1,3,6,1,4,1,4458,1000,2,2,14,0),)
	myStr = -1
	if errorIndication:
		myStr = -1
	else:
		if errorStatus:
			myStr = -1
		else:
			for name, val in varBinds:
				myStr = val
	return(myStr)

def speedDown(myHost):
	spD2 = 0
	#errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('test-agent', 'NSMX-RO', 1), cmdgen.UdpTransportTarget((myHost, 161)),(1,3,6,1,2,1,2,2,1,10,1),)
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('test-agent', 'public', 0), cmdgen.UdpTransportTarget((myHost, 161)),(1,3,6,1,2,1,2,2,1,10,1),)
	if errorIndication:
		return(0)
	else:
		if errorStatus:
			return(0)
		else:
			for name, val in varBinds:
				spD2= val
	try:
		return(int(spD2)*8)
	except:
		return(0)

def speedUp(myHost):
	spD2 = 0
	#errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('test-agent', 'NSMX-RO', 1), cmdgen.UdpTransportTarget((myHost, 161)),(1,3,6,1,2,1,2,2,1,16,1),)
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('test-agent', 'public', 0), cmdgen.UdpTransportTarget((myHost, 161)),(1,3,6,1,2,1,2,2,1,16,1),)
	if errorIndication:
		return(0)
	else:
		if errorStatus:
			return(0)
		else:
			for name, val in varBinds:
				spD2= val
	try:
		return(int(spD2)*8)
	except:
		return(0)

def pingNode(ip):
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

def goK(k):
		global active
		global Filehandle
		global TakeLog
		global curData
		global curData2
		global nodeListCount
		global cData # количество данных на графике 
		#global nodeODU
		global nodeList
		dt = time.strftime('%y.%m.%d %X')
		sk=str(k)
		myStr = ''
		nodeODU= "100.200.200."+sk# адрес ODU
		nodeGPS = "100.200.200.2"+sk # адрес GPS
		#nodeGPS = "100.100.19"+sk+".4"
		node = "100.254.254.254" # ping host
		myFile = "/home/drive/data/__"+sk
		if os.path.exists(myFile):
			if (os.path.getsize(myFile)>200000):
				os.rename(myFile, myFile+"_"+time.strftime('_%y-%m-%d_%X'))
		tm1 = time.strftime('%y-%m-%d')
		tm2 = time.strftime('%X')
		try:
					d = pingNode(node)
					GPSln = getGPS1(nodeGPS)
					GPSlt = getGPS2(nodeGPS)
					#print g1
					#print "d2="+str(d2)+" k="+sk+" Ln="+GPSln
					sd1 = speedDown(nodeODU)
					t1 = time.time()
					time.sleep(1)
					sd2 = speedDown(nodeODU)
					t = (time.time() - t1)*1000
					sDown = int((sd2 - sd1)/t)
					#print "sd="+sd+" dd=" + nodeListCount[k-1][1]
					su1 = speedUp(nodeODU)
					t2 = time.time()
					time.sleep(1)
					su2 = speedUp(nodeODU)
					t = (time.time() - t2)*1000
					sUp = int((su2- su1)/t)
					sA= getAspeed(nodeODU)/1000
					sN = "N"
					sN0 = getLink(nodeODU)
					sN3 = sN0.split(" ")
					if (len(sN3)>2):
						sN1 = sN3[2].split("-")
						if (len(sN1)>3):
							sN=sN1[2]+"-"+sN1[3]+"-"+sN1[4]+"-"+sN1[5]
					#print sN0+"=="+sN+"=="+sN3[2]
					myStr = tm1+' '+tm2+' '+str(GPSln)+' '+str(GPSlt)+' '+str(d)+sN0+' '+str(sDown)+' '+str(sUp)+' '+str(sA)
					#curData[k-1].insert(0,[k, sN, tm2, str(GPSln), str(GPSlt), str(sDown), str(sUp), str(sA)])
					
					print sk+' '+myStr
					Filehandle = open (myFile, 'a')
					Filehandle.write (myStr+"\n")    
					Filehandle.close ()
		except KeyboardInterrupt:
				#print "Ctr-C is Ok"				
				active = 0
				Filehandle = open (TakeLog, 'a')
				Filehandle.write ("Keyboard exception")
				Filehandle.close ()
				sys.exit(0)

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
    # version control
    global Filehandle
    global TakeLog
    global curData
    #global curData2
    #global myFileJson
    #global cData
    global numTrains
    global nodeList
    global train
    global nodeListCount
   # nodeList = ['192.168.200.1','192.168.200.2','192.168.200.3','192.168.200.4','192.168.200.5','192.168.200.6','192.168.200.7','1.3.0.1','192.168.200.173','192.168.200.170']
    nodeList = ['100.200.200.1','100.200.200.2','100.200.200.3','100.200.200.4','100.200.200.5','100.200.200.6','100.200.200.7','100.200.200.8','100.200.200.9','100.200.200.10']
    numTrains = 10
    monTime = 8 # час    
    sec = 60 # time in sec between request new data
    #cData = monTime *60*60/sec
    myFileJson =  "trains.json"
    curData = [0 for col in range(numTrains)]
    startGPSLn = 50.435648
    startGPSLt = 30.664955
    tm1 = time.strftime('%y-%m-%d')
    tm2 = time.strftime('%X')
    l=0
    nodeListCount = [0 for col in range(numTrains)]
    for x in xrange(0, numTrains):
	    l+=1
	    #print  "curJsonData"
	    d = 0
	    time1 = int(time.time())
	    u =0
	    time2= int(time.time())
	    nodeListCount[x]=[0 for col in range(1)]
	    nodeListCount[x] = [d,time1,u,time2]
	    curData[x]=[0 for col in range(1)]
	   # print nodeListCount[x]
	    for y in xrange(0,1):
		curData[x][y]=[x+1, 0, tm2, str(startGPSLn+0.001*l), str(startGPSLt+0.01*l), -1, -1, -1]
    TakeLog = "TakeSpeed.log"
    #print curData
    version = string.split(string.split(sys.version)[0][:3], ".")
    #k = 
    if map(int, version) < [2, 3]:
        _error("You need Python ver 2.3 or higher to run!")
    #global active
    #active = 1
   # while (active):
	#try:
	#	k=1
	#	while (k<=numTrains):
			#print str(k)+"\n"

	#		k+=1
    goK(numTrain)
   # f = open (myFileJson, 'w')
    #f.write("jsonstr="+demjson.encode(curData, compactly=True)+";") 
    #f.close ()
   # time.sleep(sec)
   
