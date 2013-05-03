#! /usr/bin/python
# -*- coding: utf-8 -*-

# import python libraries
import argparse
#import subprocess
import time

# import aggregation-platform's libraries
import dmng
import globals
import networkInterfaces
import utils

def initChains():
	utils.displayText('cyan', 'initializing chains...', 0)

	commandsList = []
	'''
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--flush', 'INPUT'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--flush', 'OUTPUT'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--flush', 'FORWARD'])
	'''
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--flush'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--flush', '--table', 'nat'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--flush', '--table', 'mangle'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--delete-chain'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--delete-chain', '--table', 'nat'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--delete-chain', '--table', 'mangle'])

	for command in commandsList:
		commandStdout, commandStderr = utils.executeCommand(command)

	#utils.displayText('cyan', 'protective filter activation...', 0)
	#displayText cyan " Protective filter activation..." "noNewLine" $logFileName
	#for filter in /proc/sys/net/ipv4/conf/*/rp_filter
	#do
	#	echo "1" > $filter
	#done
	#displayText green " OK" "newLine" $logFileName

	# in file /etc/sysctl.conf, set : net.ipv4.ip_forward=1

	#displayText cyan " IP forwarding activation..." "noNewLine" $logFileName
	#echo "1" > /proc/sys/net/ipv4/ip_forward
	#displayText green " OK" "newLine" $logFileName

def setDefaultPolicy():
	utils.displayText('cyan', 'setting default policy...', 0)

	commandsList = []
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--policy', 'INPUT', 'DROP'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--policy', 'OUTPUT', 'DROP'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--policy', 'FORWARD', 'DROP'])

	for command in commandsList:
		commandStdout, commandStderr = utils.executeCommand(command)

def setInputRules(dmngObject):

	# initializations
	loopbackIfc = 'lo'

	utils.displayText('cyan', 'setting input rules...', 0)

	commandsList = []

	# allow input traffic for established connections
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--match', 'state', '--state', 'ESTABLISHED,RELATED', '--in-interface', loopbackIfc, '--jump', 'ACCEPT'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--match', 'state', '--state', 'ESTABLISHED,RELATED', '--in-interface', globals.aviwestLanIfc, '--jump', 'ACCEPT'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--match', 'state', '--state', 'ESTABLISHED,RELATED', '--in-interface', globals.dmngLanIfc, '--jump', 'ACCEPT'])
	if globals.platformType == 'validation':
		for i in range(globals.maxNbOfEthAdapters):
			interfaceName = dmngObject.ethAdaptersInterfacesList[i][0]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--match', 'state', '--state', 'ESTABLISHED,RELATED', '--in-interface', interfaceName, '--jump', 'ACCEPT'])
		for i in range(globals.maxNbOfUsbEthAdapters):
			interfaceName = dmngObject.usbEthAdaptersInterfacesList[i][0]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--match', 'state', '--state', 'ESTABLISHED,RELATED', '--in-interface', interfaceName, '--jump', 'ACCEPT'])

	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--match', 'state', '--state', 'ESTABLISHED,RELATED', '--in-interface', globals.linuxVmStudioTrafficLanIfc, '--jump', 'ACCEPT'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--match', 'state', '--state', 'ESTABLISHED,RELATED', '--in-interface', globals.linuxVmStudioSshLanIfc, '--jump', 'ACCEPT'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--match', 'state', '--state', 'ESTABLISHED,RELATED', '--in-interface', globals.windowsVmStudioTrafficLanIfc, '--jump', 'ACCEPT'])

	# allow all input traffic on loopbackIfc
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', loopbackIfc, '--jump', 'ACCEPT'])

	# allow icmp
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', globals.aviwestLanIfc, '--protocol', 'icmp', '--jump', 'ACCEPT'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', globals.dmngLanIfc, '--protocol', 'icmp', '--jump', 'ACCEPT'])
	if globals.platformType == 'validation':
		for i in range(globals.maxNbOfEthAdapters):
			interfaceName = dmngObject.ethAdaptersInterfacesList[i][0]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', interfaceName, '--protocol', 'icmp', '--jump', 'ACCEPT'])
		for i in range(globals.maxNbOfUsbEthAdapters):
			interfaceName = dmngObject.usbEthAdaptersInterfacesList[i][0]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', interfaceName, '--protocol', 'icmp', '--jump', 'ACCEPT'])

	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', globals.linuxVmStudioTrafficLanIfc, '--protocol', 'icmp', '--jump', 'ACCEPT'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', globals.linuxVmStudioSshLanIfc, '--protocol', 'icmp', '--jump', 'ACCEPT'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', globals.windowsVmStudioTrafficLanIfc, '--protocol', 'icmp', '--jump', 'ACCEPT'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', dmngObject.controlNetworkInterface[0], '--protocol', 'icmp', '--jump', 'ACCEPT'])

	# allow icmp on ethAdaptersInterfacesList and usbEthAdaptersInterfacesList
	if globals.platformType == 'validation':
		for i in range(globals.maxNbOfEthAdapters):
			interfaceName = dmngObject.ethAdaptersInterfacesList[i][0]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', interfaceName, '--protocol', 'icmp', '--jump', 'ACCEPT'])
		for i in range(globals.maxNbOfUsbEthAdapters):
			interfaceName = dmngObject.usbEthAdaptersInterfacesList[i][0]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', interfaceName, '--protocol', 'icmp', '--jump', 'ACCEPT'])

	# allow ssh
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', globals.aviwestLanIfc, '--protocol', 'tcp', '--destination-port', '22', '--jump', 'ACCEPT'])
	#commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', globals.dmngLanIfc, '--protocol', 'tcp', '--destination-port', '22', '--jump', 'ACCEPT'])

	# allow apache 2
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', globals.aviwestLanIfc, '--protocol', 'tcp', '--destination-port', '80', '--jump', 'ACCEPT'])

	# allow synergy
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', globals.aviwestLanIfc, '--protocol', 'tcp', '--destination-port', '24800', '--jump', 'ACCEPT'])

	# allow iperf TCP/UDP default port
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', globals.dmngLanIfc, '--protocol', 'tcp', '--destination-port', '5001', '--jump', 'ACCEPT'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', globals.dmngLanIfc, '--protocol', 'udp', '--destination-port', '5001', '--jump', 'ACCEPT'])
	if globals.platformType == 'validation':
		for i in range(globals.maxNbOfEthAdapters):
			interfaceName = dmngObject.ethAdaptersInterfacesList[i][0]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', interfaceName, '--protocol', 'tcp', '--destination-port', '5001', '--jump', 'ACCEPT'])
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', interfaceName, '--protocol', 'udp', '--destination-port', '5001', '--jump', 'ACCEPT'])
		for i in range(globals.maxNbOfUsbEthAdapters):
			interfaceName = dmngObject.usbEthAdaptersInterfacesList[i][0]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', interfaceName, '--protocol', 'tcp', '--destination-port', '5001', '--jump', 'ACCEPT'])
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'INPUT', '--in-interface', interfaceName, '--protocol', 'udp', '--destination-port', '5001', '--jump', 'ACCEPT'])

	for command in commandsList:
		commandStdout, commandStderr = utils.executeCommand(command)

