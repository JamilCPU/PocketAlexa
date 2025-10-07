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
        'play media' : self.playPauseMedia,
        'pause media' : self.playPauseMedia}
        if command not in commands:
            return "EXECUTION ERROR\n 404 Not Found: '", command, "'"

        print("Executing command... '", command, "'")
        resp = commands[command]()
        return resp

    def openNotepad(self):
        subprocess.Popen('notepad')
        return "SUCCESS: Opened Notepad"
    
    def lockScreen(self):
        ctypes.windll.user32.LockWorkStation()
        return 'SUCCESS: Screen Locked'

    def playPauseMedia(self):
        time.sleep(1.5)
        pyautogui.press('space')
        return 'SUCCESS: Playing/Pausing Active Media'