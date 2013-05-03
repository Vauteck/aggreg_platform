#!/bin/bash

function getPackageInstallationStatus
{
	local functionNbOfArgs=$#
	if [ $functionNbOfArgs -ne 3 ]
	then
		displayText red "function \"getPackageInstallationStatus\" called with a bad number of arguments ($functionNbOfArgs instead of 3)" "newLine" $logFileName
		exit 1
	fi
	local locLinuxDistribution=$1
	local locPackage=$2
	local upPackageStatus=$3

	displayText normal "checking if package $locPackage is installed..." "noNewLine" $logFileName
	if [ $locLinuxDistribution == "Debian" ] || [ $locLinuxDistribution == "Ubuntu" ]
	then
		if [ "$(dpkg-query --show --showformat='${Status}' $locPackage 2> /dev/null |awk {'print $3'})" == "installed" ]
		then
			locPackageStatus="installed"
		else
			locPackageStatus="not-installed"
		fi
	elif [ $locLinuxDistribution == "Gentoo" ]
	then
		# check equery command
		#which equery > /dev/null 2>&1
		#if [ $? -ne 0 ]
		#then
		#	displayText red "equery command unknown : run \"/usr/bin/sudo emerge --ask --newuse --verbose app-portage/gentoolkit\"" "newLine" $logFileName
		#	exit 1
		#fi

		# check eix command
		which eix > /dev/null 2>&1
		if [ $? -ne 0 ]
		then
			displayText red "eix command unknown : run \"/usr/bin/sudo emerge --ask --newuse --verbose app-portage/eix\"" "newLine" $logFileName
			exit 1
		fi

		# equery command working but very slow
		#equery --no-color --quiet list --format='$cp' '*' | grep "$locPackage" > /dev/null 2>&1
		eix $locPackage | grep "Installed" > /dev/null 2>&1
		if [ $? -ne 0 ]
		then
			locPackageStatus="not-installed"
		else
			locPackageStatus="installed"
		fi
	elif [ $locLinuxDistribution == "cygwin" ]
	then
		displayText red "TODO : find a way to check that a package is installed under cygwin" "newLine" $logFileName
		exit 1
	else
		displayText red "locLinuxDistribution ($locLinuxDistribution) unknown" "newLine" $logFileName
		exit 1
	fi

	if [ $locPackageStatus == "installed" ]
	then
		displayText green "[OK]" "newLine" $logFileName
	else
		displayText red "[KO]" "newLine" $logFileName
	fi

	eval $upPackageStatus="'$locPackageStatus'"
}

