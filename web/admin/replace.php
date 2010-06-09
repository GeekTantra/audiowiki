<?php include("/var/www/html/admin/password_protect.php"); ?> 

<script src="Scripts/swfobject_modified.js" type="text/javascript"></script>
<script type="text/javascript" src="Scripts/audio-player.js"></script>  
<script type="text/javascript">  
            AudioPlayer.setup("images/player.swf", {  
                width: 300,
				animation: "no",
				transparentpagebg: "yes",
				remaining: 'yes',
				noinfo: 'yes',
				rtl: 'yes'
            });  
</script>


<?php

$id =$_GET['id'];


if ($_GET['confirmed'] == 0) { ?>
<center>
<table width="100%" align="center">
<tr>
<td align="center">
<h1>Please confirm that this is the comment you're replacing. </h1>
<p id="audioplayer_<?php=$id?>">Alternative content</p>  
<script type="text/javascript">  
AudioPlayer.embed("audioplayer_<?php=$id?>", {soundFile: "sounds/audiowikiIndia/web/<?php=$id?>.mp3"});
</script>

<br />
<br />
<br />

</td>
</tr>
</table>
<table width="40%" border="0" align="center">
  <tr>
    <?php
	echo
	"<td align=\"center\"><h1><strong><a href=\"replace.php?id=".$id."&confirmed=1\">Yes</a></strong></h1></td>";
	?>
    <td align="center"><h1><strong><a href="index.php">No</a></strong></h1></td>
  </tr>
</table>
<p>
  <?php
	
} else if ($_GET['confirmed'] == 1) { ?>

<center>
</p>
<table cellpadding="40">
  <tr>

  <?php

  echo
  "<td align=\"center\">
<a href=\"downloadComment.php?id=".$id."&path=sounds/audiowikiIndia/web/".$id.".mp3\">";

?>
Click here to download the file (mp3 format).</a></td>
</tr>
<tr>
<td>
<h1>Once you've edited this post (we recommend using <a href=http://audacity.sourceforge.net/download/>Audacity</a>), <br> upload the mp3 here:</h1>
<center>

<?php

echo
"<form enctype=\"multipart/form-data\" action=\"replace.php?confirmed=2&id=".$id." method=\"POST\">
  <p><input name=\"uploadedComment\" type=\"file\" /> 
    <input type=\"submit\" value=\"Upload\" />
  </p>
</form> 
<br />
</tr>"
?>

</table>

<p>
<?php } else if ($_GET['confirmed'] == 2) {
	
    $username="python";
    $password="rock+bait";
    $database="audiowikiIndia";

    mysql_connect(localhost,$username,$password);
    @mysql_select_db($database) or die( "Unable to select database");
	
	// Move both the mp3 web file and the wav phone file to the edited directory
	//rename('/var/www/admin/sounds/audiowikiIndia/'.$_GET['id'].'.wav', 'sounds/audiowikiIndia/edited/'.$_GET['id'].'.wav');
	//rename('/var/www/admin/sounds/audiowikiIndia/'.$_GET['id'].'.raw', 'sounds/audiowikiIndia/edited/'.$_GET['id'].'.raw');
	//rename('/var/www/admin/sounds/audiowikiIndia/web/'.$_GET['id'].'.mp3', 'sounds/audiowikiIndia/edited/'.$_GET['id'].'.mp3');
	if (rename('/var/lib/asterisk/sounds/audiowikiIndia/web/'.$_GET['id'].'.mp3', 'sounds/audiowikiIndia/edited/'.$_GET['id'].'.mp3')) {
		echo "mp3 transferred";
	}
	if (rename('/var/lib/asterisk/sounds/audiowikiIndia/'.$_GET['id'].'.wav', 'sounds/audiowikiIndia/edited/'.$_GET['id'].'.wav')) {
		echo "wav transferred";
	};
	if (rename('/var/lib/asterisk/sounds/audiowikiIndia/'.$_GET['id'].'.raw', 'sounds/audiowikiIndia/edited/'.$_GET['id'].'.raw')) {
		echo "raw transferred";
	};

	$id = $_GET['id'];
	
	$soundsDir = "/var/lib/asterisk/sounds/audiowikiIndia";
	$target_path = "/var/lib/asterisk/sounds/audiowikiIndia/web/";
	$target_path = $target_path . $id . ".mp3";
	//echo basename($_FILES['uploadedComment']['name']);
	if(move_uploaded_file($_FILES['uploadedComment']['tmp_name'], $target_path)) {
		//	$convertToMp3 = "lame -h --abr 200 ".$target_path." sounds/audiowikiIndia/web/".$_GET['id'].".mp3";
		//	exec($convertToMp3);
		$convertToWav1 = "/usr/local/bin/lame --decode $target_path $soundsDir/$id.wav";
		$convertToWav2 = "sox -V $soundsDir/$id.wav -r 8000 -c 1 $soundsDir/$id.raw";
		exec($convertToWav1, $output = array());
		//echo $convertToWav1;
		//print_r( $output );
		exec($convertToWav2);
	
		$query = "UPDATE comments SET edited = edited + 1 where id = ".$_GET['id'];
	    if (!mysql_query($query)) { echo "File uploaded but database edit count not updated."; }
		else {
			echo "<center><h1><br><br><br>Thanks! You've just edited comment". $_GET['id'].". Return to <a href=\"index.php\">library</a></h1>";
		}		
		//echo "The file ".  basename( $_FILES['uploadedComment']['name'])." has been uploaded";
	} else {
			echo "There was an error uploading the file, please try again! <br> Return to <a href=\"index.php\">library</a>";
	}
}
?>