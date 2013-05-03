#! /usr/bin/python
# -*- coding: utf-8 -*-

# import python libraries
import datetime
import re
import serial
import signal
import sys
import threading
import time

# import aggregation-platform's libraries
import globals
import utils
import trafficControl

class TimeoutException(Exception):
	pass

def timeout_handler(signum, frame):
	utils.displayText('red', 'in timeout_handler', 0)
	raise TimeoutException()

class Dmng(object):

	controlNetworkInterface = ['eth100', '00:80:8E:8F:8F:55', '172.16.100.10', '255.255.255.0', '172.16.100.255', '172.16.100.1']

	ethAdaptersInterfacesList = [
		['eth110', 'B4:31:B8:00:00:0E', '172.16.110.10', '255.255.255.0', '172.16.110.255', '172.16.110.1'],
		['eth111', 'B4:31:B8:00:00:0F', '172.16.111.10', '255.255.255.0', '172.16.111.255', '172.16.111.1']
	]

	usbEthAdaptersInterfacesList = [
		['eth120', '00:80:8E:8F:92:8B', '172.16.120.10', '255.255.255.0', '172.16.120.255', '172.16.120.1'],
		['eth121', '00:0E:C6:F0:25:53', '172.16.121.10', '255.255.255.0', '172.16.121.255', '172.16.121.1'],
		['eth122', '00:80:8E:8F:8A:E0', '172.16.122.10', '255.255.255.0', '172.16.122.255', '172.16.122.1']
	]

	wifiAdaptersInterfacesList = [
		['mlan0', '00:19:88:51:AD:22', '172.16.200.10', '255.255.255.0', '172.16.200.255', '172.16.200.1']
	]
	# constructor
	#def __init__(self):

	#def __del__(self):
		#print("TODO : in destructor")

	def connectToSerial(self, tty):
		self.lock = threading.Lock()

		self.ser = serial.Serial(
			port = tty,
			baudrate = 115200,
			bytesize = serial.EIGHTBITS,
			parity = serial.PARITY_NONE,
			stopbits = serial.STOPBITS_ONE,
			timeout = 0,
			xonxoff = False,
			rtscts = False,
			writeTimeout = None,
			dsrdtr = False,
			interCharTimeout = None
		)

		# check which port was really used
		#print(mySerial.portstr)

	def disconnectFromSerial(self):
		self.ser.close()

	def reboot(self):
		#self.setAllNetworkInterfacesState('down')
		# it is mandatory to deactivate usb before a reboot, to avoid a unplug/replug of some usb ethernet adapters sometimes, that else do not get recognized on the next reboot
		#self.deActivateUsb()
		self.writeToSerial('reboot', ['The system is going down NOW!'], 30)
		self.expectStringsOnSerial(['dmng login:'], 60)
		self.writeToSerial('admin', ['Password:'], 10)
		self.writeToSerial('ibis2010', ['#'], 10)

	def deActivateUsb(self):
		utils.displayText('cyan', 'deactivating dmng\'s usb', 0)

		# when disabling usb, assume we have 9 usb-eth adapters to build the list of expected strings to expect
		commandsList = [
			['longwood -reset_ethernet_phy 1', ['unregister \'smsc75xx\' usb-ehci-omap.[0-9]-[0-9].[0-9], smsc75xx USB 2.0 Gigabit Ethernet']],
			# TODO : understand why I get 'UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc2 in position 10: unexpected end of data' when using 'longwood -stat' command
			#['longwood -stat', ['USB HUB enable --> 1', 'Phy0 enable --> 1', 'Phy1 enable --> 0']],
			['longwood -reset_ethernet_phy 0', ['unregister \'smsc75xx\' usb-ehci-omap.[0-9]-[0-9].[0-9], smsc75xx USB 2.0 Gigabit Ethernet']],
			# TODO : understand why I get 'UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc2 in position 10: unexpected end of data' when using 'longwood -stat' command
			#['longwood -stat', ['USB HUB enable --> 1', 'Phy0 enable --> 0', 'Phy1 enable --> 0']],
			['longwood -reset_usb_hubs', ['unregister \'asix\' usb-ehci-omap.[0-9]-[0-9].[0-9].[0-9], ASIX AX88772 USB 2.0 Ethernet', 'unregister \'asix\' usb-ehci-omap.[0-9]-[0-9].[0-9].[0-9], ASIX AX88772 USB 2.0 Ethernet', 'unregister \'asix\' usb-ehci-omap.[0-9]-[0-9].[0-9].[0-9], ASIX AX88772 USB 2.0 Ethernet', 'unregister \'asix\' usb-ehci-omap.[0-9]-[0-9].[0-9].[0-9], ASIX AX88772 USB 2.0 Ethernet', 'unregister \'asix\' usb-ehci-omap.[0-9]-[0-9].[0-9].[0-9], ASIX AX88772 USB 2.0 Ethernet', 'unregister \'asix\' usb-ehci-omap.[0-9]-[0-9].[0-9].[0-9], ASIX AX88772 USB 2.0 Ethernet', 'unregister \'asix\' usb-ehci-omap.[0-9]-[0-9].[0-9].[0-9], ASIX AX88772 USB 2.0 Ethernet', 'unregister \'asix\' usb-ehci-omap.[0-9]-[0-9].[0-9].[0-9], ASIX AX88772 USB 2.0 Ethernet', 'unregister \'asix\' usb-ehci-omap.[0-9]-[0-9].[0-9].[0-9], ASIX AX88772 USB 2.0 Ethernet']]
			# TODO : understand why I get 'UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc2 in position 10: unexpected end of data' when using 'longwood -stat' command
			#['longwood -stat', ['USB HUB enable --> 0', 'Phy0 enable --> 0', 'Phy1 enable --> 0']]
		]

		for index in range(len(commandsList)):
			command = commandsList[index][0]
			expectedStringsList = commandsList[index][1]
			self.writeToSerial(command, expectedStringsList, 20)

		utils.displayText('cyan', 'waiting a little bit to not be disturbed by asynchronous traces', 20)

	def activateUsb(self):
		utils.displayText('cyan', 'activating dmng\'s usb', 0)
		# when enabling usb, assume we have 9 usb-eth adapters to build the list of expected strings to expect
		commandsList = [
			['longwood -enable_usb_hubs', ['ASIX AX88772 USB 2.0 Ethernet', 'ASIX AX88772 USB 2.0 Ethernet', 'ASIX AX88772 USB 2.0 Ethernet', 'ASIX AX88772 USB 2.0 Ethernet', 'ASIX AX88772 USB 2.0 Ethernet', 'ASIX AX88772 USB 2.0 Ethernet', 'ASIX AX88772 USB 2.0 Ethernet', 'ASIX AX88772 USB 2.0 Ethernet', 'ASIX AX88772 USB 2.0 Ethernet']],
			# TODO : understand why I get 'UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc2 in position 10: unexpected end of data' when using 'longwood -stat' command
			#['longwood -stat', ['USB HUB enable --> 1', 'Phy0 enable --> 0', 'Phy1 enable --> 0']],
			['longwood -enable_ethernet_phy 0', ['register \'smsc75xx\' at usb-ehci-omap.[0-9]-[0-9].[0-9], smsc75xx USB 2.0 Gigabit Ethernet']],
			# TODO : understand why I get 'UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc2 in position 10: unexpected end of data' when using 'longwood -stat' command
			#['longwood -stat', ['USB HUB enable --> 1', 'Phy0 enable --> 1', 'Phy1 enable --> 0']],
			['longwood -enable_ethernet_phy 1', ['register \'smsc75xx\' at usb-ehci-omap.[0-9]-[0-9].[0-9], smsc75xx USB 2.0 Gigabit Ethernet']]
			# TODO : understand why I get 'UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc2 in position 10: unexpected end of data' when using 'longwood -stat' command
			#['longwood -stat', ['USB HUB enable --> 1', 'Phy0 enable --> 1', 'Phy1 enable --> 1']]
		]

		for index in range(len(commandsList)):
			command = commandsList[index][0]
			expectedStringsList = commandsList[index][1]
			self.writeToSerial(command, expectedStringsList, 20)

		utils.displayText('cyan', 'waiting a little bit to not be disturbed by asynchronous traces', 20)

	def getUbootMode(self):
		utils.displayText('cyan', 'getting U-Boot mode', 0)
		serialOutputUntilTimeout = self.writeToSerial('fw_printenv bootmode', ['(bootmode=appli|test)|(# Error: "bootmode" not defined)'], 10)
		try:
			myRe = re.search('bootmode=appli|test', serialOutputUntilTimeout)
			ubootMode = re.sub('bootmode=', '', myRe.group())
		except:
			ubootMode = 'not set'
		return ubootMode

	def getAppliVersion(self):
		utils.displayText('cyan', 'getting appli version', 0)
		serialOutputUntilTimeout = self.writeToSerial('cat /app/appli-version | awk \'{ print $1 }\'', ['[0-9]+.[0-9]+.[0-9]+-svn[0-9]+'], 30)
		myRe = re.search('[0-9]+.[0-9]+.[0-9]+-svn[0-9]+', serialOutputUntilTimeout)
		appliVersion = myRe.group()
		return appliVersion

	def setUbootMode(self, requestedUbootMode):
		utils.displayText('cyan', 'setting U-Boot mode to %s' % requestedUbootMode, 0)
		self.writeToSerial('fw_setenv bootmode %s' % requestedUbootMode, [], 30)

	def increaseMemoryForBetterOomResistance(self):
		value = 8192
		utils.displayText('cyan', 'setting vm.min_free_kbytes to %d' % value, 0)
		# vm.min_free_kbytes : this is used to force the Linux VM to keep a minimum number of kilobytes free
		commandsList = [['sysctl -w vm.min_free_kbytes=%d' % value, ['vm.min_free_kbytes = %d' % value], 0]]

		for index in range(len(commandsList)):
			command = commandsList[index][0]
			expectedStringsList = commandsList[index][1]
			waitingTime = commandsList[index][2]
			self.writeToSerial(command, expectedStringsList, 60)
			utils.displayText('normal', 'waiting for command \'%s\' to complete' % command, waitingTime)

	def startSshServer(self):
		utils.displayText('cyan', 'starting dmng\'s ssh server', 0)

		commandsList = [['/etc/init.d/S50sshd start', ['Starting sshd: OK'], 20]]
		for index in range(len(commandsList)):
			command = commandsList[index][0]
			expectedStringsList = commandsList[index][1]
			waitingTime = commandsList[index][2]
			self.writeToSerial(command, expectedStringsList, 60)

	def renameNetworkInterfaces(self):
		if globals.useControlNetworkInterface:
			utils.displayText('cyan', 'renaming controlNetworkInterface', 0)
			interfaceName = self.controlNetworkInterface[0]
			interfaceMacAddress = self.controlNetworkInterface[1]
			command = 'nameif %s %s' % (interfaceName, interfaceMacAddress)
			self.writeToSerial(command, [], 10)

		utils.displayText('cyan', 'renaming ethAdaptersInterfacesList', 0)
		for i in range(len(self.ethAdaptersInterfacesList)):
			interfaceName = self.ethAdaptersInterfacesList[i][0]
			interfaceMacAddress = self.ethAdaptersInterfacesList[i][1]
			command = 'nameif %s %s' % (interfaceName, interfaceMacAddress)
			self.writeToSerial(command, [], 10)

		utils.displayText('cyan', 'renaming usbEthAdaptersInterfacesList', 0)
		for i in range(len(self.usbEthAdaptersInterfacesList)):
			interfaceName = self.usbEthAdaptersInterfacesList[i][0]
			interfaceMacAddress = self.usbEthAdaptersInterfacesList[i][1]
			command = 'nameif %s %s' % (interfaceName, interfaceMacAddress)
			self.writeToSerial(command, [], 10)

	def networkInterfaceFirstInit(self, interfaceName):
		'''networkInterfaceFirstInit

		initialize dmng network interface with dhcp
		'''
		# make sure wpa_supplicant is launched if interfaceName is of type wifi
		if re.search('mlan', interfaceName) != None:
			self.writeToSerial('wpa_supplicant -i %s -c /config/wifi.wpa -D wext &' % interfaceName, ['CTRL-EVENT-CONNECTED - Connection to'], 30)
			#self.writeToSerial('wpa_supplicant -i %s -c /config/wifi.wpa -D wext &' % interfaceName, ['CTRL-EVENT-CONNECTED - Connection to (?:[0-9a-fA-F]{2})\:(?:[0-9a-fA-F]{2})\:(?:[0-9a-fA-F]{2})\:(?:[0-9a-fA-F]{2})\:(?:[0-9a-fA-F]{2})\:(?:[0-9a-fA-F]{2}) completed (auth) \[id=0 id_str=\]'], 30)

		# trace 'Lease of (?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3}) obtained, lease time [0-9]+' can be cutted off by asynchronous events : do not expect it!
		self.writeToSerial('udhcpc --interface %s --quit' % interfaceName, [], 30)

	def getNetworkDeviceDriver(self, interfaceName):
		serialOutputUntilTimeout = self.writeToSerial('/usr/sbin/ethtool -i %s' % interfaceName, ['driver: smsc75xx|asix|usb', 'supports-priv-flags: no'], 10)
		myRe = re.search('driver: smsc75xx|asix|usb', serialOutputUntilTimeout)
		networkDeviceDriver = re.sub('driver: ', '', myRe.group())
		return networkDeviceDriver

	def setNetworkInterfaceState(self, interfaceName, requestedState):
		# check requestedState values
		if (requestedState != 'up') and (requestedState != 'down'):
			utils.displayText('red', '[KO] requestedState (%s) is neither \'up\', nor \'down\'' % requestedState, 0)
			utils.terminateTest(1)

		self.writeToSerial('ifconfig %s %s' % (interfaceName, requestedState), [], 10)

	def setNetworkInterfaceDefaultGw(self, interfaceName, defaultGateway):
		self.writeToSerial('route add -net 0.0.0.0 netmask 0.0.0.0 gw %s' % defaultGateway, [], 10)

	def setAllNetworkInterfacesState(self, requestedState):
		# check requestedState values
		if (requestedState != 'up') and (requestedState != 'down'):
			utils.displayText('red', '[KO] requestedState (%s) is neither \'up\', nor \'down\'' % requestedState, 0)
			utils.terminateTest(1)

		# do not modify controlNetworkInterface here... (when connected to the device through ssh, we do not want to disable this link)

		utils.displayText('cyan', 'setting up ethAdaptersInterfacesList in state %s' % requestedState, 0)
		for i in range(len(self.ethAdaptersInterfacesList)):
			interfaceName = self.ethAdaptersInterfacesList[i][0]
			self.setNetworkInterfaceState(interfaceName, requestedState)
			if (requestedState == 'up'):
				defaultGateway = self.ethAdaptersInterfacesList[i][5]
				self.setNetworkInterfaceDefaultGw(interfaceName, defaultGateway)

		utils.displayText('cyan', 'setting up usbEthAdaptersInterfacesList in state %s' % requestedState, 0)
		for i in range(len(self.usbEthAdaptersInterfacesList)):
			interfaceName = self.usbEthAdaptersInterfacesList[i][0]
			self.setNetworkInterfaceState(interfaceName, requestedState)
			if (requestedState == 'up'):
				defaultGateway = self.usbEthAdaptersInterfacesList[i][5]
				self.setNetworkInterfaceDefaultGw(interfaceName, defaultGateway)

		utils.displayText('cyan', 'setting up wifiAdaptersInterfacesList in state %s' % requestedState, 0)
		for i in range(len(self.wifiAdaptersInterfacesList)):
			interfaceName = self.wifiAdaptersInterfacesList[i][0]
			self.setNetworkInterfaceState(interfaceName, requestedState)
			if (requestedState == 'up'):
				defaultGateway = self.wifiAdaptersInterfacesList[i][5]
				self.setNetworkInterfaceDefaultGw(interfaceName, defaultGateway)

		#self.writeToSerial('/usr/bin/killall wpa_supplicant', ['CTRL-EVENT-TERMINATING - signal 15 received'], 30)
		#self.writeToSerial('/usr/bin/killall wpa_supplicant > /dev/null 2>&1', [], 10)

	def rebootAndReconfigureDmng(self):
		self.reboot()
		self.increaseMemoryForBetterOomResistance()
		self.activateUsb()
		self.renameNetworkInterfaces()
		if globals.aggregationsModes.count('kencast') != 0:
			self.writeToSerial('export LD_LIBRARY_PATH=/app/lib:/app/fazzt/lib:${LD_LIBRARY_PATH}', [], 10)

		if globals.useControlNetworkInterface:
			# --------------------------------------------------------------------------------------------------
			utils.displayText('blue', 'setting up controlNetworkInterface, that will be used to drive the dmng (no traffic control on this interface)', 0)
			# --------------------------------------------------------------------------------------------------
			interfaceName = self.controlNetworkInterface[0]
			self.networkInterfaceFirstInit(interfaceName)

			self.startSshServer()

		# --------------------------------------------------------------------------------------------------
		utils.displayText('blue', 'configuring dmng\'s involved network interfaces', 0)
		# --------------------------------------------------------------------------------------------------
		utils.displayText('blue', 'configuring %d ethAdapters' % globals.maxNbOfEthAdapters, 0)
		for i in range(globals.maxNbOfEthAdapters):
			interfaceName = self.ethAdaptersInterfacesList[i][0]
			self.networkInterfaceFirstInit(interfaceName)

		utils.displayText('blue', 'configuring %d usbEthAdapters' % globals.maxNbOfUsbEthAdapters, 0)
		for i in range(globals.maxNbOfUsbEthAdapters):
			interfaceName = self.usbEthAdaptersInterfacesList[i][0]
			self.networkInterfaceFirstInit(interfaceName)

		utils.displayText('blue', 'configuring %d wifiAdapters' % globals.maxNbOfWifiAdapters, 0)
		for i in range(globals.maxNbOfWifiAdapters):
			interfaceName = self.wifiAdaptersInterfacesList[i][0]
			self.networkInterfaceFirstInit(interfaceName)

	def expectStringsOnSerial(self, expectedStringsList, timeout):

		# initializations
		serialOutputUntilTimeout = ''
		partialSerialOutputUntilTimeout = ''

		if globals.verbose:
			utils.displayText('normal', 'expecting strings list (%s) on serial %s (timeout : %d seconds)' % (expectedStringsList, self.ser.portstr, timeout), 0)

		# Set the signal handler and a timeout second alarm
		signal.alarm(timeout)
		try:
			stringsFoundList = []
			while len(expectedStringsList) != 0:
				data = self.ser.read(self.ser.inWaiting())
				# store data in serialOutputUntilTimeout
				if data != b'':
					data = bytes.decode(data)
					serialOutputUntilTimeout += data
					partialSerialOutputUntilTimeout += data

					for expectedString in expectedStringsList:
						if re.search(expectedString, partialSerialOutputUntilTimeout) != None:
							if not globals.quiet:
								utils.displayText('green', '[OK] expected string (%s) found' % expectedString, 0)
							stringsFoundList.append(expectedString)
							# use partialSerialOutputUntilTimeout to remove found strings as soon as they are found : usefull when expecting the same string several times in serialOutputUntilTimeout
							partialSerialOutputUntilTimeout = re.sub(expectedString, '', partialSerialOutputUntilTimeout)

					# update expectedStringsList for the next pass
					for string in stringsFoundList:
						if expectedStringsList.count(string) != 0:
							expectedStringsList.remove(string)

		except TimeoutException:
			utils.displayText('red', '[KO] expectedString (%s) not found' % expectedString, 0)
			utils.displayText('red', '----- serialOutputUntilTimeout -----', 0)
			utils.displayText('normal', serialOutputUntilTimeout, 0)
			utils.displayText('red', '------------------------------------', 0)

			returnCode = utils.terminateTest(1)
			return returnCode
		finally:
			# cancel alaram
			signal.alarm(0)

		if globals.verbose:
			utils.displayText('normal', '----- serialOutputUntilTimeout -----', 0)
			utils.displayText('normal', serialOutputUntilTimeout, 0)
			utils.displayText('normal', '------------------------------------', 0)
		globals.dmngLogFileHandle.write(serialOutputUntilTimeout)
		return serialOutputUntilTimeout

	def writeToSerial(self, data, expectedStringsList, timeout):

		# compute command execution time
		if globals.verbose:
			commandStartTime = datetime.datetime.now()

		# only one concurrent access to the serial port : lock
		self.lock.acquire()

		# initializations
		serialOutputUntilTimeout = ''

		# security : timeout has to be greater than 0
		if timeout == 0:
			timeout = 10
			displayText('yellow', '[WARNING] timeout was set to 0, it has been set to 10', 0)

		# check execution result (return code) except for some commands (either the command does not return a reliable code, or we want to speed up execution time (tc commands))
		# do not check execution result of command "fw_printenv bootmode", which can fail (if bootmode environment variable does not exist, which can be the case after an upgrade)
		if data != 'reboot' and \
			data != 'admin' and \
			data != 'ibis2010' and \
			re.search('fw_printenv bootmode', data) == None and \
			re.search('longwood', data) == None and \
			re.search('wpa_supplicant', data) == None and \
			re.search('/usr/bin/killall', data) == None and \
			re.search('/sbin/tc qdisc del', data) == None and \
			re.search('streamer -s', data) == None and \
			re.search('tc qdisc', data) == None:
				data = data + '; ' + '/bin/echo returnCode=$?'
				expectedStringsList.append('returnCode=0')

		if not globals.quiet:
			utils.displayText('normal', 'sending command on serial %s : %s' % (self.ser.portstr, data) , 0)

		data = data + '\n'

		self.ser.write(data.encode('utf-8'))

		if len(expectedStringsList) > 0:
			serialOutputUntilTimeout = self.expectStringsOnSerial(expectedStringsList, timeout)
		else:
			serialOutputUntilTimeout = ''

		# only one concurrent access to the serial port : unlock
		self.lock.release()

		# compute command execution time
		if globals.verbose:
			commandEndTime = datetime.datetime.now()
			commandExecutionDuration = (commandEndTime - commandStartTime).seconds * 1000 + (commandEndTime - commandStartTime).microseconds / 1000
			utils.displayText('green', '[OK] command executed successfully in %d milliseconds' % commandExecutionDuration, 0)

		return serialOutputUntilTimeout

	# --------------------------------------------------------------------------------------------------
	# Aviwest Aggregation
	# --------------------------------------------------------------------------------------------------
	def getAviwestSstTxVersion(self, pathToFile):
		# test if file pathToFile exist and is executable
		self.writeToSerial('test -x %s' % pathToFile, [], 10)
		serialOutputUntilTimeout = self.writeToSerial('%s -V' % pathToFile, ['%s: Safe Streams Technology' % pathToFile], 10)
		#utils.displayText('red', 'serialOutputUntilTimeout : \n%s' % serialOutputUntilTimeout, 0)

		myRe = re.search('%s: Safe Streams Technology [0-9.]+~svn~[0-9]+' % pathToFile, serialOutputUntilTimeout)
		sstTxVersion = re.sub('%s: Safe Streams Technology ' % pathToFile, '', myRe.group())
		return sstTxVersion

	def getAviwestConnectionStatus(self):
		self.writeToSerial('abus-send sst-tx.get ConnectionStatus', ['ConnectionStatus=true'], 30)
		serialOutputUntilTimeout = self.writeToSerial('abus-send sst-tx.get ConnectionResult', ['ConnectionResult=0'], 30)

		myRe = re.search('Connection failed', serialOutputUntilTimeout)
		if myRe != None:
			utils.displayText('red', 'returnCode : %s (ConnectionResult is not the the expected one)' % returnCode, 0)
			utils.displayText('red', 'Connection failed (0:OK, 1:AUTH, 2:BUSY, 3:INVALID, 4:PROTOVERS, 5:KICKED, 6:TIMEOUT, 7:CONNECTION_LOST)', 0)
			utils.displayText('red', 'serialOutputUntilTimeout :\n%s' % serialOutputUntilTimeout, 0)
			utils.terminateTest(1)

		status = 'TODO'
		return status

	def waitForAviwestConnectionStatus(self):
		utils.displayText('red', 'TODO', 0)
		utils.terminateTest(1)
		self.getAviwestConnectionStatus()
		#self.writeToSerial('abus-send sst-tx.get ConnectionStatus', ['ConnectionStatus=true'], 30)
		#serialOutputUntilTimeout = self.writeToSerial('abus-send sst-tx.get ConnectionResult', ['ConnectionResult=0'], 30)

		#myRe = re.search('Connection failed', serialOutputUntilTimeout)
		#if myRe != None:
		#	utils.displayText('red', 'returnCode : %s (ConnectionResult is not the the expected one)' % returnCode, 0)
		#	utils.displayText('red', 'Connection failed (0:OK, 1:AUTH, 2:BUSY, 3:INVALID, 4:PROTOVERS, 5:KICKED, 6:TIMEOUT, 7:CONNECTION_LOST)', 0)
		#	utils.displayText('red', 'serialOutputUntilTimeout :\n%s' % serialOutputUntilTimeout, 0)
		#	utils.terminateTest(1)

		#status = 'TODO'
		#return status

	def killAviwestSstTx(self):
		utils.displayText('cyan', 'killing any remaining sst-tx instance', 0)
		self.writeToSerial('/usr/bin/killall sst-tx > /dev/null 2>&1', [], 10)

	def startAviwestSstTx(self, pathToFile, audioBitrate, videoBitrate, frameRate, gopDuration, iFramesVsPandBFramesRatio):
		# test if file pathToFile exist and is executable
		self.writeToSerial('test -x %s' % pathToFile, [], 10)
		self.writeToSerial('%s -v -d -s -T %d:%d:%dHz:%d:%d' % (pathToFile, audioBitrate, videoBitrate, frameRate, gopDuration, iFramesVsPandBFramesRatio), ['tx_aggreg_read_live_conf\(\): Config read OK'], 10)

		# TODO : check pid of sst-tx to be sure it has been correctly started

	def startAviwestBwTest(self):
		self.writeToSerial('abus-send sst-tx.BandwidthTestConnect', ['Aggreg WAIT_RESP->CONNECTED'], 30)
		self.writeToSerial('while ! abus-send sst-tx.get CommandReady | grep CommandReady=true; do sleep 1; done', ['CommandReady=true'], 30)
		status = self.getAviwestConnectionStatus()
		if status != 'connected':
			utils.displayText('red', 'status is not the expected one (current status is : %s; expected status was : connected)' % status, 0)
			utils.terminateTest(1)
		self.writeToSerial('abus-send sst-tx.BandwidthTestStart', ['Aggreg CONNECTED->BW_TEST'], 30)
		status = self.getAviwestConnectionStatus()
		if status != 'connected':
			utils.displayText('red', 'status is not the expected one (current status is : %s; expected status was : connected)' % status, 0)
			utils.terminateTest(1)

	def stopAviwestBwTest(self):
		status = self.getAviwestConnectionStatus()
		if status != 'connected':
			utils.displayText('red', 'status is not the expected one (current status is : %s; expected status was : connected)' % status, 0)
			utils.terminateTest(1)
		serialOutputUntilTimeout = self.writeToSerial('abus-send sst-tx.BandwidthTestStop', ['bitrate='], 30)
		myRe = re.search('bitrate=[0-9]+', serialOutputUntilTimeout)
		# estimatedBitrate in kbps
		estimatedBitrate = int(re.sub('bitrate=', '', myRe.group()))
		estimatedBitrate = estimatedBitrate / 1000

		if globals.verbose:
			utils.displayText('yellow', 'estimatedBitrate : %s' % estimatedBitrate, 0)

		self.writeToSerial('while ! abus-send sst-tx.get CommandReady | grep CommandReady=true; do sleep 1; done', ['CommandReady=true'], 30)
		status = self.getAviwestConnectionStatus()
		if status != 'connected':
			utils.displayText('red', 'status is not the expected one (current status is : %s; expected status was : connected)' % status, 0)
			utils.terminateTest(1)

		return estimatedBitrate

	def startAviwestStreaming(self, timeWindow):
		self.writeToSerial('abus-send sst-tx.StreamConnect timewindow=%s' % timeWindow, ['New timewindow %d ms' % timeWindow, 'Aggreg WAIT_RESP->CONNECTED'], 30)
		self.writeToSerial('while ! abus-send sst-tx.get CommandReady | grep CommandReady=true; do sleep 1; done', ['CommandReady=true'], 30)
		status = self.getAviwestConnectionStatus()
		if status != 'connected':
			utils.displayText('red', 'status is not the expected one (current status is : %s; expected status was : connected)' % status, 0)
			utils.terminateTest(1)
		self.writeToSerial('abus-send sst-tx.StreamStart', ['tx_aggreg_do_cmd: CONNECTED\(StreamStart\)'], 30)
		status = self.getAviwestConnectionStatus()
		if status != 'connected':
			utils.displayText('red', 'status is not the expected one (current status is : %s; expected status was : connected)' % status, 0)
			utils.terminateTest(1)

	def stopAviwestStreaming(self):
		#serialOutputUntilTimeout = self.writeToSerial('abus-send sst-tx.ConnectionStop', ['Aggreg STREAMING->DISCONNECTED'], 30)
		serialOutputUntilTimeout = self.writeToSerial('abus-send sst-tx.StreamStop', ['Aggreg STREAMING->DISCONNECTED'], 30)

		# set minVideoBitrate, maxVideoBitrate and avgVideoBitrate from serialOutputUntilTimeout
		regularExpression = 'Stream\(Video\) [0-9a-f]+ rtp_gen_stats: ordered_bitrate min [0-9]+ kbps, max [0-9]+ kbps, avg [0-9]+ kbps'
		myRe = re.search(regularExpression, serialOutputUntilTimeout)
		if myRe == None:
			utils.displayText('red', 'regular expression \"%s\" not found in serialOutputUntilTimeout' % regularExpression, 0)
			utils.displayText('red', 'serialOutputUntilTimeout :\n%s' % serialOutputUntilTimeout, 0)
			utils.terminateTest(1)

		minVideoBitrate = re.sub('Stream\(Video\) [0-9a-f]+ rtp_gen_stats: ordered_bitrate min', '', myRe.group())
		minVideoBitrate = re.sub('kbps, max [0-9]+ kbps, avg [0-9]+ kbps', '', minVideoBitrate)
		minVideoBitrate = int(minVideoBitrate)

		maxVideoBitrate = re.sub('Stream\(Video\) [0-9a-f]+ rtp_gen_stats: ordered_bitrate min [0-9]+ kbps, max ', '', myRe.group())
		maxVideoBitrate = re.sub('kbps, avg [0-9]+ kbps', '', maxVideoBitrate)
		maxVideoBitrate = int(maxVideoBitrate)

		avgVideoBitrate = re.sub('Stream\(Video\) [0-9a-f]+ rtp_gen_stats: ordered_bitrate min [0-9]+ kbps, max [0-9]+ kbps, avg ', '', myRe.group())
		avgVideoBitrate = re.sub(' kbps', '', avgVideoBitrate)
		avgVideoBitrate = int(avgVideoBitrate)

		# set minAudioBitrate, maxAudioBitrate and avgAudioBitrate from serialOutputUntilTimeout
		regularExpression = 'Stream\(Audio\) [0-9a-f]+ rtp_gen_stats: ordered_bitrate min [0-9]+ kbps, max [0-9]+ kbps, avg [0-9]+ kbps'
		myRe = re.search(regularExpression, serialOutputUntilTimeout)
		if myRe == None:
			utils.displayText('red', 'regular expression \"%s\" not found in serialOutputUntilTimeout' % regularExpression, 0)
			utils.displayText('red', 'serialOutputUntilTimeout :\n%s' % serialOutputUntilTimeout, 0)
			utils.terminateTest(1)

		minAudioBitrate = re.sub('Stream\(Audio\) [0-9a-f]+ rtp_gen_stats: ordered_bitrate min', '', myRe.group())
		minAudioBitrate = re.sub('kbps, max [0-9]+ kbps, avg [0-9]+ kbps', '', minAudioBitrate)
		minAudioBitrate = int(minAudioBitrate)

		maxAudioBitrate = re.sub('Stream\(Audio\) [0-9a-f]+ rtp_gen_stats: ordered_bitrate min [0-9]+ kbps, max ', '', myRe.group())
		maxAudioBitrate = re.sub('kbps, avg [0-9]+ kbps', '', maxAudioBitrate)
		maxAudioBitrate = int(maxAudioBitrate)

		avgAudioBitrate = re.sub('Stream\(Audio\) [0-9a-f]+ rtp_gen_stats: ordered_bitrate min [0-9]+ kbps, max [0-9]+ kbps, avg ', '', myRe.group())
		avgAudioBitrate = re.sub(' kbps', '', avgAudioBitrate)
		avgAudioBitrate = int(avgAudioBitrate)

		if globals.verbose:
			utils.displayText('yellow', 'minVideoBitrate : %d' % minVideoBitrate, 0)
			utils.displayText('yellow', 'maxVideoBitrate : %d' % maxVideoBitrate, 0)
			utils.displayText('yellow', 'avgVideoBitrate : %d' % avgVideoBitrate, 0)

			utils.displayText('yellow', 'minAudioBitrate : %d' % minAudioBitrate, 0)
			utils.displayText('yellow', 'maxAudioBitrate : %d' % maxAudioBitrate, 0)
			utils.displayText('yellow', 'avgAudioBitrate : %d' % avgAudioBitrate, 0)

		self.writeToSerial('abus-send sst-tx.terminate', ['res=0'], 30)

		return minVideoBitrate, maxVideoBitrate, avgVideoBitrate, minAudioBitrate, maxAudioBitrate, avgAudioBitrate

	# --------------------------------------------------------------------------------------------------
	# KenCast Aggregation
	# --------------------------------------------------------------------------------------------------
	def killKenCastFazzt(self):
		utils.displayText('cyan', 'killing any remaining fazzt instance', 0)
		self.writeToSerial('/usr/bin/killall -KILL fazzt > /dev/null 2>&1', [], 10)

	def startKenCastFazzt(self, pathToFile):
		# TODO : make a funtion for ntpdate
		#self.writeToSerial('ntpdate 172.16.100.1', ['TODO'], 10)
		# test if file pathToFile exist and is executable
		self.writeToSerial('test -x %s' % pathToFile, [], 10)
		self.writeToSerial('%s -d ; sleep 1' % pathToFile, [], 10)
		# TODO : check pid of fazzt to be sure it has been correctly started

	def startEncoder(self):
		# kohala -video_source 0 : generator (GENERATOR=0, ANALOG=1, SDI=2, HDMI=3)
		self.writeToSerial('kohala -video_source 0', [], 10)
		# kohala -video_generator 64 2  # PAL COLOR_CIRCLES
		# standard
		#       VIDEO_STANDARD_NTSC_BT656_4             = 0,    = 0x0
		#       VIDEO_STANDARD_PAL                      = 64,   = 0x40
		#       VIDEO_STANDARD_720p59_94                = 152,  = 0x98
		#       VIDEO_STANDARD_720p50                   = 146,  = 0x92
		#       VIDEO_STANDARD_1080i59_94               = 200,  = 0xC8
		#       VIDEO_STANDARD_1080i50                  = 193,  = 0xC1
		#       VIDEO_STANDARD_1080p30                  = 208,  = 0xD0
		#       VIDEO_STANDARD_1080p25                  = 209,  = 0xD1
		self.writeToSerial('kohala -video_generator 64 2', [], 10)
		##self.writeToSerial('kohala -video_generator 193 2', [], 10)
		self.writeToSerial('kohala -video_rate 0', [], 10)
		##self.writeToSerial('kohala -video_rate 2', [], 10)
		# RATE_27_MHZ       = 0x0,
		# RATE_74_175_MHZ   = 0x1,
		# RATE_74_25_MHZ    = 0x2
		self.writeToSerial('kohala -video_release', [], 10)

		#------ Audio encoder static parameters -------------------
		# GENERATOR=0, ANALOG=1, SDI=2, HDMI=3
		self.writeToSerial('enconfig -encoder 0 -audio_source 0', [], 10)
		# MONO=0, STEREO=1, DUAL_MONO=2
		self.writeToSerial('enconfig -encoder 0 -audio_channel_mode 1', [], 10)
		# AACLC=0, AACHE=1, AACHEV2=2, MPEG1L2=3
		self.writeToSerial('enconfig -encoder 0 -audio_enc_mode 3', [], 10)
		# kHz
		self.writeToSerial('enconfig -encoder 0 -audio_sample_rate 48000', [], 10)
		# Kb
		self.writeToSerial('enconfig -encoder 0 -audio_bitrate %d' % globals.audioBitrate, [], 10)
		# CBR=0, VBR=1, CAPPED_VBR=2
		self.writeToSerial('enconfig -encoder 0 -audio_bitrate_mode 0', [], 10)
		# ms
		self.writeToSerial('enconfig -encoder 0 -audio_pts_offset 0', [], 10)

		#------ Video encoder static parameters -------------------
		# GENERATOR=0, ANALOG=1, SDI=2, HDMI=3
		self.writeToSerial('enconfig -encoder 0 -video_source 0', [], 10)
		# pixels
		self.writeToSerial('enconfig -encoder 0 -video_resolution_width 720', [], 10)
		##self.writeToSerial('enconfig -encoder 0 -video_resolution_width 1920', [], 10)
		# pixels
		self.writeToSerial('enconfig -encoder 0 -video_resolution_height 576', [], 10)
		##self.writeToSerial('enconfig -encoder 0 -video_resolution_height 1080', [], 10)
		# frame_rate * 100 (2500, 2997)
		self.writeToSerial('enconfig -encoder 0 -video_frame_rate %d' % (globals.frameRate * 100), [], 10)
		# PROGRESSIVE_VIDEO=0, INTERLACED_VIDEO=1, DOUBLING_FIELD_VIDEO=2, ONE_FIELD_VIDEO=3
		self.writeToSerial('enconfig -encoder 0 -video_scan_mode 1', [], 10)
		self.writeToSerial('enconfig -encoder 0 -video_latency 0', [], 10)
		# Kb
		self.writeToSerial('enconfig -encoder 0 -video_bitrate %d' % globals.videoBitrate, [], 10)
		# CBR=0, VBR=1, CAPPED_VBR=2
		if globals.videoBitrateMode == 'CBR':
			self.writeToSerial('enconfig -encoder 0 -video_bitrate_mode 0', [], 10)
		elif globals.videoBitrateMode == 'VBR':
			self.writeToSerial('enconfig -encoder 0 -video_bitrate_mode 1', [], 10)
		else:
			utils.displayText('red', 'globals.videoBitrateMode (%s) is neither CBR nor VBR', 0)
			utils.terminateTest(1)

		# kb
		self.writeToSerial('enconfig -encoder 0 -video_capped_bitrate 10000', [], 10)

		#------ Video encoder static advanced parameters ----------
		# DISABLE=0, ENABLE=1
		self.writeToSerial('enconfig -encoder 0 -video_dyn_res_en 0', [], 10)
		# DISABLE=0, ENABLE=1
		self.writeToSerial('enconfig -encoder 0 -video_dyn_fps_en 0', [], 10)
		self.writeToSerial('enconfig -encoder 0 -video_gop_n 0', [], 10)
		self.writeToSerial('enconfig -encoder 0 -video_gop_m 0', [], 10)
		# DISABLE=0, ENABLE=1
		self.writeToSerial('enconfig -encoder 0 -video_open_gop_en 0', [], 10)
		# DISABLE=0, ENABLE=1
		self.writeToSerial('enconfig -encoder 0 -video_aspect_ratio_en 0', [], 10)
		# DISABLE=0, ENABLE=1
		self.writeToSerial('enconfig -encoder 0 -video_deinterlace_en 0', [], 10)
		self.writeToSerial('enconfig -encoder 0 -video_median_filter 0', [], 10)
		self.writeToSerial('enconfig -encoder 0 -video_dcrowl_filter 0', [], 10)
		self.writeToSerial('enconfig -encoder 0 -video_alq_mode 0', [], 10)
		# DISABLE=0, ENABLE=1
		self.writeToSerial('enconfig -encoder 0 -video_roi_en 0', [], 10)

		#------ Encoder commands ----------------------------------
		self.writeToSerial('enconfig -encoder 0 -start', [], 10)

	def startStreamer(self, timewindow):
		self.writeToSerial('streamer -s &', ['streamer - new configuration'], 10)
		self.writeToSerial('abus-send streamer.start streamMode=0 videoDev=/dev/dm-video audioDev=/dev/dm-audio timewindow=%s audioEncMode=0 audioChannelMode=1' % timewindow, ['streaming is started SUCCESSFULLY!!!'], 10)

	def killAllStreamer(self):
		utils.displayText('cyan', 'killing any remaining streamer instance', 0)
		self.writeToSerial('/usr/bin/killall streamer > /dev/null 2>&1', [], 10)

	def startKenCastBwTest(self):
		self.writeToSerial('/app/fazzt/scripts/BandwidthTestConnect.fzt', ['Connecting'], 30)
		self.waitForKenCastConnectionStatus('connected')
		self.writeToSerial('/app/fazzt/scripts/BandwidthTestStart.fzt', [], 30)
		self.waitForKenCastConnectionStatus('connected')

	def stopKenCastBwTest(self):
		self.waitForKenCastConnectionStatus('connected')
		serialOutputUntilTimeout = self.writeToSerial('/app/fazzt/scripts/BandwidthTestStop.fzt', [], 30)
		myRe = re.search('[0-9]+', serialOutputUntilTimeout)
		# estimatedBitrate in kbps
		estimatedBitrate = int(myRe.group())

		if globals.verbose:
			utils.displayText('yellow', 'estimatedBitrate : %s' % estimatedBitrate, 0)

		self.waitForKenCastConnectionStatus('connected')

		return estimatedBitrate

	def getKenCastConnectionStatus(self):
		serialOutputUntilTimeout = self.writeToSerial('/app/fazzt/scripts/ConnectionStatus.fzt', [], 30)
		if re.search('Connecting', serialOutputUntilTimeout):
			status = 'connecting'
		elif re.search('Connected', serialOutputUntilTimeout):
			status = 'connected'
		else:
			status = 'unknown'
		return status

	def waitForKenCastConnectionStatus(self, status):
		timeout = 5
		loop = 0
		while self.getKenCastConnectionStatus() != status:
			time.sleep(1)
			loop +=1
			if loop == timeout:
				break
		#status = self.getKenCastConnectionStatus()
		#serialOutputUntilTimeout = self.writeToSerial('/app/fazzt/scripts/ConnectionStatus.fzt', [], 30)
		#if re.search('Connecting', serialOutputUntilTimeout):
		#	status = 'connecting'
		#elif re.search('Connected', serialOutputUntilTimeout):
		#	status = 'connected'
		#else:
		#	status = 'unknown'

		#return status

	def startKenCastStreaming(self):
		self.writeToSerial('/app/fazzt/scripts/StreamConnect.fzt', ['Connecting'], 30)
		self.waitForKenCastConnectionStatus('connected')
		self.writeToSerial('/app/fazzt/scripts/StreamStart.fzt', [], 30)
		self.waitForKenCastConnectionStatus('connected')

	def stopKenCastStreaming(self):
		self.writeToSerial('/app/fazzt/scripts/StreamStop.fzt', [], 30)

if __name__ == '__main__':

	globals.scriptStartTime = time.time()

	# new instance of Dmng
	myDmng = Dmng()
	myDmng.connectToSerial('/dev/ttyUSB0')
	#myDmng.writeToSerial('longwood -stat', ['Phy1 enable'], 60)
	myDmng.getAviwestSstTxVersion('/tmp/sst-tx')

	#myDmng.expectStringsOnSerial(['Sent SIGTERM to all processes'], 60)
	#myDmng.writeToSerial('ls', ['appli-version'], 5)

	myDmng.disconnectFromSerial()
	del(myDmng)

	##logFileNameHandle.close()
	utils.terminateTest(0)


