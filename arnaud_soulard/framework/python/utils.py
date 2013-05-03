#! /usr/bin/python
# -*- coding: utf-8 -*-

# import python libraries
import datetime
import fileinput
import os
import re
import shutil
import subprocess
import sys
import threading
import time

# import aggregation-platform's libraries
import emails
import globals
import testReport

def displayText(textColor, textToDisplay, waitingTime):

	# check waitingTime values and add (waiting X seconds) to textToDisplay if needed
	if waitingTime < 0:
		myString = '[KO] waitingTime (%s) has to be a positive value' % waitingTime
		print('\033[1;31m' + myString + '\033[1;m')
		sys.exit(1)
	elif waitingTime > 0:
		textToDisplay = textToDisplay + ' (waiting %s seconds)' % waitingTime
	#else:
		# nothing to do

	if globals.colorEnabled:
		if textColor == 'normal':
			print(textToDisplay)
		elif textColor == 'black':
			print('\033[1;30m' + textToDisplay + '\033[1;m')
		elif textColor == 'red':
			print('\033[1;31m' + textToDisplay + '\033[1;m')
		elif textColor == 'green':
			print('\033[1;32m' + textToDisplay + '\033[1;m')
		# yellow not readable under teraterm : avoid using it
		elif textColor == 'yellow':
			print('\033[1;33m' + textToDisplay + '\033[1;m')
		elif textColor == 'blue':
			print('\033[1;34m' + textToDisplay + '\033[1;m')
		elif textColor == 'magenta':
			print('\033[1;35m' + textToDisplay + '\033[1;m')
		elif textColor == 'cyan':
			print('\033[1;36m' + textToDisplay + '\033[1;m')
		else:
			myString = '[KO] textColor (%s) unknown' % textColor
			print('\033[1;31m' + myString + '\033[1;m')
			sys.exit(1)
	else :
		print(textToDisplay)

	lock = threading.Lock()
	lock.acquire()
	# write in htmlLogFileHandle
	# convert UNIX EOLs into html newlines
	textToDisplay = re.sub('\r', '<br>', textToDisplay)
	if globals.colorEnabled:
		if textColor == 'normal':
			#globals.htmlLogFileHandle.write(textToDisplay + '<br>' + '\n')
			globals.htmlLogFileHandle.write('<font>%s</font><br>\n' % textToDisplay)
		elif textColor == 'black':
			globals.htmlLogFileHandle.write('<font color=#000000>%s</font><br>\n' % textToDisplay)
		elif textColor == 'red':
			globals.htmlLogFileHandle.write('<font color=#FF0000>%s</font><br>\n' % textToDisplay)
		elif textColor == 'green':
			globals.htmlLogFileHandle.write('<font color=#009000>%s</font><br>\n' % textToDisplay)
		# yellow not readable under teraterm : avoid using it
		elif textColor == 'yellow':
			globals.htmlLogFileHandle.write('<font color=#FF6F00>%s</font><br>\n' % textToDisplay)
		elif textColor == 'blue':
			globals.htmlLogFileHandle.write('<font color=#0000FF>%s</font><br>\n' % textToDisplay)
		elif textColor == 'magenta':
			globals.htmlLogFileHandle.write('<font color=#FF00FF>%s</font><br>\n' % textToDisplay)
		elif textColor == 'cyan':
			globals.htmlLogFileHandle.write('<font color=#009C9C>%s</font><br>\n' % textToDisplay)
		else:
			myString = '[KO] textColor (%s) unknown' % textColor
			print('\033[1;31m' + myString + '\033[1;m')
			sys.exit(1)
	else :
		globals.htmlLogFileHandle.write('<font>%s</font><br>\n' % textToDisplay)
	lock.release()

	if waitingTime > 0:
		time.sleep(waitingTime)

