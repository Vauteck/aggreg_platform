#! /usr/bin/python
# -*- coding: utf-8 -*-

# import python libraries
import re
import time

# import aggregation-platform's libraries
import globals
import utils

# testNetworkAliasesList : testNetworkAlias, macAddress, ipNetwork, ipAddress, networkMask, broadcastAddress
testNetworkAliasesList = [
	['eth1:100', '00:14:d1:23:30:ea', '172.16.100.0', '172.16.100.1', '255.255.255.0', '172.16.100.255'],
	['eth1:110', '00:14:d1:23:30:ea', '172.16.110.0', '172.16.110.1', '255.255.255.0', '172.16.110.255'],
	['eth1:111', '00:14:d1:23:30:ea', '172.16.111.0', '172.16.111.1', '255.255.255.0', '172.16.111.255'],
	['eth1:120', '00:14:d1:23:30:ea', '172.16.120.0', '172.16.120.1', '255.255.255.0', '172.16.120.255'],
	['eth1:121', '00:14:d1:23:30:ea', '172.16.121.0', '172.16.121.1', '255.255.255.0', '172.16.121.255'],
	['eth1:122', '00:14:d1:23:30:ea', '172.16.122.0', '172.16.122.1', '255.255.255.0', '172.16.122.255'],
	['eth1:200', '00:14:d1:23:30:ea', '172.16.200.0', '172.16.200.1', '255.255.255.0', '172.16.200.255']
]
#['eth1:12', '172.16.110.1', '255.255.255.0', '172.16.110.255'],
#['vboxnet0', '192.168.56.1', '255.255.255.0', '192.168.56.255'],
#['vboxnet1', '192.168.57.1', '255.255.255.0', '192.168.57.255'],
#['vboxnet2', '192.168.58.1', '255.255.255.0', '192.168.58.255'],
#['vboxnet3', '192.168.59.1', '255.255.255.0', '192.168.59.255'],

# you have to customize the file /etc/udev/rules.d/70-persistent-net.rules, to match the following list (interfaces names HAVE TO match)
# usbEthAdaptersInterfacesListForDmngEthAdapter : networkInterface, macAddress, ipNetwork, ipAddress, networkMask, broadcastAddress, gateway
usbEthAdaptersInterfacesListForDmngEthAdapter = [
	['eth110', '00:80:8E:8F:8A:D5', '172.16.110.0', '172.16.110.1', '255.255.255.0', '172.16.110.255', '172.16.110.1'],
	['eth111', '00:80:8E:8F:8E:63', '172.16.111.0', '172.16.111.1', '255.255.255.0', '172.16.111.255', '172.16.111.1']
]
# usbEthAdaptersInterfacesListForDmngUsbEthAdapter : networkInterface, macAddress, ipNetwork, ipAddress, networkMask, broadcastAddress, gateway
usbEthAdaptersInterfacesListForDmngUsbEthAdapter = [
	['eth120', '00:80:8E:8F:8E:02', '172.16.120.0', '172.16.120.1', '255.255.255.0', '172.16.120.255', '172.16.120.1'],
	['eth121', '00:80:8A:8E:79:90', '172.16.121.0', '172.16.121.1', '255.255.255.0', '172.16.121.255', '172.16.121.1'],
	['eth122', '00:80:8E:8F:91:E6', '172.16.122.0', '172.16.122.1', '255.255.255.0', '172.16.122.255', '172.16.122.1']
]

def getNetworkInterfaceInformations(networkInterface):

	'''
	if globals.platformType == 'development':
		networkInterfacesList = testNetworkAliasesList
	if globals.platformType == 'validation':
		# alias 'eth1:100' is used, even if globals.platformType is 'validation'
		networkInterfacesList = testNetworkAliasesList + usbEthAdaptersInterfacesListForDmngEthAdapter + usbEthAdaptersInterfacesListForDmngUsbEthAdapter

	# check that networkInterface is in networkInterfacesList
	possibleInterfacesList = []
	for index in range(len(networkInterfacesList)):
		possibleInterfacesList.append(networkInterfacesList[index][0])
	if possibleInterfacesList.count(networkInterface) == 0:
		utils.displayText('red', '[KO] networkInterface (%s) not in possibleInterfacesList (%s)' % (networkInterface, possibleInterfacesList), 0)
		utils.terminateTest(1)
	'''
	# retrieve informations from /sbin/ifconfig
	command = ['/usr/bin/sudo', '/sbin/ifconfig', networkInterface]
	commandStdout, commandStderr = utils.executeCommand(command)

	# get hardware address (MAC)
	myRe = re.search('HWaddr (?:[0-9a-fA-F]{2})\:(?:[0-9a-fA-F]{2})\:(?:[0-9a-fA-F]{2})\:(?:[0-9a-fA-F]{2})\:(?:[0-9a-fA-F]{2})\:(?:[0-9a-fA-F]{2})', commandStdout)
	macAddress = re.sub('HWaddr ', '', myRe.group())

	# get ipAddress
	try:
		myRe = re.search('inet addr:(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', commandStdout)
		ipAddress = re.sub('inet addr:', '', myRe.group())
	except:
		ipAddress = 'not configured'

	# get networkMask
	try:
		myRe = re.search('Mask:(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', commandStdout)
		networkMask = re.sub('Mask:', '', myRe.group())
	except:
		networkMask = 'not configured'

	# get broadcastAddress
	try:
		myRe = re.search('Bcast:(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', commandStdout)
		broadcastAddress = re.sub('Bcast:', '', myRe.group())
	except:
		broadcastAddress = 'not configured'

	# TODO : get ipv6Address (if needed in the future)
	return macAddress, ipAddress, networkMask, broadcastAddress

