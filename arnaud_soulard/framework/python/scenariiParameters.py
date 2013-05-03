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

def deserializeObject():

	utils.displayText('blue', 'deserializing full object from %s' % globals.jsonFileName, 0)

	if os.path.isfile(globals.jsonFileName):
		with open(globals.jsonFileName, 'r') as f:
			myJson = json.load(f)
	else:
			utils.displayText('red', 'file %s does not exist, run combineParameters.py first' % globals.jsonFileName, 0)
			utils.terminateTest(1)

	# deserialize scenParameters only possible if globals.scenarioId has been set
	if globals.scenarioId != -1:
		scenParameters = myJson['%06d' % globals.scenarioId]

		globals.scenarioComment = scenParameters['scenarioComment']
		globals.scenarioEvolution = scenParameters['scenarioEvolution']
		globals.scenarioDuration = int(scenParameters['scenarioDuration'])

		globals.actionMode = scenParameters['actionMode']
		globals.overEncodedBitrate = int(scenParameters['overEncodedBitrate'])
		globals.audioBitrate = int(scenParameters['audioBitrate'])
		globals.videoBitrateMode = scenParameters['videoBitrateMode']
		globals.videoBitrate = int(scenParameters['videoBitrate'])
		globals.frameRate = int(scenParameters['frameRate'])
		globals.gopDuration = int(scenParameters['gopDuration'])
		globals.iFramesVsPandBFramesRatio = int(scenParameters['iFramesVsPandBFramesRatio'])
		globals.timeWindow = int(scenParameters['timeWindow'])

		globals.gatewayBandWidth = int(scenParameters['gateway']['bandWidth'])
		globals.gatewayFixedLatency = int(scenParameters['gateway']['fixedLatency'])
		globals.gatewayInstantJitter = int(scenParameters['gateway']['jitter'])
		globals.gatewayQueueLength = int(scenParameters['gateway']['queueLength'])
		globals.gatewayPacketsLoss = int(scenParameters['gateway']['packetsLoss'])

		globals.nbOfEthAdapters = int(scenParameters['nbOfEthAdapters'])
		for i in range(globals.nbOfEthAdapters):
			globals.ethAdaptersFixedLatenciesList.append(scenParameters['ethAdapters'][i]['fixedLatency'])
			globals.ethAdaptersJittersList.append(scenParameters['ethAdapters'][i]['jitter'])
			globals.ethAdaptersBandWidthsList.append(scenParameters['ethAdapters'][i]['bandWidth'])
			globals.ethAdaptersPacketLossList.append(scenParameters['ethAdapters'][i]['packetsLoss'])
			globals.ethAdaptersQueueLengthList.append(scenParameters['ethAdapters'][i]['queueLength'])

		globals.nbOfUsbEthAdapters = int(scenParameters['nbOfUsbEthAdapters'])
		for i in range(globals.nbOfUsbEthAdapters):
			globals.usbEthAdaptersFixedLatenciesList.append(scenParameters['usbEthAdapters'][i]['fixedLatency'])
			globals.usbEthAdaptersJittersList.append(scenParameters['usbEthAdapters'][i]['jitter'])
			globals.usbEthAdaptersBandWidthsList.append(scenParameters['usbEthAdapters'][i]['bandWidth'])
			globals.usbEthAdaptersPacketLossList.append(scenParameters['usbEthAdapters'][i]['packetsLoss'])
			globals.usbEthAdaptersQueueLengthList.append(scenParameters['usbEthAdapters'][i]['queueLength'])

		globals.nbOfWifiAdapters = int(scenParameters['nbOfWifiAdapters'])
		for i in range(globals.nbOfWifiAdapters):
			globals.wifiAdaptersFixedLatenciesList.append(scenParameters['wifiAdapters'][i]['fixedLatency'])
			globals.wifiAdaptersJittersList.append(scenParameters['wifiAdapters'][i]['jitter'])
			globals.wifiAdaptersBandWidthsList.append(scenParameters['wifiAdapters'][i]['bandWidth'])
			globals.wifiAdaptersPacketLossList.append(scenParameters['wifiAdapters'][i]['packetsLoss'])
			globals.wifiAdaptersQueueLengthList.append(scenParameters['wifiAdapters'][i]['queueLength'])

	globals.lastScenarioId = myJson['lastScenarioId']
	#return scenParameters

