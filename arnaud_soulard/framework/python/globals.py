#! /usr/bin/python
# -*- coding: utf-8 -*-

# import python libraries
import os
import sys

# import aggregation-platform's libraries
import networkInterfaces
import utils

# create an empty htmlLogFileName from scriptFileName
scriptFileName = os.path.realpath(sys.argv[0])
scriptDirName = os.path.dirname(scriptFileName)
htmlLogFileName = os.path.splitext(scriptFileName)[0] + '.log.html'
dmngLogFile = scriptDirName + '/' + 'dmng.log.txt'
jsonFileName = scriptDirName + '/' + 'scenarii.json'

# empty htmlLogFileName
htmlLogFileHandle = open(htmlLogFileName, 'w')
htmlLogFileHandle.close()

# early variables declaration
indexFileName = 'index.html'

# open htmlLogFileName at the beginning of the test
htmlLogFileHandle = open(htmlLogFileName, 'a')
htmlLogFileHandle.write('<html>\n')
htmlLogFileHandle.write('<head>\n')
htmlLogFileHandle.write('<meta http-equiv="content-type" content="text/html; charset=utf8>"</meta>\n')
htmlLogFileHandle.write('<title>%s</title>\n' % htmlLogFileName)
utils.addCssInformations(htmlLogFileHandle)
htmlLogFileHandle.write('</head>\n')
htmlLogFileHandle.write('<body>\n')

# empty dmngLogFile
dmngLogFileHandle = open(dmngLogFile, 'w')
dmngLogFileHandle.close()

# open dmngLogFile at the beginning of the test
dmngLogFileHandle = open(dmngLogFile, 'a')

# inter modules variables
scenarioResult = 'OK'
platformSvnRevision = 'unknown'
appliVersion = 'unknown'
baseDirectoryForResults = '/var/www'
baseVersionsDirectoryForResults = baseDirectoryForResults + '/' + 'appliVersion'
baseScenariiDirectoryForResults = baseDirectoryForResults + '/' + 'scenarii'
sendEmail = False
colorEnabled = True
bwTestDuration = 30
quiet = False
verbose = False
scriptStartTime = 0
streamingStartTime = 0
scriptDuration = 'unknown'
#aggregationsModes = ['none', 'kencast', 'aviwest']
aggregationsModes = ['kencast']
#aggregationsModes = ['none']

maxNbOfEthAdapters = 2
maxNbOfUsbEthAdapters = 3
maxNbOfWifiAdapters = 1

# aggregationMaster sst-tx variables
# sourcesDirectory not in scriptDirName (rights problem when using sshfs)
#sourcesDirectory = scriptDirName + '/' + 'sourcesDirectory'
sourcesDirectory = '/tmp/appli'
#sourcesDirectory = '/var/tmp/aviwest/appli'
sstTxBinary = sourcesDirectory + '/' + 'Build/_install/bin/sst-tx'
# sstRxBuildDirectory not in scriptDirName (rights problem when using sshfs)
#sstRxBuildDirectory = scriptDirName + '/' + 'sstRxBuild'
sstRxBuildDirectory = '/tmp/sstRxBuild'
#sstRxBuildDirectory = '/var/tmp/aviwest/sstRxBuild'
sstRxBinary = sstRxBuildDirectory + '/' + 'aggreg-studio/sst-rx'

# studio sst-rx variables
linuxVmStudioIpAddressForSstTraffic = '192.168.56.101'
linuxVmStudioIpAddressForSsh = '192.168.57.101'
windowsVmStudioIpAddressForSstTraffic = '192.168.58.101'
windowsVmStudioIpAddressForTrafficGeneratorAndAnalyser = '192.168.59.101'
aggregationMasterLanMacAddress, aggregationMasterLanIpAddress, aggregationMasterLanNetworkMask, aggregationMasterLanBroadcastAddress = networkInterfaces.getNetworkInterfaceInformations('eth0')
gatewaySstRxBaseDirectory = '/tmp'
gatewaySstRxBinary = gatewaySstRxBaseDirectory + '/' + 'sst-rx'
gatewaySstRxLogFile = gatewaySstRxBaseDirectory + '/' + 'sstRxLogFile.txt'
gatewaySstRxLogin = 'aviwest'
gatewaySstRxPassword = 'safestreams'

# aggregationMaster network interfaces names and IP addresses

aviwestLanIfc= 'eth0'
dmngLanIfc = 'eth1'
linuxVmStudioTrafficLanIfc = 'vboxnet0'
linuxVmStudioSshLanIfc = 'vboxnet1'
windowsVmStudioTrafficLanIfc = 'vboxnet2'
windowsVmStudioSshLanIfc = 'vboxnet3'

# --------------------------------------------------------------------------------------------------
# JSON object deserialized
# --------------------------------------------------------------------------------------------------
platformType = 'not set'
scenarioId = -1
# lastScenarioId is used to limit the number of generated scenarii (it is not possible to generate too much scenarii : it would generate a too big file, it would be impossible to run all scenarii...)
lastScenarioId = -1

scenarioComment = 'not set'
scenarioEvolution = 'not set'
scenarioDuration = -1

actionMode = 'not set'
overEncodedBitrate = 'not set'
audioBitrate = 'not set'
videoBitrateMode = 'not set'
videoBitrate = 'not set'
frameRate = 'not set'
gopDuration = 'not set'
iFramesVsPandBFramesRatio = 'not set'
timeWindow = 'not set'

gatewayBandWidth = 'not set'
gatewayFixedLatency = 'not set'
gatewayInstantJitter = 'not set'
gatewayQueueLength = 'not set'
gatewayPacketsLoss = 'not set'

useControlNetworkInterface = True

nbOfEthAdapters = -1
ethAdaptersFixedLatenciesList = []
ethAdaptersJittersList = []
ethAdaptersBandWidthsList = []
ethAdaptersPacketLossList = []
ethAdaptersQueueLengthList = []

nbOfUsbEthAdapters = -1
usbEthAdaptersFixedLatenciesList = []
usbEthAdaptersJittersList = []
usbEthAdaptersBandWidthsList = []
usbEthAdaptersPacketLossList = []
usbEthAdaptersQueueLengthList = []

nbOfWifiAdapters = -1
wifiAdaptersFixedLatenciesList = []
wifiAdaptersJittersList = []
wifiAdaptersBandWidthsList = []
wifiAdaptersPacketLossList = []
wifiAdaptersQueueLengthList = []

