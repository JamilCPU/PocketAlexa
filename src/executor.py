import pyautogui
import ctypes

class Executor:
    commands = {'open Notepad' : '',
                'lock screen' : '',
                'play media' : '',
                'pause media' : '',}

    def validateCommand(command):
        return True
    
    def executeCommand(command):
        resp = commands[command]

    def openNotepad(self):
        return ""
    
    def lockScreen(self):
        ctypes.windll.user32.LockWorkStation()
        print('Screen Lock Attempted')
    def playMedia(self):
        return ""

    def pauseMedia(self):
        return ""

    
execute = Executor()
execute.lockScreen()