if __name__ == '__main__':

	globals.scriptStartTime = time.time()

	parser = argparse.ArgumentParser(description="get parameters from a scenario ID")
	# add positional arguments
	parser.add_argument("scenarioId", type=int, help="the scenario ID")

	args = parser.parse_args()

	globals.scenarioId = args.scenarioId

	scenParameters = deserializeObject()

	# for debugging purpose
	utils.displayText('normal', 'scenarioComment : %s' % globals.scenarioComment, 0)
	utils.displayText('normal', 'scenarioEvolution : %s' % globals.scenarioEvolution, 0)
	utils.displayText('normal', 'scenarioDuration : %d' % globals.scenarioDuration, 0)

	utils.displayText('normal', 'actionMode : %s' % globals.actionMode, 0)
	utils.displayText('normal', 'overEncodedBitrate : %d' % globals.overEncodedBitrate, 0)
	utils.displayText('normal', 'audioBitrate : %d' % globals.audioBitrate, 0)
	utils.displayText('normal', 'videoBitrateMode : %s' % globals.videoBitrateMode, 0)
	utils.displayText('normal', 'videoBitrate : %d' % globals.videoBitrate, 0)
	utils.displayText('normal', 'frameRate : %d' % globals.frameRate, 0)
	utils.displayText('normal', 'gopDuration : %d' % globals.gopDuration, 0)
	utils.displayText('normal', 'iFramesVsPandBFramesRatio : %d' % globals.iFramesVsPandBFramesRatio, 0)
	utils.displayText('normal', 'timeWindow : %d' % globals.timeWindow, 0)

	utils.displayText('normal', 'gatewayBandWidth : %d' % globals.gatewayBandWidth, 0)
	utils.displayText('normal', 'gatewayFixedLatency : %d' % globals.gatewayFixedLatency, 0)
	utils.displayText('normal', 'gatewayInstantJitter : %d' % globals.gatewayInstantJitter, 0)
	utils.displayText('normal', 'gatewayQueueLength : %d' % globals.gatewayQueueLength, 0)
	utils.displayText('normal', 'gatewayPacketsLoss : %d' % globals.gatewayPacketsLoss, 0)

	utils.displayText('normal', 'nbOfEthAdapters : %d' % globals.nbOfEthAdapters, 0)
	utils.displayText('normal', 'ethAdaptersFixedLatenciesList : %s' % globals.ethAdaptersFixedLatenciesList, 0)
	utils.displayText('normal', 'ethAdaptersJittersList : %s' % globals.ethAdaptersJittersList, 0)
	utils.displayText('normal', 'ethAdaptersBandWidthsList : %s' % globals.ethAdaptersBandWidthsList, 0)
	utils.displayText('normal', 'ethAdaptersPacketLossList : %s' % globals.ethAdaptersPacketLossList, 0)
	utils.displayText('normal', 'ethAdaptersQueueLengthList : %s' % globals.ethAdaptersQueueLengthList, 0)

	utils.displayText('normal', 'nbOfUsbEthAdapters : %d' % globals.nbOfUsbEthAdapters, 0)
	utils.displayText('normal', 'usbEthAdaptersFixedLatenciesList : %s' % globals.usbEthAdaptersFixedLatenciesList, 0)
	utils.displayText('normal', 'usbEthAdaptersJittersList : %s' % globals.usbEthAdaptersJittersList, 0)
	utils.displayText('normal', 'usbEthAdaptersBandWidthsList : %s' % globals.usbEthAdaptersBandWidthsList, 0)
	utils.displayText('normal', 'usbEthAdaptersPacketLossList : %s' % globals.usbEthAdaptersPacketLossList, 0)
	utils.displayText('normal', 'usbEthAdaptersQueueLengthList : %s' % globals.usbEthAdaptersQueueLengthList, 0)

	utils.displayText('normal', 'nbOfWifiAdapters : %d' % globals.nbOfWifiAdapters, 0)
	utils.displayText('normal', 'wifiAdaptersFixedLatenciesList : %s' % globals.wifiAdaptersFixedLatenciesList, 0)
	utils.displayText('normal', 'wifiAdaptersJittersList : %s' % globals.wifiAdaptersJittersList, 0)
	utils.displayText('normal', 'wifiAdaptersBandWidthsList : %s' % globals.wifiAdaptersBandWidthsList, 0)
	utils.displayText('normal', 'wifiAdaptersPacketLossList : %s' % globals.wifiAdaptersPacketLossList, 0)
	utils.displayText('normal', 'wifiAdaptersQueueLengthList : %s' % globals.wifiAdaptersQueueLengthList, 0)

	utils.displayText('normal', 'lastScenarioId : %d' % globals.lastScenarioId, 0)

	utils.terminateTest(0)
