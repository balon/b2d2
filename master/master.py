#!/usr/bin/env python
'''
	File name: master.py
	Purpose: Master Server for b2d2
	Authors: TJ Balon, Matt Topor
	Date Modified: 11/28/2017
	Python Version: 3.5
'''
# This code is property of TangoNetworksLLC & Affiliates... 
# All code is subject to the terms and conditioned defined in
# 'LICENSE.txt', which is part of this source code package.
import configparser
import sys
import os
from server import ServerHandler
import json

settings = {}					

# -------------------------------------------------------------
# 	 readConfigs -- input: configFile, Load user defined config
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
	settings["b2Bucket"] = cfg['BACKBLAZE']['BUCKET']
	settings["b2Threads"] = cfg['BACKBLAZE']['THREADS']
	settings["whitelist"] = cfg['MASTER']['WHITELIST']
	settings["storage"] = cfg['GENERAL']['LOCALSTORE']

# -------------------------------------------------------------
# 	 FTSU -- input: none, Self explanatory
def FTSU():
	"""Folder creation check for first time setup."""
	if not os.path.exists(settings["storage"]):
		os.makedirs(settings["storage"])

# -------------------------------------------------------------
# 	main -- Call entire program
def main():
	"""Main function call. Set --ftsu argument for first time setup execution. 
	Loading in JSON whitelist configuration. Opens a socket to wait for a Minion connection."""
	readConfigs()									# Read the configs from the user

	if( len(sys.argv) > 1 and sys.argv[1].lower() == "--ftsu"):
		print("Running as FTSU (First Time Set-Up)")
		FTSU()
		print("FTSU ran successfully, re-run without --ftsu parameter.")
		sys.exit()

	with open(settings["whitelist"]) as wl:			# Load the whitelist...
		decoded = json.load(wl)						# Whitelist in json for ease of use
		whitelist = []
		for x in decoded["whitelist"]:
			whitelist.append(x)						# Add each 'Whitelist' host!

	s = ServerHandler(int(settings["serverPort"]), whitelist, settings)

if __name__ == "__main__":
	"""Run main only if directly called."""
	main()


