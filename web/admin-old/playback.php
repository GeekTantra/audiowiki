<?php
	$play = $_GET['play'];

	if (!isset($play)) {
		$as = 0;
	} else {
		$as = 1;
	}
	
	$station = '12345'; //$_GET['station'];
	
	
	$date = date('Y-m-d');
	
	$view = $_POST['view'];
	if (!isset($view)) { $view = 'published'; }
	
    $username="python";
    $password="rock+bait";
    $database="audiowikiIndia";

    mysql_connect(localhost,$username,$password);
    @mysql_select_db($database) or die( "Unable to select database");

	if ($view == "published") {
		$query = "SELECT * FROM comments WHERE archived = 0 AND station = $station ORDER BY time DESC";
	}
	else if ($view == "new") {
		$query = "SELECT * FROM comments WHERE archived = 2 AND station = $station ORDER BY time DESC";
	}
	else if ($view == "all") {
		$query = "SELECT * FROM comments WHERE station = $station ORDER BY time DESC";
	}
	else {
		$query = "SELECT * FROM comments WHERE station = $station ORDER BY time DESC";
	}
		
    $result = mysql_query($query);
    $num = mysql_num_rows($result);

?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<link rel="alternate" type="application/rss+xml" title="RSS" href="rss.xml" />
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>CGNet Swara</title>

<script type="text/javascript" src="Scripts/jquery.js"></script>
<script type="text/javascript" src="Scripts/thickbox.js"></script>

<link rel="stylesheet" href="css/thickbox.css" type="text/css" media="screen" />

<style type="text/css">
<!--
.visibleDiv, #topLeft, #topRight, #bottomLeft, #bottomRight
{
	background-image: url(images/top_panel.png);
    position: fixed;
    border: solid 0px #000000;
    vertical-align: middle;
    text-align: center;
	width:100%;
}
date {
	color:#AAAAAA;
}
#topLeft
{
    top: 0px;
    left: 0px;
}
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
	color: #666;
	text-decoration: none;
}
a:visited {
	text-decoration: none;
	color: #666;
}
a:hover {
	text-decoration: none;
	color: #666;
}
a:active {
	text-decoration: none;
	color: #666;
}
-->
</style>

<script type="text/javascript" src="Scripts/jquery-latest.pack.js"></script>
<script type="text/javascript" src="Scripts/thickbox.js"></script>