def addCssInformations(fileHandle):
	fileHandle.write('<style type="text/css">\n')
	fileHandle.write('h1 {font-size:22px;}\n')
	fileHandle.write('h2 {font-size:18px;}\n')
	fileHandle.write('body {\n')
	fileHandle.write('font-size : 12px;\n')
	fileHandle.write('margin-top: 10px;\n')
	fileHandle.write('margin-right: 10px;\n')
	fileHandle.write('margin-bottom: 10px;\n')
	fileHandle.write('margin-left: 10px;\n')
	fileHandle.write('}\n')
	fileHandle.write('table {\n')
	fileHandle.write('width: 50%;\n')
	fileHandle.write('text-align: left;\n')
	fileHandle.write('border-width: 1px;\n')
	fileHandle.write('border-style: solid;\n')
	fileHandle.write('border-color: black;\n')
	fileHandle.write('font-size: 12px;\n')
	fileHandle.write('}\n')
	fileHandle.write('</style>\n')

def createResultEntry():

	displayText('blue', 'waiting for threads to terminate', 0)
	mainThread = threading.currentThread()
	for currentThread in threading.enumerate():
		if currentThread is not mainThread:
			currentThread.join()

	now = datetime.datetime.now()
	# build directory for storing results (ordered by version / date / scenarioId)
	scenarioIdDirectoryForResults = globals.baseVersionsDirectoryForResults + '/' + globals.appliVersion + '/' + '%s' % globals.scenarioId + '/' + globals.scenarioResult + '/' + now.strftime('%Y_%m_%d-%Hh%Mm%Ss')

	displayText('black', 'copying test results to %s' % scenarioIdDirectoryForResults, 0)
	httpRootTestDirectory = 'http://%s/%s' % (globals.aggregationMasterLanIpAddress, re.sub(globals.baseDirectoryForResults + '/', '', scenarioIdDirectoryForResults))
	displayText('black', 'test results are accessible here : %s' % httpRootTestDirectory, 0)

	if not os.path.isdir(scenarioIdDirectoryForResults):
		os.makedirs(scenarioIdDirectoryForResults)

	if os.path.isfile(globals.scriptDirName + '/' + os.path.basename(globals.gatewaySstRxLogFile)):
		shutil.copy(globals.scriptDirName + '/' + os.path.basename(globals.gatewaySstRxLogFile), scenarioIdDirectoryForResults)

	# close dmngLogFileHandle and copy dmngLogFileHandle
	globals.dmngLogFileHandle.close()
	shutil.copy(globals.dmngLogFile, scenarioIdDirectoryForResults)

	# create and build globals.indexFileName
	indexFileHandle = open(scenarioIdDirectoryForResults + '/' + globals.indexFileName, 'w')
	indexFileHandle.write('<html>\n')
	indexFileHandle.write('<head>\n')
	indexFileHandle.write('<meta http-equiv="content-type" content="text/html; charset=utf8>"</meta>\n')
	indexFileHandle.write('<title>aggregation-platform\'s test report</title>\n')

	addCssInformations(indexFileHandle)

	indexFileHandle.write('</head>\n')
	indexFileHandle.write('<body>\n')
	indexFileHandle.write('<h1>aggregation-platform\'s test report</h1>\n')
	indexFileHandle.write('<a href="%s">%s</a><br>\n' % (httpRootTestDirectory, httpRootTestDirectory))

	# --------------------------------------------------------------------------------------------------
	indexFileHandle.write('<h2>test caracteristics summary</h2>\n')
	# --------------------------------------------------------------------------------------------------

	indexFileHandle.write('<table>\n')

	indexFileHandle.write('<colgroup>\n')
	indexFileHandle.write('<col width="50%">\n')
	indexFileHandle.write('<col width="50%">\n')
	indexFileHandle.write('</colgroup>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>scenarioId / scenarioResult</th>\n')
	if globals.scenarioResult == 'OK':
		color = '#009000'
	else:
		color = '#FF0000'
	indexFileHandle.write('<th>%s / <font color=%s>%s</font></th>\n' % (globals.scenarioId, color, globals.scenarioResult))
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>scenarioComment</th>\n')
	indexFileHandle.write('<th>%s</th>\n' % globals.scenarioComment)
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>scenarioEvolution</th>\n')
	indexFileHandle.write('<th>%s</th>\n' % globals.scenarioEvolution)
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>scriptDuration</th>\n')
	indexFileHandle.write('<th>%s</th>\n' % globals.scriptDuration)
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>platformSvnRevision / appliVersion</th>\n')
	indexFileHandle.write('<th>%s / %s</th>\n' % (globals.platformSvnRevision, globals.appliVersion))
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('</tr>\n')
	indexFileHandle.write('</table>\n')

	# --------------------------------------------------------------------------------------------------
	indexFileHandle.write('<h2>sst-tx parameters</h2>\n')
	# --------------------------------------------------------------------------------------------------
	indexFileHandle.write('<table>\n')

	indexFileHandle.write('<colgroup>\n')
	indexFileHandle.write('<col width="50%">\n')
	indexFileHandle.write('<col width="50%">\n')
	indexFileHandle.write('</colgroup>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>actionMode</th>\n')
	indexFileHandle.write('<th>%s</th>\n' % globals.actionMode)
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('<tr>\n')
	if globals.actionMode == 'live_bw_test':
		indexFileHandle.write('<th>scenarioDuration / bwTestDuration</th>\n')
		indexFileHandle.write('<th>%s seconds / %s seconds</th>\n' % (globals.scenarioDuration, globals.bwTestDuration))
	else:
		indexFileHandle.write('<th>scenarioDuration</th>\n')
		indexFileHandle.write('<th>%s seconds</th>\n' % globals.scenarioDuration)
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>audioBitrate</th>\n')
	indexFileHandle.write('<th>%s kbps</th>\n' % globals.audioBitrate)
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>videoBitrateMode / videoBitrate / overEncodedBitrate</th>\n')
	indexFileHandle.write('<th>%s / %s kbps / %s kbps</th>\n' % (globals.videoBitrateMode, globals.videoBitrate, globals.overEncodedBitrate))
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>frameRate</th>\n')
	indexFileHandle.write('<th>%s Hz</th>\n' % globals.frameRate)
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>gopDuration / iFramesVsPandBFramesRatio</th>\n')
	indexFileHandle.write('<th>%s ms / %s %%</th>\n' % (globals.gopDuration, globals.iFramesVsPandBFramesRatio))
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>timeWindow</th>\n')
	indexFileHandle.write('<th>%s ms</th>\n' % globals.timeWindow)
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('</table>\n')

	# --------------------------------------------------------------------------------------------------
	indexFileHandle.write('<h2>gateway parameters</h2>\n')
	# --------------------------------------------------------------------------------------------------

	indexFileHandle.write('<table>\n')

	indexFileHandle.write('<colgroup>\n')
	indexFileHandle.write('<col width="50%">\n')
	indexFileHandle.write('<col width="50%">\n')
	indexFileHandle.write('</colgroup>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>gatewayBandWidth</th>\n')
	indexFileHandle.write('<th>%s kbps</th>\n' % globals.gatewayBandWidth)
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>gatewayFixedLatency</th>\n')
	indexFileHandle.write('<th>%s ms</th>\n' % globals.gatewayFixedLatency)
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>gatewayInstantJitter</th>\n')
	indexFileHandle.write('<th>%s ms</th>\n' % globals.gatewayInstantJitter)
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>gatewayQueueLength</th>\n')
	indexFileHandle.write('<th>%s packets</th>\n' % globals.gatewayQueueLength)
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>gatewayPacketsLoss</th>\n')
	indexFileHandle.write('<th>%s %%</th>\n' % globals.gatewayPacketsLoss)
	indexFileHandle.write('</tr>\n')

	indexFileHandle.write('</table>\n')

	# --------------------------------------------------------------------------------------------------
	indexFileHandle.write('<h2>dmng links</h2>\n')
	# --------------------------------------------------------------------------------------------------

	indexFileHandle.write('<table>\n')

	indexFileHandle.write('<colgroup>\n')
	indexFileHandle.write('<col width="50%">\n')
	indexFileHandle.write('<col width="50%">\n')
	indexFileHandle.write('</colgroup>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>nbOfEthAdapters</th>\n')
	indexFileHandle.write('<th>%s</th>\n' % globals.nbOfEthAdapters)
	indexFileHandle.write('</tr>\n')

	if globals.nbOfEthAdapters >= 1:
		indexFileHandle.write('<tr>\n')
		indexFileHandle.write('<th>ethAdaptersFixedLatenciesList (ms)</th>\n')
		indexFileHandle.write('<th>%s</th>\n' % globals.ethAdaptersFixedLatenciesList)
		indexFileHandle.write('</tr>\n')

		indexFileHandle.write('<tr>\n')
		indexFileHandle.write('<th>ethAdaptersJittersList (ms)</th>\n')
		indexFileHandle.write('<th>%s</th>\n' % globals.ethAdaptersJittersList)
		indexFileHandle.write('</tr>\n')

		indexFileHandle.write('<tr>\n')
		indexFileHandle.write('<th>ethAdaptersBandWidthsList (kbps)</th>\n')
		indexFileHandle.write('<th>%s</th>\n' % globals.ethAdaptersBandWidthsList)
		indexFileHandle.write('</tr>\n')

		indexFileHandle.write('<tr>\n')
		indexFileHandle.write('<th>ethAdaptersPacketLossList (%)</th>\n')
		indexFileHandle.write('<th>%s</th>\n' % globals.ethAdaptersPacketLossList)
		indexFileHandle.write('</tr>\n')

		indexFileHandle.write('<tr>\n')
		indexFileHandle.write('<th>ethAdaptersQueueLengthList (packets)</th>\n')
		indexFileHandle.write('<th>%s</th>\n' % globals.ethAdaptersQueueLengthList)
		indexFileHandle.write('</tr>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>nbOfUsbEthAdapters</th>\n')
	indexFileHandle.write('<th>%s</th>\n' % globals.nbOfUsbEthAdapters)
	indexFileHandle.write('</tr>\n')

	if globals.nbOfUsbEthAdapters >= 1:
		indexFileHandle.write('<tr>\n')
		indexFileHandle.write('<th>usbEthAdaptersFixedLatenciesList (ms)</th>\n')
		indexFileHandle.write('<th>%s</th>\n' % globals.usbEthAdaptersFixedLatenciesList)
		indexFileHandle.write('</tr>\n')

		indexFileHandle.write('<tr>\n')
		indexFileHandle.write('<th>usbEthAdaptersJittersList (ms)</th>\n')
		indexFileHandle.write('<th>%s</th>\n' % globals.usbEthAdaptersJittersList)
		indexFileHandle.write('</tr>\n')

		indexFileHandle.write('<tr>\n')
		indexFileHandle.write('<th>usbEthAdaptersBandWidthsList (kbps)</th>\n')
		indexFileHandle.write('<th>%s</th>\n' % globals.usbEthAdaptersBandWidthsList)
		indexFileHandle.write('</tr>\n')

		indexFileHandle.write('<tr>\n')
		indexFileHandle.write('<th>usbEthAdaptersPacketLossList (%)</th>\n')
		indexFileHandle.write('<th>%s</th>\n' % globals.usbEthAdaptersPacketLossList)
		indexFileHandle.write('</tr>\n')

		indexFileHandle.write('<tr>\n')
		indexFileHandle.write('<th>usbEthAdaptersQueueLengthList (packets)</th>\n')
		indexFileHandle.write('<th>%s</th>\n' % globals.usbEthAdaptersQueueLengthList)
		indexFileHandle.write('</tr>\n')

	indexFileHandle.write('<tr>\n')
	indexFileHandle.write('<th>nbOfWifiAdapters</th>\n')
	indexFileHandle.write('<th>%s</th>\n' % globals.nbOfWifiAdapters)
	indexFileHandle.write('</tr>\n')

	if globals.nbOfWifiAdapters >= 1:
		indexFileHandle.write('<tr>\n')
		indexFileHandle.write('<th>wifiAdaptersFixedLatenciesList (ms)</th>\n')
		indexFileHandle.write('<th>%s</th>\n' % globals.wifiAdaptersFixedLatenciesList)
		indexFileHandle.write('</tr>\n')

		indexFileHandle.write('<tr>\n')
		indexFileHandle.write('<th>wifiAdaptersJittersList (ms)</th>\n')
		indexFileHandle.write('<th>%s</th>\n' % globals.wifiAdaptersJittersList)
		indexFileHandle.write('</tr>\n')

		indexFileHandle.write('<tr>\n')
		indexFileHandle.write('<th>wifiAdaptersBandWidthsList (kbps)</th>\n')
		indexFileHandle.write('<th>%s</th>\n' % globals.wifiAdaptersBandWidthsList)
		indexFileHandle.write('</tr>\n')

		indexFileHandle.write('<tr>\n')
		indexFileHandle.write('<th>wifiAdaptersPacketLossList (%)</th>\n')
		indexFileHandle.write('<th>%s</th>\n' % globals.wifiAdaptersPacketLossList)
		indexFileHandle.write('</tr>\n')

		indexFileHandle.write('<tr>\n')
		indexFileHandle.write('<th>wifiAdaptersQueueLengthList (packets)</th>\n')
		indexFileHandle.write('<th>%s</th>\n' % globals.wifiAdaptersQueueLengthList)
		indexFileHandle.write('</tr>\n')

	indexFileHandle.write('</table>\n')

	indexFileHandle.write('<h2>links to log files</h2>\n')
	indexFileHandle.write('<p>\n')
	indexFileHandle.write('<a href="%s">%s</a> main script log<br>\n' % ((httpRootTestDirectory + '/' + os.path.basename(globals.htmlLogFileName)), os.path.basename(globals.htmlLogFileName)))
	if os.path.isfile(globals.scriptDirName + '/' + os.path.basename(globals.gatewaySstRxLogFile)):
		indexFileHandle.write('<a href="%s">%s</a> sst-rx session<br>\n' % ((httpRootTestDirectory + '/' + os.path.basename(globals.gatewaySstRxLogFile)), os.path.basename(globals.gatewaySstRxLogFile)))
	indexFileHandle.write('<a href="%s">%s</a> dmng console session<br>\n' % ((httpRootTestDirectory + '/' + os.path.basename(globals.dmngLogFile)), os.path.basename(globals.dmngLogFile)))
	indexFileHandle.write('</p>\n')

	indexFileHandle.write('</body>\n')
	indexFileHandle.write('</html>\n')
	indexFileHandle.close()

	testReport.buildTestReport()

	# close htmlLogFileHandle and copy htmlLogFileHandle
	globals.htmlLogFileHandle.write('</body>\n')
	globals.htmlLogFileHandle.write('</html>\n')
	globals.htmlLogFileHandle.close()
	shutil.copy(globals.htmlLogFileName, scenarioIdDirectoryForResults)

	return scenarioIdDirectoryForResults

