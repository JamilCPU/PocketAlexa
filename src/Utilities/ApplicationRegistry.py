import subprocess
import os


class ApplicationRegistry:
    def __init__(self):
        self.apps = []
        self.detectInstalledApplications()

    def detectInstalledApplications(self):
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