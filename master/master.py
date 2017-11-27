#!/usr/bin/env python
'''
	File name: master.py
	Purpose: Server binary for b2d2
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
# Debug flag, set to 1 to turn on
debug = 0

def readConfigs(configFile = "master-config.ini"):
	"""Read master-config.ini and parse/assign data from file to 
	dictionary containing all the variables and values."""
	cfg = configparser.ConfigParser()
	cfg.read(configFile)
	global settings
	global debug 

	settings["serverPort"] = cfg['MASTER']['RUN_PORT']
	settings["keepFiles"] = int(cfg['MASTER']['KEEP_FILES'])
	settings["b2Key"] = cfg['BACKBLAZE']['B2KEY']
	settings["b2Auth"] = cfg['BACKBLAZE']['B2AUTH']
	settings["whitelist"] = cfg['MASTER']['WHITELIST']
	settings["storage"] = cfg['GENERAL']['LOCALSTORE']
	debug = int(cfg['GENERAL']['DEBUG'])

def FTSU():
	"""Folder creation check for first time setup."""
	if not os.path.exists(settings["storage"]):
		os.makedirs(settings["storage"])


def main():
	"""Main function call. Set --ftsu argument for first time setup execution. 
	Loading in JSON whitelist configuration. Opens a socket to wait for a Minion connection."""
	cmdLen = len(sys.argv)
	cmdArg = str(sys.argv)
	if(cmdLen > 1 and sys.argv[1].lower() == "--ftsu"):
		print("Running as FTSU (First Time Set-Up)")
		FTSU()
		print("FTSU ran successfully, re-run without --ftsu parameter.")
		sys.exit()

	readConfigs()

	with open(settings["whitelist"]) as wl:
		decoded = json.load(wl)
		whitelist = []
		for x in decoded["whitelist"]:
			whitelist.append(x)

	s = ServerHandler(int(settings["serverPort"]), whitelist, settings)
	s.close()

if __name__ == "__main__":
	"""Run main only if directly called."""
	main()


