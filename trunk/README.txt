Here's how to link this repository with a working system:

1.
Establish these symlinks (where "audiowiki" represents the current
directory):
/var/www/html -> audiowiki/web
/var/lib/asterisk/sounds --> audiowiki/sound files/sounds/sounds
/var/lib/asterisk/agi-bin --> audiowiki

3.
Copy or customize ./extensions.conf to /etc/asterisk/