def terminateTest(status):
	'''terminate a test

	@param status : 0 for OK, anything else for KO
	'''

	if status != 0:
		globals.scenarioResult = 'KO'

	endTime = time.time()
	secondsElapsed = endTime - globals.scriptStartTime

	nbOfMinutes, nbOfSeconds = divmod(secondsElapsed, 60)
	nbOfMinutes = int(nbOfMinutes)
	nbOfSeconds = int(nbOfSeconds)

	if nbOfMinutes > 1:
		minutesUnit = 'minutes'
	else:
		minutesUnit = 'minute'

	if nbOfSeconds > 1:
		secondsUnit = 'seconds'
	else:
		secondsUnit = 'second'

	if nbOfMinutes >= 1:
		if nbOfSeconds == 0:
			globals.scriptDuration = '%d %s' % (nbOfMinutes, minutesUnit)
		else:
			globals.scriptDuration = '%d %s, %d %s' % (nbOfMinutes, minutesUnit, nbOfSeconds, secondsUnit)
	else:
		globals.scriptDuration = '%d %s' % (nbOfSeconds, secondsUnit)

	displayText('black', 'test duration : %s' % globals.scriptDuration, 0)

	scenarioIdDirectoryForResults = createResultEntry()

	if globals.sendEmail:
		emailsAddressesList = emails.getEmailsAddressesList()
		if emailsAddressesList:
			emails.sendTestResultByEmail(emailsAddressesList, scenarioIdDirectoryForResults)

	sys.exit(status)

