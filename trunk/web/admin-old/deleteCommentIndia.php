<?php include("/var/www/html/admin/password_protect.php"); ?> 
<?php
	if (isset($_POST['cancel'])) {
		// They pressed Cancel, send back to comments
		header('Location: index.php');
	}
	else {
		// They pressed Delete, remove db entry and file
		// First, find which category the comment is located in
		$username="python";
		$password="rock+bait";
		$database="audiowikiIndia";
	
		mysql_connect(localhost,$username,$password);
		@mysql_select_db($database) or die( "Unable to select database");
	
		$commentID = $_POST['id'];
		$fileDescription = $_POST['fileDescription'];
					
		// Remove the db entry
		$deleteCommand = "DELETE FROM comments WHERE id = ".$commentID.";";
		mysql_query($deleteCommand);
		
		// Remove the file
		$commentPath = "/var/lib/asterisk/sounds/audiowikiIndia/".$commentID.".wav";
		$commentWebPath = "/var/lib/asterisk/sounds/audiowikiIndia/web/".$commentID.".mp3";
		$commentRAWPath = "/var/lib/asterisk/sounds/audiowikiIndia/".$commentID.".raw";
		$newCommentPath = "/var/lib/asterisk/sounds/audiowikiIndia/trash/".$commentID.".wav";
		$newCommentWebPath = "/var/lib/asterisk/sounds/audiowikiIndia/trash/".$commentID.".mp3";
		$newCommentRAWPath = "/var/lib/asterisk/sounds/audiowikiIndia/trash/".$commentID.".raw";
		rename($commentPath, $newCommentPath);
		rename($commentWebPath, $newCommentWebPath);
		rename($commentRAWPath, $newCommentRAWPath);		
		mysql_close();

		echo "<head><meta http-equiv=\"Refresh\" content=\"2;url=index.php\"></head>
				<center>
				<br>
				<br>
				<br>
				<p><h2>Comment ".$commentID." <br /> ".$fileDescription." <br /> was deleted. </h2></p>";
	}
?>
