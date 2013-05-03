#!/bin/bash

# backup kernel configuration of many computers

function displayUsage
{
	displayText red "usage : $0 [-h|--help] [-v|--verbose]" "newLine" $logFileName
}

function checkScriptRequirements
{
	local locLinuxDistribution
	getLinuxDistribution locLinuxDistribution

	if [ $locLinuxDistribution == "Debian" ] || [ $locLinuxDistribution == "Ubuntu" ]
	then
		# check that util-linux package is installed
		getPackageInstallationStatus $locLinuxDistribution "util-linux" packageInstallationStatus
		if [ "$packageInstallationStatus" != "installed" ]
		then
			displayText red "package util-linux not installed (packageInstallationStatus : $packageInstallationStatus)" "newLine" $logFileName
			exit 1
		fi
		# check that realpath package is installed
		getPackageInstallationStatus $locLinuxDistribution "realpath" packageInstallationStatus
		if [ "$packageInstallationStatus" != "installed" ]
		then
			displayText red "package realpath not installed (packageInstallationStatus : $packageInstallationStatus)" "newLine" $logFileName
			exit 1
		fi
		# check that openssh-client package is installed
		getPackageInstallationStatus $locLinuxDistribution "openssh-client" packageInstallationStatus
		if [ "$packageInstallationStatus" != "installed" ]
		then
			displayText red "package openssh-client not installed (packageInstallationStatus : $packageInstallationStatus)" "newLine" $logFileName
			exit 1
		fi
		# check that subversion package is installed
		getPackageInstallationStatus $locLinuxDistribution "subversion" packageInstallationStatus
		if [ "$packageInstallationStatus" != "installed" ]
		then
			displayText red "package subversion not installed (packageInstallationStatus : $packageInstallationStatus)" "newLine" $logFileName
			exit 1
		fi
	elif [ $locLinuxDistribution == "Gentoo" ]
	then
		# check that sys-apps/util-linux package is installed
		getPackageInstallationStatus $locLinuxDistribution "sys-apps/util-linux" packageInstallationStatus
		if [ "$packageInstallationStatus" != "installed" ]
		then
			displayText red "package sys-apps/util-linux not installed (packageInstallationStatus : $packageInstallationStatus)" "newLine" $logFileName
			exit 1
		fi
		# check that net-misc/openssh package is installed
		getPackageInstallationStatus $locLinuxDistribution "net-misc/openssh" packageInstallationStatus
		if [ "$packageInstallationStatus" != "installed" ]
		then
			displayText red "package net-misc/openssh not installed (packageInstallationStatus : $packageInstallationStatus)" "newLine" $logFileName
			exit 1
		fi
		# check that dev-vcs/subversion package is installed
		getPackageInstallationStatus $locLinuxDistribution "dev-vcs/subversion" packageInstallationStatus
		if [ "$packageInstallationStatus" != "installed" ]
		then
			displayText red "package dev-vcs/subversion not installed (packageInstallationStatus : $packageInstallationStatus)" "newLine" $logFileName
			exit 1
		fi
	else
		displayText red "locLinuxDistribution ($locLinuxDistribution) unknown" "newLine" $logFileName
		exit 1
	fi
}

function checkParameters
{
	# initializations
	beVerbose="no"
	scpOptions=" -q"
	cpOptions="--force"

	options=$(getopt -n $scriptName --options h,v --longoptions help,verbose -- "$@")
	if [ $? -ne 0 ]
	then
		displayUsage
		exit 1
	fi

	while [ $# -gt 0 ]
	do
		case "$1" in
			-h|--help)
				displayUsage
				exit 0
			;;
			-v|--verbose)
				beVerbose="yes"
				unset scpOptions
				cpOptions="$cpOptions -v"
			;;
			--)
				shift
				break
			;;
			*)
				displayText red "unrecognized option $1" "newLine" $logFileName
				displayUsage
				exit 1
			;;
		esac
		shift
	done
}

