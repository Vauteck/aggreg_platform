#! /usr/bin/python
# -*- coding: utf-8 -*-

# import python libraries
import os
import sys
import shutil
import time

# import aggregation-platform's libraries
import globals
import utils

# module variables
armCompilerDirectory = '/home/share/tool-chain/arm-compiler/bin'
svnUrl = 'https://base.aviwest.net/svn/ibis/ibis-dmng-v3/appli/trunk'

def getSvnRevision(directory):
	command = ['/usr/bin/svnversion', '--no-newline', directory]
	commandStdout, commandStderr = utils.executeCommand(command)

	return commandStdout

def getNewAppliSvnWc(svnRevision):
	'''getNewAppliSvnWc
	'''

	# create globals.sourcesDirectory if it does not exist for a fresh checkout
	if os.path.exists(globals.sourcesDirectory):
		utils.displayText('cyan', 'deleting directory %s' % globals.sourcesDirectory, 0)
		shutil.rmtree(globals.sourcesDirectory)

	os.makedirs(globals.sourcesDirectory)

	commandsList = []
	commandsList.append(['svn', 'checkout', '--revision', svnRevision, svnUrl, globals.sourcesDirectory])

	#utils.displayText('cyan', 'updating %s to revision %s' % (globals.sourcesDirectory, svnRevision), 0)
	#commandsList.append(['svn', 'update', '--revision', svnRevision, globals.sourcesDirectory])

	for command in commandsList:
		commandStdout, commandStderr = utils.executeCommand(command)

	utils.displayText('cyan', 'updating external references to revision %s' % svnRevision, 0)
	commandsList = []
	externalReferencesCommandList = ['svn', 'update', '--revision', svnRevision]
	directoriesList = []
	directoriesList.append(globals.sourcesDirectory + '/' + 'common')
	directoriesList.append(globals.sourcesDirectory + '/' + 'aggreg-sst/aggreg-sst')
	directoriesList.append(globals.sourcesDirectory + '/' + 'dmng-lib/dmng-lib/ibis-interface/src')
	directoriesList.append(globals.sourcesDirectory + '/' + 'dmng-lib/dmng-lib/ibis-interface/include')
	directoriesList.append(globals.sourcesDirectory + '/' + 'dmng-lib/dmng-lib/aacparser/src')
	directoriesList.append(globals.sourcesDirectory + '/' + 'dmng-lib/dmng-lib/aacparser/include')
	directoriesList.append(globals.sourcesDirectory + '/' + 'include/xcom.h')
	directoriesList.append(globals.sourcesDirectory + '/' + 'include/xconfig.h')
	directoriesList.append(globals.sourcesDirectory + '/' + 'gst-plugins/gst-plugins/xcom')
	directoriesList.append(globals.sourcesDirectory + '/' + 'gst-plugins/gst-plugins/mp4mux')
	directoriesList.append(globals.sourcesDirectory + '/' + 'gst-plugins/gst-plugins/awdsp')

	# append directories to externalReferencesCommandList
	for index in range(len(directoriesList)):
		externalReferencesCommandList.append(directoriesList[index])

	commandsList.append(externalReferencesCommandList)

	for command in commandsList:
		commandStdout, commandStderr = utils.executeCommand(command)

def buildStudioSstTx():
	'''buildStudioSstTx

	executable will be launched on dmng
	'''

	if not os.path.isfile(globals.sourcesDirectory + '/' + '.svn/entries'):
		utils.displayText('red', 'globals.sourcesDirectory is not a svn working copy, call getNewAppliSvnWc first', 0)
		utils.terminateTest(1)

	commandsList = []
	commandsList.append(['CROSS_COMPILE=arm-linux-', 'PATH=%s/ccache:%s:$PATH' % (armCompilerDirectory, armCompilerDirectory), 'make', 'init', '--directory', globals.sourcesDirectory])
	commandsList.append(['CROSS_COMPILE=arm-linux-', 'PATH=%s/ccache:%s:$PATH' % (armCompilerDirectory, armCompilerDirectory), 'make', '--directory', globals.sourcesDirectory])
	commandsList.append(['test', '-x', globals.sstTxBinary])

	for command in commandsList:
		commandStdout, commandStderr = utils.executeCommand(command)


def buildStudioSstRx():
	'''buildStudioSstRx

	executable will be launched on studio-sst-rx (x86)
	'''

	if not os.path.isfile(globals.sourcesDirectory + '/' + '.svn/entries'):
		utils.displayText('red', 'globals.sourcesDirectory is not a svn working copy, call getNewAppliSvnWc first', 0)
		utils.terminateTest(1)

	if os.path.isdir(globals.sstRxBuildDirectory):
		shutil.rmtree(globals.sstRxBuildDirectory)

	os.makedirs(globals.sstRxBuildDirectory)

	# make init mandatory here (to generated the configure file)
	os.chdir(globals.sourcesDirectory)
	commandsList = []
	commandsList.append(['CROSS_COMPILE=arm-linux-', 'PATH=%s/ccache:%s:$PATH' % (armCompilerDirectory, armCompilerDirectory), 'make', 'init', '--directory', globals.sourcesDirectory])
	#commandsList.append(['PATH=%s/ccache:%s:$PATH' % (armCompilerDirectory, armCompilerDirectory), 'make', 'init', '--directory', globals.sourcesDirectory])

	for command in commandsList:
		commandStdout, commandStderr = utils.executeCommand(command)

	os.chdir(globals.sstRxBuildDirectory)
	commandsList = []
	#commandsList.append(['PATH=%s/ccache:%s:$PATH' % (armCompilerDirectory, armCompilerDirectory), 'make', 'init', '--directory', globals.sourcesDirectory])
	commandsList.append(['PATH=%s/ccache:%s:$PATH' % (armCompilerDirectory, armCompilerDirectory), '%s/aggreg-sst/aggreg-sst/configure --enable-maintainer-mode --enable-sst-rx-only --prefix=$(pwd)/inst' % globals.sourcesDirectory])
	commandsList.append(['PATH=%s/ccache:%s:$PATH' % (armCompilerDirectory, armCompilerDirectory), 'make', '--directory', globals.sstRxBuildDirectory])
	commandsList.append(['test', '-x', '%s/Build/_install/bin/sst-tx' % globals.sourcesDirectory])
	commandsList.append(['PATH=%s/ccache:%s:$PATH' % (armCompilerDirectory, armCompilerDirectory), 'make', '--directory', '%s/aggreg-common' % globals.sstRxBuildDirectory])
	commandsList.append(['PATH=%s/ccache:%s:$PATH' % (armCompilerDirectory, armCompilerDirectory), 'make', '--directory', '%s/aggreg-studio' % globals.sstRxBuildDirectory])
	commandsList.append(['test -x %s' % globals.sstRxBinary])

	for command in commandsList:
		commandStdout, commandStderr = utils.executeCommand(command)

if __name__ == '__main__':

	globals.scriptStartTime = time.time()

	#globals.platformSvnRevision = getSvnRevision(globals.scriptDirName)
	#utils.displayText('normal', 'platformSvnRevision : %s' % globals.platformSvnRevision, 0)

	getNewAppliSvnWc('HEAD')
	#sstTxBinary = buildStudioSstTx()
	#buildStudioSstRx()

	utils.terminateTest(0)
