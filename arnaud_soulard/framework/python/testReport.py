#! /usr/bin/python
# -*- coding: utf-8 -*-

# import python libraries
#import re
#import mimetypes
import os
import pdb
import re
#import smtplib
import sys
import time

# import aggregation-platform's libraries
import globals
#import subversion
import utils

def buildMainHtmlPage():

	fileName = globals.baseDirectoryForResults + '/' + 'index.html'
	title = 'aggregation-platform\'s tests results report'

	fileHandle = open(fileName, 'w')
	fileHandle.write('<html>\n')
	fileHandle.write('<head>\n')
	fileHandle.write('<meta http-equiv="content-type" content="text/html; charset=utf8>"</meta>\n')
	fileHandle.write('<title>%s</title>\n' % title)
	utils.addCssInformations(fileHandle)
	fileHandle.write('</head>\n')
	fileHandle.write('<body>\n')

	fileHandle.write('<h1>%s</h1>\n' % title)

	fileHandle.write('<table>\n')

	fileHandle.write('<colgroup>\n')
	fileHandle.write('<col width="50%">\n')
	fileHandle.write('<col width="50%">\n')
	fileHandle.write('</colgroup>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('appliVersion', 'results sorted by appliVersion'))
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii', 'results sorted by scenarioId'))
	fileHandle.write('</tr>\n')

	fileHandle.write('</table>\n')

	fileHandle.write('<h2>scenarii description</h2>\n')

	fileHandle.write('<table>\n')

	fileHandle.write('<colgroup>\n')
	fileHandle.write('<col width="50%">\n')
	fileHandle.write('<col width="50%">\n')
	fileHandle.write('</colgroup>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/0', '0'))
	fileHandle.write('<th>scenario ID used for experimentations</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii', '1-54'))
	fileHandle.write('<th>all combinations of network interfaces configured with live_bw_test, abr : 128, frameRate : 60, bandWidth : 10000, fixedLatency : 0, jitter : 0, packetsLoss : 0, queueLength : 1000, gopDuration : 1000, iFramesVsPandBFramesRatio : 50, overEncodedBitrate : 0, scenarioDuration : 120, timeWindow : 1000, videoBitrate : 10000, videoBitrateMode : VBR</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/163', '163'))
	fileHandle.write('<th>scenario pattern / network link : 1 network interface (nbOfUsbEthAdapters = 1) configured with live_bw_test, abr : 48, frameRate : 25, bandWidth : 4000, fixedLatency : 50, jitter : 300, packetsLoss : 0, queueLength : 1000, gopDuration : 500, iFramesVsPandBFramesRatio : 50, overEncodedBitrate : 0, scenarioDuration : 120, timeWindow : 2400, videoBitrate : 10000, videoBitrateMode : VBR</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/164', '164'))
	fileHandle.write('<th>idem 163, minimal value for abr : 16</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/165', '165'))
	fileHandle.write('<th>idem 163, maximal value for abr : 256</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/166', '166'))
	fileHandle.write('<th>idem 163, minimal value for frameRate : 25</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/167', '167'))
	fileHandle.write('<th>idem 163, maximal value for frameRate : 60</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/168', '168'))
	fileHandle.write('<th>idem 163, minimal value for bandWidth : 10</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/169', '169'))
	fileHandle.write('<th>idem 163, maximal value for bandWidth : 10000</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/170', '170'))
	fileHandle.write('<th>idem 163, minimal value for fixedLatency : 0</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/171', '171'))
	fileHandle.write('<th>idem 163, maximal value for fixedLatency : 600</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/172', '172'))
	fileHandle.write('<th>idem 163, minimal value for jitter : 0</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/173', '173'))
	fileHandle.write('<th>idem 163, maximal value for jitter : 3000</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/174', '174'))
	fileHandle.write('<th>idem 163, minimal value for packetsLoss : 0</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/175', '175'))
	fileHandle.write('<th>idem 163, maximal value for packetsLoss : 80</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/176', '176'))
	fileHandle.write('<th>idem 163, minimal value for queueLength : 2</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/177', '177'))
	fileHandle.write('<th>idem 163, maximal value for queueLength : 1000</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/178', '178'))
	fileHandle.write('<th>idem 163, minimal value for gopDuration : 500</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/179', '179'))
	fileHandle.write('<th>idem 163, maximal value for gopDuration : 1000</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/180', '180'))
	fileHandle.write('<th>idem 163, minimal value for iFramesVsPandBFramesRatio : 50</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/181', '181'))
	fileHandle.write('<th>idem 163, maximal value for iFramesVsPandBFramesRatio : 90</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/182', '182'))
	fileHandle.write('<th>idem 163, minimal value for timeWindow : 500</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/183', '183'))
	fileHandle.write('<th>idem 163, maximal value for timeWindow : 19000</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/184', '184'))
	fileHandle.write('<th>idem 163, minimal value for videoBitrate : 100</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('scenarii/185', '185'))
	fileHandle.write('<th>idem 163, maximal value for videoBitrate : 10000</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('</table>\n')

	fileHandle.write('</body>\n')
	fileHandle.write('</html>\n')
	fileHandle.close()

def buildHtmlPage(directory, entriesList, entriesType):

	fileName = directory + '/' + 'index.html'
	title = 'aggregation-platform\'s test report (results summary - sorted by %s)' % entriesType

	fileHandle = open(fileName, 'w')
	fileHandle.write('<html>\n')
	fileHandle.write('<head>\n')
	fileHandle.write('<meta http-equiv="content-type" content="text/html; charset=utf8>"</meta>\n')
	fileHandle.write('<title>%s</title>\n' % title)
	utils.addCssInformations(fileHandle)
	fileHandle.write('</head>\n')
	fileHandle.write('<body>\n')

	fileHandle.write('<h1>%s</h1>\n' % title)

	fileHandle.write('<table>\n')

	fileHandle.write('<colgroup>\n')
	fileHandle.write('<col width="25%">\n')
	fileHandle.write('<col width="25%">\n')
	fileHandle.write('<col width="25%">\n')
	fileHandle.write('<col width="25%">\n')
	fileHandle.write('</colgroup>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th>%s</th>\n' % entriesType)
	fileHandle.write('<th>nb of OK</th>\n')
	fileHandle.write('<th>nb of KO</th>\n')
	fileHandle.write('<th>nb of inconclusive</th>\n')
	fileHandle.write('</tr>\n')

	# sort entriesList TODO : find a better way to have the list sorted, even if directories are integers
	# -----
	for index in range(len(entriesList)):
		if entriesList[index].isdigit():
			entriesList[index] = int(entriesList[index])

	entriesList.sort()

	for index in range(len(entriesList)):
			entriesList[index] = str(entriesList[index])

	#utils.displayText('yellow', 'entriesList : %s' % entriesList, 0)
	# -----

	for entry in entriesList:
		nbOfOk = 0
		nbOfKo = 0
		nbOfInconclusive = 0
		for root, dirs, files in os.walk(directory + '/' + '%s' % entry, topdown=True, followlinks=True):
			if re.search('OK$', root) != None:
				nbOfOk += len(dirs)
			if re.search('KO$', root) != None:
				nbOfKo += len(dirs)
			if re.search('inconclusive$', root) != None:
				nbOfInconclusive += len(dirs)

		fileHandle.write('<tr>\n')
		fileHandle.write('<th><a href="%s">%s</a></th>\n' % (entry, entry))

		if nbOfOk == 0:
			fileHandle.write('<th>%s</th>\n' % nbOfOk)
		else:
			fileHandle.write('<th>%s</th>\n' % nbOfOk)
			#fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('OK', nbOfOk))
		if nbOfKo == 0:
			fileHandle.write('<th>%s</th>\n' % nbOfKo)
		else:
			fileHandle.write('<th>%s</th>\n' % nbOfKo)
			#fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('KO', nbOfKo))
		if nbOfInconclusive == 0:
			fileHandle.write('<th>%s</th>\n' % nbOfInconclusive)
		else:
			fileHandle.write('<th>%s</th>\n' % nbOfInconclusive)
			#fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('inconclusive', nbOfInconclusive))

		fileHandle.write('</tr>\n')

	fileHandle.write('</table>\n')

	fileHandle.write('</body>\n')
	fileHandle.write('</html>\n')
	fileHandle.close()

def buildScenarioHtmlPage(directory, entriesList, appliVersion, scenarioId):

	#utils.displayText('red', 'directory : %s' % directory, 0)
	#utils.displayText('red', 'entriesList : %s' % entriesList, 0)
	#utils.displayText('red', 'appliVersion : %s' % appliVersion, 0)
	#utils.displayText('red', 'scenarioId : %s' % scenarioId, 0)

	fileName = directory + '/' + 'index.html'
	title = 'aggregation-platform\'s test report (results summary for appliVersion %s, scenarioId %s)' % (appliVersion, scenarioId)

	fileHandle = open(fileName, 'w')
	fileHandle.write('<html>\n')
	fileHandle.write('<head>\n')
	fileHandle.write('<meta http-equiv="content-type" content="text/html; charset=utf8>"</meta>\n')
	fileHandle.write('<title>%s</title>\n' % title)
	utils.addCssInformations(fileHandle)
	fileHandle.write('</head>\n')
	fileHandle.write('<body>\n')

	fileHandle.write('<h1>%s</h1>\n' % title)

	fileHandle.write('<table>\n')

	fileHandle.write('<colgroup>\n')
	fileHandle.write('<col width="33%">\n')
	fileHandle.write('<col width="33%">\n')
	fileHandle.write('<col width="34%">\n')
	fileHandle.write('</colgroup>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th>nb of OK</th>\n')
	fileHandle.write('<th>nb of KO</th>\n')
	fileHandle.write('<th>nb of inconclusive</th>\n')
	fileHandle.write('</tr>\n')

	fileHandle.write('<tr>\n')

	nbOfOk = 0
	nbOfKo = 0
	nbOfInconclusive = 0
	for entry in entriesList:
		runsList = os.listdir(directory + '/' + entry)
		if runsList.count('index.html') == 1:
			runsList.remove('index.html')
		if entry == 'OK':
			nbOfOk = len(runsList)
		if entry == 'KO':
			nbOfKo = len(runsList)
		if entry == 'inconclusive':
			nbOfInconclusive = len(runsList)

	if nbOfOk == 0:
		fileHandle.write('<th>%s</th>\n' % nbOfOk)
	else:
		#fileHandle.write('<th>%s</th>\n' % nbOfOk)
		fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('OK', nbOfOk))
	if nbOfKo == 0:
		fileHandle.write('<th>%s</th>\n' % nbOfKo)
	else:
		#fileHandle.write('<th>%s</th>\n' % nbOfKo)
		fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('KO', nbOfKo))
	if nbOfInconclusive == 0:
		fileHandle.write('<th>%s</th>\n' % nbOfInconclusive)
	else:
		#fileHandle.write('<th>%s</th>\n' % nbOfInconclusive)
		fileHandle.write('<th><a href="%s">%s</a></th>\n' % ('inconclusive', nbOfInconclusive))

	fileHandle.write('</tr>\n')

	fileHandle.write('</table>\n')

	fileHandle.write('</body>\n')
	fileHandle.write('</html>\n')
	fileHandle.close()