def setOutputRules():
	utils.displayText('cyan', 'setting output rules...', 0)

	commandsList = []

	# allow output traffic for established connections
	##commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'OUTPUT', '--match', state, '--state', 'RELATED,ESTABLISHED', '--jump', 'ACCEPT'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'OUTPUT', '--match', 'state', '!', '--state', 'INVALID', '--jump', 'ACCEPT'])

	# allow everything for now (TODO)
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'OUTPUT', '--jump', 'ACCEPT'])

	for command in commandsList:
		commandStdout, commandStderr = utils.executeCommand(command)

def setForwardRules():
	utils.displayText('cyan', 'setting forward rules...', 0)

	commandsList = []

	# allow forward traffic for established connections
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'FORWARD', '--match', 'state', '--state', 'RELATED,ESTABLISHED', '--jump', 'ACCEPT'])

	# allow all forward traffic on all interfaces
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'FORWARD', '--jump', 'ACCEPT'])

	# for testing ssh
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--append', 'FORWARD', '--in-interface', globals.aviwestLanIfc, '--destination', globals.linuxVmStudioIpAddressForSsh, '--protocol', 'tcp', '--destination-port', '22', '--jump', 'ACCEPT'])

	for command in commandsList:
		commandStdout, commandStderr = utils.executeCommand(command)

