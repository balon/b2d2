'''
	File name: server.py
	Purpose: Server Class for b2bkup
	Authors: TJ Balon, Matt Topor
	Date Modified: 11/26/2017
	Python Version: 3.5
'''
# This code is property of TangoNetworksLLC & Affiliates... 
# All code is subject to the terms and conditioned defined in
# 'LICENSE.txt', which is part of this source code package.
import socket
import sys
import _thread as thread
from common import *

debug = 1

class ServerHandler:
	def __init__(self, port, wl, settings):
		self.settings = settings
		self.wl = wl
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = '0.0.0.0'
		self.port = port

		print(self.host)
		print(self.port)

		if(debug == 1):
			print("Server started")
			print("Waiting for new clients..")

		try:
			self.server.bind((self.host, self.port))
		except:
			print("Error: Could not bind port! Already in use?")
			sys.exit()

		self.server.listen(10)

		self.repeater()
		self.close()

	def repeater(self):
		while True:
			client, addr = self.server.accept()
			tmp = tuple(addr)
			if(tmp[0] in self.wl):
				thread.start_new_thread(self.backupClient,(client, addr))
			else:
				print("A non authorized client attempted to connect!")

	def backupClient(self, client, addr):
		clientIdent = self.read(1024)
		status = "Waiting"
		identPath = str(self.settings["storage"] + "/" + clientIdent.decode("utf-8") )
		
		if not os.path.exists(identPath):
			os.makedirs(identPath)

		client.self.write("[Master] Identity Recieved")
		while status not "[Minion] Complete":
			dirName = self.read(1024)
			buildPath = identPath + str(dirName)

			if not os.path.exists(buildPath)
				os.makedirs(buildPath)

			# still need to recieve big file..
			# then we need to store it
			# hash it
			# take the hash of the client
			# compare 
			# send status OK to move on

		
	def read(self, length=1024)
		return self.server.recv(length)

	def write(self, buff):
		buff = bytes(buff, 'utf-8')
		self.server.send(buff)

	def close(self):
		self.server.close()