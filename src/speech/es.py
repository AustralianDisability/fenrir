#!/usr/bin/python

# Espeak driver

class speech():
    isInitialized = False
    
    def __init__(self):
        pass

    def speak(text, queueable=True):
        if queueable == False: self.stop()

    def stop(self):
        pass

    def clear_buffer(self):
        pass
