#!/bin/bash
cd /home/swara/audiowiki
echo `date +%d-%h-%Y-%H:%M Youtube Update` >> /var/log/swara.log
/home/swara/audiowiki/youtubeswarastory.py >> /var/log/swara.log
echo `date +%d-%h-%Y-%H:%M Youtube Update Ends` >> /var/log/swara.log
cd
