import pyautogui
import ctypes
import pycaw
import time
import os
import subprocess

class Executor:    
    def executeCommand(self, command):
        commands = {'open notepad' : self.openNotepad,
        'lock screen' : self.lockScreen,
        'play media' : self.playMedia,
        'pause media' : self.pauseMedia}
        if command not in commands:
            return "EXECUTION ERROR\n 404 Not Found: '", command, "'"

        print('Executing command... ', command)
        resp = commands[command]()
        print(resp)
        return resp

    def openNotepad(self):
        subprocess.Popen('notepad')
        print('notepad opened... returning statement')
        return "Opened notepad"
    
    def lockScreen(self):
        ctypes.windll.user32.LockWorkStation()
        return 'Screen Lock Attempted'
    def playMedia(self):
        time.sleep(1.5)
        pyautogui.press('space')
        return 'Playing active media'

    def pauseMedia(self):
        time.sleep(1.5)
        pyautogui.press('space')
        return 'Pausing active media'
