import subprocess
import os

class ApplicationRegistry:
    def __init__(self):
        self.apps = []

    def detectInstalledApplications(self):
        currentDirectory = os.path.dirname(os.path.abspath(__file__))
        scriptPath = os.path.join(currentDirectory, '..', 'Scripts', 'DetectApplications.ps1')
        scriptPath = os.path.abspath(scriptPath)
        print('detecting applications')
        response = subprocess.run(
            ["powershell.exe", scriptPath],
            capture_output=True,
            text=True
        )
        if response:            
            self.recordInstalledApplications(response.stdout)
        else:
            print('failed to detect installed applications..?')

    def recordInstalledApplications(self, powershellResponse):
            print('stripped')
            #print(powershellResponse.strip())
            filteredResponse = powershellResponse.strip()
            filteredResponse = powershellResponse.split('\n')
            print(filteredResponse)


            #self.apps.append(appInfo[0])#Add the application name to our list of apps