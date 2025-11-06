from CommandRegistry import CommandRegistry
from Utilities.ModelOptimizer import ModelOptimizer
from Utilities.ApplicationRegistry import ApplicationRegistry

import os

class Autocorrect:
    #responsible for taking the interpreted speech and autocorrecting it into


    def __init__(self, commandRegistry=None):
        self.appRegistry = ApplicationRegistry()
        if commandRegistry:
            self.commandRegistry = commandRegistry
        else:
            self.commandRegistry = CommandRegistry()
        
        # Initialize optimized LLM for autocorrect
        self.modelOptimizer = ModelOptimizer()
        self._loadModel()
        self.prompt = self.setupPrompt()

    def _loadModel(self):
        """Load an optimized small LLM for autocorrect functionality"""
        success = self.modelOptimizer.loadOptimizedModel()
        if not success:
            print("Falling back to rule-based autocorrect")

    def setupPrompt(self):
        try:
            with open('Utilities/AutocorrectPrompt.txt', 'r') as file:
                promptTemplate = file.read()
        except FileNotFoundError:
            print("AutocorrectPrompt.txt not found, using fallback")
            return ""
            
        apps = ""
        for i in range(2, len(self.appRegistry.apps)):
            apps += self.appRegistry.apps[i][0] + '|'

        promptTemplate = promptTemplate.replace("{detected_apps}", apps)
        return promptTemplate

    def correctCommand(self, command):
        print('given command: ', command)
        promptWithCmd = self.prompt.replace("{user_input}", command)
        if self.modelOptimizer.model is not None:
            return self._llmCorrect(promptWithCmd, command)
        else:
            return self._fallbackCorrect(command)
    
    def _llmCorrect(self, prompt, originalCommand):
        """Use optimized LLM to correct the command"""
        print(prompt)
        try:
            response = self.modelOptimizer.generateOptimized(
                prompt, 
                maxTokens=50, 
                temperature=0.1
            )
            
            if response is None:
                return self._fallbackCorrect(originalCommand)
            print('llm response:')
            print(response)
            # Extract the corrected command from the response
            correctedCommand = self._extractCommandFromResponse(response, originalCommand)
            print('corrected command:')
            print(correctedCommand)
            return correctedCommand
            
        except Exception as e:
            print(f"LLM correction failed: {e}")
            return self._fallbackCorrect(originalCommand)
    
    def _extractCommandFromResponse(self, response, originalCommand):
        """Extract the corrected command from LLM response"""
        availableCommands = self.commandRegistry.getAvailableCommands()
        
        # Check if any available command appears in the response
        for cmd in availableCommands:
            if cmd.lower() in response.lower():
                # If it's an "open" command, validate against detected applications
                if cmd.startswith('open') and '<application_name>' in cmd:
                    print('ran open validate cmd')
                    return self._validateOpenCommand(response, originalCommand)
                return {"command": cmd}
        
        # If no match found, return original command
        return {"command": originalCommand}
    
    def _findAppInCommand(self, searchText, debug=False):
        """Find matching application in the given text and return command dict"""
        searchTextLower = searchText.lower()
        for app in self.appRegistry.apps:
            appName = app[0].lower()
            if debug:
                print('checking ', appName)
            if appName in searchTextLower:
                if debug:
                    print("Command Validated Succesfully")
                resp = {
                    "command": f"open {appName}",
                    "path": app[1]
                }
                if debug:
                    print(resp)
                return resp
        return None

    def _validateOpenCommand(self, response, originalCommand):
        """Validate and construct open command with detected application name"""
        # Get detected application names
        print('originalCommand: ', originalCommand)
        openCmd = originalCommand[5:]
        
        # Look for application names in the command
        result = self._findAppInCommand(openCmd, debug=True)
        if result:
            return result
        
        return {"command": "ERROR validating open command"}
    
    def _fallbackCorrect(self, command):
        """Fallback rule-based correction when LLM is not available"""
        commandLower = command.lower()
        availableCommands = self.commandRegistry.getAvailableCommands()
        
        # Check for open commands with application names
        if any(word in commandLower for word in ['open', 'launch', 'start', 'run']):
            result = self._findAppInCommand(commandLower)
            if result:
                return result
            
            if any(word in commandLower for word in ['notepad', 'text', 'editor']):
                return {"command": 'open notepad'}
            elif any(word in commandLower for word in ['calculator', 'calc']):
                return {"command": 'open calculator'}
            elif any(word in commandLower for word in ['browser', 'chrome', 'firefox', 'edge']):
                return {"command": 'open browser'}
            else:
                return {"command": 'open <application_name>'}
        
        # Other command types
        elif any(word in commandLower for word in ['lock', 'screen', 'secure']):
            return {"command": 'lock screen'}
        elif any(word in commandLower for word in ['play', 'music', 'video', 'resume']):
            return {"command": 'play media'}
        elif any(word in commandLower for word in ['pause', 'stop', 'halt']):
            return {"command": 'pause media'}
        
        return {"command": command}
    
