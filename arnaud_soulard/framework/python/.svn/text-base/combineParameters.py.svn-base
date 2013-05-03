#! /usr/bin/python
# -*- coding: utf-8 -*-

# import python libraries
import argparse
import itertools
import json
import os
import sys
import time

# import aggregation-platform's libraries
import globals
import utils

parser = argparse.ArgumentParser(description = "combine all aggregation-platform parameters to build a json file")
# add positional arguments
##parser.add_argument("frequency", type = int, choices = range(25, 27), help = "picture frequency")
# add optional arguments
parser.add_argument("-n", "--no-colors", action = "store_true", help = "don't use colors in displayed text")
# add conflicting optional arguments
group = parser.add_mutually_exclusive_group()
group.add_argument("-q", "--quiet", action = "store_true", help = "be quiet")
group.add_argument("-v", "--verbose", action = "store_true", help = "be verbose")

args = parser.parse_args()

# overwrite inter modules variables
if args.no_colors:
	globals.colorEnabled = False
if args.quiet:
	globals.quiet = True
if args.verbose:
	globals.verbose = True

# --------------------------------------------------------------------------------------------------
# Common parameters
# --------------------------------------------------------------------------------------------------
# scenarioDuration : 60 seconds is a minimum for the aggregation algorithm to be tested
scenarioDuration = 120
scenarioComment = 'scenario automatically generated'
#scenarioEvolutionList = ['all parameters are constant during the scenario', 'TODO']
scenarioEvolutionList = ['all parameters are constant during the scenario']

# --------------------------------------------------------------------------------------------------
# Action parameters
# --------------------------------------------------------------------------------------------------
# actionModesList
#actionModesList = ['live_bw_test', 'live', 'forward']
actionModesList = ['forward']

# --------------------------------------------------------------------------------------------------
# SST-TX parameters
# --------------------------------------------------------------------------------------------------
# audioBitratesList is always CBR (unit : kbps)
#audioBitratesList = [16, 64, 256]
audioBitratesList = [128]
# videoBitratesList is CBR or VBR (unit : kbps)
#videoBitratesList = [100, 800, 2500, 10000]
videoBitratesList = [10000]
# videoBitratesModesList
#videoBitratesModesList = ['CBR', 'VBR']
videoBitratesModesList = ['VBR']
# frameRatesList in Hz
#frameRatesList = [25, 60]
frameRatesList = [60]
# gopDurationsList in ms
#gopDurationsList = [500, 1000]
gopDurationsList = [1000]
# iFramesVsPandBFramesRatiosList in %
#iFramesVsPandBFramesRatiosList = [50, 90]
iFramesVsPandBFramesRatiosList = [50]
# overEncodedBitratesList : plusieurs modes : respect de la consigne, dépassement de la consigne, dépassement de la spécification (bug encodeur) : indiquer (en kbps) le dépassement de la consigne/spec
overEncodedBitratesList = [0]

# timeWindowsList in ms
#timeWindowsList = [500, 1000, 2400, 6000, 19000]
timeWindowsList = [1000]

# --------------------------------------------------------------------------------------------------
# links parameters
# --------------------------------------------------------------------------------------------------
nbOfEthAdaptersList = [0, 1, 2]
# nbOfUsbEthAdaptersList : number of usbEthAdapters configured at the beginning of the test
#nbOfUsbEthAdaptersList = [1, 2, 4, 9]
nbOfUsbEthAdaptersList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
nbOfWifiAdaptersList =  [0, 1]

# bandWidthsList in kbps
#bandWidthsList = [1500, 10000]
#bandWidthsList = [10, 10000]
bandWidthsList = [10000]
# fixedLatenciesList in ms
#fixedLatenciesList = [1, 50, 350, 600]
fixedLatenciesList = [0]
# instantJittersList in ms
#instantJittersList = [0, 300, 1000, 3000]
#instantJittersList = [300]
instantJittersList = [0]
# queuesLengthsList in number of packets
#queuesLengthsList = [2, 10, 1000]
queuesLengthsList = [1000]
# packetsLossList in %
#packetsLossList = [0, 5, 30, 50, 80]
#packetsLossList = [0, 30]
packetsLossList = [0]

