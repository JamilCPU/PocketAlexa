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
             
        if "open " in command:
            return self.openApplicationByName(command)

        if command not in commands:
            return "EXECUTION ERROR: 404 Command Not Found: '", command, "'"

        print("Executing command... '", command, "'")
        
        print('EXECUTING STANDARD COMMAND')
        return commands[command]()

    def openApplicationByName(self, command):
        print(command)
        application = command[5:]
        print(application)
        subprocess.Popen(application)
        return "SUCCESS: Opened " + application

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