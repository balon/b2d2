'''
	File name: server.py
	Purpose: Server Class for b2d2
	Authors: TJ Balon, Matt Topor
	Date Modified: 11/26/2017
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

class ServerHandler:
	"""Handles server socket connections. Verifies clients, and reads backup data."""
	def __init__(self, port, wl, settings):
		"""Returns host, port variables. Attempts to bind host and port."""
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = '0.0.0.0'
		self.settings = settings
		self.wl = wl

		try:
			self.server.bind((self.host, port))
		except:
			print("Error: Could not bind port! Already in use?")
			sys.exit()

		self.server.listen(10)
		self.repeater()

	def repeater(self):
		"""Starts new thread for every client accepted to server."""
		while True:
			client, addr = self.server.accept()

			tmp = tuple(addr)
			if(tmp[0] in self.wl):
				thread.start_new_thread(self.backupClient,(client, addr))
			else:
				print("A non authorized client attempted to connect!")

	def backupClient(self, client, addr):
		"""Initialization for every client that connects to server."""
		client = ClientHandler(client, addr)
		clientIdent = client.read(1024)

		identPath = str(self.settings["storage"] + "/" + clientIdent.decode("utf-8") )
		
		if not os.path.exists(identPath):
			os.makedirs(identPath) 

		complete = "Not finished"
		client.writestr("[Master] Identity Recieved")
		while(complete != "Success [OK]"):
			bkupDir = client.read(1024)
			baseDir = str(identPath + "/" + bkupDir.decode("utf-8"))

			if not os.path.exists(baseDir):
				os.makedirs(baseDir)

			client.writestr(("[Master] Backup dir name recieved: " + str(bkupDir)))

			bkupName = client.read(1024)
			buildPath = str(baseDir + "/" + bkupName.decode("utf-8"))
			
			client.writestr("[Master] Backup name recieved")

			bkupSize = str(client.read(1024))
			print("Expecting..." + str(bkupSize))

			client.writestr("[Master] Backup size recieved")

			fptr = open(str(buildPath), 'wb')
			buff = client.read(1024)
			total = len(buff)

			while True:
				fptr.write(buff)

				print(total)
				print(bkupSize)
				
				if (str(total) != str(bkupSize)):
					print("frank fuck u for python and snake")
					buff = client.read(1024)
					total = total + len(buff)
				else:
					break
			print("YOU FUCKING GOT HERE MATE")
			fptr.close()

			client.writestr("[Master] File recieved")
			clientHash = client.read(1024)
			fileDigest = hashFile(buildPath)

			if(clientHash == fileDigest):
				client.writestr("[Master] Hash matches!")
			else:
				client.writestr("[Master] Hash mismatch!")

		del client

	def close(self):
		"""Closes server socket connection."""
		self.server.close()