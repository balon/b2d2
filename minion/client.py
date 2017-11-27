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
	"""Handles client socket establishment.

	Attributes:
		client: A socket containing ip and port."""
	def __init__(self, ip, port):
		"""Return a client socket connection with ip and port."""
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect((ip, port))

	def read(self):
		"""Return recieved data."""
		return self.client.recv(1024)

	def sendall(self, buff):
		"""Sends all data from client."""
		buff = bytes(buff, 'utf-8')
		self.client.sendall(buff)

	def close(self):
		"""Closes of client socket connection."""
		self.client.close()