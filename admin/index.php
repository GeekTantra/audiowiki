<?

    $forum = $_GET['forum_key'];
    $language = $_GET['language'];

    $username="python";
    $password="rock+bait";
    $database="audiowikibeta";

    mysql_connect(localhost,$username,$password);
    @mysql_select_db($database) or die( "Unable to select database");

    $query = "SELECT id, `key`, time, description FROM comments WHERE `key` = ".$forum." AND language = '$language' ORDER BY time ASC";
    $result = mysql_query($query);
	$num = mysql_numrows($result);
	
	$query2 = "SELECT `key`, description FROM categories ORDER BY `key` ASC;";
	// "SELECT DISTINCT categories.`key`,categories.description FROM categories,comments WHERE comments.`key` = categories.`key` ORDER BY `key` ASC;";
	// "SELECT DISTINCT categories.description,comments.`key` FROM categories, comments WHERE comments.`key` < 10 and comments.`key`=categories.key 
	// and comments.language = '$language' ORDER BY comments.`key` ASC;";
	$result2 = mysql_query($query2);

	$query3 = "SELECT description FROM categories WHERE `key` = ".$forum;
	$result3 = mysql_query($query3);

	$query4 = "SELECT language from languages;";
	$languages = mysql_query($query4);

?>

<center><p>
<?
while ($row = mysql_fetch_array($languages)) {
    if ($row['language'] == $language) {
        echo  "<b><a href=\"index.php?forum_key=".$forum."&language=".$row['language']."\">".$row['language']."</a></b> ";
    }
    else {
    	echo  "<a href=\"index.php?forum_key=".$forum."&language=".$row['language']."\">".$row['language']."</a> ";
    }
}
?>
</center></p>


<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title><? echo mysql_result($result3,0); ?></title>
<style type="text/css">
<!--
body {
	background-image: url(images/top_panel.png);
	background-repeat:repeat-x;
	margin-left: 0px;
	margin-top: 0px;
	margin-right: 0px;
	margin-bottom: 0px;
}
div.leftTitle {  
	padding-top: 1px;  
	padding-right: 0px;  
	padding-bottom: 2px;  
	padding-left: 10px;  
} 
div.rightTitle {  
	padding-top: 1px;  
	padding-right: 14px;  
	padding-bottom: 2px;  
	padding-left: 0px;  
} 
body,td,th {
	font-family: Arial, Helvetica, sans-serif;
}
p.sample {
	font-family: sans-serif;
	font-style: normal;
	font-variant: normal;
	font-weight: bold;
	font-size: 50px;
	line-height: 100%;
	word-spacing: normal;
	letter-spacing: normal;
	text-decoration: none;
	text-transform: none;
	text-align: center;
	text-indent: 0ex;
	color: #FFFFFF;
}
a:link {
	color: #CCC;
	text-decoration: none;
}
a:visited {
	text-decoration: none;
	color: #CCC;
}
a:hover {
	text-decoration: none;
	color: #CCC;
}
a:active {
	text-decoration: none;
	color: #CCC;
}
-->
</style>

<script type="text/javascript" src="Scripts/jquery-latest.pack.js"></script>
<script type="text/javascript" src="Scripts/thickbox.js"></script>

<script src="Scripts/jquery.min.js" type="text/javascript" charset="utf-8"></script>
<script src="Scripts/jquery.jeditable.js" type="text/javascript" charset="utf-8"></script>
<script type="text/javascript" charset="utf-8">
$(function() {
	$(".edit").editable("update_db.php",
	   { 
	      indicator : "Updating...",
	      tooltip   : "Doubleclick to edit...",
	      event     : "dblclick",
	      style     : "inherit"
	    }
	 );
});
</script>
<script src="Scripts/swfobject_modified.js" type="text/javascript"></script>
<script type="text/javascript" src="/Scripts/audio-player.js"></script>  
<script type="text/javascript">  
            AudioPlayer.setup("images/player.swf", {  
                width: 300,
				transparentpagebg: "yes",
				remaining: 'yes',
				noinfo: 'yes',
				rtl: 'yes'
            });  
</script>  

</head>

<body text="#333333" link="#CCCCCC" vlink="#CCCCCC" alink="#CCCCCC">


<center>
<p class="sample"><? echo mysql_result($result3,0); ?></p>


<form action="index.php" method="GET">
<div align="center">
<select name="forum_key" onChange="this.form.submit();">
<?
while ($row = mysql_fetch_array($result2)) {
	if ($forum == $row['key']) {
		echo  "<option selected value=\"".$row['key']."\">".$row['key']." ".$row['description']."</option>";
	}	
	else {
		echo  "<option value=\"".$row['key']."\">".$row['key']." ".$row['description']."</option>";
	}
}
?>
</select>
<?
echo "<input type=\"hidden\" value=\"".$language."\" name=\"language\">";
?>
</div>
</form>

<p>
<?
if ($num == 0) {
	echo "<h1>No comments! <br> Call (617) 861-4471 to add your thoughts.</h1>";
#    <center><br><br>This is the admin page for CSAIL's Audio Wikipedia Project <br>
#			Commit Group <br><br><br><br><br>
}
else {
	echo "<center><table width=\"100%\" border=\"0\" cellpadding=\"0\" cellspacing=\"0\">";
}

$i = 1;
while ($row = mysql_fetch_array($result)) {
	if ($i % 2 == 1) {
		//Even row, background color is gray
		$color = "#E6E8FA";
		$i++;
	}
	else {
		//Odd row, background color is white
		$color = "#FFFFFF";
		$i++;
		
	}
	
	echo  "<tr bgcolor=\"" . $color . "\">
    		<td height=\"40\" width=\"3%\">&nbsp;</td>
			<td width=\"66%\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" . $row['id'] . " | <b id=\"" . $row['id'] . "\" class=\"edit\" style=\"display: inline\">"
			. $row['description'] . "</b></td>
    		<td width=\"23%\">
			
			<p id=\"audioplayer_".$i."\">Alternative content</p>  
            <script type=\"text/javascript\">  
            AudioPlayer.embed(\"audioplayer_" . $i . "\", {soundFile: \"sounds/audiowiki-beta/global/".$language."/".$row['key']."/web/".$row['id'].".mp3\"});  
            </script>  
			
			</td>
			<td width=\"20\"><a href=\"confirmDelete.php?id=" . $row['id'] .
			"&language=".$language."&fileDescription=".$row['description']."\"><img src=\"images/delete.png\" alt=\"delete comment\"".
			"width=\"20\" height=\"20\" align=\"absmiddle\" /></a></td>

    		<td width=\"4%\">&nbsp;</td>

  		</tr>";
	}
	mysql_close();
?>
  </table>
  <center>
<br />
<img src="images/icon.png" width="100" height="90" alt="Audio Wikipedia" />
<br />
<br />
</body>
</html>
