#!/bin/bash

function displayText
{
	local functionNbOfArgs=$#
	if [ $functionNbOfArgs -ne 3 ] && [ $functionNbOfArgs -ne 4 ]
	then
		echo "Usage : displayText \"text color\" \"text with/without color\" \"newLine|noNewLine\" [locLogFileName]"
		exit 1
	fi

	local locTextColor=$1
	local locTextToDisplay=$2
	local locDisplayNewLine=$3

	if [ $functionNbOfArgs -eq 4 ]
	then
		locLogFileName=$4
	else
		locLogFileName=""
	fi

	# check locTextToDisplay possible values
	case "$locTextColor" in
		"normal")
		local colorCode="normal"
		;;
		"black")
		local colorCode="\\e[1;30m"
		;;
		"red")
		local colorCode="\\e[1;31m"
		;;
		"green")
		local colorCode="\\e[1;32m"
		;;
		"yellow")
		local colorCode="\\e[1;33m"
		;;
		"blue")
		local colorCode="\\e[1;34m"
		;;
		"magenta")
		local colorCode="\\e[1;35m"
		;;
		"cyan")
		local colorCode="\\e[1;36m"
		;;
		*)
		echo "locTextColor ($locTextColor) not supported"
		if test -n "$locLogFileName"
		then
			echo "locTextColor ($locTextColor) not supported" >> $locLogFileName
		fi
		exit 1;;
	esac

	# check locDisplayNewLine possible values
	case "$locDisplayNewLine" in
		"newLine")
		;;
		"noNewLine")
		;;
		*)
		echo "locDisplayNewLine ($locDisplayNewLine) not supported"
		if test -n "$locLogFileName"
		then
			echo "locDisplayNewLine ($locDisplayNewLine) not supported" >> $locLogFileName
		fi
		exit 1;;
	esac

	if [ $locDisplayNewLine == "newLine" ]
	then
		if [ $colorCode == "normal" ]
		then
			echo -e "$locTextToDisplay"
		else
			echo -e "$colorCode$locTextToDisplay\\033[0;39m"
		fi
		if test -n "$locLogFileName"
		then
			echo -e "$locTextToDisplay" >> $locLogFileName
		fi
	elif [ $locDisplayNewLine == "noNewLine" ]
	then
		if [ $colorCode == "normal" ]
		then
			echo -ne "$locTextToDisplay"
		else
			echo -ne "$colorCode$locTextToDisplay\\033[0;39m"
		fi
		if test -n "$locLogFileName"
		then
			echo -ne "$locTextToDisplay" >> $locLogFileName
		fi
	fi

}

# for debug purpose
#displayText "$@"

