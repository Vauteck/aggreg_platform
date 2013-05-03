#! /usr/bin/python
# -*- coding: utf-8 -*-

# import python libraries
import argparse
import json
import os
import pdb
import re
import signal
import subversion
import sys
import time
import threading

# import aggregation-platform's libraries
import dmng
import globals
import nat
import networkInterfaces
import scenariiParameters
import studioSstRx
import trafficControl
import utils

globals.scriptStartTime = time.time()

parser = argparse.ArgumentParser(description="launch a scenario on aggregation-platform")
# add positional arguments
parser.add_argument("platformType", action="store", help="platform type : development|validation")
parser.add_argument("scenarioId", type=int, help="the scenario ID")
# add optional arguments
parser.add_argument("-d", "--directory", action="store", help="base directory for storing results")
parser.add_argument("-m", "--send-email", action="store_true", help="send an email corresponding to the user logged")
parser.add_argument("--no-colors", action="store_true", help="don't use colors in displayed text")
parser.add_argument('-r', "--reboot-dmng", action="store_true", help="reboot dmng and reconfigure its network interfaces")
parser.add_argument("-a", "--disable-traffic-control-on-sender-side", action="store_true", help="disable traffic control on sender side")
parser.add_argument("-b", "--disable-traffic-control-on-receiver-side", action="store_true", help="disable traffic control on receiver side")
parser.add_argument("-c", "--skip-iptables", action="store_true", help="skip iptables rules set")
parser.add_argument("-e", "--disable-control-network-interface", action="store_true", help="disable control network interface (if set, implies that copies using scp will not be done)")

group = parser.add_mutually_exclusive_group()
group.add_argument("-q", "--quiet", action="store_true", help="be quiet")
group.add_argument("-v", "--verbose", action="store_true", help="be verbose")

# add conflicting optional arguments
if globals.aggregationsModes.count('aviwest') != 0:
	group1 = parser.add_mutually_exclusive_group()
	group1.add_argument("-btx", "--build_last_sst-tx", action="store_true", help="build and use the last version of sst-tx")
	group1.add_argument("-utx", "--sst-tx", action="store", help="use the given version of sst-tx")

	group2 = parser.add_mutually_exclusive_group()
	group2.add_argument("-brx", "--build_last_sst-rx", action="store_true", help="build and use the last version of sst-rx")
	group2.add_argument("-urx", "--sst-rx", action="store", help="use the given version of sst-rx")

args = parser.parse_args()

# overwrite inter modules variables
globals.platformType = args.platformType
globals.scenarioId = args.scenarioId

if args.directory:
	globals.baseDirectoryForResults = args.directory
if args.send_email:
	globals.sendEmail = True
if args.no_colors:
	globals.colorEnabled = False
if globals.aggregationsModes.count('aviwest') != 0:
	if args.sst_rx:
		globals.sstRxBinary = args.sst_rx
	if args.sst_tx:
		globals.sstTxBinary = args.sst_tx
if args.quiet:
	globals.quiet = True
if args.verbose:
	globals.verbose = True
if args.reboot_dmng:
	rebootNeeded = True
else:
	rebootNeeded = False
if args.disable_control_network_interface:
	globals.useControlNetworkInterface = False

# --------------------------------------------------------------------------------------------------
# check parameters
# --------------------------------------------------------------------------------------------------
if os.path.isfile(globals.baseDirectoryForResults):
	os.remove(globals.baseDirectoryForResults)
	utils.displayText('yellow', '[WARNING] globals.baseDirectoryForResults (%s) was a file, it is supposed to be a directory, it has been deleted' % globals.baseDirectoryForResults, 0)

if not os.path.isdir(globals.baseDirectoryForResults):
	os.makedirs(globals.baseDirectoryForResults)

#if globals.aggregationsModes.count('aviwest') != 0:
#	if args.build_last_sst_tx or args.build_last_sst_rx:
#		utils.displayText('red', 'testWithAviwestAggregation set to %s whereas a sst-tx/sst-rx build has been requested (args.build_last_sst_tx : %s, args.build_last_sst_rx : %s)' % (globals.testWithAviwestAggregation, args.build_last_sst_tx, args.build_last_sst_rx), 0)
#		utils.terminateTest(1)

if globals.platformType != 'development' and globals.platformType != 'validation':
	utils.displayText('red', 'platformType (%s) is neither development nor validation' % globals.platformType, 0)
	utils.terminateTest(1)

if (globals.platformType == 'validation') and args.reboot_dmng:
	utils.displayText('red', 'validation platform cannot reboot the dmng, since it does not use its serial port at all', 0)
	utils.terminateTest(1)

if globals.aggregationsModes.count('aviwest') != 0:
	if not args.build_last_sst_rx and not args.sst_rx:
		utils.displayText('red', 'neither --build_last_sst-rx nor --sst-rx command line option specified : you need to specify one of those options', 0)
		utils.terminateTest(1)

globals.platformSvnRevision = subversion.getSvnRevision(globals.scriptDirName)
utils.displayText('black', 'aggregation-platform\'s svn revision : %s' % globals.platformSvnRevision, 0)

if globals.aggregationsModes.count('aviwest') != 0:
	# --------------------------------------------------------------------------------------------------
	# BUILD SST-TX/SST-RX IF ASKED TO DO SO
	# --------------------------------------------------------------------------------------------------
	if args.build_last_sst_tx or args.build_last_sst_rx:
		utils.displayText('blue', 'getting a new appli working copy', 0)
		subversion.getNewAppliSvnWc('HEAD')

	if args.build_last_sst_tx:
		utils.displayText('blue', 'building sst-tx', 0)
		subversion.buildStudioSstTx()

		if args.build_last_sst_rx:
			utils.displayText('blue', 'building sst-rx', 0)
			subversion.buildStudioSstRx()

scenParameters = scenariiParameters.deserializeObject()

# check values
if globals.nbOfEthAdapters > globals.maxNbOfEthAdapters:
	utils.displayText('red', '[KO] globals.nbOfEthAdapters (%d) > globals.maxNbOfEthAdapters (%d)' % (globals.nbOfEthAdapters, globals.maxNbOfEthAdapters), 0)
	utils.terminateTest(1)
if globals.nbOfUsbEthAdapters > globals.maxNbOfUsbEthAdapters:
	utils.displayText('red', '[KO] globals.nbOfUsbEthAdapters (%d) > globals.maxNbOfUsbEthAdapters (%d)' % (globals.nbOfUsbEthAdapters, globals.maxNbOfUsbEthAdapters), 0)
	utils.terminateTest(1)
if globals.nbOfWifiAdapters > globals.maxNbOfWifiAdapters:
	utils.displayText('red', '[KO] globals.nbOfWifiAdapters (%d) > globals.maxNbOfWifiAdapters (%d)' % (globals.nbOfWifiAdapters, globals.maxNbOfWifiAdapters), 0)
	utils.terminateTest(1)