def main():
	for scenarioEvolution in scenarioEvolutionList:
		for audioBitrate in audioBitratesList:
			for videoBitrate in videoBitratesList:
				for frameRate in frameRatesList:
					for gopDuration in gopDurationsList:
						for iFramesVsPandBFramesRatio in iFramesVsPandBFramesRatiosList:
							createScenariiWithGivenSstTxParameters(scenarioEvolution, audioBitrate, videoBitrate, frameRate, gopDuration, iFramesVsPandBFramesRatio)

def createScenariiWithGivenSstTxParameters(scenarioEvolution, audioBitrate, videoBitrate, frameRate, gopDuration, iFramesVsPandBFramesRatio):
	for nbOfEthAdapters in nbOfEthAdaptersList:
		for nbOfUsbEthAdapters in nbOfUsbEthAdaptersList:
			for nbOfWifiAdapters in nbOfWifiAdaptersList:

				for gatewayBandWidth in bandWidthsList:
					for gatewayFixedLatency in fixedLatenciesList:
						for gatewayInstantJitter in instantJittersList:
							for gatewayQueueLength in queuesLengthsList:
								for gatewayPacketsLoss in packetsLossList:
									createScenariiWithGivenLinkParameters(scenarioEvolution, audioBitrate, videoBitrate, frameRate, gopDuration, iFramesVsPandBFramesRatio, nbOfEthAdapters, nbOfUsbEthAdapters, nbOfWifiAdapters, gatewayBandWidth, gatewayFixedLatency, gatewayInstantJitter, gatewayQueueLength, gatewayPacketsLoss)

def createScenariiWithGivenLinkParameters(scenarioEvolution, audioBitrate, videoBitrate, frameRate, gopDuration, iFramesVsPandBFramesRatio, nbOfEthAdapters, nbOfUsbEthAdapters, nbOfWifiAdapters, gatewayBandWidth, gatewayFixedLatency, gatewayInstantJitter, gatewayQueueLength, gatewayPacketsLoss):

	# base scenarii
	for videoBitrateMode in videoBitratesModesList:
		if videoBitrateMode == 'VBR':
			for actionMode in actionModesList:
				if actionMode == 'live_bw_test':
					for timeWindow in timeWindowsList:
						for overEncodedBitrate in overEncodedBitratesList:
							addEntry(scenarioComment, scenarioEvolution, scenarioDuration, actionMode, overEncodedBitrate, audioBitrate, videoBitrateMode, videoBitrate, frameRate, gopDuration, iFramesVsPandBFramesRatio, timeWindow, nbOfEthAdapters, nbOfUsbEthAdapters, nbOfWifiAdapters, gatewayBandWidth, gatewayFixedLatency, gatewayInstantJitter, gatewayQueueLength, gatewayPacketsLoss)
				elif actionMode == 'live':
					for timeWindow in timeWindowsList:
						overEncodedBitrate = 0
						addEntry(scenarioComment, scenarioEvolution, scenarioDuration, actionMode, overEncodedBitrate, audioBitrate, videoBitrateMode, videoBitrate, frameRate, gopDuration, iFramesVsPandBFramesRatio, timeWindow, nbOfEthAdapters, nbOfUsbEthAdapters, nbOfWifiAdapters, gatewayBandWidth, gatewayFixedLatency, gatewayInstantJitter, gatewayQueueLength, gatewayPacketsLoss)
				elif actionMode == 'forward':
					timeWindow = 'not used'
					overEncodedBitrate = 0
					addEntry(scenarioComment, scenarioEvolution, scenarioDuration, actionMode, overEncodedBitrate, audioBitrate, videoBitrateMode, videoBitrate, frameRate, gopDuration, iFramesVsPandBFramesRatio, timeWindow, nbOfEthAdapters, nbOfUsbEthAdapters, nbOfWifiAdapters, gatewayBandWidth, gatewayFixedLatency, gatewayInstantJitter, gatewayQueueLength, gatewayPacketsLoss)
				else:
					utils.displayText('red', 'actionMode %s not treated" failed' % actionMode, 0)
					sys.exit(1)

		elif videoBitrateMode == 'CBR':
			for actionMode in actionModesList:
				if actionMode == 'live_bw_test':
					# no live_bw_test in CBR
					#utils.displayText('yellow', 'no live_bw_test in CBR, no scenario generated', 0)
					continue
				elif actionMode == 'live':
					for timeWindow in timeWindowsList:
						overEncodedBitrate = 0
						addEntry(scenarioComment, scenarioEvolution, scenarioDuration, actionMode, overEncodedBitrate, audioBitrate, videoBitrateMode, videoBitrate, frameRate, gopDuration, iFramesVsPandBFramesRatio, timeWindow, nbOfEthAdapters, nbOfUsbEthAdapters, nbOfWifiAdapters, gatewayBandWidth, gatewayFixedLatency, gatewayInstantJitter, gatewayQueueLength, gatewayPacketsLoss)
				elif actionMode == 'forward':
					overEncodedBitrate = 0
					addEntry(scenarioComment, scenarioEvolution, scenarioDuration, actionMode, overEncodedBitrate, audioBitrate, videoBitrateMode, videoBitrate, frameRate, gopDuration, iFramesVsPandBFramesRatio, timeWindow, nbOfEthAdapters, nbOfUsbEthAdapters, nbOfWifiAdapters, gatewayBandWidth, gatewayFixedLatency, gatewayInstantJitter, gatewayQueueLength, gatewayPacketsLoss)
				else:
					utils.displayText('red', 'actionMode %s not treated" failed' % actionMode, 0)
					sys.exit(1)
		else:
			utils.displayText('red', 'videoBitrateMode %s not treated" failed' % videoBitrateMode, 0)
			sys.exit(1)


