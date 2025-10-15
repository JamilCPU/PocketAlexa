class Autocorrect:
    #responsible for taking the interpreted speech and autocorrecting it into

    def correctCommand(self, command, executor):
        correctedCommand = command
        ##call the ai model and prompt it
        ##the model needs context of the command's functionality
        #to that end, perhaps autocorrect should import executor?
