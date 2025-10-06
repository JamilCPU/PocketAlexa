import pyautogui
import ctypes
import pycaw
import time
import os

class Executor:    
    def executeCommand(self, command):
        commands = {'open notepad' : self.openNotepad,
        'lock screen' : self.lockScreen,
        'play media' : self.playMedia,
        'pause media' : self.pauseMedia}
        if command not in commands:
            return "CRITICAL FAILURE"

        print('Executing command... ', command)
        resp = commands[command]()

    def openNotepad(self):
        os.system('notepad')
        return 'Notepad opened'
    
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