def executeCommand(command):
	treatErrorAsWarning = 'no'
	commandString = ' '.join(command)

	if not globals.quiet:
		displayText('normal', 'executing command : %s' % commandString, 0)

	if globals.verbose:
		commandStartTime = datetime.datetime.now()

	# do not check return codes for some commands
	if re.search('/sbin/ifconfig', commandString) != None:
		treatErrorAsWarning = 'yes'

	# using "env=" is taken into account on aggregationMaster, not when running remote commands on studio-sst-rx
	# TODO : try to use shell = False (try with only the command : make init --directory globals.sourcesDirectory)
	#p = subprocess.Popen(commandString, bufsize=-1, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, env={'LANG':'en_GB.utf-8'})
	p = subprocess.Popen(command, bufsize=-1, shell = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE, env={'LANG':'en_GB.utf-8'})
	commandStdout, commandStderr = p.communicate()

	# decode commandStdout and commandStderr (bytes objects) to produce strings
	commandStdout = commandStdout.decode("utf-8")
	commandStderr = commandStderr.decode("utf-8")

	# compute command execution time
	if globals.verbose:
		commandEndTime = datetime.datetime.now()
		commandExecutionDuration = (commandEndTime - commandStartTime).seconds * 1000 + (commandEndTime - commandStartTime).microseconds / 1000

	if p.returncode == 0:
		if globals.verbose:
			displayText('green', '[OK] command executed successfully in %d milliseconds' % commandExecutionDuration, 0)
		elif not globals.quiet:
			displayText('green', '[OK] command executed successfully', 0)
	else:
		if treatErrorAsWarning == 'yes':
			if globals.verbose:
				displayText('yellow', '[WARNING] the following command failed after %d milliseconds of execution : %s' % (commandExecutionDuration, ' '.join(command)), 0)
			else:
				displayText('yellow', '[WARNING] the following command failed : %s' % ' '.join(command), 0)
		else:
			if globals.verbose:
				displayText('red', '[KO] the following command failed after %d milliseconds of execution : %s' % (commandExecutionDuration, ' '.join(command)), 0)
			else:
				displayText('red', '[KO] the following command failed : %s' % ' '.join(command), 0)

	if p.returncode != 0 or globals.verbose:
		displayText('normal', 'commandStdout :', 0)
		displayText('normal', commandStdout, 0)
		displayText('normal', 'commandStderr :', 0)
		displayText('normal', commandStderr, 0)

	if p.returncode != 0 and treatErrorAsWarning =='no':
		terminateTest(1)

	return commandStdout, commandStderr