# --------------------------------------------------------------------------------------------------
# DO NOT START TEST IF actionMode IS FORWARD. DO NOT PUBLISH RESULTS (DO NOT PUBLISH KNOWN KO RESULTS)
# --------------------------------------------------------------------------------------------------
if globals.actionMode == 'forward':
	utils.displayText('red', 'TODO : %s not yet supported in framework DO NOT PUBLISH RESULTS (DO NOT PUBLISH KNOWN KO RESULTS)' % globals.actionMode, 0)
	sys.exit(1)
	#utils.terminateTest(1)

# --------------------------------------------------------------------------------------------------
# STEP BY STEP RUN
# --------------------------------------------------------------------------------------------------

# enable signal for dmng
signal.signal(signal.SIGALRM, dmng.timeout_handler)

# new instance of Dmng
myDmng = dmng.Dmng()
if globals.platformType == 'development':
	myDmng.connectToSerial('/dev/ttyS0')

	# --------------------------------------------------------------------------------------------------
	utils.displayText('blue', 'checking U-Boot mode', 0)
	# --------------------------------------------------------------------------------------------------
	initialUbootMode = myDmng.getUbootMode()
	if initialUbootMode == 'test':
		utils.displayText('green', '[OK] U-Boot mode is the right one (%s)' % initialUbootMode, 0)

	if initialUbootMode != 'test':
		myDmng.setUbootMode('test')
		rebootNeeded = True

# --------------------------------------------------------------------------------------------------
utils.displayText('blue', 'deconfiguring aggregationMaster\'s all network interfaces', 0)
# --------------------------------------------------------------------------------------------------
# deconfigure all network aliases
for interfaceName in [networkInterfaces.testNetworkAliasesList[i][0] for i in range(len(networkInterfaces.testNetworkAliasesList))]:
	networkInterfaces.setState(interfaceName, 'down')
# deconfigure all usb-eth adapters (for any globals.platformType)
for interfaceName in [networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[i][0] for i in range(len(networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter))]:
	networkInterfaces.setState(interfaceName, 'down')
for interfaceName in [networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[i][0] for i in range(len(networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter))]:
	networkInterfaces.setState(interfaceName, 'down')
# --------------------------------------------------------------------------------------------------
utils.displayText('blue', 'configuring aggregationMaster\'s all network interfaces', 0)
# --------------------------------------------------------------------------------------------------
if globals.platformType == 'development':
	if globals.useControlNetworkInterface:
		utils.displayText('normal', 'configuring aggregationMaster\'s controlNetworkInterface (for driving the device over ssh)', 0)
		networkInterfaces.setState(networkInterfaces.testNetworkAliasesList[0][0], 'up')

if globals.maxNbOfEthAdapters > 0:
	if globals.platformType == 'development':
		utils.displayText('blue', 'configuring network aliases on aggregationMaster (corresponding to ethAdapters on dmng (globals.maxNbOfEthAdapters : %d))' % globals.maxNbOfEthAdapters, 0)
		for interfaceName in [networkInterfaces.testNetworkAliasesList[1 + i][0] for i in range(0, globals.maxNbOfEthAdapters)]:
			networkInterfaces.setState(interfaceName, 'up')
	elif globals.platformType == 'validation':
		utils.displayText('blue', 'configuring ethAdapters on aggregationMaster (corresponding to ethAdapters on dmng (globals.maxNbOfEthAdapters : %d))' % globals.maxNbOfEthAdapters, 0)
		for interfaceName in [networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[i][0] for i in range(0, globals.maxNbOfEthAdapters)]:
			networkInterfaces.setState(interfaceName, 'up')

if globals.maxNbOfUsbEthAdapters > 0:
	if globals.platformType == 'development':
		utils.displayText('blue', 'configuring network aliases on aggregationMaster (corresponding to usbEthAdapters on dmng (globals.maxNbOfUsbEthAdapters : %d))' % globals.maxNbOfUsbEthAdapters, 0)
		for interfaceName in [networkInterfaces.testNetworkAliasesList[1 + i + globals.maxNbOfEthAdapters][0] for i in range(0, globals.maxNbOfUsbEthAdapters)]:
			networkInterfaces.setState(interfaceName, 'up')
	elif globals.platformType == 'validation':
		utils.displayText('blue', 'configuring usbEthAdapters on aggregationMaster (corresponding to usbEthAdapters on dmng (globals.maxNbOfUsbEthAdapters : %d))' % globals.maxNbOfUsbEthAdapters, 0)
		for interfaceName in [networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[i][0] for i in range(0, globals.maxNbOfUsbEthAdapters)]:
			networkInterfaces.setState(interfaceName, 'up')

if globals.maxNbOfWifiAdapters > 0:
	utils.displayText('blue', 'configuring network aliases on aggregationMaster corresponding to wifiAdapters on dmng (globals.maxNbOfWifiAdapters : %d)' % globals.maxNbOfWifiAdapters, 0)
	for interfaceName in [networkInterfaces.testNetworkAliasesList[1 + i + globals.maxNbOfEthAdapters + globals.maxNbOfUsbEthAdapters][0] for i in range(0, globals.maxNbOfWifiAdapters)]:
		networkInterfaces.setState(interfaceName, 'up')

# --------------------------------------------------------------------------------------------------
utils.displayText('blue', 'restarting isc-dhcp-server (required after shuting down/up all network interfaces)', 0)
# --------------------------------------------------------------------------------------------------
commandsList = []
commandsList.append(['/usr/bin/sudo', '/sbin/stop', 'isc-dhcp-server'])
commandsList.append(['/usr/bin/sudo', '/sbin/start', 'isc-dhcp-server'])

for command in commandsList:
	commandStdout, commandStderr = utils.executeCommand(command)

if globals.platformType == 'development':
	if rebootNeeded:
		# --------------------------------------------------------------------------------------------------
		utils.displayText('blue', 'rebooting dmng', 0)
		# --------------------------------------------------------------------------------------------------
		myDmng.rebootAndReconfigureDmng()

		currentUbootMode = myDmng.getUbootMode()
		if currentUbootMode == 'test':
			utils.displayText('green', '[OK] U-Boot mode is the right one (%s)' % currentUbootMode, 0)
		else:
			utils.displayText('red', '[KO] U-Boot mode is still not the expected one (test). It is currently : %s' % currentUbootMode, 0)
			utils.terminateTest(1)

