<?php
    $dir = $_POST['dir'];
    
    /*dh = opendir($dir) or die("Cannot open dir $dir");
    while (($entry = readdir($dh))) {
        if (is_file($entry) && !fnmatch('*~', $entry) && !fnmatch('#*#', $entry)) {
                echo $entry ."<br />";
            }
    }
    closedir($dh);
	*/
	$ffs = scandir($dir);
  	//echo '<ol>';
    foreach($ffs as $ff){
        if($ff != '.' && $ff != '..'){
            echo $ff."\n";
            //if(is_dir($dir.'/'.$ff)) listFolderFiles($dir.'/'.$ff);
            //echo '</li>';
        }
    }
    //echo '</ol>';


?>
