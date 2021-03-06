#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import os, struct, sys, pty, tty, termios, shlex, signal, pyte, time, fcntl ,getpass
from select import select
from fenrirscreenreader.core import debug
from fenrirscreenreader.core.eventData import fenrirEventType
from fenrirscreenreader.core.screenDriver import screenDriver
from fenrirscreenreader.utils import screen_utils


class fenrirScreen(pyte.Screen):
    def set_margins(self, *args, **kwargs):
        kwargs.pop("private", None)
        super(fenrirScreen, self).set_margins(*args, **kwargs)

class Terminal:
    def __init__(self, columns, lines, p_in):
        self.text = ''
        self.attributes = None
        self.screen = fenrirScreen(columns, lines)
        self.screen.write_process_input = \
            lambda data: p_in.write(data.encode())
        self.stream = pyte.ByteStream()
        self.stream.attach(self.screen)
    def feed(self, data):
        self.stream.feed(data)

    def updateAttributes(self, initialize = False):
        buffer = self.screen.buffer
        lines = None
        if not initialize:
            lines = self.screen.dirty
        else:
            lines = range(self.screen.lines)
            self.attributes = [[list(attribute[1:]) + [False, 'default', 'default'] for attribute in line.values()] for line in buffer.values()]
        for y in lines:
            try:
                t = self.attributes[y]
            except:
                self.attributes.append([])

            self.attributes[y] = [list(attribute[1:]) + [False, 'default', 'default'] for attribute in (buffer[y].values())]
            if len(self.attributes[y]) < self.screen.columns:
                diff = self.screen.columns - len(self.attributes[y])
                self.attributes[y] += [['default', 'default', False, False, False, False, False, False, 'default', 'default']]   * diff

    def resize(self, lines, columns):
        self.screen.resize(lines, columns)
        self.setCursor()
        self.updateAttributes(True)
    def setCursor(self, x = -1, y = -1):
        xPos = x
        yPos = y
        if xPos == -1:
            xPos = self.screen.cursor.x
        if yPos == -1:
            yPos = self.screen.cursor.y
        self.screen.cursor.x = min(self.screen.cursor.x, self.screen.columns - 1)
        self.screen.cursor.y = min(self.screen.cursor.y, self.screen.lines - 1)
    def GetScreenContent(self):
        cursor = self.screen.cursor
        self.text = '\n'.join(self.screen.display)
        self.updateAttributes(self.attributes == None)
        self.screen.dirty.clear()
        return {"cursor": (cursor.x, cursor.y),
            'lines': self.screen.lines,
            'columns': self.screen.columns,
            "text": self.text, 
            'attributes': self.attributes.copy(),
            'screen': 'pty',
            'screenUpdateTime': time.time(),
        }.copy()

