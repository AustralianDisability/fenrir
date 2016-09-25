#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import time
from core import debug
from core import inputEvent

class inputManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
        self.env['runtime']['settingsManager'].loadDriver(\
          self.env['runtime']['settingsManager'].getSetting('keyboard', 'driver'), 'inputDriver')
        # init LEDs with current state
        self.env['input']['newNumLock'] = self.env['runtime']['inputDriver'].getNumlock()
        self.env['input']['oldNumLock'] = self.env['input']['newNumLock']
        self.env['input']['newCapsLock'] = self.env['runtime']['inputDriver'].getCapslock()
        self.env['input']['oldCapsLock'] = self.env['input']['newCapsLock']
        self.env['input']['newScrollLock'] = self.env['runtime']['inputDriver'].getScrollLock()
        self.env['input']['oldScrollLock'] = self.env['input']['newScrollLock']
        self.grabDevices()

    def shutdown(self):
        self.env['runtime']['inputManager'].releaseDevices()
        self.env['runtime']['settingsManager'].shutdownDriver('inputDriver')

    def getInputEvent(self):
        eventReceived = False
        mEvent = self.env['runtime']['inputDriver'].getInputEvent()
        if mEvent:
            mEvent['EventName'] = self.convertEventName(mEvent['EventName'])        
            if mEvent['EventValue'] == 0:
                return False  
            eventReceived = True
            if mEvent['EventState'] == 0:
                if mEvent['EventName'] in self.env['input']['currInput']:
                    self.env['input']['currInput'].remove(mEvent['EventName'])
                    self.env['input']['currInput'] = sorted(self.env['input']['currInput'])
            elif mEvent['EventState'] == 1:
                if not mEvent['EventName'] in self.env['input']['currInput']:
                    self.env['input']['currInput'].append(mEvent['EventName'])
                    self.env['input']['currInput'] = sorted(self.env['input']['currInput'])
            elif mEvent['EventState'] == 2:
                pass
            else:
                pass  
            self.env['input']['oldNumLock'] = self.env['input']['newNumLock']
            self.env['input']['newNumLock'] = self.env['runtime']['inputDriver'].getNumlock()
            self.env['input']['oldCapsLock'] = self.env['input']['newCapsLock'] 
            self.env['input']['newCapsLock'] = self.env['runtime']['inputDriver'].getCapslock()
            self.env['input']['oldScrollLock'] = self.env['input']['newScrollLock'] 
            self.env['input']['newScrollLock'] = self.env['runtime']['inputDriver'].getScrollLock()
            self.env['input']['lastInputTime'] = time.time()
            self.env['input']['shortcutRepeat'] = 1
        return eventReceived
    
    def grabDevices(self):
        if self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'grabDevices'):
            self.env['runtime']['inputDriver'].grabDevices()

    def releaseDevices(self):
        self.env['runtime']['inputDriver'].releaseDevices()

    def convertEventName(self, eventName):
        if not eventName:
            return ''
        
        if eventName == 'KEY_LEFTCTRL':
            eventName = 'KEY_CTRL'         
        elif eventName == 'KEY_RIGHTCTRL':
            eventName = 'KEY_CTRL'
        elif eventName == 'KEY_LEFTSHIFT':
            eventName = 'KEY_SHIFT'
        elif eventName == 'KEY_RIGHTSHIFT':
            eventName = 'KEY_SHIFT'
        elif eventName == 'KEY_LEFTALT':
            eventName = 'KEY_ALT'
        elif eventName == 'KEY_RIGHTALT':
            eventName = 'KEY_ALT'
        elif eventName == 'KEY_LEFTMETA':
            eventName = 'KEY_META'
        elif eventName == 'KEY_RIGHTMETA':
            eventName = 'KEY_META'            
        if self.isFenrirKey(eventName):
            eventName = 'KEY_FENRIR'
        return eventName
	
    def isConsumeInput(self):
        return self.env['runtime']['commandManager'].isCommandQueued() and \
          not self.env['input']['keyForeward']
        #and
        #  not (self.env['input']['keyForeward'] or \
        #  self.env['runtime']['settingsManager'].getSettingAsBool(, 'keyboard', 'grabDevices'))
 
    def clearEventBuffer(self):
        self.env['runtime']['inputDriver'].clearEventBuffer()
          
    def writeEventBuffer(self):
        try:
            self.env['runtime']['inputDriver'].writeEventBuffer()
            time.sleep(0.005)
            self.clearEventBuffer()
        except Exception as e:
            print(e)
            self.env['runtime']['debug'].writeDebugOut("Error while writeUInput",debug.debugLevel.ERROR)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)

    def isFenrirKeyPressed(self):
        return 'KEY_FENRIR' in self.env['input']['currInput']

    def noKeyPressed(self):
        return self.env['input']['currInput'] == []
        
    def getPrevDeepestInput(self):
        shortcut = []
        shortcut.append(self.env['input']['shortcutRepeat'])
        shortcut.append(sorted(self.env['input']['prevDeepestInput']))

    def getPrevShortcut(self):
        shortcut = []
        shortcut.append(self.env['input']['shortcutRepeat'])
        shortcut.append(sorted(self.env['input']['prevInput']))
        return str(shortcut)

    def getCurrShortcut(self):
        shortcut = []
        shortcut.append(self.env['input']['shortcutRepeat'])
        shortcut.append(sorted(self.env['input']['currInput']))
        return str(shortcut)
        
    def isFenrirKey(self, eventName):
        return eventName in self.env['input']['fenrirKey']

    def getCommandForShortcut(self, shortcut):
        shortcut = shortcut.upper()
        if not self.shortcutExists(shortcut):
            return '' 
        return self.env['bindings'][shortcut].upper()

    def shortcutExists(self, shortcut):
        return( str(shortcut).upper() in self.env['bindings'])
