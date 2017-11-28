'''
	File name: server.py
	Purpose: Server Class of b2d2
	Authors: TJ Balon, Matt Topor
	Date Modified: 11/28/2017
	Python Version: 3.5
'''
# This code is property of TangoNetworksLLC & Affiliates... 
# All code is subject to the terms and conditioned defined in
# 'LICENSE.txt', which is part of this source code package.
import socket
import sys
import os
import _thread as thread
from common import *
from clientoffload import *
from subprocess import call

class ServerHandler:
	"""Handles server socket connections. Verifies clients, and reads backup data."""

	# -------------------------------------------------------------
	# 	 ServerHandler -- input: port, whitelist, settings
	def __init__(self, port, wl, settings):
		"""Returns host, port variables. Attempts to bind host and port."""
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = '0.0.0.0'				# bind to all interfaces
		self.settings = settings			# pass in user defined settings
		self.wl = wl 						# load whitelist to prevent bad-users

		try:
			self.server.bind((self.host, port))
		except:
			print("Error: Could not bind port! Already in use?")
			sys.exit()

		self.server.listen(10) 					
		self.repeater()						# spawn repeater to poll for clients

	# -------------------------------------------------------------
	# 	 delete -- delete object, close dying connections
	def __del__(self):	
		self.server.close()					# during death, close server socket

	# -------------------------------------------------------------
	# 	 repeater -- input: none, polling loop for server
	def repeater(self):
		"""Starts new thread for every client accepted to server."""
		while True:
			client, addr = self.server.accept()

			tmp = tuple(addr)
			if(tmp[0] in self.wl):
				# new thread to handle client a-sync. No blocking allowed!
				thread.start_new_thread(self.backupClient,(client, addr))
			else:
				print("A non authorized client attempted to connect!")
				print("Unauthorized IP: " + str(addr))

	# -------------------------------------------------------------
	# 	 backupClient -- input: client, address, backup routine
	def backupClient(self, client, addr):
		"""Initialization for every client that connects to server."""
		client = ClientHandler(client, addr)
		clientIdent = client.read(1024)				# recieve: identity of client

		identPath = str(self.settings["storage"] + "/" + clientIdent.decode("utf-8") )
		
		if not os.path.exists(identPath):
			os.makedirs(identPath) 			# each server has identity, make a localpath

		status = "Not finished"
		client.writestr("[Master] Identity Recieved")
		while(status != "[Droid] All transfers complete!"):
			bkupDir = client.read(1024)
			baseDir = str(identPath + "/" + bkupDir.decode("utf-8"))	# get backup identity

			if not os.path.exists(baseDir):
				os.makedirs(baseDir)		# does the path exist? make it if not

			client.writestr(("[Master] Backup dir name recieved: " + str(bkupDir)))

			# we need to build a bucket path for correct handling
			bucketSub = str( clientIdent.decode("utf-8") + "/" + bkupDir.decode("utf-8"))

			bkupName = client.read(1024) 	# name of backup
			buildPath = str(baseDir + "/" + bkupName.decode("utf-8"))
			bucketFN = str(bucketSub + "/" + bkupName.decode("utf-8"))

			client.writestr("[Master] Backup name recieved")

			bkupSize = client.read(1024) 			# get the size of backup for transfer
			bkupSize = bkupSize.decode("utf-8")

			client.writestr("[Master] Backup size recieved")

			fptr = open(str(buildPath), 'wb')
			buff = client.read(1024)				# read the first byte
			total = len(buff)						# create a total to compare to inital size

			while True:
				fptr.write(buff)					# write to file
				
				if(str(total) != str(bkupSize)):	
					buff = client.read(1024)
					total = total + len(buff)
				else:								# we've recieved file, get out
					break
			fptr.close()							# close the stream

			client.writestr("[Master] File recieved")
			clientHash = client.read(1024) 			# get client hash
			fileDigest = hashFile(buildPath)		# create hash of transfered file
			clientHash = clientHash.decode("utf-8")

			if(clientHash == fileDigest):			# are they the same? validate!
				client.writestr("[Master] Hash matches!")
			else:
				client.writestr("[Master] Hash mismatch!")

			print("Pushing to BackBlaze...")
			# Make calls to auth to backblaze, and upload the file
			call(["b2", "authorize-account", self.settings["b2Key"], self.settings["b2Auth"]])
			call(["b2", "upload-file", "--threads", self.settings["b2Threads"], self.settings["b2Bucket"], buildPath, bucketFN ])

			files = os.listdir(baseDir) 			# get files in dir
			numFiles = len(files)					# count them!

			if(numFiles > self.settings["keepFiles"]):	# are there more than user wants?
				delFile = min(os.listdir(baseDir), key=lambda p: os.path.getctime(os.path.join(baseDir, p)))
				os.remove(baseDir + "/" + delFile) 	# delete!
			else:
				print("There are less files than the keep files setting, skipping cleaning up.. ")

			status = client.read(1024)				# get status.. is client finished?
			status = status.decode("utf-8")
			print(status)

			client.writestr("[Master] STATUS OK") 	# send a final OK before next transfer

		del client

	# -------------------------------------------------------------
	# 	 close -- input: none, close socket
	def close(self):
		"""Closes server socket connection."""
		self.server.close()