def buildRunsHtmlPage(directory, entriesList, appliVersion, scenarioId, scenarioResult):

	fileName = directory + '/' + 'index.html'
	title = 'aggregation-platform\'s test report'

	fileHandle = open(fileName, 'w')
	fileHandle.write('<html>\n')
	fileHandle.write('<head>\n')
	fileHandle.write('<meta http-equiv="content-type" content="text/html; charset=utf8>"</meta>\n')
	fileHandle.write('<title>%s</title>\n' % title)
	utils.addCssInformations(fileHandle)
	fileHandle.write('</head>\n')
	fileHandle.write('<body>\n')

	fileHandle.write('<h1>%s</h1>\n' % title)

	fileHandle.write('<table>\n')

	fileHandle.write('<colgroup>\n')
	fileHandle.write('<col width="100%">\n')
	fileHandle.write('</colgroup>\n')

	fileHandle.write('<tr>\n')
	fileHandle.write('<th>runs with appliVersion %s, scenarioId %s, scenarioResult %s</th>\n' % (appliVersion, scenarioId, scenarioResult))
	fileHandle.write('</tr>\n')

	for entry in entriesList:
		fileHandle.write('<tr>\n')
		fileHandle.write('<th><a href="%s">%s</a></th>\n' % (entry, entry))
		fileHandle.write('</tr>\n')

	fileHandle.write('</table>\n')

	fileHandle.write('</body>\n')
	fileHandle.write('</html>\n')
	fileHandle.close()

	# create symbolink link to have results ordered by scenarioEntry / appliVersion / scenarioResult / run
	scenarioEntry = globals.baseScenariiDirectoryForResults  + '/' + '%s' % scenarioId + '/' + appliVersion
	if not os.path.isdir(scenarioEntry):
		os.makedirs(scenarioEntry)
	if not os.path.islink(scenarioEntry + '/' + scenarioResult):
		os.symlink(directory, scenarioEntry + '/' + scenarioResult)