class driver(screenDriver):
    def __init__(self):
        screenDriver.__init__(self)
        self.signalPipe = os.pipe()
        self.p_out = None
        self.terminal = None
        self.p_pid = -1
        signal.signal(signal.SIGWINCH, self.handleSigwinch)
    def initialize(self, environment):
        self.env = environment
        self.command = self.env['runtime']['settingsManager'].getSetting('general','shell')
        self.shortcutType = self.env['runtime']['inputManager'].getShortcutType()
        self.env['runtime']['processManager'].addCustomEventThread(self.terminalEmulation)
    def getCurrScreen(self):
        self.env['screen']['oldTTY'] = 'pty'
        self.env['screen']['newTTY'] = 'pty'
 
    def injectTextToScreen(self, msgBytes, screen = None):
        if not screen:
            screen = self.p_out.fileno()
        if isinstance(msgBytes, str):
            msgBytes = bytes(msgBytes, 'UTF-8')
        os.write(screen, msgBytes)

    def getSessionInformation(self):
        self.env['screen']['autoIgnoreScreens'] = []
        self.env['general']['prevUser'] = getpass.getuser()
        self.env['general']['currUser'] = getpass.getuser()
    def readAll(self, fd, timeout = 0.3, interruptFd = None, len = 65536):
        msgBytes = b'' 
        fdList = []
        fdList += [fd]
        if interruptFd:
            fdList += [interruptFd]
        starttime = time.time()
        while True:
            r = screen_utils.hasMoreWhat(fdList, 0.0001)
            # nothing more to read
            if not fd in r:
                break
            data = os.read(fd, len)
            if data == b'':
                raise EOFError
            msgBytes += data
            # exit on interrupt available
            if interruptFd in r:
                break
            # respect timeout but wait a little bit of time to see if something more is here
            if (time.time() - starttime) >= timeout:
                break
        return msgBytes
    def openTerminal(self, columns, lines, command):
        p_pid, master_fd = pty.fork()
        if p_pid == 0:  # Child.
            argv = shlex.split(command)
            env = os.environ.copy()
            #values are VT100,xterm-256color,linux
            try: 
                if env["TERM"] == '':
                    env["TERM"] = 'linux'
            except:
                env["TERM"] = 'linux'
            os.execvpe(argv[0], argv, env)
        # File-like object for I/O with the child process aka command.
        p_out = os.fdopen(master_fd, "w+b", 0)
        return Terminal(columns, lines, p_out), p_pid, p_out
    def resizeTerminal(self,fd):
        s = struct.pack('HHHH', 0, 0, 0, 0)
        s = fcntl.ioctl(0, termios.TIOCGWINSZ, s)
        fcntl.ioctl(fd, termios.TIOCSWINSZ, s)
        lines, columns, _, _ = struct.unpack('hhhh', s)
        return lines, columns
    def getTerminalSize(self, fd):
        s = struct.pack('HHHH', 0, 0, 0, 0)
        lines, columns, _, _ = struct.unpack('HHHH', fcntl.ioctl(fd, termios.TIOCGWINSZ, s))
        return lines, columns
    def handleSigwinch(self, *args):
        os.write(self.signalPipe[1], b'w')
    def terminalEmulation(self,active , eventQueue):
        try:
            old_attr = termios.tcgetattr(sys.stdin)
            tty.setraw(0)
            lines, columns = self.getTerminalSize(0)
            if self.command == '':
                self.command = screen_utils.getShell()
            self.terminal, self.p_pid, self.p_out = self.openTerminal(columns, lines, self.command)
            lines, columns = self.resizeTerminal(self.p_out)
            self.terminal.resize(lines, columns)
            fdList = [sys.stdin, self.p_out, self.signalPipe[0]]
            while active.value:
                r, _, _ = select(fdList, [], [], 1)
                # none
                if r == []:
                    continue
                # signals
                if self.signalPipe[0] in r:
                    os.read(self.signalPipe[0], 1)
                    lines, columns = self.resizeTerminal(self.p_out)
                    self.terminal.resize(lines, columns)
                # input
                if sys.stdin in r:
                    try:
                        msgBytes = self.readAll(sys.stdin.fileno(), len=4096)
                    except (EOFError, OSError):
                        eventQueue.put({"Type":fenrirEventType.StopMainLoop,"Data":None}) 
                        break
                    if self.shortcutType == 'KEY':
                        try:
                            self.injectTextToScreen(msgBytes)
                        except:
                            eventQueue.put({"Type":fenrirEventType.StopMainLoop,"Data":None}) 
                            break
                    else:
                        eventQueue.put({"Type":fenrirEventType.ByteInput,
                            "Data":msgBytes })
                # output
                if self.p_out in r:
                    try:
                        msgBytes = self.readAll(self.p_out.fileno(), interruptFd=sys.stdin.fileno())
                    except (EOFError, OSError):
                        eventQueue.put({"Type":fenrirEventType.StopMainLoop,"Data":None}) 
                        break
                    # feed and send event bevore write, the pyte already has the right state
                    # so fenrir already can progress bevore os.write what should give some better reaction time
                    self.terminal.feed(msgBytes)
                    eventQueue.put({"Type":fenrirEventType.ScreenUpdate,
                        "Data":screen_utils.createScreenEventData(self.terminal.GetScreenContent())
                    })
                    self.injectTextToScreen(msgBytes, screen=sys.stdout.fileno())
        except Exception as e:  # Process died?
            print(e)
            eventQueue.put({"Type":fenrirEventType.StopMainLoop,"Data":None}) 
        finally:
            os.kill(self.p_pid, signal.SIGTERM)
            self.p_out.close()
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)
            eventQueue.put({"Type":fenrirEventType.StopMainLoop,"Data":None}) 
            sys.exit(0)
         
    def getCurrApplication(self):
        pass
