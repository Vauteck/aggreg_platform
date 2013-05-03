#! /usr/bin/python
# -*- coding: utf-8 -*-

# import python libraries
import csv
import re
import subprocess
import sys
import time

# import aggregation-platform's libraries
import globals
import utils
import networkInterfaces

def executeCommandsList(commandsList):
	for command in commandsList:
		'''
		# get tcQdiscAction from commandsList (get qdisc position, guess action position (which comes next))
		try:
			qdiscIndex = command.index('qdisc')
		except:
			utils.displayText('yellow', '[WARNING] \'qdisc\' not found in command (%s)' % command, 0)
			#utils.terminateTest(1)

		actionIndex = qdiscIndex + 1
		tcQdiscAction = command[actionIndex]
		'''
		commandString = ' '.join(command)
		if not globals.quiet:
			utils.displayText('normal', 'executing command : %s' % commandString, 0)

		p = subprocess.Popen(command, bufsize=-1, shell = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE, env={'LANG':'en_GB.utf-8'})
		commandStdout, commandStderr = p.communicate()

		# decode commandStdout and commandStderr (bytes objects) to produce strings
		commandStdout = commandStdout.decode("utf-8")
		commandStderr = commandStderr.decode("utf-8")

		'''
		# TODO : if tcQdiscAction is del : ignore any error which can be linked to the fact that no traffic control configuration was set. Maybe we could do something better here.
		if tcQdiscAction != 'del':
			if p.returncode != 0:
				utils.displayText('red', 'the following command failed : %s' % ' '.join(command), 0)
				if globals.verbose:
					utils.displayText('normal', 'commandStdout :', 0)
					utils.displayText('normal', commandStdout, 0)
					utils.displayText('normal', 'commandStderr :', 0)
					utils.displayText('normal', commandStderr, 0)
				utils.terminateTest(1)
		'''
	return commandStdout, commandStderr

def buildCommandsListForReset(networkInterface):
	commandsList = []
	commandsList.append(['/sbin/tc', 'qdisc', 'del', 'dev', networkInterface, 'root'])
	# control incoming traffic on validation platform if networkInterface is in usbEthAdaptersInterfacesListForDmngEthAdapter or usbEthAdaptersInterfacesListForDmngUsbEthAdapter
	if globals.platformType == 'validation' and re.search('eth', networkInterface) != None:
		commandsList.append(['/sbin/tc', 'qdisc', 'del', 'dev', networkInterface, 'ingress'])
	return commandsList

def buildCommandsListForDisplay(networkInterface):
	commandsList = []
	commandsList.append(['/sbin/tc', '-s', 'qdisc', 'ls', 'dev', networkInterface])
	return commandsList

