#!/bin/python
from utils import word_utils
initialized = False
try:
    import enchant
    initialized = True
except:
    pass
    
class command():
    def __init__(self):
        self.language = ''
        self.spellChecker = None
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self):
        return 'removes the current word from the exceptions dictionary'        
    def run(self, environment):
        if not initialized:
           environment['runtime']['outputManager'].presentText(environment, 'pychant is not installed', interrupt=True) 
           return environment
        if environment['runtime']['settingsManager'].getSetting(environment, 'general', 'spellCheckLanguage') != self.language:
            try:
                self.spellChecker = enchant.Dict(environment['runtime']['settingsManager'].getSetting(environment, 'general', 'spellCheckLanguage'))
                self.language = environment['runtime']['settingsManager'].getSetting(environment, 'general', 'spellCheckLanguage')
            except:
                return environment    

        if (environment['screenData']['newCursorReview'] != None):
            cursorPos = environment['screenData']['newCursorReview'].copy()
        else:
            cursorPos = environment['screenData']['newCursor'].copy()
            
        # get the word
        newContent = environment['screenData']['newContentText'].split('\n')[cursorPos['y']]
        x, y, currWord =  word_utils.getCurrentWord(cursorPos['x'], 0, newContent)                  

        if currWord != '':
            if self.spellChecker.is_removed(currWord):
                environment['runtime']['outputManager'].presentText(environment, currWord + ' is already removed from dict',soundIcon='Cancel', interrupt=True)                
            else:
                self.spellChecker.remove(currWord)             
                environment['runtime']['outputManager'].presentText(environment, currWord + ' removed',soundIcon='Accept', interrupt=True)                    
                    
        return environment
    def setCallback(self, callback):
        pass