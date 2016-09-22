#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import time

input = {
'currInput': [],
'prevInput': [], 
'prevDeepestInput': [], 
'currEvent': None, 
'eventBuffer': [],
'shortcutRepeat': 0,
'fenrirKey': ['KEY_FENRIR'],
'keyForeward': False,
'lastInputTime':time.time(),
'oldNumLock': True,
'newNumLock':True,
'oldScrollLock': True,
'newScrollLock':True,
'oldCapsLock':False,
'newCapsLock':False
}

inputEvent = {
'EventName': '',
'EventValue': '',
'EventSec': 0,
'EventUsec': 0,
'EventState': 0,
}