def buildCommandsList(networkInterface, action, networkDeviceDriver, bandWidth, fixedLatency, instantJitter, packetsLoss, queueLength):

	# check action values
	if (action != 'add') and (action != 'change'):
		utils.displayText('red', '[KO] action (%s) is neither \'add\', nor \'change\'' % action, 0)
		utils.terminateTest(1)

	limitValueInBytes=100000
	# packetSizeInBytes : a packet is supposed to weigh 1024 Bytes max
	packetSizeInBytes=1024

	# TBF parameters
	# http://lartc.org/manpages/tc-tbf.html

	# limit / latency : The limit parameter is the number of bytes to queue before packets are tail dropped. LIMIT IS THE NUMBER OF BYTES THAT CAN BE QUEUED WAITING FOR TOKENS TO BECOME AVAILABLE. The limit parameter tells us how big the queue of packets waiting to be sent can be.	You can also specify this the other way around by setting the latency parameter, which specifies the maximum amount of time a packet can sit in the TBF. The latter calculation takes into account the size of the bucket, the rate and possibly the peakrate (if set). These two parameters are mutually exclusive.In Linux 2.6.1 and later if you attach a qdisc to your tbf class, the limit is ignored in favor of your attached qdisc.

	# burst / buffer / maxburst : Size of the bucket, in bytes. This is the maximum amount of bytes that tokens can be available for instantaneously. In general, larger shaping rates require a larger buffer. For 10mbit/s on Intel, you need at least 10kbyte buffer if you want to reach your configured rate! The minimum buffer size can be calculated by dividing the rate by HZ (ARSO : equivalent to CONFIG_HZ in kernel?) On 2012_08_01, CONFIG_HZ in dmng is supposed to be set to 250 HZ. ARSO : the result is too small for tbf to behave as we expect it to do.
	configHz = 250

	# mpu : A zero-sized packet does not use zero bandwidth. For ethernet, no packet uses less than 64 bytes. The Minimum Packet Unit determines the minimal token usage (specified in bytes) for a packet. Defaults to zero.

	# rate : The speed knob. See remarks above about limits! See tc(8) for units. The rate tells us how fast tokens enter the buffer.	PLEASE NOTE THAT IN THE ACTUAL IMPLEMENTATION, TOKENS CORRESPOND TO BYTES, NOT PACKETS.

	# peakrate : Maximum depletion rate of the bucket. Limited to 1mbit/s on Intel, 10mbit/s on Alpha. THE PEAKRATE DOES NOT NEED TO BE SET, IT IS ONLY NECESSARY IF PERFECT MILLISECOND TIMESCALE SHAPING IS REQUIRED. The normal bucket is used to limit the average rate data is sent but allow bursts of traffic to go through.  THE PEAKRATE BUCKET IS USED TO LIMIT THE SPEED THOSE BURSTS ARE SENT. To calculate the maximum possible peakrate, multiply the configured mtu by configHz : 1500 x 250 = 375000 bps = 375 kbps : it is not usable for our bitrates (10kbps-10Mbps).

	# mtu / minburst : Specifies the size of the peakrate bucket. For perfect accuracy, should be set to the MTU of the interface. If a peakrate is needed, but some burstiness is acceptable, this size can be raised. A 3000 byte minburst allows around 3mbit/s of peakrate, given 1000 byte packets.

	queueLengthInBytes=queueLength * packetSizeInBytes

	# maxburstValueInBytes in Bytes
	# values found by using iperf (in TCP/UDP) and making experiences
	if networkDeviceDriver == 'asix':
		# asix : usb ethernet
		#maxburstValueInBytes = bandWidth / configHz
		maxburstValueInBytes = bandWidth * 25
	elif networkDeviceDriver == 'smsc75xx':
		# smsc75xx : gigabit ethernet
		maxburstValueInBytes = bandWidth * 50
	elif networkDeviceDriver == 'usb':
		# usb : wifi
		maxburstValueInBytes = bandWidth * 50
	elif networkDeviceDriver == 'r8169':
		maxburstValueInBytes = bandWidth * 10
	elif networkDeviceDriver == 'virtualBox':
		maxburstValueInBytes = bandWidth * 10
	else:
		utils.displayText('red', 'networkDeviceDriver (%s) unknown' % networkDeviceDriver, 0)
		utils.terminateTest(1)

	commandsList = []

	# queueLength' unit is in number of packets

	# bufferSize'unit is in bytes
	#bufferSize = 1024 * queueLength
	#bufferSize = 1024 * 2000

	# units :
	# kbit : kilobits or kilobits per second
	# kb : kilobytes
	# b : bytes

	# -----
	# pfifo / bfifo : does not allow traffic shaping
	# http://blog.edseek.com/~jasonb/articles/traffic_shaping/qdiscs.html
	# -----
	#commandsList.append(['/sbin/tc', 'qdisc', 'add', 'dev', networkInterface, 'root', 'handle', '1:', 'bfifo', 'limit', '%dkbit' % bandWidth])

	# control incoming traffic on validation platform if networkInterface is in usbEthAdaptersInterfacesListForDmngEthAdapter or usbEthAdaptersInterfacesListForDmngUsbEthAdapter
	if globals.platformType == 'validation' and re.search('eth', networkInterface) != None:
		# we will use ifb110 for eth110, ifb111 for eth111... The file /etc/modules has to contain something like this : "ifb numifbs=256"
		ifbDevice = re.sub('eth', 'ifb', networkInterface)
		commandsList.append(['/sbin/tc', 'qdisc', action, 'dev', networkInterface, 'ingress'])
		commandsList.append(['/sbin/tc', 'filter', action, 'dev', networkInterface, 'parent', 'ffff:', 'protocol', 'ip', 'u32', 'match', 'u32', '0', '0', 'flowid', '1:1', 'action', 'mirred', 'egress', 'redirect', 'dev', ifbDevice])
		networkInterface = ifbDevice

	# -----
	# tbf
	# -----
	commandsList.append(['/sbin/tc', 'qdisc', action, 'dev', networkInterface, 'root', 'handle', '1:', 'tbf', 'rate', '%dkbit' % bandWidth, 'maxburst', '%db' % maxburstValueInBytes, 'limit', '%db' % (maxburstValueInBytes + queueLengthInBytes)])

	# -----
	# try with htb...
	# -----
	#commandsList.append(['/sbin/tc', 'qdisc', 'add', 'dev', networkInterface, 'root', 'handle', '1:', 'htb', 'default', '99', 'r2q', '5'])
	#commandsList.append(['/sbin/tc', 'qdisc', 'add', 'dev', networkInterface, 'parent', 'handle', '1:', 'htb', 'rate', '%dkbit' % bandWidth, 'ceil', '%dkbit' % bandWidth])

	###commandsList.append(['/sbin/tc', 'qdisc', 'add', 'dev', networkInterface, 'root', 'handle', '1:', 'htb'])
	###commandsList.append(['/sbin/tc', 'class', 'add', 'dev', networkInterface, 'parent', '1:', 'classid', '1:1', 'htb', 'rate', '%dmbit' % 100, 'ceil', '%dmbit' % 100])
	##commandsList.append(['/sbin/tc', 'qdisc', 'add', 'dev', networkInterface, 'parent', '1:1', 'classid', '1:10', 'htb', 'rate', '%dkbit' % bandWidth, 'ceil', '%dkbit' % bandWidth])
	#commandsList.append(['/sbin/tc', 'qdisc', 'add', 'dev', networkInterface, 'protocol', 'ip', '1:1', 'parent', '1:0', 'prio', '1', 'handle', '2', 'fw', 'classid', '1:10'])
	##commandsList.append(['/sbin/tc', 'qdisc', 'add', 'dev', networkInterface, 'parent', '1:10', 'handle', '10:', 'sfq', 'quantum', '1500b', 'perturb', '10'])

	#default 30
	#$TC class add dev $IF parent 1: classid 1:1 htb rate $DNLD

	# -----
	# try with cbq...
	# CBQ is the most complex qdisc available, the most hyped, the least understood, and probably the trickiest one to get right. This is not because the authors are evil or incompetent, far from it, it's just that the CBQ algorithm isn't all that precise and doesn't really match the way Linux works.
	# -----

	#commandsList.append(['/sbin/tc', 'qdisc', 'add', 'dev', networkInterface, 'root', 'handle', '1:0', 'cbq', 'bandwidth', '1mbit', 'avpkt', '1000'])
	#commandsList.append(['/sbin/tc', 'class', 'add', 'dev', networkInterface, 'parent', '1:', 'classid', '1:1', 'cbq', 'rate', '700kbit', 'allot', '1500', 'prio' , '5', 'bounded', 'isolated'])
	#commandsList.append(['/sbin/tc', 'filter', 'add', 'dev', networkInterface, 'parent', '1:', 'protocol', 'ip', 'prio', '16', 'u32', 'match', 'ip', 'dst', '172.16.110.1', 'flowid', '1:1'])

	# -----
	# try with hfsc... (not available on dmng)
	# -----
	##commandsList.append(['/sbin/tc', 'qdisc', 'add', 'dev', networkInterface, 'root', 'handle', '1:0', 'hfsc', 'default', '1'])
	#commandsList.append(['/sbin/tc', 'class', 'add', 'dev', networkInterface, 'parent', '1:0', 'classid', '1:1', 'hfsc', 'rt', 'm2', '1mbit'])
	##commandsList.append(['/sbin/tc', 'class', 'add', 'dev', networkInterface, 'parent', '1:0', 'classid', '1:1', 'hfsc', 'sc', 'rate', '1000kbit', 'ul', 'rate', '1000kbit'])

	#tc qdisc add dev eth0 root handle 1: hfsc
	#tc class add dev eth0 parent 1: classid 1:1 hfsc sc rate 1000kbit ul rate 1000kbit
	#tc class add dev eth0 parent 1:1 classid 1:10 hfsc sc rate 500kbit ul rate 1000kbit
	#tc class add dev eth0 parent 1:1 classid 1:20 hfsc sc rate 500kbit ul rate 1000kbit
	#tc class add dev eth0 parent 1:10 classid 1:11 hfsc sc umax 1500b dmax 53ms rate 400kbit ul rate 1000kbit
	#tc class add dev eth0 parent 1:10 classid 1:12 hfsc sc umax 1500b dmax 30ms rate 100kbit ul rate 1000kbit

	# -----
	# loss, delay...
	# -----
	#commandsList.append(['/sbin/tc', 'qdisc', action, 'dev', networkInterface, 'parent', '1:1', 'handle', '2:', 'pfifo', 'limit', '%db' % queueLengthInBytes])
	# this is the netem loss command that causes "1 datagrams received out-of-order" error message when testing with iperf. It simply indicates that packets are reordered.
	# when there is latency, iperf says there is loss, whereas there is no loss using ping!!!

	commandsList.append(['/sbin/tc', 'qdisc', action, 'dev', networkInterface, 'parent', '1:1', 'handle', '2:', 'netem', 'loss', '%d%%' % packetsLoss, 'limit', '%db' % limitValueInBytes])

	if fixedLatency == 0 or instantJitter == 0:
		commandsList.append(['/sbin/tc', 'qdisc', action, 'dev', networkInterface, 'parent', '2:1', 'handle', '3:', 'netem', 'delay', '%dms' % fixedLatency, 'limit', '%db' % limitValueInBytes])
	else:
		commandsList.append(['/sbin/tc', 'qdisc', action, 'dev', networkInterface, 'parent', '2:1', 'handle', '3:', 'netem', 'delay', '%dms' % fixedLatency, '%dms' % instantJitter, 'distribution', 'normal', 'limit', '%db' % limitValueInBytes])

	commandsList.append(['/sbin/tc', 'qdisc', action, 'dev', networkInterface, 'parent', '3:1', 'handle', '4:', 'pfifo', 'limit', '%db' % limitValueInBytes])

	return commandsList

