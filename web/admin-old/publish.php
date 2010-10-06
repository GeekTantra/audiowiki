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
	
	$info = mysql_fetch_array($result);

	$posts = $_GET['selectedPost'];
	
	for ($i=0; $i<count($posts); $i++) {
		$commentID = $posts[$i];
		$update = "UPDATE comments SET archived = 0 WHERE id = '$commentID'";
        	mysql_query($update);
	}
	
	mysql_close();
	
	header('Location: http://audiowiki.no-ip.org/admin/index.php');
	
?>
