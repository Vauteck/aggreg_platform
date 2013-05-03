<?php

	session_start();

	$pids = $_SESSION['pids'];
	for($i = 0; $i < count($pids); $i++)
	{
		$cmd = 'sudo kill -9 '.$pids[$i];
		echo $cmd."\n";
		exec($cmd);
	}
	
	unset($_SESSION['pids']);
	
	// init itf list
	$itf_list = array();
	$cmd = "/sbin/ifconfig | /bin/grep eth | awk '{print $1;}'";
	exec($cmd, $itf_list);
	for($i = 0; $i < count($itf_list); $i++)
	{
		$cmd = 'sudo ./aggreg_netem.sh stop '.$itf_list[$i];
		echo $cmd."\n";
		exec($cmd);
	}

?>
