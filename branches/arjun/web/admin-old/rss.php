<?php
$station = '12345';
$username="python";
$password="rock+bait";
$database="audiowikiIndia";

mysql_connect(localhost,$username,$password);
@mysql_select_db($database) or die( "Unable to select database");

$query = "SELECT * FROM comments WHERE archived = 0 AND station = $station ORDER BY time DESC";
	
$result = mysql_query($query);
$num = mysql_num_rows($result);

$fp = fopen ("rss.xml", "w");

fwrite ($fp, "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
fwrite ($fp, "<rss version=\"2.0\" xmlns:atom=\"http://www.w3.org/2005/Atom\">\n");
fwrite($fp, "<channel>\n");
fwrite($fp, "<title>Swara: Voice of the Developing World</title>\n");
fwrite($fp, "<description>Brought to you by MIT and Microsoft</description>\n");
fwrite($fp, "<link>http://swara.no-ip.org/admin/playback.php</link>\n");
fwrite($fp, "<language>en-us</language>\n");
fwrite($fp, "<pubDate>Fri, 31 Dec 1999 23:59:59 EST</pubDate>\n");
fwrite($fp, "<lastBuildDate>Fri, 31 Dec 1999 23:59:59 EST</lastBuildDate>\n");
fwrite($fp, "<docs>http://blogs.law.harvard.edu/tech/rss</docs>\n");
fwrite($fp, "<generator>MIT CSAIL RSS Editor</generator>\n");
fwrite($fp, "<managingEditor>latif@mit.edu (Latif Alam)</managingEditor>\n");
fwrite($fp, "<webMaster>latif@mit.edu (Latif Alam)</webMaster>\n");
		while ($row = mysql_fetch_array($result)) {
			$UNIX_time_posted = strtotime($row['time']);
			$day = date("D",$UNIX_time_posted);
			$dayOfMonth = date("d",$UNIX_time_posted);
			$month = date("M",$UNIX_time_posted);
			$year = date("Y",$UNIX_time_posted);
			$hours = date("H",$UNIX_time_posted);
			$minutes = date("i",$UNIX_time_posted);
			$seconds = date("s",$UNIX_time_posted);
			$datePosted = "$day, $dayOfMonth $month $year $hours:$minutes:$seconds GMT";
			echo $datePosted;
			 fwrite ($fp, "<item>\n");
				fwrite ($fp, "<title>\n");
					fwrite ($fp, $row['id']."\n");
				fwrite ($fp, "</title>\n");
				fwrite ($fp, "<description>\n");
					fwrite ($fp, $row['description']."\n");
				fwrite ($fp, "</description>\n");
				fwrite ($fp, "<link>\n");
					fwrite ($fp, "http://swara.no-ip.org/admin/playback.php?play=".$row['id']."\n");
				fwrite ($fp, "</link>\n");
				fwrite ($fp, "<guid isPermaLink=\"false\">\n");
					fwrite ($fp, "http://swara.no-ip.org/admin/playback.php?play=".$row['id']."\n");
				fwrite ($fp, "</guid>\n");
				fwrite ($fp, "<pubDate>\n");
					fwrite ($fp, "$datePosted\n"); //$row['time']."\n");
				fwrite ($fp, "</pubDate>\n");
			fwrite ($fp, "</item>\n");
		}
fwrite($fp, "</channel>\n");
fwrite($fp, "</rss>");
?>