#!/bin/bash
#le script netem.sh permet de simuler les pertes, le delai et la fréquence de sortie d'une interface réseau
#Nom de l'interface réseau à simuler
IF=eth0
#Debit sortant
BWU=500kbit
#Delai de transit 
DELAYU=10ms
# % de paquets perdus 
LOSSU=1% 


start ()
{
	# Redirect traffic to the corresponding ifb itf to allow traffic controll on ingress traffic
	echo $IF
	IFB="ifb"${IF:3}
	MAX_BURST=${BWU%"kbit"}
	PEAKRATE=$(echo "scale=3; ($MAX_BURST + 1) / 1000" | bc)
	MAX_BURST=`expr $MAX_BURST \* 1024`
	NODE="root"
	LIMIT=30
	
	stop $IF
	sudo tc qdisc add dev $IF ingress
	sudo tc filter add dev $IF parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev $IFB

	echo "sudo tc qdisc add dev $IFB root handle 1: netem delay $DELAYU loss $LOSSU"
	sudo tc qdisc add dev $IFB root handle 1: netem delay $DELAYU loss $LOSSU
	if [[ $DELAYU != "0ms" ]]
	then
		DELAY_IN_SEC=$(echo "scale=3; ${DELAYU%"ms"} / 1000" | bc)
		echo "delay in sec = $DELAY_IN_SEC"
		LIMIT=$(echo "$DELAY_IN_SEC * ${BWU%"kbit"}" | bc)
		echo "limit = $LIMIT"
	fi
	echo "sudo tc qdisc add dev $IFB parent 1:1 handle 2 tbf rate ${BWU} burst 3000b limit ${LIMIT}kbit peakrate ${PEAKRATE}mbit mtu 1600"
	sudo tc qdisc add dev $IFB parent 1:1 handle 2 tbf rate ${BWU} burst 3000b limit ${LIMIT}kbit peakrate ${PEAKRATE}mbit mtu 1600
}

help ()
{
	echo "Command: ./aggreg_netem.sh <start|change|stop|restart|show|help> <interface> <output rate> <sent delay>  <% loss packet>"
	echo "Example To start aggreg_netem sh: ./aggreg_netem.sh start eth0 500kbit 10ms 10%"
	echo "Example To change aggreg_netem sh: ./aggreg_netem.sh change eth0 1mbit 1ms 2%"
	echo "Example To stop aggreg_netem sh: ./aggreg_netem.sh stop eth0"
	echo "Example To show aggreg_netem sh: ./aggreg_netem.sh show eth0 "
	echo "Example To restart aggreg_netem sh: ./aggreg_netem.sh restart"
	echo "Example simulate Server UDP: iperf -s -u -i 1 "
	echo "Example To simulate Client UDP: iperf -c <server ip addr> -u -b <output frequence: example : 10M>"
}

change ()
{
	IFB="ifb"${IF:3}
	MAX_BURST=${BWU%"kbit"}
	PEAKRATE=$(echo "scale=3; ($MAX_BURST + 1) / 1000" | bc)
	MAX_BURST=`expr $MAX_BURST \* 1024`
	NODE="root"
	LIMIT=30
	#sudo tc qdisc change dev $IFB  root handle 1: tbf rate $BWU maxburst 55000b limit 56000b
	#sudo tc qdisc change dev $IFB  parent 1:1 handle 2: netem loss $LOSSU  limit 100000b
	#sudo tc qdisc change dev $IFB  parent 2:1 handle 3: netem delay $DELAYU limit 100000b
	#sudo tc qdisc change dev $IFB  parent 3:1 handle 4: pfifo limit 100000b

	echo "sudo tc qdisc change dev $IFB root handle 1: netem delay $DELAYU loss $LOSSU"
	sudo tc qdisc change dev $IFB root handle 1: netem delay $DELAYU loss $LOSSU
	if [[ $DELAYU != "0ms" ]]
	then
		DELAY_IN_SEC=$(echo "scale=3; ${DELAYU%"ms"} / 1000" | bc)
		echo "delay in sec = $DELAY_IN_SEC"
		LIMIT=$(echo "$DELAY_IN_SEC * ${BWU%"kbit"}" | bc)
		echo "limit = $LIMIT"
	fi
	echo "sudo tc qdisc change dev $IFB parent 1:1 handle 2 tbf rate ${BWU} burst 3000b limit ${LIMIT}kbit peakrate ${PEAKRATE}mbit mtu 1600"
	sudo tc qdisc change dev $IFB parent 1:1 handle 2 tbf rate ${BWU} burst 3000b limit ${LIMIT}kbit peakrate ${PEAKRATE}mbit mtu 1600

}

