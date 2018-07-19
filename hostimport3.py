#!/usr/bin/env python3.6

#author: Brijan Shrestha

from pyzabbix import ZabbixAPI
from pathlib import Path
import csv
import sys
import os
import datetime
from progressbar import ProgressBar, Percentage, ETA, ReverseBar, RotatingMarker, Timer

##Logging
def log_write(txt):
	print(txt)
	openLog = open(logfile, 'w')
	openLog.write(txt)
	openLog.close()
def log_append(txt):
	print(txt)
	openLog = open(logfile, 'w')
	openLog.write(txt)
	openLog.close()
	
dt=str(datetime.datetime.now())
logfile = './hostimport.log'
newname = 'logfile.' + dt
if os.path.exists('logfile') == True:
	os.rename(logfile, newname)
	txt='Import initiated..\nChecking CSV file...'
	log_write(txt)
else:
	txt='Import initiated..\nChecking CSV file...'
	log_write(txt)

##Check for csv file imput##
filename=os.path.basename(__file__)
try:
	csvfile=sys.argv[1]
except:
	print(" Usage:", filename, "/path/to/csv/file.csv")
	print("")
	txt='Location of csv file not provided!'
	log_append(txt)	
	sys.exit(1)

#if os.path.exists('csvfile') == True:
#	txt='Reading {} to load branches...'.format(csvfile)
#	log_append(txt)
#else:
#	txt = 'Cannot locate the file {}'.format(csvfile)
#	log_append(txt)
#`	sys.exit(1)

##Authenticate with server##
zapi = ZabbixAPI("http://localhost/zabbix")
zapi.login(user="Admin", password="password")

##Prompt for user group###
grpname = []
grpid = []
print('name',':','groupid')
for h in zapi.hostgroup.get():
	print(h['name'],':',h['groupid'])
	grpname.append(h['name'])
	grpid.append(h['groupid'])
#print(grpname)
#print(grpid)
val=input("Input the groupid:")
try:
	gid = int(val)
	if gid in grpid:
		print('Adding the hosts in csv file to groupid grpid.'())
except:
	print("Enter a valid groupid!")
	sys.exit(1)

##Read csv file
arq = csv.reader(open(csvfile))
lines = sum(1 for line in arq)
f = csv.reader(open(csvfile), delimiter=',')
bar = ProgressBar(maxval=lines,widgets=[Percentage(), ReverseBar(), ETA(), RotatingMarker(), Timer()]).start()
i = 0

##API call##
for [bcode,location,bsname,ip1,vendor] in f:
#    print(bcode + ' ' + location + ' ' + bsname, ip1, ip2)
     hostadd = zapi.host.create(
         host= (bcode + ' ' + location + ' ' +bsname + vendor),
	 name= (bsname +' ' + vendor),
         status= 0,
         interfaces=[{
             "type": 1,
             "main": "1",
             "useip": 1,
             "ip": ip1,
             "dns": "",
             "port": 10050},
	     {
             "type": 2,
             "main": "1",
             "useip": 1,
             "ip": ip1,
             "dns": "",
             "port": 161
         }],
         groups=[{
             "groupid": gid
         }],
         templates=[{
            "templateid": 10186
         }]
     )
 
 
     i += 1
     bar.update(i)

bar.finish
print(" ")
