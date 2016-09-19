#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass 
    def getDescription(self, environment):
        return 'clears the currently selected clipboard'     

    def run(self, environment):
        environment['commandBuffer']['currClipboard'] = -1
        del environment['commandBuffer']['clipboard'][:]
        environment['runtime']['outputManager'].presentText(environment, 'clipboard cleared', interrupt=True)
        return                
    def setCallback(self, callback):
        pass
