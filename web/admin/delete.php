<?php include("/var/www/html/admin/password_protect.php"); ?> 
<?php
    $username="python";
    $password="rock+bait";
    $database="audiowikiIndia";

    mysql_connect(localhost,$username,$password);
    @mysql_select_db($database) or die( "Unable to select database");

    $query = "SELECT * FROM comments ORDER BY time DESC";
    $result = mysql_query($query);
    $num = mysql_numrows($result);
	
	$posts = $_GET['selectedPost'];
	
	for ($i=0; $i<count($posts); $i++) {
		$commentID = $posts[$i];
		echo $commentID;
		// Delete database entry.
		$deleteCommand = "DELETE FROM comments WHERE id = ".$commentID.";";
		mysql_query($deleteCommand);
	
		// Delete files.
		$commentPath = "/var/lib/asterisk/sounds/audiowikiIndia/".$commentID.".wav";
		$commentWebPath = "/var/lib/asterisk/sounds/audiowikiIndia/web/".$commentID.".mp3";
		$newCommentPath = "/var/lib/asterisk/sounds/audiowikiIndia/trash/".$commentID.".wav";
		$newCommentWebPath = "/var/lib/asterisk/sounds/audiowikiIndia/trash/".$commentID.".mp3";
		rename($commentPath, $newCommentPath);
		rename($commentWebPath, $newCommentWebPath);
	}
	
	header('Location: http://audiowiki.no-ip.org/admin/index.php');
	
	mysql_close();

?>
