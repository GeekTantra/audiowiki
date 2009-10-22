<?
	if (isset($_POST['cancel'])) {
		// They pressed Cancel, send back to comments
		header('Location: index.php?forum_key=1&language=english');
	}
	else {
		// They pressed Delete, remove db entry and file
		// First, find which category the comment is located in
		$username="python";
		$password="rock+bait";
		$database="audiowikibeta";
	
		mysql_connect(localhost,$username,$password);
		@mysql_select_db($database) or die( "Unable to select database");
	
		$commentID = $_POST['id'];
		$language = $_POST['language'];
		$fileDescription = $_POST['fileDescription'];
		
		$getCategoryKey = "SELECT `key` FROM comments WHERE id = '" . $commentID . "';";
		$categoryKeyArray = mysql_fetch_row(mysql_query($getCategoryKey));
		$key = $categoryKeyArray[0];
		
		// Remove the db entry
		$deleteCommand = "DELETE FROM comments WHERE id = '" . $commentID . "';";
		mysql_query($deleteCommand);
		
		// Remove the file
		$commentPath = "/var/lib/asterisk/sounds/audiowiki-beta/global/".$language."/".$key."/".$commentID.".wav";
		$commentWebPath = "/var/lib/asterisk/sounds/audiowiki-beta/global/".$language."/".$key."/web/".$commentID.".mp3";
		$newCommentPath = "/var/lib/asterisk/sounds/audiowiki-beta/old_comments/" . $commentID . ".wav";
		$newCommentWebPath = "/var/lib/asterisk/sounds/audiowiki-beta/old_comments/" . $commentID . ".mp3";
		rename($commentPath, $newCommentPath);
		rename($commentWebPath, $newCommentWebPath);
		
		mysql_close();

		echo "<head><meta http-equiv=\"Refresh\" content=\"2; URL=index.php?forum_key=1&language=english\"></head>
				<center>
				<br>
				<br>
				<br>
				<p><h2>Comment ".$commentID." in ".$fileDescription." (".$language.") was deleted. </h2></p>";
	}

?>
