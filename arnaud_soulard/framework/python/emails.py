#! /usr/bin/python
# -*- coding: utf-8 -*-

# import python libraries
#import re
import mimetypes
import os
import re
import smtplib
import sys
import time

from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

# import aggregation-platform's libraries
import globals
import subversion
import utils

def getEmailsAddressesList():
	''' to avoid specifying email addresses, make a link between login name and email addresses

	'''

	userLogged = os.getlogin()
	emailsAddressesList = []

	if userLogged == 'arnaud':
		emailsAddressesList.append('asoulard@aviwest.com')
		#emailsAddressesList.append('arnaud.soulard@gmail.com')
	elif userLogged == 'sfillod':
		emailsAddressesList.append('sfillod@aviwest.com')
	else :
		utils.displayText('red', 'userLogged (%s) unknown' % userLogged, 0)
		sys.exit(1)
		#utils.terminateTest(1)

	return emailsAddressesList

def sendTestResultByEmail(receivers, scenarioIdDirectoryForResults):
	''' send test result by email
	'''

	# Create a text message with html attachments
	msg = MIMEMultipart()
	msg['From'] = 'asoulard@aviwest.com'
	msg['To'] = ', '.join(receivers)
	msg['Subject'] = 'aggregation-platform test result %s for scenarioId : %s' % (globals.scenarioResult, globals.scenarioId)

	# build attachedFilesList
	attachedFilesList = [scenarioIdDirectoryForResults + '/' + globals.indexFileName]
	for attachedFile in os.listdir(scenarioIdDirectoryForResults):
		if os.path.isfile(scenarioIdDirectoryForResults + '/' + attachedFile):
			fileExtension = os.path.splitext(attachedFile)[1][1:]
			if fileExtension == 'html' or fileExtension == 'txt':
				if attachedFile != globals.indexFileName:
					attachedFilesList.append(scenarioIdDirectoryForResults + '/' + attachedFile)

	for attachedFile in attachedFilesList:
			part = MIMEBase('application', "octet-stream")
			with open(attachedFile, 'r') as f:
				part.set_payload(f.read())
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachedFile))
			msg.attach(part)

	mailServer = smtplib.SMTP_SSL('smtp.aviwest.com', 465)
	mailServer.login(msg['From'], 'A14z25e36')
	mailServer.send_message(msg)
	mailServer.close()

if __name__ == '__main__':

	globals.scriptStartTime = time.time()

	# sendTestResultByEmail is called in utils.terminateTest()
	utils.terminateTest(0)