# --------------------------------------------------------------------------------------------------
utils.displayText('blue', 'deconfiguring aggregationMaster\'s all network interfaces', 0)
# --------------------------------------------------------------------------------------------------
# deconfigure all network aliases (except the one used for controlNetworkInterface)
for interfaceName in [networkInterfaces.testNetworkAliasesList[1 + i][0] for i in range(len(networkInterfaces.testNetworkAliasesList) - 1)]:
	networkInterfaces.setState(interfaceName, 'down')
# deconfigure all usb-eth adapters (for any globals.platformType)
for interfaceName in [networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[i][0] for i in range(len(networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter))]:
	networkInterfaces.setState(interfaceName, 'down')
for interfaceName in [networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[i][0] for i in range(len(networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter))]:
	networkInterfaces.setState(interfaceName, 'down')

# --------------------------------------------------------------------------------------------------
utils.displayText('blue', 'configuring aggregationMaster\'s involved network interfaces', 0)
# --------------------------------------------------------------------------------------------------

if globals.nbOfEthAdapters > 0:
	if globals.platformType == 'development':
		utils.displayText('blue', 'configuring network aliases on aggregationMaster (corresponding to ethAdapters on dmng (globals.nbOfEthAdapters : %d))' % globals.nbOfEthAdapters, 0)
		for interfaceName in [networkInterfaces.testNetworkAliasesList[1 + i][0] for i in range(0, globals.nbOfEthAdapters)]:
			networkInterfaces.setState(interfaceName, 'up')
	elif globals.platformType == 'validation':
		utils.displayText('blue', 'configuring ethAdapters on aggregationMaster (corresponding to ethAdapters on dmng (globals.nbOfEthAdapters : %d))' % globals.nbOfEthAdapters, 0)
		for interfaceName in [networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[i][0] for i in range(0, globals.nbOfEthAdapters)]:
			networkInterfaces.setState(interfaceName, 'up')

if globals.nbOfUsbEthAdapters > 0:
	if globals.platformType == 'development':
		utils.displayText('blue', 'configuring network aliases on aggregationMaster (corresponding to usbEthAdapters on dmng (globals.nbOfUsbEthAdapters : %d))' % globals.nbOfUsbEthAdapters, 0)
		for interfaceName in [networkInterfaces.testNetworkAliasesList[1 + i + globals.maxNbOfEthAdapters][0] for i in range(0, globals.nbOfUsbEthAdapters)]:
			networkInterfaces.setState(interfaceName, 'up')
	elif globals.platformType == 'validation':
		utils.displayText('blue', 'configuring usbEthAdapters on aggregationMaster (corresponding to usbEthAdapters on dmng (globals.nbOfUsbEthAdapters : %d))' % globals.nbOfUsbEthAdapters, 0)
		for interfaceName in [networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[i][0] for i in range(0, globals.nbOfUsbEthAdapters)]:
			networkInterfaces.setState(interfaceName, 'up')

if globals.nbOfWifiAdapters > 0:
	utils.displayText('blue', 'configuring network aliases on aggregationMaster corresponding to wifiAdapters on dmng (globals.nbOfWifiAdapters : %d)' % globals.nbOfWifiAdapters, 0)
	for interfaceName in [networkInterfaces.testNetworkAliasesList[1 + i + globals.maxNbOfEthAdapters + globals.maxNbOfUsbEthAdapters][0] for i in range(0, globals.nbOfWifiAdapters)]:
		networkInterfaces.setState(interfaceName, 'up')

# --------------------------------------------------------------------------------------------------
utils.displayText('blue', 'restarting isc-dhcp-server (required after shutting down/up all network interfaces)', 0)
# --------------------------------------------------------------------------------------------------
commandsList = []
commandsList.append(['/usr/bin/sudo', '/sbin/stop', 'isc-dhcp-server'])
commandsList.append(['/usr/bin/sudo', '/sbin/start', 'isc-dhcp-server'])

for command in commandsList:
	commandStdout, commandStderr = utils.executeCommand(command)

if not args.skip_iptables:
	# --------------------------------------------------------------------------------------------------
	utils.displayText('blue', 'setting iptables rules on aggregationMaster', 0)
	# --------------------------------------------------------------------------------------------------
	nat.initChains()
	nat.setDefaultPolicy()
	nat.setInputRules(myDmng)
	nat.setOutputRules()
	nat.setForwardRules()
	nat.setNatPostroutingRules()
	nat.setNatOutputRules()
	nat.setNatPreroutingRules(myDmng)
	#nat.setMangleOutputRules()
	#nat.setManglePreroutingRules()
	if not globals.quiet:
		nat.displayRules()

