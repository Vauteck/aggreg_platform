#!/bin/bash

function getSvnStatus
{
	local functionNbOfArgs=$#
	if [ $functionNbOfArgs -ne 2 ]
	then
		displayText red "function \"getSvnStatus\" called with a bad number of arguments ($functionNbOfArgs instead of 2)" "newLine" $logFileName
		exit 1
	fi
	local fileName=$1
	local upSvnStatus=$2

	locSvnStatus=$(svn st $fileName | gawk '{ print $1 }')

	eval $upSvnStatus="'$locSvnStatus'"
}

