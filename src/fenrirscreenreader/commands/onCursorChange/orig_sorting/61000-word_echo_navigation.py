#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import word_utils
import string

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No Description found'     

    def run(self):
        # is navigation?    
        if not abs(self.env['screen']['oldCursor']['x'] - self.env['screen']['newCursor']['x']) > 1:
            return

        # just when cursor move worddetection is needed
        if not self.env['runtime']['cursorManager'].isCursorHorizontalMove():
            return
        # for now no new line
        if self.env['runtime']['cursorManager'].isCursorVerticalMove():
            return
        # currently writing
        if self.env['runtime']['screenManager'].isDelta():
            return            
        
        # get the word            
        newContent = self.env['screen']['newContentText'].split('\n')[self.env['screen']['newCursor']['y']]
        x, y, currWord, endOfScreen, lineBreak = \
          word_utils.getCurrentWord(self.env['screen']['newCursor']['x'], 0, newContent)                          
        
        # is there a word?        
        if currWord == '':
            return

        # at the start of a word        
        if (x + len(currWord) != self.env['screen']['newCursor']['x'])  and \
          (self.env['screen']['newCursor']['x'] != x):
            return     

        self.env['runtime']['outputManager'].presentText(currWord, interrupt=True, flush=False)

    def setCallback(self, callback):
        pass

