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
import tarfile
import sys
import json
import os
import logging
import hashlib
from datetime import datetime
from common import *
from client import ClientHandler

# Global Variable Definition
settings = {}
debug = 0

# Gloal Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('minion.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

def readConfigs(configFile = "minion-config.ini"):
	cfg = configparser.ConfigParser()
	cfg.read(configFile)
	global settings
	global debug

	debug = int(cfg['GENERAL']['DEBUG'])
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

	if(debug == 1):
		logger.info("Configuration loaded successfully, proceeding with settings:")
		for k, v in settings.items():
			logger.info(str(k) + ": " + str(v))
		logger.info("Relaunch with new file to change configuration preferences.")

def FTSU():
	if not os.path.exists(settings["storage"]):
		os.makedirs(settings["storage"])

	# Eventually.. generate certificates for SSL

def tarFile(paths, buildPath):
	tar = tarfile.open(buildPath, "w:gz")
	for path in paths:
		tar.add(path)
	logger.info("Tar Created: " + buildPath)
	tar.close()

def hashFile(path):
	sha1 = hashlib.sha1()

	with open(path, 'rb') as f:
		while True:
			data = f.read(65535)
			if not data:
				break
			sha1.update(data)

	print(sha1.hexdigest())

def main():
	readConfigs()

	if( len(sys.argv) > 1 and sys.argv[1].lower() == "--ftsu"):
		print("Running as FTSU (First Time Set-Up)")
		FTSU()
		print("FTSU ran successfully, re-run without --ftsu parameter.")
		sys.exit()

	with open(settings["backups"]) as backups:
		decoded = json.load(backups)

	try:
		c = ClientHandler(settings["masterAddr"], int(settings["masterPort"]))
	except:
		logger.info("Could not connect to server.. is server running?")
		sys.exit()

	c.sendall(bytes(settings["identity"], 'utf-8'))

	for item in decoded["items"]:
		if not os.path.exists(settings["storage"] + "/" + item["name"]):
			os.makedirs(settings["storage"] + "/" + item["name"])

		cT = datetime.now()
		tStamp = str(cT.year) + "-" + str(cT.month) + "-" + str(cT.day) + "-" \
		+ str(cT.hour) + str(cT.minute)  + str(cT.second)
		buildPath = str(settings["storage"] + "/" + item["name"] \
		+ "/" + tStamp + ".tar.gz")
		
		tarFile(item["paths"], buildPath)
		fileDigest = hashFile(buildPath)

if __name__ == "__main__":
	main()