stop ()
{
	IFB="ifb"${IF:3}
	sudo tc qdisc del dev $IFB root
	echo "tc qdisc del dev $IFB root"
}

restart ()
{
	stop 
	sleep 1 
	start
}


show ()
{
	IFB="ifb"${IF:3}
	tc -s qdisc ls dev $IFB
}

case "$1" in 
start) 
	if [ -z "$2" ]  || [ -z "$3" ] || [ -z "$4" ] || [ -z "$5" ]
    	then
    	echo "Usage: $0 <start|change|stop|restart|show|help> <interface> <output rate> <packet delay> < % loss packet>"
    	echo "example:  ./aggreg_netem.sh start eth0 500kbit 10ms 10%" 
    	exit
	fi 
   	if test  -n "$2" 
   	then 
   		IF=$2 
   		echo "IF=$2"
    fi 
   	if test -n "$3" 
    then 
    	BWU=$3 
    	echo "BWU=$3" 
    fi 
   	if test -n "$4"
    then 
    	DELAYU=$4 
     	echo "DELAYU=$4" 
    fi 
   	if test -n "$5"
    then
    	LOSSU=$5
     	echo "LOSSU= $5"
    fi 
	#echo "tc qdisc add dev $IF root handle 1:0 netem delay $DELAYU 10ms loss $LOSSU 25% distribution normal"
	#echo "tc qdisc add dev $IF parent 1:1 handle 10: tbf rate $BWU buffer 3200 limit 6000"
   	start 
   	echo "done";;

change) 
	if [ -z "$2" ]  || [ -z "$3" ] ||[ -z "$4" ] ||[ -z "$5" ]
    then
    	echo "Usage: $0 <start|change|stop|restart|show|help> <interface> <output rate> <packet delay> < % loss packet>"
    	echo "example:  ./aggreg_netem.sh change eth0 500kbit 10ms 10%" 
    	exit
    fi 
   	if test  -n "$2" 
   	then 
   		IF=$2 
   		echo "IF=$2"
    fi 
   	if test -n "$3" 
    then
     	BWU=$3 
    	echo "BWU=$3" 
    fi 
   	if test -n "$4"
    then 
     	DELAYU=$4 
     	echo "DELAYU=$4" 
    fi 
   	if test -n "$5"
    then
     	LOSSU=$5
     	echo "LOSSU= $5"
    fi  
   	change 
   	echo "done";;

stop)

 	if [ -z "$2" ]
  	then
    	echo "Usage: $0 <start|stop|restart|show> <interface> "
    	echo "example:  ./aggreg_netem.sh stop eth0 " 
 	exit
 	fi
 	if test -n "$2"
  	then
    	IF=$2
    	echo "IF=$2" 
   	stop
 	fi 
   		echo "stop done";;  
restart) 

	echo - n "Restarting WAN simul: " 
	restart 
	echo "done";;

help) 
	help 
	echo "done";;

show) 
	if [ -z "$2" ]
  	then
    	echo "Usage: $0 <start|stop|restart|show> <interface> "
    	echo "example:  ./aggreg_netem.sh show eth0 " 
    exit 
 	fi 
 	if test -n "$2"
    then
    	IF=$2 
      	echo "IF=$2" 
	fi 
	echo "WAN simul status for $IF:" 
	show 
	echo "";;

*)

  	echo "Usage: $0 <start|change|stop|restart|show|help> <interface> <output rate> <packet delay> < % loss packet>"
  	echo "example:  ./aggreg_netem.sh start eth0 500kbit 10ms 10%" 
 	;;

esac

exit 0

