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
from client import ClientHandler
import json

# Global Variable Definition
settings = {}
debug = 0

def readConfigs(configFile = "minion-config.ini"):
	cfg = configparser.ConfigParser()
	cfg.read(configFile)
	global settings
	global debug

	debug = int(cfg['GENERAL']['DEBUG'])
	settings["runMode"] = (cfg['MINION']['RUNMODE']).lower()
	settings["identity"] = cfg['MINION']['IDENTIFIER']
	settings["backups"] = cfg['MINION']['BACKUPFILE']

	if(settings["runMode"] == "remote"):
		settings["masterAddr"] = cfg['REMOTE']['SERVERADDR']
		settings["masterPort"] = cfg['REMOTE']['SERVERPORT']
	elif(settings["runMode"] == "standalone"):
		settings["b2Key"] = cfg['STANDALONE']['B2KEY']
		settings["b2Auth"]  = cfg['STANDALONE']['B2AUTH'] 
		settings["keepFiles"] = int(cfg['STANDALONE']['KEEP_FILES'])	
	else:
		print("Error! Incorrect run-mode, expecting (remote/standalone).")
		print("Recieved: " + settings["runMode"])
		sys.exit()

	if(debug == 1):
		print("Configuration loaded successfully, proceeding with settings:")
		for k, v in settings.items():
			print(str(k) + ": " + str(v))
		print("Relaunch with new file to change configuration preferences.")

def FTSU():
	# Make initial folder
	# Eventually.. generate certificates for SSL
	pass

def main():
	cmdLen = len(sys.argv)
	cmdArg = str(sys.argv)
	if(cmdLen > 1 and sys.argv[1].lower() == "--ftsu"):
		print("Running as FTSU (First Time Set-Up)")
		FTSU()
		print("FTSU ran successfully, re-run without --ftsu parameter.")
		sys.exit()

	readConfigs()

	with open(settings["backups"]) as backups:
		decoded = json.load(backups)
		for x in decoded["items"]:
			print(x["name"])



	#c = ClientHandler(settings["masterAddr"], int(settings["masterPort"]))


if __name__ == "__main__":
	main()