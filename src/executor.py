import pyautogui
import ctypes
import pycaw
import time
import os
import subprocess

class Executor:    
    def executeCommand(self, execution):
        commands = {
        'lock screen' : self.lockScreen,
        'play media' : self.playPauseMedia,
        'pause media' : self.playPauseMedia}
    
        executionCmd = execution['command']

        if "open " in executionCmd:
            return self.openApplicationByName(execution)

        if executionCmd not in commands:
            return "EXECUTION ERROR: 404 Command Not Found: '", executionCmd, "'"

        print("Executing command... '", executionCmd, "'")
        
        print('EXECUTING STANDARD COMMAND')
        return commands[executionCmd]()

    def openApplicationByName(self, execution):
        print(execution)
        application = execution['command'][5:]
        path = execution['path']
        print(path)
        print(application)
        if not path:
            return "ERROR: Application Path not Listed"
        os.startfile(path)
        return "SUCCESS: Opened " + application
    
    def lockScreen(self):
        ctypes.windll.user32.LockWorkStation()
        return 'SUCCESS: Screen Locked'

    def playPauseMedia(self):
        time.sleep(1.5)
        pyautogui.press('space')
        return 'SUCCESS: Playing/Pausing Active Media'