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
        print('llmcorrect')
        try:
            # Generate response using optimized model
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
            
            return correctedCommand
            
        except Exception as e:
            print(f"LLM correction failed: {e}")
            return self._fallbackCorrect(originalCommand)
    
    def _extractCommandFromResponse(self, response, originalCommand):
        """Extract the corrected command from LLM response"""
        # Look for the corrected command in the response
        availableCommands = self.commandRegistry.getAvailableCommands()
        
        # Check if any available command appears in the response
        for cmd in availableCommands:
            if cmd.lower() in response.lower():
                # If it's an "open" command, validate against detected applications
                if cmd.startswith('open') and '<application_name>' in cmd:
                    return self._validateOpenCommand(response, originalCommand)
                return cmd
        
        # If no match found, return original command
        return originalCommand
    
    def _validateOpenCommand(self, response, originalCommand):
        """Validate and construct open command with detected application name"""
        # Get detected application names
        appNames = [app[0] for app in self.appRegistry.apps]  # app[0] is the application name
        
        # Look for application names in the response
        for appName in appNames:
            if appName.lower() in response.lower():
                return f"open {appName.lower()}"
        
        # If no specific app found, return generic open command
        return "open <application_name>"
    
    def _fallbackCorrect(self, command):
        """Fallback rule-based correction when LLM is not available"""
        commandLower = command.lower()
        availableCommands = self.commandRegistry.getAvailableCommands()
        
        # Check for open commands with application names
        if any(word in commandLower for word in ['open', 'launch', 'start', 'run']):
            # Look for specific application names
            appNames = [app[0].lower() for app in self.appRegistry.apps]
            for appName in appNames:
                if appName in commandLower:
                    return f'open {appName}'
            
            # Fallback to generic application commands
            if any(word in commandLower for word in ['notepad', 'text', 'editor']):
                return 'open notepad'
            elif any(word in commandLower for word in ['calculator', 'calc']):
                return 'open calculator'
            elif any(word in commandLower for word in ['browser', 'chrome', 'firefox', 'edge']):
                return 'open browser'
            else:
                return 'open <application_name>'
        
        # Other command types
        elif any(word in commandLower for word in ['lock', 'screen', 'secure']):
            return 'lock screen'
        elif any(word in commandLower for word in ['play', 'music', 'video', 'resume']):
            return 'play media'
        elif any(word in commandLower for word in ['pause', 'stop', 'halt']):
            return 'pause media'
        
        return command
    