function backupSystemConfiguration
{
	computersArray[0]="aggregation-development 22 x86 Ubuntu"
	computersArray[1]="aggregation-validation 22 x64 Ubuntu"
	computersArray[2]="studio-sst-rx 10022 x64 Ubuntu"

	# check what computers are up and build computersDownIndexes
	for ((index=0;index<${#computersArray[@]};index++))
	do
		set -- ${computersArray[index]}
		targetComputerName=$1
		isComputerUp $targetComputerName locComputerStatus
		if [ $locComputerStatus != "up" ]
		then
			computersDownIndexes="$computersDownIndexes $index"
			computersDownList="$computersDownList $targetComputerName"
		fi
	done

	# remove computers that have been found down in computersArray
	for index in $(echo $computersDownIndexes | fmt --split-only --width=1 | sort --numeric-sort --reverse)
	do
		unset computersArray[index]
	done

	displayText red "$(echo $computersDownList | sed "s/ /, /g") are down; no backup will been done for those computers" "newLine" $logFileName
	displayText blue "Press enter to continue or any key + enter to exit" "newLine" $logFileName
	read locUserResponse
	if test -n "$locUserResponse"
	then
		exit 1
	fi

	for ((index=0;index<${#computersArray[@]};index++))
	do
		set -- ${computersArray[index]}
		targetComputerName=$1
		sshPort=$2
		targetArchitectureType=$3
		targetLinuxDistribution=$4

		# /etc/X11/xorg.conf is still used under Gentoo for nvidia configuration for example : therefore it is in the list
		# /etc/ssmtp/revaliases cannot be saved when logged as normal user
		# /etc/ssmtp/ssmtp.conf cannot be saved when logged as normal user
		filesList="
			$HOME/.bash_aliases
			$HOME/.bash_profile
			$HOME/.bashrc
			$HOME/.muttrc
			$HOME/.screenrc
			$HOME/.subversion/config
			$HOME/.vimrc
			/etc/X11/gdm/Init/Default
			/etc/X11/gdm/custom.conf
			/etc/X11/xorg.conf
			/etc/cpufreqd.conf
			/etc/default/grub
			/etc/dhcp/dhcpd.conf
			/etc/exports
			/etc/fstab
			/etc/fuse.conf
			/etc/hosts
			/etc/hosts.allow
			/etc/hosts.deny
			/etc/issue
			/etc/mime.types
			/etc/modprobe.d/blacklist.conf
			/etc/modprobe.d/nvidia.conf
			/etc/nsswitch.conf
			/etc/ntp.conf
			/etc/profile
			/etc/proftpd/proftpd.conf
			/etc/rsyncd.conf
			/etc/samba/smb.conf
			/etc/services
			/etc/slim.conf
			/etc/ssh/sshd_config
			/etc/synergy.conf
			/etc/sysctl.conf
			/etc/udev/rules.d/70-persistent-net.rules
			/etc/wvdial.conf
			/etc/xinetd.d/swat
			/usr/share/cups/mime/mime.convs
			/usr/src/linux/.config
		"
		# add files to filesList, depending on targetLinuxDistribution
		if [ $targetLinuxDistribution == "Debian" ]
		then
			filesList="$filesList
				/boot/grub/grub.cfg
				/etc/apt/sources.list.d/debian_backports.list
				/etc/apt/sources.list.d/debian_multimedia.list
				/etc/apt/sources.list.d/debian_security.list
				/etc/apt/sources.list.d/debian_stable.list
				/etc/apt/sources.list.d/eclipse.list
				/etc/bash.bashrc
				/etc/default/isc-dhcp-server
				/etc/default/ntp
				/etc/default/ntpdate
				/etc/default/rcS
				/etc/gdm3/Init/Default
				/etc/hostname
				/etc/inetd.conf
				/etc/init.d/halt
				/etc/kbd/config
				/etc/kde4/kdm/Xsetup
				/etc/kde4/kdm/Xstartup
				/etc/kde4/kdm/kdmrc
				/etc/modprobe.d/alsa-base.conf
				/etc/modprobe.d/touchpad.conf
				/etc/modules
				/etc/network/interfaces
				/usr/src/linux/.config
			"
		elif [ $targetLinuxDistribution == "Gentoo" ]
		then
			filesList="$filesList
				/boot/grub2/grub.cfg
				/etc/bash/bashrc
				/etc/conf.d/alsasound
				/etc/conf.d/hostname
				/etc/conf.d/hwclock
				/etc/conf.d/keymaps
				/etc/conf.d/modules
				/etc/conf.d/net
				/etc/conf.d/ntp-client
				/etc/conf.d/ntpd
				/etc/conf.d/xdm
				/etc/env.d/02locale
				/etc/genkernel.conf
				/etc/layman/layman.cfg
				/etc/locale.gen
				/etc/modprobe.d/alsa.conf
				/etc/portage/make.conf
				/etc/portage/make.profile
				/etc/portage/package.env/main
				/etc/porticron.conf
				/etc/rc.conf
				/etc/wpa_supplicant/wpa_supplicant.conf
				/usr/share/config/kdm/Xsetup
				/usr/share/config/kdm/Xstartup
				/usr/share/config/kdm/kdmrc
				/var/portage/layman/make.conf
			"
		elif [ $targetLinuxDistribution == "Ubuntu" ]
		then
			filesList="$filesList
				/boot/grub/grub.cfg
				/etc/bash.bashrc
				/etc/default/isc-dhcp-server
				/etc/default/ntp
				/etc/default/ntpdate
				/etc/default/rcS
				/etc/hostname
				/etc/init.d/halt
				/etc/kbd/config
				/etc/kde4/kdm/Xsetup
				/etc/kde4/kdm/Xstartup
				/etc/kde4/kdm/kdmrc
				/etc/modprobe.d/alsa-base.conf
				/etc/modules
				/etc/network/interfaces
				/usr/src/linux/.config
			"
		else
			displayText red "targetLinuxDistribution ($targetLinuxDistribution) unknown" "newLine" $logFileName
			exit 1
		fi

		displayText blue "backup $targetComputerName's system configuration files" "newLine" $logFileName

		for currentFile in $filesList
		do
			if [ $beVerbose == "yes" ]
			then
				displayText cyan "file $currentFile backed up to $scriptDirectory/../../files/$targetLinuxDistribution/$targetArchitectureType/$targetComputerName$currentFile" "newLine" $logFileName
			fi
			# create $(dirname $scriptDirectory/../../files/$targetLinuxDistribution/$targetArchitectureType/$targetComputerName$currentFile), if needed
			if ! test -d $(dirname $scriptDirectory/../../files/$targetLinuxDistribution/$targetArchitectureType/$targetComputerName$currentFile)
			then
				executeCommand "svn mkdir --parents $(dirname $scriptDirectory/../../files/$targetLinuxDistribution/$targetArchitectureType/$targetComputerName$currentFile) > /dev/null 2>&1" "true"
				displayText blue "directory $(dirname $scriptDirectory/../../files/$targetLinuxDistribution/$targetArchitectureType/$targetComputerName$currentFile) has been created and added under subversion" "newLine" $logFileName
			fi

			if [ $targetComputerName != $hostName ]
			then
				# check source file existence
				executeCommand "ssh -p $sshPort $targetComputerName test -f $currentFile" "false"
				returnCode=$?
				if [ $returnCode -eq 0 ]
				then
					# since I did not find a "--force" for the scp command, I remove the destination file (in case it is read-only) to be able for scp to do the job
					if test -f $scriptDirectory/../../files/$targetLinuxDistribution/$targetArchitectureType/$targetComputerName$currentFile
					then
						executeCommand "rm -f $scriptDirectory/../../files/$targetLinuxDistribution/$targetArchitectureType/$targetComputerName$currentFile" "true"
					fi
					executeCommand "scp -P $sshPort$scpOptions $targetComputerName:$currentFile $scriptDirectory/../../files/$targetLinuxDistribution/$targetArchitectureType/$targetComputerName$currentFile" "true"
				fi
			else
				# check source file existence
				if test -f $currentFile
				then
					executeCommand "cp $cpOptions $currentFile $scriptDirectory/../../files/$targetLinuxDistribution/$targetArchitectureType/$targetComputerName$currentFile" "true"
				else
					displayText yellow "$currentFile do not exist, it has not been backed up" "newLine" $logFileName
				fi
			fi
			getSvnStatus $scriptDirectory/../../files/$targetLinuxDistribution/$targetArchitectureType/$targetComputerName$currentFile svnStatus
			if [ "$svnStatus" == "?" ]
			then
				executeCommand "svn add $scriptDirectory/../../files/$targetLinuxDistribution/$targetArchitectureType/$targetComputerName$currentFile > /dev/null 2>&1" "true"
				displayText blue "file $scriptDirectory/../../files/$targetLinuxDistribution/$targetArchitectureType/$targetComputerName$currentFile has been added under subversion" "newLine" $logFileName
			fi
		done
	done

	displayText red "$(echo $computersDownList | sed "s/ /, /g") are down; no backup has been done for those computers" "newLine" $logFileName
}

# main

hostName=$(hostname)
scriptName=$(realpath $0)
scriptDirectory=$(dirname $scriptName)
logFileName=$(echo $scriptName | sed "s/^\(.*\)\.sh$/\1\.log/g")

# empty logFileName
if test -f $logFileName
then
	rm $logFileName
fi
touch $logFileName

source $scriptDirectory/utils/displayText.sh
source $scriptDirectory/utils/executeCommand.sh
source $scriptDirectory/utils/getLinuxDistribution.sh
source $scriptDirectory/utils/getPackageInstallationStatus.sh
source $scriptDirectory/utils/getSvnStatus.sh
source $scriptDirectory/utils/isComputerUp.sh

checkScriptRequirements
checkParameters "$@"

backupSystemConfiguration

exit 0