def remoteFileCopy(remotePort, scpSource, scpDestination):
	displayText('cyan', 'copying file from %s to %s' % (scpSource, scpDestination), 0)

	command = ['scp', '-P', str(remotePort), scpSource, scpDestination]
	commandStdout, commandStderr = executeCommand(command)

def patchAppliConfigurationFile(appliConfigurationFile):
	if not os.path.isfile(appliConfigurationFile):
		displayText('red', 'appliConfigurationFile (%s) does not exist' % appliConfigurationFile, 0)
		terminateTest(1)

	sectionFound = False
	for line in fileinput.FileInput(appliConfigurationFile, inplace=1):
		# search for section : "studioProfile": {
		if re.match('(.*)"studioProfile": {(.*)', line):
			sectionFound = True

		if sectionFound == True:
			# update studio IP address from globals.windowsVmStudioIpAddressForSstTraffic
			if re.match('(.*)"ipAddress": "(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})",(.*)', line):
				line = re.sub('"ipAddress": "(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})",', '"ipAddress": "%s",' % globals.windowsVmStudioIpAddressForSstTraffic, line)
				sectionFound = False

		# write line
		print(line, end='')

if __name__ == '__main__':

	globals.scriptStartTime = time.time()

	displayText('normal', 'normal text', 0)
	displayText('black', 'black text', 0)
	displayText('red', 'red text', 0)
	displayText('green', 'green text', 0)
	displayText('yellow', 'yellow text', 0)
	displayText('blue', 'blue text', 0)
	displayText('magenta', 'magenta text', 0)
	displayText('cyan', 'cyan text', 0)
	terminateTest(0)