def getNetworkInterfaceLinkStatus(networkInterface):
	utils.displayText('red', 'TODO : testing an IP alias with ethtool always report : \'Link detected: yes\'. It cannot be used here.', 0)
	utils.terminateTest(1)

	command = ['/usr/bin/sudo', '/sbin/ethtool', networkInterface]
	commandStdout, commandStderr = utils.executeCommand(command)

	# get "Link detected:"
	myRe = re.search('Link detected: yes|no', commandStdout)
	linkDetected = re.sub('Link detected: ', '', myRe.group())

	if linkDetected == 'yes':
		networkInterfaceStatus = 'up'
	elif linkDetected == 'no':
		networkInterfaceStatus = 'down'
	else:
		utils.displayText('red', '[KO] linkDetected (%s) is neither \'yes\', nor \'no\'' % linkDetected, 0)
		utils.terminateTest(1)

	return networkInterfaceStatus

def waitForNetworkInterfaceStatus(networkInterface, expectedStatus):

	'''
	# wait for loop based on getNetworkInterfaceLinkStatus
	# initializations
	timeout = 60
	loop = 0
	while True:
		status = getNetworkInterfaceLinkStatus(networkInterface)
		if globals.verbose:
			utils.displayText('normal', 'expecting networkInterface %s\'s link status %s, current status : %s' % (networkInterface, expectedStatus, status), 0)
		if status == expectedStatus:
			if not globals.quiet:
				utils.displayText('green', '[OK] networkInterface %s\'s link status is the expected one (%s)' % (networkInterface, status), 0)
			break
		time.sleep(0.5)
		loop +=1
		if loop == timeout:
			utils.displayText('red', 'networkInterface %s\'s expected link status was %s, current status is : %s' % (networkInterface, expectedStatus, status), 0)
			return 1
	'''
	# wait for loop based on getNetworkInterfaceInformations
	# compute requestedIpAddress only if expectedStatus is up
	if expectedStatus == 'up':
		if globals.platformType == 'development':
			networkInterfacesList = testNetworkAliasesList
		if globals.platformType == 'validation':
			# alias 'eth1:100' is used, even if globals.platformType is 'validation'
			networkInterfacesList = testNetworkAliasesList + usbEthAdaptersInterfacesListForDmngEthAdapter + usbEthAdaptersInterfacesListForDmngUsbEthAdapter

		# get networkInterface's index in the list
		index = (([networkInterfacesList[i][0] for i in range(len(networkInterfacesList))]).index(networkInterface))

		# get corresponding requestedIpAddress, requestedNetworkMask, requestedBroadcastAddress
		requestedIpAddress = networkInterfacesList[index][2]
		requestedNetworkMask = networkInterfacesList[index][3]
		requestedBroadcastAddress = networkInterfacesList[index][4]

	# initializations
	timeout = 60
	loop = 0

	while True:
		macAddress, ipAddress, networkMask, broadcastAddress = getNetworkInterfaceInformations(networkInterface)
		if globals.verbose:
			utils.displayText('normal', 'expecting networkInterface %s\'s status %s' % (networkInterface, expectedStatus), 0)
		if expectedStatus == 'down':
			if ipAddress == 'not configured' and networkMask == 'not configured' and broadcastAddress == 'not configured':
				if not globals.quiet:
					utils.displayText('green', '[OK] networkInterface %s\'s status is down (ipAddress, networkMask and broadcastAddress are in state \'not configured\')' % networkInterface, 0)
				break
		if expectedStatus == 'up':
			if ipAddress == requestedIpAddress:
				if not globals.quiet:
					utils.displayText('green', '[OK] networkInterface %s\'s status is up and ipAddress is the requested one (%s)' % (networkInterface, ipAddress), 0)
				break
		time.sleep(0.5)
		loop +=1
		if loop == timeout:
			utils.displayText('red', 'networkInterface %s\'s expected status was %s' % (networkInterface, expectedStatus), 0)
			return 1

	return 0

def setState(networkInterface, requestedState):

	# check requestedState values
	if (requestedState != 'up') and (requestedState != 'down'):
		utils.displayText('red', '[KO] requestedState (%s) is neither \'up\', nor \'down\'' % requestedState, 0)
		utils.terminateTest(1)

	if requestedState == 'down':
		command = ['/usr/bin/sudo', '/sbin/ifdown', networkInterface]

	if requestedState == 'up':
		command = ['/usr/bin/sudo', '/sbin/ifup', networkInterface]

	commandStdout, commandStderr = utils.executeCommand(command)

	'''
	returnCode = waitForNetworkInterfaceStatus(networkInterface, requestedState)
	if returnCode != 0:
		utils.terminateTest(1)
	'''