def setNatPostroutingRules():
	utils.displayText('cyan', 'setting nat postrouting rules (source NAT)...', 0)

	commandsList = []

	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'POSTROUTING', '--out-interface', globals.aviwestLanIfc, '--jump', 'MASQUERADE'])

	# allow any kind of traffic to go back from studio to globals.dmngLanIfc
	if globals.platformType == 'development':
		commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'POSTROUTING', '--out-interface', globals.dmngLanIfc, '--jump', 'MASQUERADE'])
	if globals.platformType == 'validation':
		for index in range(0, len(networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter)):
			interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[index][0]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'POSTROUTING', '--out-interface', interfaceName, '--jump', 'MASQUERADE'])
			
		for index in range(0, len(networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter)):
			interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[index][0]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'POSTROUTING', '--out-interface', interfaceName, '--jump', 'MASQUERADE'])

	#commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'POSTROUTING', '--source', '192.168.56.0/255.255.255.0', '--out-interface', globals.aviwestLanIfc, '--jump', 'MASQUERADE'])
	#commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'POSTROUTING', '--source', '127.0.0.1/255.255.255.0', '--out-interface', globals.aviwestLanIfc, '--jump', 'MASQUERADE'])

	#commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'POSTROUTING', '--out-interface', globals.linuxVmStudioTrafficLanIfc, '--jump', 'MASQUERADE'])
	#commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'POSTROUTING', '--out-interface', globals.linuxVmStudioSshLanIfc, '--jump', 'MASQUERADE'])
	#commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'POSTROUTING', '--out-interface', globals.windowsVmStudioTrafficLanIfc, '--jump', 'MASQUERADE'])

	for command in commandsList:
		commandStdout, commandStderr = utils.executeCommand(command)

def setNatOutputRules():
	utils.displayText('cyan', 'setting nat output rules rules...', 0)

	commandsList = []

	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'OUTPUT', '--jump', 'ACCEPT'])

	for command in commandsList:
		commandStdout, commandStderr = utils.executeCommand(command)

