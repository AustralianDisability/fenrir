#!/bin/python
from utils import debug
class outputManager():
    def __init__(self):
        pass
    def presentText(self, environment, text, interrupt=True, soundIcon = ''):
        environment['runtime']['debug'].writeDebugOut(environment,"presentText:\nsoundIcon:'"+soundIcon+"'\nText:\n" + text ,debug.debugLevel.INFO)
        if self.playSoundIcon(environment, soundIcon, interrupt):
            environment['runtime']['debug'].writeDebugOut(environment,"presentText:\n" + text ,debug.debugLevel.INFO)            
            return
        self.speakText(environment, text, interrupt)
        self.brailleText(environment, text, interrupt)

    def speakText(self, environment, text, interrupt=True):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'enabled'):
            environment['runtime']['debug'].writeDebugOut(environment,"INFO speech disabled in outputManager.speakText",debug.debugLevel.INFO)
            return
        if environment['runtime']['speechDriver'] == None:
            environment['runtime']['debug'].writeDebugOut(environment,"Error no speechDriver in outputManager.speakText",debug.debugLevel.ERROR)
            return
        if interrupt:
            self.interruptOutput(environment)
        try:
            environment['runtime']['speechDriver'].setLanguage(environment['runtime']['settingsManager'].getSetting(environment, 'speech', 'language'))
        except Exception as e:
            environment['runtime']['debug'].writeDebugOut(environment,"Error while setting speech language in outputManager.speakText",debug.debugLevel.ERROR)
            environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR)
        
        try:
            environment['runtime']['speechDriver'].setVoice(environment['runtime']['settingsManager'].getSetting(environment, 'speech', 'voice'))
        except Exception as e:
            environment['runtime']['debug'].writeDebugOut(environment,"Error while setting speech voice in outputManager.speakText",debug.debugLevel.ERROR)
            environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR)        
        
        try:
            environment['runtime']['speechDriver'].setPitch(environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'speech', 'pitch'))
        except Exception as e:
            environment['runtime']['debug'].writeDebugOut(environment,"Error while setting speech pitch in outputManager.speakText",debug.debugLevel.ERROR)
            environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR)            
        
        try:
            environment['runtime']['speechDriver'].setRate(environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'speech', 'rate'))
        except Exception as e:
            environment['runtime']['debug'].writeDebugOut(environment,"Error while setting speech rate in outputManager.speakText",debug.debugLevel.ERROR)
            environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR)            
        
        try:
            environment['runtime']['speechDriver'].setModule(environment['runtime']['settingsManager'].getSetting(environment, 'speech', 'module'))
        except Exception as e:
            environment['runtime']['debug'].writeDebugOut(environment,"Error while setting speech module in outputManager.speakText",debug.debugLevel.ERROR)
            environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR)

        try:            
            environment['runtime']['speechDriver'].setVolume(environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'speech', 'volume'))
        except Exception as e:
            environment['runtime']['debug'].writeDebugOut(environment,"Error while setting speech volume in outputManager.speakText ",debug.debugLevel.ERROR)
            environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR)            
        
        try:
            environment['runtime']['speechDriver'].speak(text)
        except Exception as e:
            environment['runtime']['debug'].writeDebugOut(environment,"Error while \"speak\" in outputManager.speakText ",debug.debugLevel.ERROR)
            environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR)            

    def brailleText(self, environment, text, interrupt=True):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'braille', 'enabled'):
            return
        if environment['runtime']['brailleDriver'] == None:
            return        
        print('braille:'+text)
    def interruptOutput(self, environment):
        environment['runtime']['speechDriver'].cancel()
        environment['runtime']['soundDriver'].cancel()

    def playSoundIcon(self, environment, soundIcon = '', interrupt=True):
        if soundIcon == '':
            return False
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'sound', 'enabled'):
            environment['runtime']['debug'].writeDebugOut(environment,"INFO sound disabled in outputManager.speakText",debug.debugLevel.INFO)        
            return False  
            
        if environment['runtime']['soundDriver'] == None:
            environment['runtime']['debug'].writeDebugOut(environment,"Error no speechDriver in outputManager.speakText",debug.debugLevel.ERROR)        
            return False       
        try:
            environment['runtime']['soundDriver'].setVolume(environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'sound', 'volume'))
            environment['runtime']['soundDriver'].playSoundFile(environment['soundIcons'][soundIcon], interrupt)
            return True
        except Exception as e:
            environment['runtime']['debug'].writeDebugOut(environment,"Error while \"playSoundIcon\" in outputManager.speakText ",debug.debugLevel.ERROR)
            environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR)            
        return False
