#!/usr/bin/python
# -*- coding: utf-8 -*-
#Menu system
import sys
from asteriskinterface import *

# incoming call data
while True:
    line = readline()
    if line == '':
        break

# retrive the number called into the "number" variable
sys.stdout.write('GET VARIABLE NUMBER\n')
sys.stdout.flush()
number = sys.stdin.readline()
debugPrint(number)

# play whatever audio file you want
playFile('/home/thies/audiowiki/sound\ files/sounds/htest')
