from CommandRegistry import CommandRegistry

class Autocorrect:
    #responsible for taking the interpreted speech and autocorrecting it into

    def __init__(self, commandRegistry=None):
        if commandRegistry:
            self.commandRegistry = commandRegistry
        else:
            self.commandRegistry = CommandRegistry()

    def correctCommand(self, command):
        prompt = ""
        with open('Utilities/AutocorrectPrompt.txt', 'r') as file:
            prompt = file.read()
        prompt = prompt + command
        
        #make call to ai model with prmopt
        
        #validate returned value and return back to the server
       
    
