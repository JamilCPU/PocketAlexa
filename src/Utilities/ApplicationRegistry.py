import subprocess
import os
import json


class ApplicationRegistry:
    def __init__(self):
        self.apps = []
        currentDirectory = os.path.dirname(os.path.abspath(__file__))
        self.cacheFilePath = os.path.join(currentDirectory, "..", "applications_cache.json")
        self.cacheFilePath = os.path.abspath(self.cacheFilePath)
        self.detectInstalledApplications()

    def detectInstalledApplications(self):
        if os.path.exists(self.cacheFilePath):
            self.loadApplicationsFromFile(self.cacheFilePath)
        else:
            self.runPowerShellDetection()
    
    def loadApplicationsFromFile(self, filePath):
        """Load applications from cached JSON file"""
        try:
            with open(filePath, 'r', encoding='utf-8') as f:
                self.apps = json.load(f)
            print(f"Loaded {len(self.apps)} applications from cache")
        except Exception as e:
            print(f"Error loading applications from cache: {e}")
            print("Falling back to PowerShell detection...")
            self.runPowerShellDetection()
    
    def saveApplicationsToFile(self, filePath=None):
        """Save applications to JSON cache file"""
        if filePath is None:
            filePath = self.cacheFilePath
        try:
            with open(filePath, 'w', encoding='utf-8') as f:
                json.dump(self.apps, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(self.apps)} applications to cache")
        except Exception as e:
            print(f"Error saving applications to cache: {e}")
    
    def runPowerShellDetection(self):
        """Run PowerShell script to detect applications and save to cache"""
        currentDirectory = os.path.dirname(os.path.abspath(__file__))
        scriptPath = os.path.join(
            currentDirectory, "..", "Scripts", "DetectApplications.ps1"
        )
        scriptPath = os.path.abspath(scriptPath)
        print("detecting applications")
        response = subprocess.run(
            ["powershell.exe", scriptPath], capture_output=True, text=True
        )
        if response:
            self.recordInstalledApplications(response.stdout)
            self.saveApplicationsToFile()
        else:
            print("failed to detect installed applications..?")

    def recordInstalledApplications(self, powershellResponse):
        print('recording installed apps')
        lines = powershellResponse.strip().split("\n")
        
        # Parse list format: "Property : Value" with empty lines between entries
        # Format: DisplayName : App Name
        #         Executable  : C:\Path\To\App.exe
        current_app = {}
        for line in lines:
            line = line.strip()
            
            # Skip empty lines - they separate app entries
            if not line:
                # Empty line means we should finalize current app if we have both properties
                if current_app and 'DisplayName' in current_app and 'Executable' in current_app:
                    # Remove quotes from path if present
                    path = current_app['Executable'].strip('"')
                    self.apps.append([current_app['DisplayName'], path])
                current_app = {}
                continue
            
            # Parse "Property : Value" format
            if ' : ' in line:
                parts = line.split(' : ', 1)
                if len(parts) == 2:
                    prop_name = parts[0].strip()
                    prop_value = parts[1].strip()
                    current_app[prop_name] = prop_value
        
        # Handle last app if no trailing empty line
        if current_app and 'DisplayName' in current_app and 'Executable' in current_app:
            path = current_app['Executable'].strip('"')
            self.apps.append([current_app['DisplayName'], path])
        print(self.apps)
        print(f"Loaded {len(self.apps)} applications")