import subprocess
import os

class ApplicationRegistry:
    def __init__(self):
        self.apps = []
        self.detectInstalledApplications()

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
            filteredResponse = powershellResponse.strip()
            lines = powershellResponse.split('\n')

            for line in lines:
                if line.strip():
                    parts = [part for part in line.split('  ') if part.strip()]
                    self.apps.append(parts[0])