def setNatPreroutingRules(dmngObject):
	utils.displayText('cyan', 'setting nat prerouting rules (destination NAT)...', 0)

	commandsList = []

	# allow iperf TCP/UDP default port
	'''
	if globals.platformType == 'validation':
		for index in range(0, len(networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter)):
			interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[index][0]
			ipNetwork = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[index][2]
			networkMask = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[index][4]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'udp', '--source', '%s/%s' % (ipNetwork, networkMask), '--source-port', '46065', '--jump', 'DNAT', '--to-destination', '%s' % globals.windowsVmStudioIpAddressForSstTraffic])
		for index in range(0, len(networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter)):
			interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[index][0]
			ipNetwork = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[index][2]
			networkMask = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[index][4]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'udp', '--source', '%s/%s' % (ipNetwork, networkMask), '--source-port', '46065', '--jump', 'DNAT', '--to-destination', '%s' % globals.windowsVmStudioIpAddressForSstTraffic])
	'''
	
	# for Aviwest aggregation
	if globals.platformType == 'development':
		for index in range(1, len(networkInterfaces.testNetworkAliasesList)):
			interfaceName = networkInterfaces.testNetworkAliasesList[index][0]
			ipNetwork = networkInterfaces.testNetworkAliasesList[index][2]
			networkMask = networkInterfaces.testNetworkAliasesList[index][4]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'udp', '--source', '%s/%s' % (ipNetwork, networkMask), '--destination-port', '7900:7940', '--jump', 'DNAT', '--to-destination', '%s' % globals.linuxVmStudioIpAddressForSstTraffic])
	if globals.platformType == 'validation':
		for index in range(0, len(networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter)):
			interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[index][0]
			ipNetwork = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[index][2]
			networkMask = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[index][4]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'udp', '--source', '%s/%s' % (ipNetwork, networkMask), '--destination-port', '7900:7940', '--jump', 'DNAT', '--to-destination', '%s' % globals.linuxVmStudioIpAddressForSstTraffic])
		for index in range(0, len(networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter)):
			interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[index][0]
			ipNetwork = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[index][2]
			networkMask = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[index][4]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'udp', '--source', '%s/%s' % (ipNetwork, networkMask), '--destination-port', '7900:7940', '--jump', 'DNAT', '--to-destination', '%s' % globals.linuxVmStudioIpAddressForSstTraffic])

	# for KenCast aggregation
	if globals.platformType == 'development':
		for index in range(1, len(networkInterfaces.testNetworkAliasesList)):
			interfaceName = networkInterfaces.testNetworkAliasesList[index][0]
			ipNetwork = networkInterfaces.testNetworkAliasesList[index][2]
			networkMask = networkInterfaces.testNetworkAliasesList[index][4]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'udp', '--source', '%s/%s' % (ipNetwork, networkMask), '--destination-port', '8000:8050', '--jump', 'DNAT', '--to-destination', '%s' % globals.windowsVmStudioIpAddressForSstTraffic])
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'tcp', '--source', '%s/%s' % (ipNetwork, networkMask), '--destination-port', '%d' % 4038, '--jump', 'DNAT', '--to-destination', '%s' % globals.windowsVmStudioIpAddressForSstTraffic])

	if globals.platformType == 'validation':
		for index in range(0, len(networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter)):
			interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[index][0]
			ipNetwork = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[index][2]
			networkMask = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[index][4]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'udp', '--source', '%s/%s' % (ipNetwork, networkMask), '--destination-port', '8000:8050', '--jump', 'DNAT', '--to-destination', '%s' % globals.windowsVmStudioIpAddressForSstTraffic])
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'tcp', '--source', '%s/%s' % (ipNetwork, networkMask), '--destination-port', '%d' % 4038, '--jump', 'DNAT', '--to-destination', '%s' % globals.windowsVmStudioIpAddressForSstTraffic])

		for index in range(0, len(networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter)):
			interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[index][0]
			ipNetwork = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[index][2]
			networkMask = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[index][4]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'udp', '--source', '%s/%s' % (ipNetwork, networkMask), '--destination-port', '8000:8050', '--jump', 'DNAT', '--to-destination', '%s' % globals.windowsVmStudioIpAddressForSstTraffic])
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'tcp', '--source', '%s/%s' % (ipNetwork, networkMask), '--destination-port', '%d' % 4038, '--jump', 'DNAT', '--to-destination', '%s' % globals.windowsVmStudioIpAddressForSstTraffic])

	# without any aggregation
	if globals.platformType == 'development':
		for index in range(1, len(networkInterfaces.testNetworkAliasesList)):
			interfaceName = networkInterfaces.testNetworkAliasesList[index][0]
			ipNetwork = networkInterfaces.testNetworkAliasesList[index][2]
			networkMask = networkInterfaces.testNetworkAliasesList[index][4]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'udp', '--source', '%s/%s' % (ipNetwork, networkMask), '--destination-port', '1234:1270', '--jump', 'DNAT', '--to-destination', '%s' % globals.windowsVmStudioIpAddressForSstTraffic])
	if globals.platformType == 'validation':
		for index in range(0, len(networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter)):
			interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[index][0]
			ipNetwork = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[index][2]
			networkMask = networkInterfaces.usbEthAdaptersInterfacesListForDmngEthAdapter[index][4]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'udp', '--source', '%s/%s' % (ipNetwork, networkMask), '--destination-port', '1234:1270', '--jump', 'DNAT', '--to-destination', '%s' % globals.windowsVmStudioIpAddressForSstTraffic])
		for index in range(0, len(networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter)):
			interfaceName = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[index][0]
			ipNetwork = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[index][2]
			networkMask = networkInterfaces.usbEthAdaptersInterfacesListForDmngUsbEthAdapter[index][4]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'udp', '--source', '%s/%s' % (ipNetwork, networkMask), '--destination-port', '1234:1270', '--jump', 'DNAT', '--to-destination', '%s' % globals.windowsVmStudioIpAddressForSstTraffic])

	# for iperf testing (tcp port 7910)
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', globals.dmngLanIfc, '--protocol', 'tcp', '--destination-port', '%d' % 7910, '--jump', 'DNAT', '--to-destination', '%s:%d' % (globals.linuxVmStudioIpAddressForSstTraffic, 7910)])
	if globals.platformType == 'validation':
		for i in range(globals.maxNbOfEthAdapters):
			interfaceName = dmngObject.ethAdaptersInterfacesList[i][0]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'tcp', '--destination-port', '%d' % 7910, '--jump', 'DNAT', '--to-destination', '%s:%d' % (globals.linuxVmStudioIpAddressForSstTraffic, 7910)])
		for i in range(globals.maxNbOfUsbEthAdapters):
			interfaceName = dmngObject.usbEthAdaptersInterfacesList[i][0]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'tcp', '--destination-port', '%d' % 7910, '--jump', 'DNAT', '--to-destination', '%s:%d' % (globals.linuxVmStudioIpAddressForSstTraffic, 7910)])

	# for iperf testing (udp port 7911)
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', globals.dmngLanIfc, '--protocol', 'udp', '--destination-port', '%d' % 7911, '--jump', 'DNAT', '--to-destination', '%s:%d' % (globals.linuxVmStudioIpAddressForSstTraffic, 7911)])
	if globals.platformType == 'validation':
		for i in range(globals.maxNbOfEthAdapters):
			interfaceName = dmngObject.ethAdaptersInterfacesList[i][0]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'udp', '--destination-port', '%d' % 7911, '--jump', 'DNAT', '--to-destination', '%s:%d' % (globals.linuxVmStudioIpAddressForSstTraffic, 7911)])
		for i in range(globals.maxNbOfUsbEthAdapters):
			interfaceName = dmngObject.usbEthAdaptersInterfacesList[i][0]
			commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', interfaceName, '--protocol', 'udp', '--destination-port', '%d' % 7911, '--jump', 'DNAT', '--to-destination', '%s:%d' % (globals.linuxVmStudioIpAddressForSstTraffic, 7911)])

	# for testing ssh
	#commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', globals.aviwestLanIfc, '--protocol', 'tcp', '--destination-port', '11111', '--jump', 'DNAT', '--to-destination', '%s:22' % globals.linuxVmStudioIpAddressForSsh])

	# for trafficGenerator/trafficAnalyser communication channel
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', networkInterfaces.testNetworkAliasesList[0][0], '--protocol', 'tcp', '--destination-port', '%d' % 9000, '--jump', 'DNAT', '--to-destination', '%s:%d' % (globals.windowsVmStudioIpAddressForTrafficGeneratorAndAnalyser, 9000)])

	# for accessing dmng from Aviwest LAN
	if globals.platformType == 'development':
		commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', globals.aviwestLanIfc, '--protocol', 'tcp', '--destination-port', '%d' % 5322, '--jump', 'DNAT', '--to-destination', '%s:%d' % (dmngObject.controlNetworkInterface[2], 5322)])

	# for accessing web dmng from Aviwest LAN
	#commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', globals.aviwestLanIfc, '--protocol', 'tcp', '--destination-port', '%d' % 8888, '--jump', 'DNAT', '--to-destination', '%s:%d' % (dmngObject.controlNetworkInterface[2], 8888)])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--append', 'PREROUTING', '--in-interface', globals.aviwestLanIfc, '--protocol', 'tcp', '--destination-port', '%d' % 8888, '--jump', 'DNAT', '--to-destination', '%s:%d' % ('192.168.10.10', 8888)])

	for command in commandsList:
		commandStdout, commandStderr = utils.executeCommand(command)

