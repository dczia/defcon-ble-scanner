#!v/bin/python
import os
import sys
import time
from datetime import datetime
from bluepy.btle import Scanner
from termcolor import  colored

"""
DC Zia 2017 BLE Scanner (Defcon 25)
https://github.com/dczia/dc25-ble-scanner
http://dczia.net/
https://twitter.com/DCZia505
"""

# Initialize the BLE scanner
scanner = Scanner()

# List of manufacturer ID's considered part of the DCZia group.
US = ['5050']

class Neighbor():
	"""
	Basic field accessor class for scan data we care about.
	"""
	def __init__(self, appearance, manufacturer, localName, dB):
		self.appearance = appearance
		self.manufacturer = manufacturer
		self.localName = localName
		self.dB = dB

	def __lt__(self, other):
		# Sort by signal strength
		return self.dB < other.dB

def getNeighbors():
	"""
	Scans for 2 seconds and returns list of nearby BLE devices with the 0xDC19
	(Defcon 25 Appearance).
	"""
	devices = scanner.scan(2)
	neighbors = []
	for dev in devices:
		appearance = None
		manufacturer = None
		localName = None
		for (adtype, desc, value) in dev.getScanData():
			if desc.lower() == "appearance":
				appearance = value.lower()
			if desc.lower() == "manufacturer":
				manufacturer = value[0:4]
			if desc.lower() == "complete local name":
				localName = value

		if appearance == "dc19" and manufacturer is not None:
			neighbors.append(Neighbor(appearance, manufacturer, localName, dev.rssi))
	scanner.clear()
	return neighbors

def getus(neighbors):
	""" Return list of devices that are considered "us" (part of DCZia)"""
	return [n for n in neighbors if n.manufacturer in US]

def getthem(neighbors):
	""" Return list of all other devices not considered "us" (part of DCZia)"""
	return [n for n in neighbors if n.manufacturer not in US]

def savetofile(neighbors):
	"""
	Save the discovered BLE devices to a file including the current timestamp.
	"""
	f = open('contacts.txt', 'a')
	f.write("%s\n" % datetime.now())
	for n in neighbors:
		f.write("%s %s %sdB\n" % (n.localName, n.manufacturer, n.dB))
	f.close()

if __name__=='__main__':
	try:
		while True:
			# Find all the nearby BLE devices, sort them, and save them to file.
			neighbors = getNeighbors()
			neighbors.sort()
			os.system('clear')
			savetofile(neighbors)

			# Separate out out nearby BLE devices into list of "us" vs "them".
			us = getus(neighbors)
			them = getthem(neighbors)

			# Print out pretty colors.
			print(colored("[ DCZia / 0x5050 ]", "green", attrs=["bold"]))
			print(colored("========================================", "green", attrs=["bold"]))
			if len(us) == 0:
				print(colored("--", "green"))
			for n in us:
				print(colored("%s (%sdB)" % (n.localName, n.dB), "green"))

			print(colored("[     0xDC19     ]", "cyan", attrs=["bold"]))
			print(colored("========================================", "cyan", attrs=["bold"]))
			if len(them) == 0:
				print(colored("--", "cyan"))
			for n in them:
				print(colored("%s (0x%s, %sdB)" % (n.localName, n.manufacturer, n.dB), "cyan"))
	except KeyboardInterrupt:
		# kbye
		print("Exiting...")
