#!/bin/bash

function getLinuxDistribution
{
	local functionNbOfArgs=$#
	if [ $functionNbOfArgs -ne 1 ]
	then
		displayText red "function \"getLinuxDistribution\" called with a bad number of arguments ($functionNbOfArgs instead of 1)" "newLine" $logFileName
		exit 1
	fi
	local upLinuxDistribution=$1

	operatingSystem=$(uname --operating-system)

	case "$operatingSystem" in
		"GNU/Linux")
			executeCommand "which lsb_release > /dev/null 2>&1" "false"
			returnCode=$?
			if [ $returnCode -ne 0 ]
			then
				displayText red "package \"lsb_release\" not installed" "newLine" $logFileName
				exit 1
			fi
			eval $upLinuxDistribution=$(lsb_release --id --short)
		;;
		"Cygwin")
			eval $upLinuxDistribution="cygwin"
		;;
		*)
			eval $upLinuxDistribution="unknown"
		;;
	esac

	if [ "$upLinuxDistribution" == "unknown" ]
	then
		displayText red "upLinuxDistribution unknown" "newLine" $logFileName
		exit 1
	fi
}
