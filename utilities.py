#helper functions for the asterisk menu system.
#Meant to be import *'d

import os
import sys
import random

def debugPrint(str):
    sys.stderr.write(str+'\n')
    sys.stderr.flush()
    os.system("echo %s >> /var/log/swara.log" %str)

class KeyPressException(Exception):
    def __init__(self, key):
        self.key = key
    def __str__(self):
        return repr(self.key) + ' was pressed.'

def newKeyDict():
    return {'0':RaiseZero,'#':Nop}

def RaiseZero():
    raise KeyPressException('0')

def RaiseKey(key):
    raise KeyPressException(key)

def Nop():
    pass

def removeTempFile(fname):
    os.remove(fname)

def coloredText(string, color=False, bold=False):
    colors_dict = {
        'gray': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'white': '37',
        'crimson': '38',
        'highlighted_red': '41',
        'highlighted_green': '42',
        'highlighted_brown': '43',
        'highlighted_blue': '44',
        'highlighted_magenta': '45',
        'highlighted_cyan': '46',
        'highlighted_gray': '47',
        'highlighted_crimson': '48',
    }
    if colors_dict.has_key(color):
        bold_attr = ('', '1')[bold]
        return '\033['+ bold_attr +';'+colors_dict[color] + 'm' + string + '\033['+ bold_attr +';m'
    else:
        return string

def keyPressCLIPrompt(string, key):
    key_colors = ['highlighted_red', 'highlighted_green', 'highlighted_brown', 'highlighted_blue', 'highlighted_magenta', 'highlighted_cyan', 'highlighted_gray', 'highlighted_crimson', ]
    random.shuffle(key_colors)
    return coloredText("\t--"+'Press ', 'blue') + coloredText(key, key_colors[0], True) + coloredText(' for ', 'blue') + coloredText(string, 'blue', True) + coloredText('.', 'blue')

