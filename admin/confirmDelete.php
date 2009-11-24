
<html>
<center>
<br>
<br>
<br>
<p><h2>Are you sure you want to delete comment <? echo $_GET['id']; ?></h2></p>
<p><h2>language: <? echo $_GET['language']; ?></h2></p>
<p><h2>description: <? echo $_GET['fileDescription']; ?></h2></p>

<form action="deleteComment.php" method="POST">
    <input type="submit" name="delete" value="Delete" />
    <input type="submit" name="cancel" value="Cancel" />
    <input type="hidden" name="id" value="<? echo $_GET['id']; ?>" />
    <input type="hidden" name="language" value="<? echo $_GET['language']; ?>" />
    <input type="hidden" name="fileDescription" value="<? echo $_GET['fileDescription']; ?>" />
</form>
</center>
</html>