def driveLinkTrafficControl(interfaceName, filename, dmngObject='', threadName = ''):

	if globals.platformType == 'development':
		networkDeviceDriver = dmngObject.getNetworkDeviceDriver(interfaceName)
	if globals.platformType == 'validation':	
		networkDeviceDriver = 'asix'

	# read filename content and build linkEvolution
	with open(filename, 'r') as fileHandle:
		csvFileContent = csv.reader(fileHandle, delimiter=',', quotechar='|')
		linkEvolution = []
		newEntry = []
		for line in csvFileContent:
			# ignore malformated, comments lines (beginning with #) and blank lines
			#utils.displayText('yellow', 'line : %s' % line, 0)
			#if not re.match('#(.*)', line):
			if len(line) == 6:
				#if not re.match('#*aaa(.*)', line):
				#if (not re.match('#*aaa(.*)', line)) and (len(line) == 6):
				newEntry.append(int(line[0]))
				newEntry.append(int(line[1]))
				newEntry.append(int(line[2]))
				newEntry.append(int(line[3]))
				newEntry.append(int(line[4]))
				newEntry.append(int(line[5]))
				linkEvolution.append(newEntry)
				newEntry = []
			else:
				utils.displayText('yellow', 'malformated or blank lines in file : %s' % filename, 0)

	# set traffic control parameters
	for linkCommand in linkEvolution:
		# at the time instantTime, change traffic control parameters
		instantTime = int(linkCommand[0])

		while True:
			currentTime = time.time()
			secondsElapsed = currentTime - globals.streamingStartTime
			#utils.displayText('yellow', 'secondsElapsed : %s' % secondsElapsed, 0)
			if (secondsElapsed >= instantTime):
				bandWidth = linkCommand[1]
				fixedLatency = linkCommand[2]
				instantJitter = linkCommand[3]
				queueLength = linkCommand[4]
				packetsLoss = linkCommand[5]

				utils.displayText('cyan', 'replacing traffic control parameters on %s after %.3f secs of test : bandWidth : %d; fixedLatency : %d; instantJitter : %d; queueLength : %d; packetsLoss : %d' % (interfaceName, secondsElapsed, bandWidth, fixedLatency, instantJitter, queueLength, packetsLoss), 0)

				commandsList = buildCommandsList(interfaceName, 'change', networkDeviceDriver, bandWidth, fixedLatency, instantJitter, packetsLoss, queueLength)
				if globals.platformType == 'development':
					for command in commandsList:
						commandString = ' '.join(command)
						dmngObject.writeToSerial(commandString, [], 10)
				if globals.platformType == 'validation':
					for command in commandsList:
						# insert /usr/bin/sudo before each command
						command.insert(0, '/usr/bin/sudo')
					commandStdout, commandStderr = executeCommandsList(commandsList)

				break
	#utils.displayText('yellow', 'linkEvolution : %s' % linkEvolution, 0)

if __name__ == '__main__':

	globals.scriptStartTime = time.time()

	utils.displayText('red', 'TODO __main__ TOWRITE', 0)
	utils.terminateTest(0)
