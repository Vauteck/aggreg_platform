#! /usr/bin/python
# -*- coding: utf-8 -*-

# import python libraries
import os
import pdb
import re
import subprocess
import sys
import time

# import aggregation-platform's libraries
import globals
import utils

class studioSstRx(object):
	'''Documentation de studioSstRx'''

	# constructor
	def __init__(self, hostname, sshPort):

		self.host_name = hostname
		self.port = sshPort
		self.ssh = None
		#print("TODO : in constructor")

	def __del__(self):
		pass
		#print("TODO : in destructor")

	def kill(self):
		'''kill any instance of sst-rx self.host_name (through ssh on port self.port)
		'''

		command = ['/usr/bin/ssh', '-T', '-p', '%d' % self.port, '%s' % self.host_name, '/usr/bin/killall sst-rx > /dev/null 2>&1']
		commandString = ' '.join(command)
		if not globals.quiet:
			utils.displayText('normal', 'executing command : %s' % commandString, 0)

		p = subprocess.Popen(command, bufsize=-1, shell = False, stdin= None, stdout = subprocess.PIPE, stderr = subprocess.PIPE, env={'LANG':'en_GB.utf-8'})
		p.communicate()

	def start(self):
		'''run command on self.host_name in background (through ssh on port self.port)

		@param command : command to launch
		@return process ID
		'''

		commandsList = []
		commandsList.append(['/usr/bin/ssh', '-T', '-p', '%d' % self.port, '%s' % self.host_name, 'test -x %s' % globals.gatewaySstRxBinary])
		commandsList.append(['test', '-x', globals.sstRxBinary])

		for command in commandsList:
			commandStdout, commandStderr = utils.executeCommand(command)

		command = ['/usr/bin/ssh', '-T', '-p', '%d' % self.port, '%s' % self.host_name, '%s -v -T -L %s -l %s:%s' % (globals.gatewaySstRxBinary, globals.gatewaySstRxLogFile, globals.gatewaySstRxLogin, globals.gatewaySstRxPassword)]
		commandString = ' '.join(command)
		if not globals.quiet:
			utils.displayText('normal', 'executing command : %s' % commandString, 0)

		self.ssh = subprocess.Popen(command, bufsize=-1, shell = False, stdin = None, stdout = subprocess.PIPE, stderr = subprocess.PIPE, env={'LANG':'en_GB.utf-8'})

		if self.ssh == None:
			utils.displayText('red', '[KO] the following command failed : %s' % ' '.join(command), 0)
			utils.terminateTest(1)

if __name__ == '__main__':

	globals.scriptStartTime = time.time()

	# new instance of studioSstRx
	myStudioSstRx = studioSstRx(globals.linuxVmStudioIpAddressForSsh, 22)

	'''
	utils.displayText('cyan', 'killing any remaining sst-rx instance', 0)
	myStudioSstRx.kill()

	utils.displayText('cyan', 'starting an instance of sst-rx', 0)
	myStudioSstRx.start()

	utils.displayText('yellow', 'waiting for test', 5)

	utils.displayText('cyan', 'killing any remaining sst-rx instance', 0)
	myStudioSstRx.kill()

	utils.displayText('cyan', 'terminating sst-rx', 0)
	myStudioSstRx.ssh.terminate()
	'''
	utils.terminateTest(0)
