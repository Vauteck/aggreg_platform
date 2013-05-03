<?php
	$cmd="./aggreg_netem.sh stop {$_POST["itf"]}";
	exec($cmd);
	$cmd="./aggreg_netem.sh start {$_POST["itf"]} {$_POST["bandwidth"]}kbit {$_POST["delay"]}ms {$_POST["loss"]}%";
	exec($cmd);
?>
