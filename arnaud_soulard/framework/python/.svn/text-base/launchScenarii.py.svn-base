#! /usr/bin/python
# -*- coding: utf-8 -*-

# import python libraries
import random
import subprocess
import time

# import aggregation-platform's libraries
import globals
import utils
import scenariiParameters

#globals.scriptStartTime = time.time()

# deserialize object to update globals.lastScenarioId
scenariiParameters.deserializeObject()

# launch scenarioId 0 with --build_last_sst-rx --build_last_sst-tx options
#subprocess.call('python launchScenario.py --build_last_sst-rx --build_last_sst-tx --send-email 0', shell=True)

# create a sorted list of scenarii IDs
scenariiIdsList = []
for scenarioId in range(0, (int(globals.lastScenarioId) + 1)):
	scenariiIdsList.append(scenarioId)

# shuffle this list
#random.shuffle(scenariiIdsList)

# run launchScenario.py for each ID
for scenarioId in scenariiIdsList:
	#print(scenarioId)
	subprocess.call('python launchScenario.py -utx %s/Build/_install/bin/sst-tx -urx %s/aggreg-studio/sst-rx %d --send-email' % (globals.sourcesDirectory, globals.sstRxBuildDirectory, scenarioId), shell=True)
	#--send-email
	#--reboot-dmng
#utils.terminateTest(0)
