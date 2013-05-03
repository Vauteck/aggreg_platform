#!/bin/bash

time_max_value=0
itf_list=""

# Function that will load netem conf for each itf
# param : directory path to where the itf config files are stored
load_global_conf() 
{
	if [ -z "$1" ]
	then
		dir="."
	else
		dir=$1
	fi
	
	echo $dir

	IFS_DEFAULT_VALUE=$IFS
	IFS=$'\n'
	result=`ls $dir | grep eth | grep .txt`
	for itf_file in $result
	do
		echo "parsing $itf_file"
		itf_name=${itf_file%".txt"}
		itf_list=$itf_list" "$itf_name
		IFS=$'\n'
		itf_file_content=`cat $dir\/$itf_file`
		index=0
		time=0
		for line in $itf_file_content
		do
			#echo $line_
			index=${index+1}
			IFS=$', '
			read -a tab <<< "${line}"
			# Time value
			if [ ${#tab[@]} -ne 6 ]
			then
				echo "bad line (${index}) detected in ${itf_file} config file : ${line}"
			else
				if [ $time -eq 0 ]
				then
					time=1
				fi

				if [ ${#commands_table[${time}]} -eq 0 ]
				then
					echo "commands_table[${time}] doesn't exist"
					commands_table[$time]="${itf_name} ${tab[1]} ${tab[2]} ${tab[3]} ${tab[4]} ${tab[5]}"
					echo "${commands_table[${time}]}"
				else
					commands_table[$time]="${commands_table[$time]}/${itf_name} ${tab[1]} ${tab[2]} ${tab[3]} ${tab[4]} ${tab[5]}"
				fi
				
				time=`expr ${tab[0]} + $time`
			
				if [ $time -gt $time_max_value ]
				then
					time_max_value=$time
				fi
			fi
		done
		if [ ${#commands_table[${time}]} -eq 0 ]
		then
			echo "commands_table[${time}] doesn't exist"
			commands_table[$time]="${itf_name} stop"
			echo "${commands_table[${time}]}"
		else
			commands_table[$time]="${commands_table[$time]}/${itf_name} stop"
		fi
	done
	IFS=$IFS_DEFAULT_VALUE
}

apply_command()
{
	if [ -z "$1" ]
	then
		echo "${0} : invalid index argument"
	else
		IFS_DEFAULT_VALUE=$IFS
		IFS=$'\/'
		echo "${O} : commands_tables[${1}] = ${commands_table[${1}]}"
		for itf_line in ${commands_table[${1}]}
		do
			echo "${itf_line}"
			IFS=$' '
			read -a params <<< "${itf_line}"
			if [ ${#params[@]} -ne 6 ]
			then
				if [ "${params[1]}" == "stop" ]
				then
					echo "stopping tc on itf ${params[0]}"
					./aggreg_netem.sh stop ${params[0]} ${params[1]}
				else
					echo "bad number of args ; read ${#params[@]}, expected 6 or stop ..."
			fi
			else
				echo "applying command on ${params[0]} : ${params[1]}kbits, ${params[2]}ms, ${params[5]}%"
				./aggreg_netem.sh start ${params[0]} ${params[1]}kbit ${params[2]}ms ${params[3]}%
			fi
		done
		IFS=$IFS_DEFAULT_VALUE
	fi
}

main_loop() 
{
	index=0
	
	# Start netem on all itf
	for i in $itf_list
	do
		echo "Starting netem on $i"
		#./aggreg_netem.sh start $i 1000mbit 0ms 0%
	done
	while [ $index -le $time_max_value ]
	do
		index=$[index + 1]
		sleep 1
		if [ ${#commands_table[${index}]} -eq 0 ]
		then
			echo "no command at time ${index}, sleeping ..."
		else
			echo "-- commands_table[${index}] = ${commands_table[${index}]}"
			apply_command $index
		fi
	done

	#for i in $itf_list
	#do
	#	echo "Stopping netem on $i"
	#	./aggreg_netem.sh stop $i
	#done
}

declare -A commands_table

load_global_conf $1 
main_loop

