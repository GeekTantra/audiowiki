#!/bin/bash
cd /home/swara/audiowiki
echo `date +%d-%h-%Y-%H:%M Twitter Update` >> /var/log/swara.log
/home/swara/audiowiki/tweetswarastory.py >> /var/log/swara.log
echo `date +%d-%h-%Y-%H:%M Twitter Update Ends` >> /var/log/swara.log
cd