for aggregationMode in globals.aggregationsModes:
	# --------------------------------------------------------------------------------------------------
	utils.displayText('blue', 'launching streaming test with aggregation : %s' % aggregationMode, 0)
	# --------------------------------------------------------------------------------------------------
	#if not rebootNeeded:
		#myDmng.rebootAndReconfigureDmng()

	if globals.platformType == 'development':
		deviceOnWhichSettingTc = 'dmng'
	elif globals.platformType == 'validation':
		deviceOnWhichSettingTc = 'aggregationMaster'

	# --------------------------------------------------------------------------------------------------
	utils.displayText('blue', 'resetting %s\'s traffic control parameters on involved network interfaces' % deviceOnWhichSettingTc, 0)
	# --------------------------------------------------------------------------------------------------
	for i in range(globals.nbOfEthAdapters):
		if globals.platformType == 'development':
			interfaceName = myDmng.ethAdaptersInterfacesList[i][0]
		elif globals.platformType == 'validation':
			interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[i][0]
		commandsList = trafficControl.buildCommandsListForReset(interfaceName)
		if globals.platformType == 'development':
			for command in commandsList:
				commandString = ' '.join(command)
				myDmng.writeToSerial(commandString, [], 10)
		elif globals.platformType == 'validation':
			for command in commandsList:
				# insert /usr/bin/sudo before each command
				command.insert(0, '/usr/bin/sudo')
			commandStdout, commandStderr = trafficControl.executeCommandsList(commandsList)

	for i in range(globals.nbOfUsbEthAdapters):
		if globals.platformType == 'development':
			interfaceName = myDmng.usbEthAdaptersInterfacesList[i][0]
		elif globals.platformType == 'validation':
			interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[i][0]
		commandsList = trafficControl.buildCommandsListForReset(interfaceName)
		if globals.platformType == 'development':
			for command in commandsList:
				commandString = ' '.join(command)
				myDmng.writeToSerial(commandString, [], 10)
		elif globals.platformType == 'validation':
			for command in commandsList:
				# insert /usr/bin/sudo before each command
				command.insert(0, '/usr/bin/sudo')
			commandStdout, commandStderr = trafficControl.executeCommandsList(commandsList)

	for i in range(globals.nbOfWifiAdapters):
		if globals.platformType == 'development':
			interfaceName = myDmng.wifiAdaptersInterfacesList[i][0]
		elif globals.platformType == 'validation':
			interfaceName = networkInterfaces.testNetworkAliasesList[1 + i + globals.maxNbOfEthAdapters + globals.maxNbOfUsbEthAdapters][0]
		commandsList = trafficControl.buildCommandsListForReset(interfaceName)
		if globals.platformType == 'development':
			for command in commandsList:
				commandString = ' '.join(command)
				myDmng.writeToSerial(commandString, [], 10)
		elif globals.platformType == 'validation':
			for command in commandsList:
				# insert /usr/bin/sudo before each command
				command.insert(0, '/usr/bin/sudo')
			commandStdout, commandStderr = trafficControl.executeCommandsList(commandsList)

	if aggregationMode == 'none' or aggregationMode == 'kencast':
		receiverInterface = globals.windowsVmStudioTrafficLanIfc
	elif aggregationMode == 'aviwest':
		receiverInterface = globals.linuxVmStudioTrafficLanIfc

	# --------------------------------------------------------------------------------------------------
	utils.displayText('blue', 'resetting %s\'s traffic control parameters' % receiverInterface, 0)
	# --------------------------------------------------------------------------------------------------
	commandsList = trafficControl.buildCommandsListForReset(receiverInterface)
	# insert /usr/bin/sudo before each command
	for command in commandsList:
		command.insert(0, '/usr/bin/sudo')
	commandStdout, commandStderr = trafficControl.executeCommandsList(commandsList)
	if globals.platformType == 'development':
		# --------------------------------------------------------------------------------------------------
		utils.displayText('blue', 'setting down all dmng network interfaces', 0)
		# --------------------------------------------------------------------------------------------------
		myDmng.setAllNetworkInterfacesState('down')

		# --------------------------------------------------------------------------------------------------
		utils.displayText('blue', 'setting up dmng\'s involved network interfaces', 0)
		# --------------------------------------------------------------------------------------------------
		utils.displayText('blue', 'setting up %d nbOfEthAdapters' % globals.nbOfEthAdapters, 0)
		for i in range(globals.nbOfEthAdapters):
			interfaceName = myDmng.ethAdaptersInterfacesList[i][0]
			myDmng.setNetworkInterfaceState(interfaceName, 'up')
			defaultGateway = myDmng.ethAdaptersInterfacesList[i][5]
			myDmng.setNetworkInterfaceDefaultGw(interfaceName, defaultGateway)

		utils.displayText('blue', 'setting up %d usbEthAdapters' % globals.nbOfUsbEthAdapters, 0)
		for i in range(globals.nbOfUsbEthAdapters):
			interfaceName = myDmng.usbEthAdaptersInterfacesList[i][0]
			myDmng.setNetworkInterfaceState(interfaceName, 'up')
			defaultGateway = myDmng.usbEthAdaptersInterfacesList[i][5]
			myDmng.setNetworkInterfaceDefaultGw(interfaceName, defaultGateway)

		utils.displayText('blue', 'setting up %d wifiAdapters' % globals.nbOfWifiAdapters, 0)
		for i in range(globals.nbOfWifiAdapters):
			interfaceName = myDmng.wifiAdaptersInterfacesList[i][0]
			myDmng.setNetworkInterfaceState(interfaceName, 'up')
			defaultGateway = myDmng.wifiAdaptersInterfacesList[i][5]
			myDmng.setNetworkInterfaceDefaultGw(interfaceName, defaultGateway)

		myDmng.killAviwestSstTx()
		myDmng.killKenCastFazzt()
		myDmng.killAllStreamer()

		if globals.useControlNetworkInterface:
			if aggregationMode == 'none':
				appliConfigurationFile = globals.scriptDirName + '/' + '../targetConfigurationFiles/without_aggregation/appli.conf'
			elif aggregationMode == 'aviwest':
				appliConfigurationFile = globals.scriptDirName + '/' + '../targetConfigurationFiles/with_aviwest_aggregation/appli.conf'
			elif aggregationMode == 'kencast':
				appliConfigurationFile = globals.scriptDirName + '/' + '../targetConfigurationFiles/with_kencast_aggregation/appli.conf'

			utils.patchAppliConfigurationFile(appliConfigurationFile)
			utils.remoteFileCopy(5322, appliConfigurationFile, 'admin@%s:/config/appli.conf' % myDmng.controlNetworkInterface[2])

		if aggregationMode == 'kencast':
			if globals.useControlNetworkInterface:
				# create configuration files on the fly
				fileHandle = open('../targetConfigurationFiles/with_kencast_aggregation/contact.conf', 'w')
				fileHandle.write('<object class="Contact" name="studio" username="aviwest" password="ibisdmng" ip="%s" url="%s">\n' % (globals.windowsVmStudioIpAddressForSstTraffic, globals.aggregationMasterLanIpAddress))
				fileHandle.close()

				fileHandle = open('../targetConfigurationFiles/with_kencast_aggregation/fazzt.conf', 'w')
				fileHandle.write('<object class="Fazzt" name="fazzt" livefec="20" filefec="10" timewindow="%d" packetsize="996">\n' % globals.timeWindow)
				fileHandle.close()

				fileHandle = open('../targetConfigurationFiles/with_kencast_aggregation/ibis.conf', 'w')
				fileHandle.write('<attribute name="contact" value="studio">\n')
				fileHandle.write('<attribute name="fazzt" value="fazzt">\n')
				fileHandle.write('<attribute name="videoRate" value="%d">\n' % globals.videoBitrate)
				fileHandle.write('<attribute name="audioRate" value="%d">\n' % globals.audioBitrate)
				fileHandle.write('<attribute name="path" value="%s">\n' % '/media/mmcblk1p1/test.mp4')
				fileHandle.write('<attribute name="rtpPort" value="1234">\n')
				fileHandle.close()

				# copy the generated configuration files on the dmng
				utils.remoteFileCopy(5322, globals.scriptDirName + '/' + '../targetConfigurationFiles/with_kencast_aggregation/contact.conf', 'admin@%s:/config/contact.conf' % myDmng.controlNetworkInterface[2])
				utils.remoteFileCopy(5322, globals.scriptDirName + '/' + '../targetConfigurationFiles/with_kencast_aggregation/fazzt.conf', 'admin@%s:/config/fazzt.conf' % myDmng.controlNetworkInterface[2])
				utils.remoteFileCopy(5322, globals.scriptDirName + '/' + '../targetConfigurationFiles/with_kencast_aggregation/ibis.conf', 'admin@%s:/config/ibis.conf' % myDmng.controlNetworkInterface[2])

		elif aggregationMode == 'aviwest':
			if args.build_last_sst_tx or args.sst_tx:
				if globals.useControlNetworkInterface:
					sstTxBinaryOnDmng = '/tmp/sst-tx'
					utils.remoteFileCopy(5322, globals.sstTxBinary, 'admin@%s:%s' % (myDmng.controlNetworkInterface[2], sstTxBinaryOnDmng))
			else:
				utils.displayText('yellow', '[WARNING] neither a sst-tx build requested nor a sst-tx specified : using the embedded one (This is certainly not what you want)', 0)
				sstTxBinaryOnDmng = '/app/bin/sst-tx'

			globals.appliVersion = myDmng.getAviwestSstTxVersion(sstTxBinaryOnDmng)
		else:
			globals.appliVersion = myDmng.getAppliVersion()

		utils.displayText('black', 'appliVersion : %s' % globals.appliVersion, 0)

	if args.disable_traffic_control_on_sender_side:
		utils.displayText('yellow', 'traffic control parameters not set on sender side', 0)
	else:
		# --------------------------------------------------------------------------------------------------
		utils.displayText('blue', 'setting up aggregationMaster\'s traffic control parameters on involved network interfaces', 0)
		# --------------------------------------------------------------------------------------------------
		for i in range(globals.nbOfEthAdapters):
			if globals.platformType == 'development':
				interfaceName = myDmng.ethAdaptersInterfacesList[i][0]
			elif globals.platformType == 'validation':
				interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[i][0]
			fixedLatency = globals.ethAdaptersFixedLatenciesList[i]
			jitter = globals.ethAdaptersJittersList[i]
			bandWidth = globals.ethAdaptersBandWidthsList[i]
			packetsLoss = globals.ethAdaptersPacketLossList[i]
			queueLength = globals.ethAdaptersQueueLengthList[i]
			if globals.platformType == 'development':
				networkDeviceDriver = myDmng.getNetworkDeviceDriver(interfaceName)
			elif globals.platformType == 'validation':
				networkDeviceDriver = 'r8169'
			commandsList = trafficControl.buildCommandsList(interfaceName, 'add', networkDeviceDriver, bandWidth, fixedLatency, jitter, packetsLoss, queueLength)
			if globals.platformType == 'development':
				for command in commandsList:
					commandString = ' '.join(command)
					myDmng.writeToSerial(commandString, [], 10)
			elif globals.platformType == 'validation':
				for command in commandsList:
					# insert /usr/bin/sudo before each command
					command.insert(0, '/usr/bin/sudo')
				commandStdout, commandStderr = trafficControl.executeCommandsList(commandsList)

		for i in range(globals.nbOfUsbEthAdapters):
			if globals.platformType == 'development':
				interfaceName = myDmng.usbEthAdaptersInterfacesList[i][0]
			elif globals.platformType == 'validation':
				interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[i][0]
			fixedLatency = globals.usbEthAdaptersFixedLatenciesList[i]
			jitter = globals.usbEthAdaptersJittersList[i]
			bandWidth = globals.usbEthAdaptersBandWidthsList[i]
			packetsLoss = globals.usbEthAdaptersPacketLossList[i]
			queueLength = globals.usbEthAdaptersQueueLengthList[i]
			if globals.platformType == 'development':
				networkDeviceDriver = myDmng.getNetworkDeviceDriver(interfaceName)
			elif globals.platformType == 'validation':
				networkDeviceDriver = 'r8169'
			commandsList = trafficControl.buildCommandsList(interfaceName, 'add', networkDeviceDriver, bandWidth, fixedLatency, jitter, packetsLoss, queueLength)
			if globals.platformType == 'development':
				for command in commandsList:
					commandString = ' '.join(command)
					myDmng.writeToSerial(commandString, [], 10)
			elif globals.platformType == 'validation':
				for command in commandsList:
					# insert /usr/bin/sudo before each command
					command.insert(0, '/usr/bin/sudo')
				commandStdout, commandStderr = trafficControl.executeCommandsList(commandsList)

		for i in range(globals.nbOfWifiAdapters):
			if globals.platformType == 'development':
				interfaceName = myDmng.wifiAdaptersInterfacesList[i][0]
			elif globals.platformType == 'validation':
				interfaceName = networkInterfaces.testNetworkAliasesList[1 + i + globals.maxNbOfEthAdapters + globals.maxNbOfUsbEthAdapters][0]
			fixedLatency = globals.wifiAdaptersFixedLatenciesList[i]
			jitter = globals.wifiAdaptersJittersList[i]
			bandWidth = globals.wifiAdaptersBandWidthsList[i]
			packetsLoss = globals.wifiAdaptersPacketLossList[i]
			queueLength = globals.wifiAdaptersQueueLengthList[i]
			if globals.platformType == 'development':
				networkDeviceDriver = myDmng.getNetworkDeviceDriver(interfaceName)
			elif globals.platformType == 'validation':
				networkDeviceDriver = 'r8169'
			commandsList = trafficControl.buildCommandsList(interfaceName, 'add', networkDeviceDriver, bandWidth, fixedLatency, jitter, packetsLoss, queueLength)
			if globals.platformType == 'development':
				for command in commandsList:
					commandString = ' '.join(command)
					myDmng.writeToSerial(commandString, [], 10)
			elif globals.platformType == 'validation':
				for command in commandsList:
					# insert /usr/bin/sudo before each command
					command.insert(0, '/usr/bin/sudo')
				commandStdout, commandStderr = trafficControl.executeCommandsList(commandsList)

	if args.disable_traffic_control_on_receiver_side:
		utils.displayText('yellow', 'traffic control parameters not set on receiver side', 0)
	else:
		if aggregationMode == 'none' or aggregationMode == 'kencast':
			receiverInterface = globals.windowsVmStudioTrafficLanIfc
		elif aggregationMode == 'aviwest':
			receiverInterface = globals.linuxVmStudioTrafficLanIfc
		# --------------------------------------------------------------------------------------------------
		utils.displayText('blue', 'setting up %s\'s traffic control parameters' % receiverInterface, 0)
		# --------------------------------------------------------------------------------------------------
		commandsList = trafficControl.buildCommandsList(receiverInterface, 'add', 'virtualBox', globals.gatewayBandWidth, globals.gatewayFixedLatency, globals.gatewayInstantJitter, globals.gatewayPacketsLoss, globals.gatewayQueueLength)
		# insert /usr/bin/sudo before each command
		for command in commandsList:
			command.insert(0, '/usr/bin/sudo')
		commandStdout, commandStderr = trafficControl.executeCommandsList(commandsList)


	if aggregationMode == 'aviwest' or aggregationMode == 'kencast':
		# --------------------------------------------------------------------------------------------------
		utils.displayText('blue', 'starting %s aggregation test' % aggregationMode, 0)
		# --------------------------------------------------------------------------------------------------

	if aggregationMode == 'aviwest':
		if globals.platformType == 'development':
			# --------------------------------------------------------------------------------------------------
			utils.displayText('blue', 'starting sst-rx on studio-sst-rx', 0)
			# --------------------------------------------------------------------------------------------------
			# delete any remaining os.path.basename(globals.gatewaySstRxLogFile) file for later results copy
			if os.path.isfile(globals.scriptDirName + '/' + os.path.basename(globals.gatewaySstRxLogFile)):
				os.remove(globals.scriptDirName + '/' + os.path.basename(globals.gatewaySstRxLogFile))

			# new instance of studioSstRx
			myStudioSstRx = studioSstRx.studioSstRx(globals.linuxVmStudioIpAddressForSsh, 22)

			utils.displayText('cyan', 'killing any remaining sst-rx instance', 0)
			myStudioSstRx.kill()

			if args.build_last_sst_rx or args.sst_rx:
				utils.displayText('blue', 'copying sst-rx', 0)
				utils.displayText('cyan', 'copying file %s on sst-rx to %s' % (file, globals.gatewaySstRxBinary), 0)
				utils.remoteFileCopy(22, globals.sstRxBinary, '%s:%s' % (globals.linuxVmStudioIpAddressForSsh, globals.gatewaySstRxBinary))

			utils.displayText('cyan', 'starting an instance of sst-rx', 0)
			myStudioSstRx.start()

			myDmng.startAviwestSstTx(sstTxBinaryOnDmng, globals.audioBitrate, globals.videoBitrate, globals.frameRate, globals.gopDuration, globals.iFramesVsPandBFramesRatio)
		elif globals.platformType == 'validation':
			utils.displayText('red', 'TODO', 0)
			utils.terminateTest(1)

	if aggregationMode == 'kencast':
		if globals.platformType == 'development':
			myDmng.startKenCastFazzt('/opt/Fazzt/bin/fazzt')

	if aggregationMode == 'aviwest' or aggregationMode == 'kencast':
		if globals.actionMode == 'live_bw_test':
			if globals.platformType == 'development':
				# --------------------------------------------------------------------------------------------------
				utils.displayText('cyan', 'starting %s bandwidth test' % aggregationMode, 0)
				# --------------------------------------------------------------------------------------------------
				if aggregationMode == 'aviwest':
					myDmng.startAviwestBwTest()
				elif aggregationMode == 'kencast':
					myDmng.startKenCastBwTest()

			if globals.platformType == 'development':
				# --------------------------------------------------------------------------------------------------
				utils.displayText('cyan', '%s bandwidth test in progress...' % aggregationMode, globals.bwTestDuration)
				# --------------------------------------------------------------------------------------------------
				# --------------------------------------------------------------------------------------------------
				utils.displayText('cyan', 'stopping %s bandwidth test' % aggregationMode, 0)
				# --------------------------------------------------------------------------------------------------
				if aggregationMode == 'aviwest':
					estimatedBitrate = myDmng.stopAviwestBwTest()
				elif aggregationMode == 'kencast':
					estimatedBitrate = myDmng.stopKenCastBwTest()
			elif globals.platformType == 'validation':
				utils.displayText('yellow', 'you have to stop bandwidth test manually', 0)

		if globals.actionMode == 'live_bw_test' or globals.actionMode == 'live':
			if globals.platformType == 'development':
				# --------------------------------------------------------------------------------------------------
				utils.displayText('cyan', 'starting %s streaming test' % aggregationMode, 0)
				# --------------------------------------------------------------------------------------------------
				if aggregationMode == 'aviwest':
					myDmng.startAviwestStreaming(globals.timeWindow)
				elif aggregationMode == 'kencast':
					myDmng.startKenCastStreaming()

	if aggregationMode == 'none' or aggregationMode == 'kencast':
		if globals.platformType == 'development':
			# --------------------------------------------------------------------------------------------------
			utils.displayText('blue', 'starting encoder', 0)
			# --------------------------------------------------------------------------------------------------
			myDmng.startEncoder()
			# --------------------------------------------------------------------------------------------------
			utils.displayText('blue', 'starting streamer', 0)
			# --------------------------------------------------------------------------------------------------
			myDmng.startStreamer(globals.timeWindow)
			
		if globals.platformType == 'validation':
			utils.displayText('yellow', 'start streaming manually on the dmng and press enter when ready', 0)
			input()
			
	globals.streamingStartTime = time.time()

	# --------------------------------------------------------------------------------------------------
	# if globals.scenarioEvolution is set to '3G links simulation', take into account link parameters variations over the time
	# else, wait for globals.scenarioDuration
	# --------------------------------------------------------------------------------------------------
	if not args.disable_traffic_control_on_sender_side and (globals.scenarioEvolution == '3G links simulation'):
		scenarioDirectory = globals.scriptDirName + '/../scenarii/%s/' % globals.scenarioId
		if not os.path.isdir(scenarioDirectory):
			utils.displayText('red', 'scenarioDirectory (%s) does not exist' % scenarioDirectory, 0)
			sys.exit(1)
		for i in range(globals.nbOfEthAdapters):
			if globals.platformType == 'development':
				interfaceName = myDmng.ethAdaptersInterfacesList[i][0]
			elif globals.platformType == 'validation':
				interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[i][0]
			interfaceEvolutionFileName = scenarioDirectory + interfaceName + '.txt'
			if os.path.isfile(interfaceEvolutionFileName):
				threadName = interfaceName + '_trafficControlThread'
				if globals.platformType == 'development':
					threadName = threading.Thread(None, trafficControl.driveLinkTrafficControl, None, (interfaceName, interfaceEvolutionFileName, myDmng,), {'threadName':'thread %s' % threadName})
				elif globals.platformType == 'validation':
					threadName = threading.Thread(None, trafficControl.driveLinkTrafficControl, None, (interfaceName, interfaceEvolutionFileName,), {'threadName':'thread %s' % threadName})
				threadName.start()
			else:
				utils.displayText('yellow', '[WARNING] interfaceEvolutionFileName (%s) does not exist' % interfaceEvolutionFileName, 0)

		for i in range(globals.nbOfUsbEthAdapters):
			if globals.platformType == 'development':
				interfaceName = myDmng.usbEthAdaptersInterfacesList[i][0]
			elif globals.platformType == 'validation':
				interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[i][0]
			interfaceEvolutionFileName = scenarioDirectory + interfaceName + '.txt'
			if os.path.isfile(interfaceEvolutionFileName):
				threadName = interfaceName + '_trafficControlThread'
				if globals.platformType == 'development':
					threadName = threading.Thread(None, trafficControl.driveLinkTrafficControl, None, (interfaceName, interfaceEvolutionFileName, myDmng,), {'threadName':'thread %s' % threadName})
				elif globals.platformType == 'validation':
					threadName = threading.Thread(None, trafficControl.driveLinkTrafficControl, None, (interfaceName, interfaceEvolutionFileName,), {'threadName':'thread %s' % threadName})
				threadName.start()
			else:
				utils.displayText('yellow', '[WARNING] interfaceEvolutionFileName (%s) does not exist' % interfaceEvolutionFileName, 0)

		for i in range(globals.nbOfWifiAdapters):
			if globals.platformType == 'development':
				interfaceName = myDmng.wifiAdaptersInterfacesList[i][0]
			elif globals.platformType == 'validation':
				interfaceName = networkInterfaces.testNetworkAliasesList[1 + i + globals.maxNbOfEthAdapters + globals.maxNbOfUsbEthAdapters][0]
			interfaceEvolutionFileName = scenarioDirectory + interfaceName + '.txt'
			if os.path.isfile(interfaceEvolutionFileName):
				threadName = interfaceName + '_trafficControlThread'
				if globals.platformType == 'development':
					threadName = threading.Thread(None, trafficControl.driveLinkTrafficControl, None, (interfaceName, interfaceEvolutionFileName, myDmng), {'threadName':'thread %s' % threadName})
				elif globals.platformType == 'validation':
					threadName = threading.Thread(None, trafficControl.driveLinkTrafficControl, None, (interfaceName, interfaceEvolutionFileName,), {'threadName':'thread %s' % threadName})
				threadName.start()
			else:
				utils.displayText('yellow', '[WARNING] interfaceEvolutionFileName (%s) does not exist' % interfaceEvolutionFileName, 0)

	# --------------------------------------------------------------------------------------------------
	utils.displayText('cyan', '%s streaming test in progress...' % aggregationMode, globals.scenarioDuration)
	# --------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------
	utils.displayText('cyan', 'stopping %s streaming test' % aggregationMode, 0)
	# --------------------------------------------------------------------------------------------------
	if globals.platformType == 'development':
		if aggregationMode == 'aviwest':
			minVideoBitrate, maxVideoBitrate, avgVideoBitrate, minAudioBitrate, maxAudioBitrate, avgAudioBitrate = myDmng.stopAviwestStreaming()
		elif aggregationMode == 'kencast':
			myDmng.stopKenCastStreaming()

	elif globals.platformType == 'validation':
		utils.displayText('yellow', 'you have to stop %s streaming test manually' % aggregationMode, 0)
		utils.displayText('yellow', '/app/fazzt/scripts/StreamStop.fzt', 0)
		utils.displayText('yellow', '/app/fazzt/scripts/ConnectionStatus.fzt', 0)
		utils.displayText('yellow', 'echo $?', 0)

	if not globals.quiet:
		# --------------------------------------------------------------------------------------------------
		utils.displayText('blue', 'displaying %s\'s traffic control parameters on involved network interfaces' % deviceOnWhichSettingTc, 0)
		# --------------------------------------------------------------------------------------------------

		for i in range(globals.nbOfEthAdapters):
			if globals.platformType == 'development':
				interfaceName = myDmng.ethAdaptersInterfacesList[i][0]
			elif globals.platformType == 'validation':
				interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[i][0]
			commandsList = trafficControl.buildCommandsListForDisplay(interfaceName)
			if globals.platformType == 'development':
				for command in commandsList:
					commandString = ' '.join(command)
					serialOutputUntilTimeout = myDmng.writeToSerial(commandString, ['backlog'], 10)
					utils.displayText('normal', 'serialOutputUntilTimeout :\n%s' % serialOutputUntilTimeout, 0)
			elif globals.platformType == 'validation':
				for command in commandsList:
					# insert /usr/bin/sudo before each command
					command.insert(0, '/usr/bin/sudo')
				commandStdout, commandStderr = trafficControl.executeCommandsList(commandsList)

		for i in range(globals.nbOfUsbEthAdapters):
			if globals.platformType == 'development':
				interfaceName = myDmng.usbEthAdaptersInterfacesList[i][0]
			elif globals.platformType == 'validation':
				interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[i][0]
			commandsList = trafficControl.buildCommandsListForDisplay(interfaceName)
			if globals.platformType == 'development':
				for command in commandsList:
					commandString = ' '.join(command)
					serialOutputUntilTimeout = myDmng.writeToSerial(commandString, ['backlog'], 10)
					utils.displayText('normal', 'serialOutputUntilTimeout :\n%s' % serialOutputUntilTimeout, 0)
			elif globals.platformType == 'validation':
				for command in commandsList:
					# insert /usr/bin/sudo before each command
					command.insert(0, '/usr/bin/sudo')
				commandStdout, commandStderr = trafficControl.executeCommandsList(commandsList)

		for i in range(globals.nbOfWifiAdapters):
			if globals.platformType == 'development':
				interfaceName = myDmng.wifiAdaptersInterfacesList[i][0]
			elif globals.platformType == 'validation':
				interfaceName = networkInterfaces.testNetworkAliasesList[1 + i + globals.maxNbOfEthAdapters + globals.maxNbOfUsbEthAdapters][0]
			commandsList = trafficControl.buildCommandsListForDisplay(interfaceName)
			if globals.platformType == 'development':
				for command in commandsList:
					commandString = ' '.join(command)
					serialOutputUntilTimeout = myDmng.writeToSerial(commandString, ['backlog'], 10)
					utils.displayText('normal', 'serialOutputUntilTimeout :\n%s' % serialOutputUntilTimeout, 0)
			elif globals.platformType == 'validation':
				for command in commandsList:
					# insert /usr/bin/sudo before each command
					command.insert(0, '/usr/bin/sudo')
				commandStdout, commandStderr = trafficControl.executeCommandsList(commandsList)

		if aggregationMode == 'none' or aggregationMode == 'kencast':
			receiverInterface = globals.windowsVmStudioTrafficLanIfc
		elif aggregationMode == 'aviwest':
			receiverInterface = globals.linuxVmStudioTrafficLanIfc

		# --------------------------------------------------------------------------------------------------
		utils.displayText('blue', 'displaying %s\'s traffic control parameters' % receiverInterface, 0)
		# --------------------------------------------------------------------------------------------------
		commandsList = trafficControl.buildCommandsListForDisplay(receiverInterface)
		# insert /usr/bin/sudo before each command
		for command in commandsList:
			command.insert(0, '/usr/bin/sudo')
		commandStdout, commandStderr = trafficControl.executeCommandsList(commandsList)
		utils.displayText('normal', 'commandStdout :', 0)
		utils.displayText('normal', commandStdout, 0)
		utils.displayText('normal', 'commandStderr :', 0)
		utils.displayText('normal', commandStderr, 0)

	if globals.platformType == 'development':
		if aggregationMode == 'aviwest':
			# --------------------------------------------------------------------------------------------------
			utils.displayText('blue', 'stopping sst-rx on studio-sst-rx', 0)
			# --------------------------------------------------------------------------------------------------
			utils.displayText('cyan', 'killing any remaining sst-rx instance', 0)
			myStudioSstRx.kill()
			utils.displayText('cyan', 'terminating sst-rx', 0)
			myStudioSstRx.ssh.terminate()

			# retrieve globals.gatewaySstRxLogFile
			utils.remoteFileCopy(22, '%s:%s' % (globals.linuxVmStudioIpAddressForSsh, globals.gatewaySstRxLogFile), globals.scriptDirName)

			# check statistics
			#utils.displayText('red', 'globals.audioBitrate : %s' % globals.audioBitrate, 0)
			#utils.displayText('red', 'globals.videoBitrate : %s' % globals.videoBitrate, 0)
			#utils.displayText('red', 'avgAudioBitrate : %s' % avgAudioBitrate, 0)
			#utils.displayText('red', 'avgVideoBitrate : %s' % avgVideoBitrate, 0)

			if globals.actionMode == 'live_bw_test':
				diffRatioBwTest=40
				if int(estimatedBitrate - diffRatioBwTest * estimatedBitrate / 100) < avgVideoBitrate < int(estimatedBitrate + diffRatioBwTest * estimatedBitrate / 100):
					utils.displayText('green', '[OK] avgVideoBitrate (%d) equals at +/- %d%% estimatedBitrate (%d)' % (avgVideoBitrate, diffRatioBwTest, estimatedBitrate), 0)
				else:
					utils.displayText('red', '[KO] avgVideoBitrate (%d) does not equal at +/- %d%% estimatedBitrate (%d)' % (avgVideoBitrate, diffRatioBwTest, estimatedBitrate), 0)
					utils.terminateTest(1)

			diffRatioStreamingTest=20
			if int(globals.audioBitrate - diffRatioStreamingTest * globals.audioBitrate / 100) < avgAudioBitrate < int(globals.audioBitrate + diffRatioStreamingTest * globals.audioBitrate / 100):
				utils.displayText('green', '[OK] avgAudioBitrate (%d) equals at +/- %d%% scenario audioBitrate (%d)' % (avgAudioBitrate, diffRatioStreamingTest, globals.audioBitrate), 0)
			else:
				utils.displayText('red', '[KO] avgAudioBitrate (%d) does not equal at +/- %d%% scenario audioBitrate (%d)' % (avgAudioBitrate, diffRatioStreamingTest, globals.audioBitrate), 0)
				utils.terminateTest(1)
			#if int(globals.videoBitrate - diffRatioStreamingTest * globals.videoBitrate / 100) < avgVideoBitrate < int(globals.videoBitrate + diffRatioStreamingTest * globals.videoBitrate / 100):
			#	utils.displayText('green', '[OK] avgVideoBitrate (%d) equals at +/- %d%% scenario videoBitrate (%d)' % (avgVideoBitrate, diffRatioStreamingTest, globals.videoBitrate), 0)
			#else:
			#	utils.displayText('red', '[KO] avgVideoBitrate (%d) does not equal at +/- %d%% scenario videoBitrate (%d)' % (avgVideoBitrate, diffRatioStreamingTest, globals.videoBitrate), 0)
			#	utils.terminateTest(1)

		## --------------------------------------------------------------------------------------------------
		#utils.displayText('blue', 'stopping sst-rx on studio-sst-rx', 0)
		## --------------------------------------------------------------------------------------------------

		#utils.displayText('cyan', 'killing any remaining sst-rx instance', 0)
		#myStudioSstRx.kill()

		#utils.displayText('cyan', 'terminating sst-rx', 0)
		#myStudioSstRx.ssh.terminate()

		## retrieve globals.gatewaySstRxLogFile
		#utils.remoteFileCopy(22, '%s:%s' % (globals.linuxVmStudioIpAddressForSsh, globals.gatewaySstRxLogFile), globals.scriptDirName)

		# check statistics
		#utils.displayText('red', 'globals.audioBitrate : %s' % globals.audioBitrate, 0)
		#utils.displayText('red', 'globals.videoBitrate : %s' % globals.videoBitrate, 0)
		#utils.displayText('red', 'avgAudioBitrate : %s' % avgAudioBitrate, 0)
		#utils.displayText('red', 'avgVideoBitrate : %s' % avgVideoBitrate, 0)

		#if globals.actionMode == 'live_bw_test':
		#	diffRatioBwTest=40
		#	if int(estimatedBitrate - diffRatioBwTest * estimatedBitrate / 100) < avgVideoBitrate < int(estimatedBitrate + diffRatioBwTest * estimatedBitrate / 100):
		#		utils.displayText('green', '[OK] avgVideoBitrate (%d) equals at +/- %d%% estimatedBitrate (%d)' % (avgVideoBitrate, diffRatioBwTest, estimatedBitrate), 0)
		#	else:
		#		utils.displayText('red', '[KO] avgVideoBitrate (%d) does not equal at +/- %d%% estimatedBitrate (%d)' % (avgVideoBitrate, diffRatioBwTest, estimatedBitrate), 0)
		#		utils.terminateTest(1)

		#diffRatioStreamingTest=20
		#if int(globals.audioBitrate - diffRatioStreamingTest * globals.audioBitrate / 100) < avgAudioBitrate < int(globals.audioBitrate + diffRatioStreamingTest * globals.audioBitrate / 100):
		#	utils.displayText('green', '[OK] avgAudioBitrate (%d) equals at +/- %d%% scenario audioBitrate (%d)' % (avgAudioBitrate, diffRatioStreamingTest, globals.audioBitrate), 0)
		#else:
		#	utils.displayText('red', '[KO] avgAudioBitrate (%d) does not equal at +/- %d%% scenario audioBitrate (%d)' % (avgAudioBitrate, diffRatioStreamingTest, globals.audioBitrate), 0)
		#	utils.terminateTest(1)
		#if int(globals.videoBitrate - diffRatioStreamingTest * globals.videoBitrate / 100) < avgVideoBitrate < int(globals.videoBitrate + diffRatioStreamingTest * globals.videoBitrate / 100):
		#	utils.displayText('green', '[OK] avgVideoBitrate (%d) equals at +/- %d%% scenario videoBitrate (%d)' % (avgVideoBitrate, diffRatioStreamingTest, globals.videoBitrate), 0)
		#else:
		#	utils.displayText('red', '[KO] avgVideoBitrate (%d) does not equal at +/- %d%% scenario videoBitrate (%d)' % (avgVideoBitrate, diffRatioStreamingTest, globals.videoBitrate), 0)
		#	utils.terminateTest(1)

if globals.platformType == 'development':
	myDmng.disconnectFromSerial()
del(myDmng)

utils.terminateTest(0)
