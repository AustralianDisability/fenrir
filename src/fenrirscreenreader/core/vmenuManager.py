#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import os


class vmenuManager():
    def __init__(self):
        self.menuDict = {}
        self.currIndex = None
        self.currMenu = ''
        self.active = False
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getActive(self):
        return self.active
    def togglelMode(self, currMenu = ''):
        self.setActive(not self.getActive(), currMenu)
    def setActive(self, active, currMenu = ''):
        self.active = active
        self.currMenu = currMenu
        if active:
            self.createMenuTree()        
            self.env['bindings'][str([1, ['KEY_ESC']])] = 'TOGGLE_TUTORIAL_MODE'
            self.env['bindings'][str([1, ['KEY_UP']])] = 'PREV_HELP'
            self.env['bindings'][str([1, ['KEY_DOWN']])] = 'NEXT_HELP'
            self.env['bindings'][str([1, ['KEY_SPACE']])] = 'CURR_HELP'
            self.env['bindings'][str([1, ['KEY_LEFT']])] = 'NEXT_HELP'
            self.env['bindings'][str([1, ['KEY_RIGHT']])] = 'CURR_HELP'
            self.env['bindings'][str([1, ['KEY_ENTER']])] = 'CURR_HELP'            
        else:
            try:
                self.menuDict = {}
                self.currIndex = None
                self.currMenu = ''
                self.currLevel = 0
                self.active = False
                del(self.env['bindings'][str([1, ['KEY_ESC']])])
                del(self.env['bindings'][str([1, ['KEY_UP']])])
                del(self.env['bindings'][str([1, ['KEY_DOWN']])])
                del(self.env['bindings'][str([1, ['KEY_SPACE']])])
                del(self.env['bindings'][str([1, ['KEY_LEFT']])])
                del(self.env['bindings'][str([1, ['KEY_RIGHT']])])                
                del(self.env['bindings'][str([1, ['KEY_ENTER']])])                
            except:
                pass                     

    
    def createMenuTree(self):
        self.currIndex = None        
        self.menuDict = fs_tree_to_dict( '/home/chrys/Projekte/fenrir/src/fenrirscreenreader/commands/vmenu/KEY')
        if len(self.menuDict) > 0:
            self.currIndex = 0
    def executeMenu(self):
        if self.currIndex == None:
            return    
    def incLevel(self):
        if self.currIndex == None:
            return    
        if len(self.currIndex) == 1:
            return
        try:
            r = self.getValueByPath(self.menuDict, self.currIndex +[0]):
            if not r:
                return
            if not isinstance(r, dict):
                return
            if r == {}:
                return
        except:
            return
        self.currIndex.append(0)
    def decLevel(self):
        if self.currIndex == None:
            return    
        if len(self.currIndex) == 1:
            return        
        self.currIndex.remove(len(self.currIndex) - 1)
    def nextIndex(self):
        if self.currIndex == None:
            return    
        self.currIndex[len(self.currIndex) - 1] += 1
        if self.currIndex[len(self.currIndex) - 1] >= len(self.getNestedByPath(self.menuDict, self.currIndex[:-1])):
           self.currIndex[len(self.currIndex) - 1] = 0 
    def prevIndex(self):
        if self.currIndex == None:
            return    
        if len(self.currIndex) - 1 < self.currLevel:
            return
        self.currIndex[len(self.currIndex) - 1] -= 1
        if self.currIndex[len(self.currIndex) - 1] < 0:
           self.currIndex[len(self.currIndex) - 1] = len(self.getNestedByPath(self.menuDict, self.currIndex[:-1])) - 1
    def fs_tree_to_dict(self, path_):
        for root, dirs, files in os.walk(path_):
            tree = {d: fs_tree_to_dict(os.path.join(root, d)) for d in dirs}
            tree.update({f: root + '/' + f for f in files})
            return tree  # note we discontinue iteration trough os.walk
    def getKeysByPath(self, complete, path):
        if not isinstance(complete, dict):
            return[]
        d = complete
        for i in path[:-1]:
            d = d[list(d.keys())[i]]
        return list(d.keys())

    def getValueByPath(self, complete, path):
        if not isinstance(complete, dict):
            return None
        d = complete.copy()
        for i in path:
            d = d[list(d.keys())[i]]
        return d
''''
import os
level = [0]

def fs_tree_to_dict( path_):
    file_token = ''
    for root, dirs, files in os.walk(path_):
        tree = {d: fs_tree_to_dict(os.path.join(root, d)) for d in dirs}
        print(files, root, dirs)
        tree.update({f: root + '/' + f for f in files})
        return tree  # note we discontinue iteration trough os.walk


v = fs_tree_to_dict( '/home/chrys/Projekte/fenrir/src/fenrirscreenreader/commands/vmenu/KEY')        


def getNestedByPath(complete, path):
    path = path.copy()
    if path != []:
        index = list(complete.keys())[path[0]]
        path.remove(0)
        nested = getNestedByPath(complete[index], path)
        return nested
    else:
        return complete

def getKeysByPath(complete, path):
    d = complete
    for i in path[:-1]:
        d = d[list(d.keys())[i]]
    return list(d.keys())


def getValueByPath(complete, path):
    d = complete
    for i in path:
        d = d[list(d.keys())[i]]
    return d


c = [0,0,0]


getKeysByPath(v,c)
getValueByPath(v,c)

''''
