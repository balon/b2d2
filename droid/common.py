#!/usr/bin/env python
'''
	File name: common.py
	Purpose: Shared functions for b2d2
	Authors: TJ Balon, Matt Topor
	Date Modified: 11/26/2017
	Python Version: 3.5
'''
# This code is property of TangoNetworksLLC & Affiliates... 
# All code is subject to the terms and conditioned defined in
# 'LICENSE.txt', which is part of this source code package.
import tarfile
import hashlib
"""Common functions library among both droid and master."""

def tarFile(paths, buildPath):
	"""Creation of tar.gz compression."""
	tar = tarfile.open(buildPath, "w:gz")
	for path in paths:
		tar.add(path)
	tar.close()

def hashFile(path):
	"""Returns hash value."""
	sha1 = hashlib.sha1()

	with open(path, 'rb') as f:
		while True:
			data = f.read(65535)
			if not data:
				break
			sha1.update(data)

	return sha1.hexdigest()