<script src="Scripts/jquery.min.js" type="text/javascript" charset="utf-8"></script>
<script src="Scripts/jquery.jeditable.js" type="text/javascript" charset="utf-8"></script>
<script type="text/javascript" charset="utf-8">
$(function() {
	$(".edit").editable("update_description.php",
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
<script type="text/javascript" src="Scripts/audio-player.js"></script>  
<script type="text/javascript">  
            AudioPlayer.setup("images/player.swf", {  
                width: 300,
				transparentpagebg: "yes",
				remaining: 'yes',
				noinfo: 'yes',
				rtl: 'yes'
            });  
</script>

<SCRIPT language="JavaScript">
function OnSubmitForm()
{
	if(document.pressed == 'Archive')
	{
		document.myform.action ="archive.php";
		document.myform.submit();
	}
	if(document.pressed == 'Publish')
	{
		document.myform.action ="publish.php";
		document.myform.submit();
	}
	else  if(document.pressed == 'Delete')
	{
		document.myform.action ="delete.php";
		document.myform.submit();
	}
	return true;
}
</SCRIPT>
<SCRIPT language="JavaScript">
function unCheckAll(field)
{
for (i = 0; i < field.length; i++)
	field[i].checked = false ;
}
</script>
<script type="text/javascript" language="javascript" src="niftyplayer.js"></script>
</head>

<body onload="unCheckAll(document.myform.selectedPost);" text="#333333" link="#666666" vlink="#666666" alink="#666666">
<div class="visibleDiv" id="topLeft">
	<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,0,0" width="165" height="38" id="niftyPlayer1" align="">
	<param name=movie value="niftyplayer.swf?file=sounds/audiowikiIndia/web/<?php=$play?>.mp3&as=<?php=$as?>">
	<param name=quality value=high>
	<param name=bgcolor value=#FFFFFF>
	<embed src="niftyplayer.swf?file=sounds/audiowikiIndia/web/<?php=$play?>.mp3&as=<?php=$as?>" quality=high bgcolor=#FFFFFF width="165" height="38" name="niftyPlayer1" align="" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer">
	</embed>
	</object>
</div>

<p class="sample">CGNet Swara</p>


<FORM name="myform" id="myform" onSubmit="return OnSubmitForm();" method="get">
<?php
if ($num == 0) {
	echo "<br><br><h1 align=\"center\">No posts!!<br> Call 8066932500 to add your thoughts.</h1>";
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
	// 2 Unread
	// 1 Archived
	// 0 Live
	if ($row['archived'] == 2) { $status = "unread"; $textcolor = "color:#990000;"; $fontStyle="b";}
	if ($row['archived'] == 1) { $status = "archived"; $textcolor = "color:#B0B0B0;"; $fontStyle="p";}
	if ($row['archived'] == 0) { $status = "live"; $textcolor = "color:#484848;"; $fontStyle="p";}

/*
	echo 
	"<tr height=\"35\" bgcolor=\"" . $color . "\">
		<td width=\"2%\">
		</td>
		<td width=\"2%\">
        	<input type=\"checkbox\" name=\"selectedPost[]\" id=\"selectedPost\" value=\"".$row['id']."\"> <br />
		</td>
		<td width=\"52%\"><$fontStyle id=\"" . $row['id'] . "\" class=\"edit\" style=\"$textcolor display: inline\">". $row['description'] . "</$fontStyle>
		</td>
    		<td width=\"30%\">
				<p id=\"audioplayer_".$i."\">Alternative content</p>
           		<script type=\"text/javascript\">
            	AudioPlayer.embed(\"audioplayer_" . $i . "\", {soundFile: \"sounds/audiowikiIndia/web/".$row['id'].".mp3\"});
            	</script>
			</td>
		<td width=\"3%\"><a href=\"confirmDeleteIndia.php?id=".$row['id']."&fileDescription=".$row['description']."\">
			<img src=\"images/delete.png\" alt=\"delete comment\""."width=\"20\" height=\"20\" align=\"absmiddle\" /></a>
		</td>
    	<td width=\"5%\"><a href=\"replace.php?id=".$row['id']."&confirmed=0\">edit</a>
		</td>
  	</tr>";
*/
/*if ($row['time'] )
2010-03-22 15:41:22
Y-m-d
*/

// $date = $date
$year = substr($date,-10,4);
$day = substr($date,-2,2);
$month = substr($date,-5,2);

$dateOfPost = substr($row['time'],-19,10);
$dayOfPost = substr($row['time'],-11,2);
$monthOfPost = substr($row['time'],-14,2);
$yearOfPost = substr($row['time'],-19,4);

$daysAgo = $day-$dayOfPost;
$monthsAgo = $month-$monthOfPost;
$yearsAgo = $year-$yearOfPost;

if ($daysAgo == 0 && $monthsAgo == 0 && $yearsAgo == 0) {
	$displayPostDate = "Today";
} else if ($daysAgo == 1 && $monthsAgo == 0 && $yearsAgo == 0) {
	$displayPostDate = "Yesterday";
} else if ($daysAgo > 1 && $monthsAgo == 0 && $yearsAgo == 0) {
	$displayPostDate = $daysAgo . " days ago";
} else if ($monthsAgo == 1 && $yearsAgo == 0) {
	$displayPostDate = "Last month";
} else if ($monthsAgo > 1 && $yearsAgo == 0) {
	$displayPostDate = $monthsAgo . " months ago";
} else if ($yearsAgo == 1) {
	$displayPostDate = "Last year";
} else if ($yearsAgo > 1) {
	$displayPostDate = $yearsAgo . " years ago";
}

$displayPostDate = "<date>".$displayPostDate."</date>";

	echo 
	"<tr height=\"35\" bgcolor=\"" . $color . "\">
		<td width=\"2%\">
		</td>
		<td width=\"93%\"><$fontStyle id=\"" . $row['id'] . "\" 
class=\"\" style=\"$textcolor display: inline\">". $row['description'] . " " . $displayPostDate . "</$fontStyle>
		</td>		
    		<td width=\"5%\" align=\"center\">
				<a href=\"javascript:niftyplayer('niftyPlayer1').loadAndPlay('sounds/audiowikiIndia/web/".$row['id'].".mp3')\" title=\"Post ID: ".$row['id']."\">play</a>
			</td>
		</td>
  	</tr>";
	}
// The following code is from the moderator version.
/*
	echo 
	"<tr height=\"35\" bgcolor=\"" . $color . "\">
		<td width=\"2%\">
		</td>
		<td width=\"8%\">
        	<input type=\"checkbox\" name=\"selectedPost[]\" id=\"selectedPost\" value=\"".$row['id']."\"> <br />
		</td>
		<td width=\"77%\"><$fontStyle id=\"" . $row['id'] . "\" class=\"edit\" style=\"$textcolor display: inline\">". $row['description'] . "</$fontStyle>
		</td>		
    		<td width=\"3%\">
				<a href=\"javascript:niftyplayer('niftyPlayer1').loadAndPlay('sounds/audiowikiIndia/web/".$row['id'].".mp3')\">play</a>
			</td>
		<td width=\"3%\"><a href=\"confirmDeleteIndia.php?id=".$row['id']."&fileDescription=".$row['description']."\">
			<img src=\"images/delete.png\" alt=\"delete comment\""."width=\"20\" height=\"20\" align=\"absmiddle\" /></a>
		</td>
    	<td width=\"5%\"><a href=\"replace.php?id=".$row['id']."&confirmed=0\">edit</a>
		</td>
  	</tr>";
	}
*/
	mysql_close();
?>
</form>
</table>
<center>
<br />
<br />
<br />
<br />
</body>
</html>
