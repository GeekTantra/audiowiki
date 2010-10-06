<?php include("/var/www/html/admin/password_protect.php"); ?> 
<?php

$path = $_GET['path'];
$id = $_GET['id'];

$filename = 'comment_'.$id.".mp3";

	header('Content-disposition: attachment; filename='.$filename);
	header('Content-type: application/mp3');
	readfile($path);
	
	header('Location: http://audiowiki.no-ip.org/admin/index.php');

?>