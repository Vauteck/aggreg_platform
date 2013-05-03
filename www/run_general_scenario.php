<?php

session_start();

$session_id = escapeshellarg(session_id());
$itf_scenarios_array = $_POST["itf"];
$loop = $_POST["loop"];

$my_array = json_decode($itf_scenarios_array, true);

//echo "array count = ".count($my_array)."\n";
$pids = array();
for($i=0; $i < count($my_array); $i++)
{
	$command = 'php run_itf_scenario.php '.$my_array[$i]["interface"][0].' '.$my_array[$i]["scenario"].' '.$loop.' '.$session_id.' > /dev/null 2>&1 & echo $!;';
	//echo $command."\n";
	$pids[$i] =  exec($command, $output);
}

$_SESSION['pids'] = $pids;

?>
