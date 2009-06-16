
Setting Up the Audio Wikipedia Database --

In order to recreate the Audio Wikipedia system, the following scripts must be run on your host server. MySQL must be installed before running these scripts.

categories.sql
comments.sql
threads.sql
users.sql

You can use the following command from the command line:
shell> mysql < backup_file.sql

See http://dev.mysql.com/doc/refman/5.1/en/recovery-from-backups.html for more information.

The categories.txt file contains the current categories loaded on the polwatta.csail.mit.edu server. Feel free to change these, but make sure you change the corresponding audio files (see /sound files), as well.

-- The  MIT Audio Wikipedia Team