def buildTestReport():

	buildMainHtmlPage()

	for root, dirs, files in os.walk(globals.baseVersionsDirectoryForResults, topdown=True):
		if root == globals.baseVersionsDirectoryForResults:
			if dirs.count('unknown') == 1:
				dirs.remove('unknown')

			buildHtmlPage(root, dirs, 'appliVersion')

		if re.search(globals.baseVersionsDirectoryForResults + '/' + '[0-9.]+~svn~[0-9]+$', root) != None or re.search(globals.baseVersionsDirectoryForResults + '/' + '[0-9]+.[0-9]+.[0-9]+-svn[0-9]+$', root) != None:
			buildHtmlPage(root, dirs, 'scenarioId')

		if re.search(globals.baseVersionsDirectoryForResults + '/' + '[0-9.]+~svn~[0-9]+' + '/' + '[0-9]+$', root) != None or re.search(globals.baseVersionsDirectoryForResults + '/' + '[0-9]+.[0-9]+.[0-9]+-svn[0-9]+' + '/' + '[0-9]+$', root) != None:
			dirs.sort()

			directorySplitList = root.split('/')
			scenarioId = directorySplitList[len(directorySplitList) -1]
			appliVersion = directorySplitList[len(directorySplitList) -2]

			buildScenarioHtmlPage(root, dirs, appliVersion, scenarioId)

		if re.search(globals.baseVersionsDirectoryForResults + '/' + '[0-9.]+~svn~[0-9]+' + '/' + '[0-9]+' + '/' + 'OK$|KO$|inconclusive$', root) != None or re.search(globals.baseVersionsDirectoryForResults + '/' + '[0-9]+.[0-9]+.[0-9]+-svn[0-9]+' + '/' + '[0-9]+' + '/' + 'OK$|KO$|inconclusive$', root) != None:
			dirs.sort()

			directorySplitList = root.split('/')
			appliVersion = directorySplitList[len(directorySplitList) -3]
			scenarioId = directorySplitList[len(directorySplitList) -2]
			scenarioResult = directorySplitList[len(directorySplitList) -1]

			buildRunsHtmlPage(root, dirs, appliVersion, scenarioId, scenarioResult)

	for root, dirs, files in os.walk(globals.baseScenariiDirectoryForResults, topdown=True, followlinks=True):

		if root == globals.baseScenariiDirectoryForResults:
			buildHtmlPage(root, dirs, 'scenarioId')

		if re.search(globals.baseScenariiDirectoryForResults + '/' + '[0-9]+$', root) != None:
			buildHtmlPage(root, dirs, 'appliVersion')

		if re.search(globals.baseScenariiDirectoryForResults + '/' + '[0-9]+' + '/' + '[0-9.]+~svn~[0-9]+$', root) != None or re.search(globals.baseScenariiDirectoryForResults + '/' + '[0-9]+' + '/' + '[0-9]+.[0-9]+.[0-9]+-svn[0-9]+$', root) != None:

			directorySplitList = root.split('/')
			appliVersion = directorySplitList[len(directorySplitList) -1]
			scenarioId = directorySplitList[len(directorySplitList) -2]

			buildScenarioHtmlPage(root, dirs, appliVersion, scenarioId)

		'''
		if re.search(globals.baseScenariiDirectoryForResults + '/' + '[0-9]+' + '/' + '[0-9.]+~svn~[0-9]+' + '/' + 'OK$|KO$|inconclusive$', root) != None:
			utils.displayText('blue', 'root : %s' % root, 0)
			utils.displayText('red', 'dirs : %s' % dirs, 0)
			utils.displayText('red', 'files : %s' % files, 0)

			directorySplitList = root.split('/')
			appliVersion = directorySplitList[len(directorySplitList) -3]
			scenarioId = directorySplitList[len(directorySplitList) -2]
			scenarioResult = directorySplitList[len(directorySplitList) -1]
			utils.displayText('black', 'appliVersion : %s' % appliVersion, 0)
			utils.displayText('black', 'scenarioId : %s' % scenarioId, 0)
			utils.displayText('black', 'scenarioResult : %s' % scenarioResult, 0)
			sys.exit(1)
			sys.exit(1)
			#buildHtmlPage(root, dirs, 'scenarioId')
			buildRunsHtmlPage(root, dirs, appliVersion, scenarioId, scenarioResult)
		'''

if __name__ == '__main__':

	globals.scriptStartTime = time.time()

	buildTestReport()

	utils.terminateTest(0)
