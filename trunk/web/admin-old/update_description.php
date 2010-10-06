<?php include("/var/www/html/admin/password_protect.php"); ?> 
<?php
	$username="python";
	$password="rock+bait";
	$database="audiowikiIndia";

	mysql_connect(localhost,$username,$password);
	@mysql_select_db($database) or die("Unable to select database");
		
	$update = mysql_query("UPDATE comments SET description = '" . $_POST['value'] . "' WHERE id = '" . $_POST['id'] . "';");
																					  
	mysql_close();
?>
