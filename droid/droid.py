#!/usr/bin/env python
'''
	File name: droid.py
	Purpose: Client socket for b2d2
	Authors: TJ Balon, Matt Topor
	Date Modified: 11/28/2017
	Python Version: 3.5
'''
# This code is property of TangoNetworksLLC & Affiliates... 
# All code is subject to the terms and conditioned defined in
# 'LICENSE.txt', which is part of this source code package.
import configparser
import sys
import json
import os
import logging
from datetime import datetime
from common import *
from client import SpawnClient

# Global Variable Definition
settings = {}

# Gloal Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('droid.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

# -------------------------------------------------------------
# 	 readConfigs -- input: configFile, Load user defined config
def readConfigs(configFile = "droid-config.ini"):
	"""Read configuration file and parse user defined options from file into
	settings dictionary. Settings will dictate run options during execution. """
	cfg = configparser.ConfigParser()
	cfg.read(configFile)
	global settings

	settings["runMode"] = (cfg['MINION']['RUNMODE']).lower()
	settings["identity"] = cfg['MINION']['IDENTIFIER']

	settings["backups"] = cfg['MINION']['BACKUPFILE']
	settings["storage"] = cfg['GENERAL']['LOCALSTORE']

	if(settings["runMode"] == "remote"):
		settings["masterAddr"] = cfg['REMOTE']['SERVERADDR']
		settings["masterPort"] = cfg['REMOTE']['SERVERPORT']
	elif(settings["runMode"] == "standalone"):
		settings["b2Key"] = cfg['STANDALONE']['B2KEY']
		settings["b2Auth"]  = cfg['STANDALONE']['B2AUTH'] 
		settings["keepFiles"] = int(cfg['STANDALONE']['KEEP_FILES'])	
	else:
		logger.info("Error! Incorrect run-mode, expecting (remote/standalone).")
		logger.info("Recieved: " + settings["runMode"])
		sys.exit()

	logger.info("Configuration loaded successfully, proceeding with settings:")
	for k, v in settings.items():
		logger.info(str(k) + ": " + str(v))
	logger.info("Edit settings and relaunch for changes.")

# -------------------------------------------------------------
# 	 FTSU -- input: none, Self explanatory
def FTSU():
	"""Folder creation check for first time setup."""
	if not os.path.exists(settings["storage"]):
		os.makedirs(settings["storage"])

# -------------------------------------------------------------
# 	main -- Call entire program
def main():
	"""Main function call. First time setup execution. Loading in JSON backup configuration.
	Opens a socket to connect to the Master. Compresses the data, and sends it all to master."""
	readConfigs()									# Read the configs from the user

	if( len(sys.argv) > 1 and sys.argv[1].lower() == "--ftsu"):
		print("Running as FTSU (First Time Set-Up)")
		FTSU()
		print("FTSU ran successfully, re-run without --ftsu parameter.")
		sys.exit()

	with open(settings["backups"]) as backups:
		decoded = json.load(backups)			# load the files to backup

	try:
		c = SpawnClient(settings["masterAddr"], int(settings["masterPort"]))
	except:
		logger.info("Could not connect to server.. is server running?")
		sys.exit()

	c.sendstr(settings["identity"])				# we must identify to server
	srvRes = c.read(1024)						# confirm server got it
	print(srvRes)

	count = 0

	for item in decoded["items"]:
		if not os.path.exists(settings["storage"] + "/" + item["name"]):
			os.makedirs(settings["storage"] + "/" + item["name"])

		cT = datetime.now()						# get current
		bkupName = str(cT.year) + "-" + str(cT.month) + "-" + str(cT.day) + "-" \
		+ str(cT.hour) + str(cT.minute)  + str(cT.second) + ".tar.gz"
		buildPath = str(settings["storage"] + "/" + item["name"] \
		+ "/" + bkupName)						# buildpath will be tar location
		
		tarFile(item["paths"], buildPath)		# create a tar of a folder
		fileDigest = hashFile(buildPath)		# get a hash of the file for validation
		print(fileDigest)

		c.sendstr(item["name"])					# send name of backup identification
		srvRes = c.read(1024) 					
		print(srvRes)

		c.sendstr(bkupName)						# send name of backup file name
		srvRes = c.read(1024)
		print(srvRes)

		bkupSize = str(os.path.getsize(buildPath)) 
		c.sendstr(bkupSize)						# send the file size of backup file
		srvRes = c.read(1024)
		print(srvRes)

		fptr= open(buildPath, 'rb')				# open a file stream to read
		buff = fptr.read(1024)					# get first bit of data to transfer

		while(buff):
			c.sendbytes(buff)					# send data
			buff = fptr.read(1024)				# load more of buffer, until EOF
		fptr.close()

		srvRes = c.read(1024)					
		print(srvRes)

		c.sendstr(fileDigest)					# send hash for validation
		srvRes = c.read(1024)					# was it valid?
		print(srvRes)

		os.remove(buildPath)					# clean up our temp file!
		if(item == decoded["items"][-1]):		
			break								# end of data? break!
		else:
			c.sendstr("[Droid] I still have data!")
			srvRes = c.read(1024)
			print(srvRes)

	c.sendstr("[Droid] All transfers complete!")
	srvRes = c.read(1024)
	print(srvRes)
	c.close()									# close client socket

if __name__ == "__main__":
	"""Run main only if directly called."""
	main()