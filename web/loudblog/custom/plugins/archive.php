<?php

// -------------------------------------------------------------------------------
// LoudBlog plugin
// Simple Archive
// by Gerrit van Aaken
//
// Configure "ul#archive" in your style-sheet file to style
// this component. The current month is tagged with "ul#archive li.active"
//
// Available attributes
//      begin = Start the archive at this month.
//				for example: "2004-10", "2006-04" ...
//      end = Stop the archive at this month.
// 				for example: "2005-10", "2006-3" ...
//		To show all postings, just don't assign atributes!
//
// Released under the Gnu General Public License
// http://www.gnu.org/copyleft/gpl.html
// -------------------------------------------------------------------------------

function archive($context) {
	$attributes = getattributes($context);
	$content = '';
	
	// define something
	$displayMonth['01'] = 'january';
	$displayMonth['02'] = 'february';
	$displayMonth['03'] = 'march';
	$displayMonth['04'] = 'april';
	$displayMonth['05'] = 'may';
	$displayMonth['06'] = 'june';
	$displayMonth['07'] = 'july';
	$displayMonth['08'] = 'august';
	$displayMonth['09'] = 'september';
	$displayMonth['10'] = 'october';
	$displayMonth['11'] = 'november';
	$displayMonth['12'] = 'december';

	// parse attributes
	if(isset($attributes['begin'])) {
		$startlist = $attributes['begin'];
	} else {
		$startlist = "1900-01";
	}

	if(isset($attributes['end'])) {
		$stoplist = $attributes['end'];
	} else {
		$stoplist = "2020-12";
	}

	//define data for db-query
	
	// start the archive on ...
	$month = (int) substr($startlist,5,2);
	$year = substr($startlist,0,4);
	
	$firstDay = mktime(0, 0, 0, $month, 1, $year);
	
	// end the archive on ...
	$month = (int) substr($stoplist,5,2);
	$year = substr($stoplist,0,4);
	$lastDay = mktime(23, 59, 59, ($month+1), 0, $year);

	// get post dates
	$dosql = "SELECT posted FROM ".$GLOBALS['prefix']."lb_postings WHERE posted >= '" . date("Y-m-d H:i:s", $firstDay) . "' AND posted < '" . date("Y-m-d H:i:s", $lastDay) . "' AND status = '3' ORDER BY posted";
	$result = $GLOBALS['lbdata']->Execute($dosql);
    $rows = $result->GetArray();
   
   
   //show all months where postings exist
   $content .= "\n<ul id=\"archive\">\n";
   $prevmonth = "foobar";
   if (isset($_GET['date'])) {
   		$activemonth = substr($_GET['date'], 0, 7);
   } else {
   		$activemonth = "";
   }
   foreach ($rows as $row) {
		$thismonth = date("Y-m", strtotime($row['posted']));
   		if ($thismonth != $prevmonth) {
   			$moncode = substr($thismonth,5,2);
   			$year = substr($thismonth,0,4);
   			if ($thismonth == $activemonth) {
   				$class = " class=\"active\"";
   			} else {
   				$class = "";
   			}
   			$content .= "    <li".$class."><a href=\"?date=".$thismonth."\">";
   			$content .= $displayMonth[$moncode]." ".$year."</a></li>\n";
   }
   $prevmonth = $thismonth;
   }
   
   $content .= "</ul>\n\n";


	return $content;
}

?>