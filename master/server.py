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
import threading as thread

debug = 1

class ServerHandler:
	def __init__(self, port):
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
		except socket.error as msg:
			print("Error attempting to bind port. Err: " + str(msg[0]) + ' Message ' + str(msg[1]))
			sys.exit()

		self.server.listen(10)

		while True:
			client, addr = self.server.accept()
			print(client)
			print(addr)
			
	def backup(self):
		pass

	def send(self, buff):
		self.server.send(buff)

	def close(self):
		self.server.close()