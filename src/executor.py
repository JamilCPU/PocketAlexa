import pyautogui
import ctypes
import pycaw
import time

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
        import os
        os.system('notepad')
        print('Notepad opened')
    
    def lockScreen(self):
        ctypes.windll.user32.LockWorkStation()
        print('Screen Lock Attempted')
    def playMedia(self):

        pyautogui.press('space')
        print('Playing active media')

    def pauseMedia(self):
        pyautogui.press('space')
        print('Pausing active media')

    
execute = Executor()
#execute.lockScreen()
execute.openNotepad()