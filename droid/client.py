'''
	File name: client.py
	Purpose: Client socket handling for b2d2
	Authors: TJ Balon, Matt Topor
	Date Modified: 11/26/2017
	Python Version: 3.5
'''
# This code is property of TangoNetworksLLC & Affiliates... 
# All code is subject to the terms and conditioned defined in
# 'LICENSE.txt', which is part of this source code package.
import socket

class SpawnClient:
	"""Handles client socket establishment."""
	def __init__(self, ip, port):
		"""Return a client socket connection with ip and port."""
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect((ip, port))

	def read(self, length=1024):
		"""Return recieved data, only expecting Status Msgs."""
		return self.client.recv(length)

	def sendstr(self, buff):
		buff = bytes(buff, 'utf-8')
		self.client.sendall(buff)

	def sendbytes(self, buff):
		"""Sends all data from client."""
		self.client.sendall(buff)

	def close(self):
		"""Closes of client socket connection."""
		self.client.close()