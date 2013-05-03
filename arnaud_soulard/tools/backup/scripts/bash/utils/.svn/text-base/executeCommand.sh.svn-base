#!/bin/bash

# execute a command without expected string check (2 arg)
# execute a command with expected string check (4 args)
function executeCommand
{
	local functionNbOfArgs=$#
	if [ $functionNbOfArgs -ne 2 ] && [ $functionNbOfArgs -ne 4 ]
	then
		displayText red "function \"executeCommand\" called with a bad number of arguments ($functionNbOfArgs instead of 2 or 4)" "newLine" $logFileName
		exit 1
	fi

	local command=$1
	# checkExecutionResult : check execution result. Exit if it is set to true, continue if it is set to false
	local checkExecutionResult=$2
	if [ $functionNbOfArgs -ne 4 ]
	then
		# TODO : use expectedString and timeout (usefull in case of a long time running command)
		local expectedString=$3
		local timeout=$4
	fi

	# check checkExecutionResult
	if [ $checkExecutionResult != "true" ] && [ $checkExecutionResult != "false" ]
	then
		displayText red "checkExecutionResult ($checkExecutionResult) unknown" "newLine" $logFileName
		exit 1
	fi

	displayText cyan "running command : $command" "newLine" $logFileName
	eval $command
	returnCode=$?

	if [ $returnCode -eq 0 ]
	then
		displayText green "[OK] command terminated correctly" "newLine" $logFileName
	else
		if [ $checkExecutionResult == "true" ]
		then
			displayText red "[KO] command returned error $returnCode" "newLine" $logFileName
			exit 1
		elif [ $checkExecutionResult == "false" ]
		then
			displayText yellow "[WARNING] command returned error $returnCode" "newLine" $logFileName
		else
			displayText red "checkExecutionResult ($checkExecutionResult) unknown" "newLine" $logFileName
			exit 1
		fi
	fi
	return $returnCode
}
