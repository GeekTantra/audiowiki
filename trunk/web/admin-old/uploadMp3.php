<?php include("/var/www/html/admin/password_protect.php"); ?> 
<?php
    if (getenv(HTTP_X_FORWARDED_FOR)) {
		$pipaddress = getenv(HTTP_X_FORWARDED_FOR);
		$ipaddress = getenv(REMOTE_ADDR);
    } else {
		$ipaddress = getenv(REMOTE_ADDR);
    }

    $username="python";
    $password="rock+bait";
    $database="audiowikiIndia";

    mysql_connect(localhost,$username,$password);
    @mysql_select_db($database) or die( "Unable to select database");
	
	$query = "INSERT INTO comments (user, station) VALUES ('$ipaddress', '12345')";
	if (!mysql_query($query)) {echo "Error inserting into database.";};
	
	$id = mysql_insert_id();
	
	$soundsDir = "/var/lib/asterisk/sounds/audiowikiIndia";
	
	$mp3_target = "$soundsDir/web/$id.mp3";
	//move_uploaded_file($_FILES['uploadMp3']['tmp_name'], $mp3_target);
	//echo basename( $_FILES['uploadMp3']['name']); 
	echo "<br />";
	if(move_uploaded_file($_FILES['uploadMp3']['tmp_name'], $mp3_target)) {
		$convertToWav1 = "/usr/local/bin/lame --decode $mp3_target $soundsDir/$id.wav";
		$convertToWav2 = "sox -V $soundsDir/$id.wav -r 8000 -c 1 $soundsDir/$id.raw";
//		$p = "chmod 777 $mp3_target";
//		exec($p);
		exec($convertToWav1, $output = array());
		//echo $convertToWav1;
		//print_r( $output );
		exec($convertToWav2);
		echo "<center><br><br><br><h1>The file ".basename( $_FILES['uploadMp3']['name'])." has been uploaded.\n </h1><br>";
		echo "<a href=\"index.php\">back</a>";
	} else {
	        echo "There was an error uploading the file, please try again!";
	}
?>
