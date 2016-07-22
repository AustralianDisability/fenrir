#!/bin/python

def getPrevLine(currX,currY, currText):
    if currText == '':
        return -1, -1, ''
    wrappedLines = currText.split('\n')         
    x = currX
    y = currY 
    if y - 1 >= 0:
        y -= 1
    x = 0
    currLine = wrappedLines[y]                   
    return x, y, currLine

def getCurrentLine(currX,currY, currText):
    if currText == '':
        return -1, -1, ''
    wrappedLines = currText.split('\n')         
    x = currX
    y = currY
    x = 0
    currLine = wrappedLines[y]
    return x, y, currLine

def getNextLine(currX,currY, currText):
    if currText == '':
        return -1, -1, ''
    wrappedLines = currText.split('\n')         
    x = currX
    y = currY
    if y + 1 < len(wrappedLines):
        y += 1
    x = 0
    currLine = wrappedLines[y]    
    return x, y, currLine
