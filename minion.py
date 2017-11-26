#!/usr/bin/env python
'''
	File name: minion.py
	Purpose: Client binary for b2bkup
	Authors: TJ Balon, Matt Topor
	Date Modified: 11/26/2017
	Python Version: 3.5
'''
# This code is property of TangoNetworksLLC & Affiliates... 
# All code is subject to the terms and conditioned defined in
# 'LICENSE.txt', which is part of this source code package.
import configparser
import sys

# Global Variable Definition
runMode = None
identity = None
b2Key = None
b2Auth = None
keepFiles = None
masterAddr = None
masterPort = None

def readConfigs(configFile = "minion-config.ini"):
	cfg = configparser.ConfigParser()
	cfg.read(configFile)

	global runMode
	global identity
	runMode = cfg['MINION']['RUNMODE']
	runMode = runMode.lower()
	identitiy = cfg['MINION']['IDENTIFIER']

	if(runMode == "remote"):
		global masterAddr
		global masterPort 
		masterAddr = cfg['REMOTE']['SERVERADDR']
		masterPort = cfg['REMOTE']['SERVERPORT']
	elif(runMode == "standalone"):
		global b2Key
		global b2Auth 
		global keepFiles
		b2Key = cfg['STANDALONE']['B2KEY']
		b2Auth = cfg['STANDALONE']['B2AUTH'] 
		keepFiles = int(cfg['STANDALONE']['KEEP_FILES'])	
	else:
		print("Error! Incorrect run-mode, expecting (remote/standalone).")
		print("Recieved: " + runMode)
		sys.exit()


readConfigs()