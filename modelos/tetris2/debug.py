'''
debug.py

contains the debugging and logging functions and variables
'''
import sys

# ---------------------- #
debug = False
logdata = True
playsounds = True
	
# ---------------------- #

class dummylog(object):
	def write(self, string): pass

if debug and logdata:
	log = open('log.txt', 'w')
else:
	log = open('log.txt', 'w')