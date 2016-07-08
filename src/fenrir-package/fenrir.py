#!/bin/python

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import os, sys, time, signal

DEBUG = False

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())

from threading import Thread
from core import environment 
from core import inputManager
from utils import debug

from speech import espeak as es
from speech import speechd as sd
from screen import linux as lx

class fenrir():
    def __init__(self):
        self.threadUpdateScreen = None
        self.threadHandleInput = None
        self.threadHandleCommandQueue = None
        self.environment = environment.environment
        self.environment['runtime']['inputManager'] = inputManager.inputManager()
        if DEBUG:
            self.environment['runtime']['debug'] = debug.debug()
        signal.signal(signal.SIGINT, self.captureSignal)

        # the following hard coded, in future we have a config loader
        self.environment['runtime']['speechDriver'] = sd.speech()
        self.environment['runtime']['screenDriver'] = lx.screenManager()

    def proceed(self):
        self.threadUpdateScreen = Thread(target=self.updateScreen, args=())
        self.threadHandleInput = Thread(target=self.handleInput, args=())
        self.threadCommandQueue = Thread(target=self.handleCommandQueue, args=())
        self.threadUpdateScreen.start()
        self.threadHandleInput.start()
        self.threadCommandQueue.start()
        while(self.environment['generalInformation']['running']):
            time.sleep(2)
        self.shutdown()

    def handleInput(self):
        while(self.environment['generalInformation']['running']):
            self.environment = self.environment['runtime']['inputManager'].getKeyPressed(self.environment)

    def updateScreen(self):
        while(self.environment['generalInformation']['running']):
            self.environment = self.environment['runtime']['screenDriver'].analyzeScreen(self.environment)

    def handleCommandQueue(self):
        while(self.environment['generalInformation']['running']):
            self.environment = self.environment # command queue here

    def shutdown(self):
        self.environment['generalInformation']['running'] = False
        if self.environment['runtime']['speechDriver'] != None:
            self.environment['runtime']['speechDriver'].shutdown()
        if self.environment['runtime']['debug'] != None:
            self.environment['runtime']['debug'].closeDebugFile()

    def captureSignal(self, siginit, frame):
        self.shutdown()

app = fenrir()
app.proceed()
