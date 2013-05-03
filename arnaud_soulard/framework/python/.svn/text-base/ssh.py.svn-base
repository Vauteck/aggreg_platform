#! /usr/bin/python
# -*- coding: utf-8 -*-

# TODO : on 2012_10_26, the only module compatible with python 2 and 3 I found is libssh2 (git://github.com/wallunit/ssh4py).
#no working module has been found for python 3.2 : I tried out fabric, kivy-remote-shell, paramiko, dev-python/ssh, ssh4py...

# import python modules
import datetime
import pyssh
import sys
import time

# import aggregation-platform's libraries
import globals
import utils

class SshSession(object):

	def __init__(self, targetName, targetSshPort, targetUsername, targetPassword):
		utils.displayText('normal', 'creating a new ssh session : login as %s using basic password authentication' % targetUsername, 0)
		self.session = pyssh.connect(hostname=targetName, port=targetSshPort, username=targetUsername, password=targetPassword)
		if self.session == None:
			utils.displayText('red', '[KO] pyssh.connect returned : %s' % self.session, 0)
			sys.exit(1)

	def __del__(self):
		utils.displayText('normal', 'closing %s' % self.session, 0)
		self.session.disconnect()

	def executeCommands(self, commandsList):
		# execute commands in the ssh connection
		for command in commandsList:
			commandStartTime = datetime.datetime.now()

			commandExecutionResult = self.session.execute(command)
			commandStdout = commandExecutionResult.as_str()

			utils.displayText('normal', 'commandStdout : %s' % commandStdout, 0)

			commandEndTime = datetime.datetime.now()
			commandExecutionDuration = (commandEndTime - commandStartTime).seconds * 1000 + (commandEndTime - commandStartTime).microseconds / 1000

			returnCode = commandExecutionResult.return_code
			if returnCode == 0:
				utils.displayText('green', '[OK] command "%s" executed in %.3d milliseconds successfully' % (command, commandExecutionDuration), 0)
			else:
				utils.displayText('red', '[KO] command "%s" executed in %.3d milliseconds but returned an error (returnCode : %s)' % (command, commandExecutionDuration, returnCode), 0)
				sys.exit(1)

if __name__ == '__main__':

	globals.scriptStartTime = time.time()

	# new instance of Dmng
	# no public key authentication configuration needed : benefit : no further confiuguration / drawback : password stored in file
	mySshSession = SshSession('aggregationMaster', 5322, 'admin', 'ibis2010')

	commandsList = []
	for i in range(0, 2):
		commandsList.append('ls -l /tmp')

	mySshSession.executeCommands(commandsList)
	del(mySshSession)

	utils.terminateTest(0)