def setMangleOutputRules():
	utils.displayText('cyan', 'setting mangle output rules...', 0)

	commandsList = []

	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'mangle', '--append', 'OUTPUT', '--jump', 'LOG', '--log-level 7', '--log-prefix', 'MANGLE-OUTPUT: '])

	for command in commandsList:
		commandStdout, commandStderr = utils.executeCommand(command)

def setManglePreroutingRules():
	utils.displayText('cyan', 'setting mangle prerouting rules...', 0)

	commandsList = []

	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'mangle', '--append', 'PREROUTING', '--jump', 'LOG', '--log-level 7', '--log-prefix', 'MANGLE-PREROUTING: '])

	for command in commandsList:
		commandStdout, commandStderr = utils.executeCommand(command)

def displayRules():
	utils.displayText('cyan', 'current rules are the following...', 0)

	commandsList = []

	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--line-numbers', '--list', '--numeric', '--verbose'])
	commandsList.append(['/usr/bin/sudo', '/sbin/iptables', '--table', 'nat', '--line-numbers', '--list', '--numeric', '--verbose'])

	for command in commandsList:
		commandStdout, commandStderr = utils.executeCommand(command)
		utils.displayText('normal', 'commandStdout :', 0)
		utils.displayText('normal', commandStdout, 0)

if __name__ == '__main__':

	globals.scriptStartTime = time.time()

	parser = argparse.ArgumentParser(description="launch a scenario on aggregation-platform")
	# add positional arguments
	parser.add_argument("platformType", action="store", help="platform type : development|validation")

	args = parser.parse_args()
	globals.platformType = args.platformType

	if globals.platformType != 'development' and globals.platformType != 'validation':
		utils.displayText('red', 'platformType (%s) is neither development nor validation' % globals.platformType, 0)
		utils.terminateTest(1)

	# new instance of Dmng
	myDmng = dmng.Dmng()

	initChains()
	setDefaultPolicy()
	setInputRules(myDmng)
	setOutputRules()
	setForwardRules()
	setNatPostroutingRules()
	setNatOutputRules()
	setNatPreroutingRules(myDmng)
	#setMangleOutputRules()
	#setManglePreroutingRules()
	displayRules()

	del(myDmng)

	utils.terminateTest(0)
