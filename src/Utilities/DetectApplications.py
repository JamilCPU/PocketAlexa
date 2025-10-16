import subprocess

class DetectApplications:
    def detectInstalledApplications():
        response = subprocess.Popen(
            ["powershell.exe", "../Scripts/DetectApplications.ps1"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

    def recordInstalledApplications():
