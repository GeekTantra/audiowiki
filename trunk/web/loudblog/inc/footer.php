<?php ?>

</div>

<div id="footer">



<p> &copy; 2010 <a href="http://www.audiowiki.no-ip.org">CGNet Swara</a> <?php
if ($access)
echo " | ".bla("footer_logged")." ". $_SESSION['nickname'] . " | <a href=\"index.php?do=logout\">".bla("footer_logout")."</a>"; ?>



</p>

</div>

</body>
</html>


