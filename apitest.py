#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from pyzabbix import ZabbixAPI
import csv
import sys
import os

server = "http://127.0.0.1/zabbix" 
username = "Admin" 
password = "password"

zapi = ZabbixAPI(server = server)

zapi.login(username, password)

#var= zapi.trigger.get({"expandExpression": "extend", "triggerids": range(0, 100)})
#print(var)

from pprint import pprint

#print "Connected to Zabbix API Version %s" % zapi.appinfo.version()

#for h in zapi.template.get(output=["name","templateids"]):
#    pprint(h)

grpname = []
print('name',':','groupid')
for h in zapi.hostgroup.get():
	print(h['name'])
	print(h['name'],':',h['groupid'])
	grpname.append(h['name'])
print(grpname)
        #grplist = (h['groupid'])
#val=input("Input the groupid:")
#try:
#	grpid = int(val)
#	if grpid in grplist:
#		print('Adding the hosts in csv file to groupid grpid.'())
#except:
#        print("Enter a valid groupid!")

#for h in zapi.host.get(filter={"host":"Zabbix server"}):
#    pprint(h)

#for h in zapi.host.get(filter={"host":"test"}):
#    pprint(h)
