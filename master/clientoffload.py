'''
	File name: clientoffload.py
	Purpose: ClientHandler offload from server
	Authors: TJ Balon, Matt Topor
	Date Modified: 11/28/2017
	Python Version: 3.5
'''
# This code is property of TangoNetworksLLC & Affiliates... 
# All code is subject to the terms and conditioned defined in
# 'LICENSE.txt', which is part of this source code package.
import socket

class ClientHandler:
	"""Handles the client's read/write/close functions."""

	# -------------------------------------------------------------
	# 	 ClientHandler -- input: client, addr, establish new client
	def __init__(self, client, addr):
		self.client = client
		self.addr = addr

	# -------------------------------------------------------------
	# 	 del -- input: none, destroy client, close socket
	def __del__(self):
		print("Deleting client: " + str(self.addr))
		self.client.close()

	# -------------------------------------------------------------
	# 	 read -- input: length, read x-size from socket
	def read(self, length=1024):
		"""Return recieved data, only expecting Status Msgs."""
		return self.client.recv(length)

	# -------------------------------------------------------------
	# 	 writestr -- input: buff, byte encode buffer to socket
	def writestr(self, buff):
		buff = bytes(buff, 'utf-8')
		self.client.sendall(buff)

	# -------------------------------------------------------------
	# 	 writebytes -- input: buff, write byte stream to socket
	def writebytes(self, buff):
		"""Sends all data from client."""
		self.client.sendall(buff)

	# -------------------------------------------------------------
	# 	 close -- input: none, close socket
	def close(self):
		"""Closes of client socket connection."""
		self.client.close()