def addEntry(scenarioComment, scenarioEvolution, scenarioDuration, actionMode, overEncodedBitrate, audioBitrate, videoBitrateMode, videoBitrate, frameRate, gopDuration, iFramesVsPandBFramesRatio, timeWindow, nbOfEthAdapters, nbOfUsbEthAdapters, nbOfWifiAdapters, gatewayBandWidth, gatewayFixedLatency, gatewayInstantJitter, gatewayQueueLength, gatewayPacketsLoss):

	global nbOfNewScenarii

	# mix eth parameters
	for ethAdaptersBandWidthsSubList in itertools.combinations_with_replacement(bandWidthsList, nbOfEthAdapters):
		for ethAdaptersFixedLatenciesSubList in itertools.combinations_with_replacement(fixedLatenciesList, nbOfEthAdapters):
			for ethAdaptersInstantJittersSubList in itertools.combinations_with_replacement(instantJittersList, nbOfEthAdapters):
				for ethAdaptersQueuesLengthsSubList in itertools.combinations_with_replacement(queuesLengthsList, nbOfEthAdapters):
					for ethAdaptersPacketsLossSubList in itertools.combinations_with_replacement(packetsLossList, nbOfEthAdapters):

						# mix usbEthAdapters parameters
						for usbEthAdaptersBandWidthsSubList in itertools.combinations_with_replacement(bandWidthsList, nbOfUsbEthAdapters):
							for usbEthAdaptersFixedLatenciesSubList in itertools.combinations_with_replacement(fixedLatenciesList, nbOfUsbEthAdapters):
								for usbEthAdaptersInstantJittersSubList in itertools.combinations_with_replacement(instantJittersList, nbOfUsbEthAdapters):
									for usbEthAdaptersQueuesLengthsSubList in itertools.combinations_with_replacement(queuesLengthsList, nbOfUsbEthAdapters):
										for usbEthAdaptersPacketsLossSubList in itertools.combinations_with_replacement(packetsLossList, nbOfUsbEthAdapters):

											# mix wifi parameters
											for wifiAdaptersBandWidthsSubList in itertools.combinations_with_replacement(bandWidthsList, nbOfWifiAdapters):
												for wifiAdaptersFixedLatenciesSubList in itertools.combinations_with_replacement(fixedLatenciesList, nbOfWifiAdapters):
													for wifiAdaptersInstantJittersSubList in itertools.combinations_with_replacement(instantJittersList, nbOfWifiAdapters):
														for wifiAdaptersQueuesLengthsSubList in itertools.combinations_with_replacement(queuesLengthsList, nbOfWifiAdapters):
															for wifiAdaptersPacketsLossSubList in itertools.combinations_with_replacement(packetsLossList, nbOfWifiAdapters):

																# for debugging purpose
																#utils.displayText('normal', '---------------------------------------------------------- summary of parameters ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', 0)
																#utils.displayText('blue', 'scenarioComment : %s' % scenarioComment, 0)
																#utils.displayText('blue', 'scenarioEvolution : %s' % scenarioEvolution, 0)
																#utils.displayText('blue', 'scenarioDuration : %d' % scenarioDuration, 0)
																#utils.displayText('blue', 'actionModesList : %s' % actionModesList, 0)
																#utils.displayText('blue', 'audioBitratesList : %s' % audioBitratesList, 0)
																#utils.displayText('blue', 'videoBitratesList : %s' % videoBitratesList, 0)
																#utils.displayText('blue', 'videoBitratesModesList : %s' % videoBitratesModesList, 0)
																#utils.displayText('blue', 'frameRatesList : %s' % frameRatesList, 0)
																#utils.displayText('blue', 'gopDurationsList : %s' % gopDurationsList, 0)
																#utils.displayText('blue', 'iFramesVsPandBFramesRatiosList : %s' % iFramesVsPandBFramesRatiosList, 0)
																#utils.displayText('blue', 'overEncodedBitratesList : %s' % overEncodedBitratesList, 0)
																#utils.displayText('blue', 'timeWindowsList : %s' % timeWindowsList, 0)
																#utils.displayText('blue', 'gatewayBandWidth : %s' % gatewayBandWidth, 0)
																#utils.displayText('blue', 'gatewayFixedLatency : %s' % gatewayFixedLatency, 0)
																#utils.displayText('blue', 'gatewayInstantJitter : %s' % gatewayInstantJitter, 0)
																#utils.displayText('blue', 'gatewayQueueLength : %s' % gatewayQueueLength, 0)
																#utils.displayText('blue', 'gatewayPacketsLoss : %s' % gatewayPacketsLoss, 0)

																#utils.displayText('blue', 'nbOfEthAdaptersList : %s' % nbOfEthAdaptersList, 0)
																#utils.displayText('blue', 'ethAdaptersBandWidthsSubList : %s' % str(ethAdaptersBandWidthsSubList), 0)
																#utils.displayText('blue', 'ethAdaptersFixedLatenciesSubList : %s' % str(ethAdaptersFixedLatenciesSubList), 0)
																#utils.displayText('blue', 'ethAdaptersInstantJittersSubList : %s' % str(ethAdaptersInstantJittersSubList), 0)
																#utils.displayText('blue', 'ethAdaptersQueuesLengthsSubList : %s' % str(ethAdaptersQueuesLengthsSubList), 0)
																#utils.displayText('blue', 'ethAdaptersPacketsLossSubList : %s' % str(ethAdaptersPacketsLossSubList), 0)
																#utils.displayText('blue', 'nbOfUsbEthAdaptersList : %s' % nbOfUsbEthAdaptersList, 0)
																#utils.displayText('blue', 'usbEthAdaptersBandWidthsSubList : %s' % str(usbEthAdaptersBandWidthsSubList), 0)
																#utils.displayText('blue', 'usbEthAdaptersFixedLatenciesSubList : %s' % str(usbEthAdaptersFixedLatenciesSubList), 0)
																#utils.displayText('blue', 'usbEthAdaptersInstantJittersSubList : %s' % str(usbEthAdaptersInstantJittersSubList), 0)
																#utils.displayText('blue', 'usbEthAdaptersQueuesLengthsSubList : %s' % str(usbEthAdaptersQueuesLengthsSubList), 0)
																#utils.displayText('blue', 'usbEthAdaptersPacketsLossSubList : %s' % str(usbEthAdaptersPacketsLossSubList), 0)
																#utils.displayText('blue', 'nbOfWifiAdaptersList : %s' % nbOfWifiAdaptersList, 0)
																#utils.displayText('blue', 'wifiAdaptersBandWidthsSubList : %s' % str(wifiAdaptersBandWidthsSubList), 0)
																#utils.displayText('blue', 'wifiAdaptersFixedLatenciesSubList : %s' % str(wifiAdaptersFixedLatenciesSubList), 0)
																#utils.displayText('blue', 'wifiAdaptersInstantJittersSubList : %s' % str(wifiAdaptersInstantJittersSubList), 0)
																#utils.displayText('blue', 'wifiAdaptersQueuesLengthsSubList : %s' % str(wifiAdaptersQueuesLengthsSubList), 0)
																#utils.displayText('blue', 'wifiAdaptersPacketsLossSubList : %s' % str(wifiAdaptersPacketsLossSubList), 0)
																#utils.displayText('normal', '-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', 0)

																fullEntry = {}
																fullEntry['scenarioComment'] = scenarioComment
																fullEntry['scenarioEvolution'] = scenarioEvolution
																fullEntry['scenarioDuration'] = scenarioDuration
																fullEntry['actionMode'] = actionMode
																fullEntry['overEncodedBitrate'] = overEncodedBitrate
																fullEntry['audioBitrate'] = audioBitrate
																fullEntry['videoBitrateMode'] = videoBitrateMode
																fullEntry['videoBitrate'] = videoBitrate
																fullEntry['frameRate'] = frameRate
																fullEntry['gopDuration'] = gopDuration
																fullEntry['iFramesVsPandBFramesRatio'] = iFramesVsPandBFramesRatio
																fullEntry['timeWindow'] = timeWindow
																fullEntry['gateway'] = {'bandWidth' : gatewayBandWidth, 'fixedLatency' : gatewayFixedLatency, 'jitter' : gatewayInstantJitter, 'queueLength' : gatewayQueueLength, 'packetsLoss' : gatewayPacketsLoss}

																# set parameters for each eth link
																fullEntry['nbOfEthAdapters'] = nbOfEthAdapters
																fullEntry['ethAdapters'] = []
																for index in range(0, nbOfEthAdapters):
																	# for debugging purpose
																	#utils.displayText('cyan', 'ethAdaptersBandWidthsSubList[%d] : %d' % (index, ethAdaptersBandWidthsSubList[index]), 0)
																	#utils.displayText('cyan', 'ethAdaptersFixedLatenciesSubList[%d] : %d' % (index, ethAdaptersFixedLatenciesSubList[index]), 0)
																	#utils.displayText('cyan', 'ethAdaptersInstantJittersSubList[%d] : %d' % (index, ethAdaptersInstantJittersSubList[index]), 0)
																	#utils.displayText('cyan', 'ethAdaptersQueuesLengthsSubList[%d] : %d' % (index, ethAdaptersQueuesLengthsSubList[index]), 0)
																	#utils.displayText('cyan', 'ethAdaptersPacketsLossSubList[%d] : %d' % (index, ethAdaptersPacketsLossSubList[index]), 0)
																	partialEntry = {}

																	partialEntry['bandWidth'] = ethAdaptersBandWidthsSubList[index]
																	partialEntry['fixedLatency'] = ethAdaptersFixedLatenciesSubList[index]
																	partialEntry['jitter'] = ethAdaptersInstantJittersSubList[index]
																	partialEntry['queueLength'] = ethAdaptersQueuesLengthsSubList[index]
																	partialEntry['packetsLoss'] = ethAdaptersPacketsLossSubList[index]

																	fullEntry['ethAdapters'].append(partialEntry)

																# set parameters for each usb-eth link
																fullEntry['nbOfUsbEthAdapters'] = nbOfUsbEthAdapters
																fullEntry['usbEthAdapters'] = []
																for index in range(0, nbOfUsbEthAdapters):
																	# for debugging purpose
																	#utils.displayText('cyan', 'usbEthAdaptersBandWidthsSubList[%d] : %d' % (index, usbEthAdaptersBandWidthsSubList[index]), 0)
																	#utils.displayText('cyan', 'usbEthAdaptersFixedLatenciesSubList[%d] : %d' % (index, usbEthAdaptersFixedLatenciesSubList[index]), 0)
																	#utils.displayText('cyan', 'usbEthAdaptersInstantJittersSubList[%d] : %d' % (index, usbEthAdaptersInstantJittersSubList[index]), 0)
																	#utils.displayText('cyan', 'usbEthAdaptersQueuesLengthsSubList[%d] : %d' % (index, usbEthAdaptersQueuesLengthsSubList[index]), 0)
																	#utils.displayText('cyan', 'usbEthAdaptersPacketsLossSubList[%d] : %d' % (index, usbEthAdaptersPacketsLossSubList[index]), 0)
																	partialEntry = {}

																	partialEntry['bandWidth'] = usbEthAdaptersBandWidthsSubList[index]
																	partialEntry['fixedLatency'] = usbEthAdaptersFixedLatenciesSubList[index]
																	partialEntry['jitter'] = usbEthAdaptersInstantJittersSubList[index]
																	partialEntry['queueLength'] = usbEthAdaptersQueuesLengthsSubList[index]
																	partialEntry['packetsLoss'] = usbEthAdaptersPacketsLossSubList[index]

																	fullEntry['usbEthAdapters'].append(partialEntry)

																# set parameters for each wifi link
																fullEntry['nbOfWifiAdapters'] = nbOfWifiAdapters
																fullEntry['wifiAdapters'] = []
																for index in range(0, nbOfWifiAdapters):
																	# for debugging purpose
																	#utils.displayText('cyan', 'wifiAdaptersBandWidthsSubList[%d] : %d' % (index, wifiAdaptersBandWidthsSubList[index]), 0)
																	#utils.displayText('cyan', 'wifiAdaptersFixedLatenciesSubList[%d] : %d' % (index, wifiAdaptersFixedLatenciesSubList[index]), 0)
																	#utils.displayText('cyan', 'wifiAdaptersInstantJittersSubList[%d] : %d' % (index, wifiAdaptersInstantJittersSubList[index]), 0)
																	#utils.displayText('cyan', 'wifiAdaptersQueuesLengthsSubList[%d] : %d' % (index, wifiAdaptersQueuesLengthsSubList[index]), 0)
																	#utils.displayText('cyan', 'wifiAdaptersPacketsLossSubList[%d] : %d' % (index, wifiAdaptersPacketsLossSubList[index]), 0)
																	partialEntry = {}

																	partialEntry['bandWidth'] = wifiAdaptersBandWidthsSubList[index]
																	partialEntry['fixedLatency'] = wifiAdaptersFixedLatenciesSubList[index]
																	partialEntry['jitter'] = wifiAdaptersInstantJittersSubList[index]
																	partialEntry['queueLength'] = wifiAdaptersQueuesLengthsSubList[index]
																	partialEntry['packetsLoss'] = wifiAdaptersPacketsLossSubList[index]

																	fullEntry['wifiAdapters'].append(partialEntry)

																# add fullEntry only if it is not already present in myJson
																entryExist = False
																for index in range(0, len(myJson) - 1):
																	currentScenario = myJson['%06d' % index]
																	if fullEntry == currentScenario:
																		entryExist = True
																		break

																if entryExist:
																	utils.displayText('yellow', '[WARNING] scenario already present in file %s' % globals.jsonFileName, 0)
																else:
																	newScenarii['%06d' % nbOfNewScenarii] = fullEntry
																	nbOfNewScenarii += 1
