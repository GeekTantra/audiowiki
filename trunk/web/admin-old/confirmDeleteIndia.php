<?php include("/var/www/html/admin/password_protect.php"); ?> 

<html>
<center>
<br>
<br>
<br>
<p><h2>Are you sure you want to delete comment <?php echo $_GET['id']; ?></h2></p>
<p><h2>"<?php echo $_GET['fileDescription'];?>"</h2></p>

<form action="deleteCommentIndia.php" method="POST">
    <input type="submit" name="delete" value="Delete" />
    <input type="submit" name="cancel" value="Cancel" />
    <input type="hidden" name="id" value="<?php echo $_GET['id']; ?>" />
    <input type="hidden" name="fileDescription" value="<?php echo $_GET['fileDescription']; ?>" />
</form>

</center>
</html>