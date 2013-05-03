#!/bin/bash

function isComputerUp
{
	local functionNbOfArgs=$#
	if [ $functionNbOfArgs -ne 2 ]
	then
		displayText red "function \"getArchitectureType\" called with a bad number of arguments ($functionNbOfArgs instead of 2)" "newLine" $logFileName
		exit 1
	fi
	local computerName=$1
	local upComputerStatus=$2

	ping -c 1 $computerName > /dev/null 2>&1
	if [ $? -eq 0 ]
	then
		computerStatus="up"
	else
		computerStatus="down"
	fi

	eval $upComputerStatus="'$computerStatus'"
}

