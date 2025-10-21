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

    def _loadModel(self):
        """Load an optimized small LLM for autocorrect functionality"""
        success = self.modelOptimizer.loadOptimizedModel()
        if not success:
            print("Falling back to rule-based autocorrect")

    def correctCommand(self, command):
        # Read the prompt template
        try:
            with open('Utilities/AutocorrectPrompt.txt', 'r') as file:
                prompt_template = file.read()
        except FileNotFoundError:
            print("AutocorrectPrompt.txt not found, using fallback")
            return self._fallbackCorrect(command)
        
        # Replace the placeholder with the actual command
        full_prompt = prompt_template.replace("{user_input}", command)
        
        if self.modelOptimizer.model is not None:
            return self._llmCorrect(full_prompt, command)
        else:
            return self._fallbackCorrect(command)
    
    def _llmCorrect(self, prompt, originalCommand):
        """Use optimized LLM to correct the command"""
        try:
            # Generate response using optimized model
            response = self.modelOptimizer.generateOptimized(
                prompt, 
                maxTokens=50, 
                temperature=0.1
            )
            
            if response is None:
                return self._fallbackCorrect(originalCommand)
            
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
                return cmd
        
        # If no match found, return original command
        return originalCommand
    
    def _fallbackCorrect(self, command):
        """Fallback rule-based correction when LLM is not available"""
        commandLower = command.lower()
        availableCommands = self.commandRegistry.getAvailableCommands()
        
        # Simple keyword matching
        if any(word in commandLower for word in ['notepad', 'text', 'editor']):
            return 'open notepad'
        elif any(word in commandLower for word in ['lock', 'screen', 'secure']):
            return 'lock screen'
        elif any(word in commandLower for word in ['play', 'music', 'video', 'resume']):
            return 'play media'
        elif any(word in commandLower for word in ['pause', 'stop', 'halt']):
            return 'pause media'
        
        return command
    
