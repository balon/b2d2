#!/usr/bin/env python
'''
	File name: master.py
	Purpose: Server binary for b2bkup
	Authors: TJ Balon, Matt Topor
	Date Modified: 11/26/2017
	Python Version: 3.5
'''
# This code is property of TangoNetworksLLC & Affiliates... 
# All code is subject to the terms and conditioned defined in
# 'LICENSE.txt', which is part of this source code package.
import configparser
import sys
from server import ServerHandler
import json

settings = {}
debug = 0

def readConfigs(configFile = "master-config.ini"):
	cfg = configparser.ConfigParser()
	cfg.read(configFile)
	global settings
	global debug 

	settings["serverPort"] = cfg['MASTER']['RUN_PORT']
	settings["keepFiles"] = int(cfg['MASTER']['KEEP_FILES'])
	settings["b2Key"] = cfg['BACKBLAZE']['B2KEY']
	settings["b2Auth"] = cfg['BACKBLAZE']['B2AUTH']
	settings["whitelist"] = cfg['MASTER']['WHITELIST']
	debug = int(cfg['GENERAL']['DEBUG'])

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

	with open(settings["whitelists"]) as wl:
		decoded = json.load(wl)
		for x in decoded["whitelist"]:
			print(x)



	#s = ServerHandler(int(settings["serverPort"]))


if __name__ == "__main__":
	main()


