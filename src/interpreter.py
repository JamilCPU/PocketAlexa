import os
import json
from vosk import Model, KaldiRecognizer
class Interpreter:
    def __init__(self):
        voskModel = os.path.join("../models/vosk-model-small-en-us-0.15")
        self.vosk = Model(voskModel)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.recognizer.SetWords(true)

    def parseSpeech(speechFromClient):
        try:
            if self.recognizer.AcceptWaveform(audio_data):
                result = json.loads(self.recognizer.Result())
                return result.get('text', '').strip()
            else:
                partial_result = json.loads(self.recognizer.PartialResult())
                return partial_result.get('partial', '').strip()
                
        except Exception as e:
            return f"ERROR: Speech processing failed - {str(e)}"
