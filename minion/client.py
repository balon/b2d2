'''
	File name: client.py
	Purpose: Client Class for b2bkup
	Authors: TJ Balon, Matt Topor
	Date Modified: 11/26/2017
	Python Version: 3.5
'''
# This code is property of TangoNetworksLLC & Affiliates... 
# All code is subject to the terms and conditioned defined in
# 'LICENSE.txt', which is part of this source code package.
import socket

class ClientHandler:
	def __init__(self, ip, port):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect((ip, port))

	def read(self):
		return self.client.recv(1024)

	def sendall(self, buff):
		self.client.sendall(buff)

	def close(self):
		self.client.close()