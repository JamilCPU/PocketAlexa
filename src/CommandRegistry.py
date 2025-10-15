class CommandRegistry:
    def __init__(self):
        self.commands = {
            'open <application_name>' : 'Opens any given application',
            'lock screen' : 'Locks the computer screen'
            'play media' : 'Plays or resumes media',
            'pause media' : 'Pauses media'
        }

    def getAvailableCommands(self):
        return list(self.commands.keys())