# main

globals.scriptStartTime = time.time()

# initializations
newScenarii = {}
nbOfNewScenarii = 0

if not os.path.isfile(globals.jsonFileName):
	utils.displayText('red', 'file %s does not exist, create an empty one first' % globals.jsonFileName, 0)
	utils.terminateTest(1)

utils.displayText('blue', 'deserializing full object from %s' % globals.jsonFileName, 0)

if os.path.isfile(globals.jsonFileName):
	with open(globals.jsonFileName, 'r') as f:
		myJson = json.load(f)
else:
		utils.displayText('red', 'file %s does not exist, run combineParameters.py first' % globals.jsonFileName, 0)
		utils.terminateTest(1)

lastScenarioId = myJson['lastScenarioId']

main()

if nbOfNewScenarii > 0:
	utils.displayText('black', 'writing %d scenarii in file %s' % (nbOfNewScenarii, globals.jsonFileName), 0)

	for index in range(0, len(newScenarii)):
		myJson['%06d' % (int(lastScenarioId) + index + 1)] = newScenarii['%06d' % index]

	myJson['lastScenarioId'] = '%06d' % (int(lastScenarioId) + len(newScenarii))

	with open(globals.jsonFileName, 'w') as f:
		json.dump(myJson, f, sort_keys = True, indent=2)
else:
	utils.displayText('green', 'no new scenario to add in file %s' % globals.jsonFileName, 0)
	utils.terminateTest(1)
