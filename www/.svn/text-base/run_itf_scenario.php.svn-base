<?php

function build_netem_itf_array_rules($scenario_file)
{
	$file_path = "scenarios/".$scenario_file;
	echo $file_path."\n";
	$handle = fopen($file_path, "r");
	$rules_count = 0;
	$itf_rules = array();
	if ($handle)
	{
    	while (($buffer = fgets($handle, 4096)) !== false)
		{
			//echo $rules_count."\n";
			$line_values = split(",", $buffer);
			$itf_rules[$rules_count]["time"] = trim($line_values[0], "\n ");
			$itf_rules[$rules_count]["rate"] = trim($line_values[1], "\n ");
			$itf_rules[$rules_count]["latency"] = trim($line_values[2], "\n ");
			$itf_rules[$rules_count]["loss"] = trim($line_values[5], "\n ");
			$rules_count++;
		}
    }
    if (!feof($handle)) 
	{
       	 echo "Error: unexpected fgets() fail\n";
    }
    fclose($handle);
	return $itf_rules;
}

if($argc < 4)
{
	echo "-1";
	exit;
}


$itf_rules['interface'] = $argv[1];
$itf_rules['rules'] = build_netem_itf_array_rules($argv[2]);
$loop = $argv[3];

$cmd = 'sudo ./aggreg_netem.sh start '.$itf_rules['interface'].' '.$itf_rules['rules'][0]["rate"].'kbit '.$itf_rules['rules'][0]["latency"].'ms '.$itf_rules['rules'][0]["loss"].'%';
echo $cmd."\n";
exec($cmd);
sleep($itf_rules['rules'][0]["time"]);

do
{
	for($i=1; $i<count($itf_rules['rules']); $i++)
	{
		// apply netem rule
		$cmd = 'sudo ./aggreg_netem.sh change '.$itf_rules['interface'].' '.$itf_rules['rules'][$i]["rate"].'kbit '.$itf_rules['rules'][$i]["latency"].'ms '.$itf_rules['rules'][$i]["loss"].'%';
		echo $cmd."\n";
		exec($cmd);
		sleep($itf_rules['rules'][$i]["time"]);
	}
} while($loop == 'true');

$cmd = 'sudo ./aggreg_netem.sh stop '.$itf_rules['interface'];
exec($cmd);

?>
