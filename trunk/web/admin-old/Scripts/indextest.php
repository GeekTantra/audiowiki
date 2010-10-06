<?php include("/var/www/html/admin/password_protect.php"); ?>
<?
	$playFileOnLoad = $_POST['play'];
	
	if (!isset($playFileOnLoad)) {
		$as = 0;
	} else {
		$as = 1;
	}

	$station = '12345';//$_GET['station'];
	
	$view = $_POST['view'];
	if (!isset($view)) { $view = 'all'; }
	
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
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>CGNet Swara</title>
<script language="text/javascript" src="Scripts/wimpy.js"></script>
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

#topLeft
{
    top: 0px;
    left: 0px;
}
#bottomLeft
{
	position: fixed;
	bottom: 0px;
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
<!--<script type="text/javascript" src="Scripts/audio-player.js"></script>  
<script type="text/javascript">  
            AudioPlayer.setup("images/player.swf", {  
                width: 300,
				transparentpagebg: "yes",
				remaining: 'yes',
				noinfo: 'yes',
				rtl: 'yes'
            });  
</script>
-->
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
<div id="wimpyTarget" align="center">
<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=8,0,0,0" width="370" height="55" id="wimpy" align="center">
<param name="allowScriptAccess" value="always" />
<param name="movie" value="http://audiowiki.no-ip.org/admin/wimpy.swf" />
<param name="loop" value="false" />
<param name="menu" value="false" />
<param name="quality" value="high" />
<param name="scale" value="noscale" />
<param name="salign" value="lt" />
<param name="bgcolor" value="#94B2D1" />
<param name="flashvars" value="wimpyApp=http://localhost/swara/html/admin/testmp3/wimpy.php&wimpySkin=http://localhost/swara/html/admin/testmp3/skins/skin_mini.xml&startPlayingOnload=yes&wimpySkin=http://localhost/swara/html/admin/testmp3/skins/skin_mini.xml" />
<param name="wmode" value="opaque" />
<embed src="http://audiowiki.no-ip.org/admin/wimpy.swf" flashvars="wimpyApp=http://audiowiki.no-ip.org/admin/wimpy.php&wimpySkin=http://audiowiki.no-ip.org/admin/skins/skin_mini.xml&startPlayingOnload=yes&wimpySkin=http://audiowiki.no-ip.org/admin/skins/skin_mini.xml" loop="false" wmode="opaque" menu="false" quality="high" width="370" height="55" scale="noscale" salign="lt" name="wimpy" align="center" bgcolor="#94B2D1" allowScriptAccess="always" allowFullScreen="true" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" />
</object> </div>

<script language="JavaScript">

	var MySettings = new Object();
	MySettings.wimpySkin =  "skins/skin_mini.xml";
	MySettings.startPlayingOnLoad = "yes";
	MySettings.bkgdColor = "#94B2D1";
	MySettings.wimpyWidth = "370";
	MySettings.wimpyHeight = "55";
	MySettings.bufferAudio = "5";
	
	makeWimpyPlayer(MySettings);
	
</script>
<br />
<br />
<p class="sample">CGNet Swara</p>
<div class="visibleDiv" id="bottomLeft">
<table width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="#666" style="color:#FFF">
  <tr>
    <td></td>
    <td>
    	  <INPUT TYPE="SUBMIT" name="Operation" onClick="document.pressed=this.value;return OnSubmitForm();" VALUE="Publish">
    	  <INPUT TYPE="SUBMIT" name="Operation" onClick="document.pressed=this.value;return OnSubmitForm();" VALUE="Archive">
    	  <INPUT TYPE="SUBMIT" name="Operation" onClick="document.pressed=this.value;return OnSubmitForm();" VALUE="Delete">
    </td>
    <td>
          <FORM  name="post_view" id="post_view" ACTION="index.php" METHOD=POST onSubmit="return dropdown(this.gourl)" style="border:0;">
          view:
          <select name="view" onchange="document.post_view.submit();"><option value="published" <? if ($view=='published') {echo 'selected';} ?>>Published Posts</option>
            <option value="new" <? if ($view=='new') {echo 'selected';} ?>>New Posts</option>
            <option value="all" <? if ($view=='all') {echo 'selected';} ?>>All Posts</option>
          </select>
          </FORM>
    </td>
    <td align="right">
    <form enctype="multipart/form-data" action="uploadMp3.php?" method="POST">
	  <input name="uploadMp3" type="file" /> 
	    <input type="submit" value="Upload" />
	</form>
	</td>
  </tr>
</table>
</div>


<FORM name="myform" id="myform" onSubmit="return OnSubmitForm();" method="get">
<?
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
		<td width=\"8%\">
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

	echo 
	"<tr height=\"35\" bgcolor=\"" . $color . "\">
		<td width=\"3%\">
		</td>
		<td width=\"2%\">
        	<input type=\"checkbox\" name=\"selectedPost[]\" id=\"selectedPost\" value=\"".$row['id']."\"> <br />
		</td>
		<td width=\"80%\"><$fontStyle id=\"" . $row['id'] . "\" class=\"edit\" style=\"$textcolor display: inline\">". $row['description'] . "</$fontStyle>
		<td width=\"1%\">
		</td>
		</td>		
    		<td width=\"10%\">
				<a href=\"JavaScript:;" onClick="wimpy_addTrack(true,'sounds/audiowikiIndia/web/1061.mp3', '','','','');\">play</a>
				<a href=\"confirmDeleteIndia.php?id=".$row['id']."&fileDescription=".$row['description']."\">delete </a>
				<a href=\"replace.php?id=".$row['id']."&confirmed=0\">edit</a>
		</td>
		<td width=\"2%\">
		</td>
  	</tr>";
	}
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

<a href=\"javascript:niftyplayer('niftyPlayer1').loadAndPlay('sounds/audiowikiIndia/web/".$row['id'].".mp3')\">play </a>

<a href=\"javascript:;" onClick="wimpy_addTrack(true,'sounds/audiowikiIndia/web/".$row['id'].".mp3', '','','','');\">play</a>
				