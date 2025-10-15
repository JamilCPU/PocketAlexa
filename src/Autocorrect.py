from CommandRegistry import CommandRegistry

class Autocorrect:
    #responsible for taking the interpreted speech and autocorrecting it into

    def __init__(self, commandRegistry=None):
        if commandRegistry:
            self.commandRegistry = commandRegistry
        else:
            self.commandRegistry = CommandRegistry()

    def correctCommand(self, command):
        correctedCommand = command
        ##call the ai model and prompt it
        ##the model needs context of the command's functionality
        #to that end, perhaps autocorrect should import executor?
