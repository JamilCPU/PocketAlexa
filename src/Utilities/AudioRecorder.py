import pyaudio
import threading
import time

class AudioRecorder:
    """
    Audio recording class for capturing speech from microphone
    and converting it to bytes format for transmission
    """
    
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.recording = False
        self.audio_data = []
        self.recording_thread = None
        
        # Audio configuration (matching Vosk requirements)
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
    
    def start_recording(self):
        """Start recording audio from microphone"""
        if self.recording:
            print("Already recording!")
            return
            
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        self.recording = True
        self.audio_data = []
        
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.start()
        print("Recording started... Speak now!")
    
    def _record_audio(self):
        """Internal method to continuously record audio"""
        while self.recording:
            try:
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                self.audio_data.append(data)
            except Exception as e:
                print(f"Recording error: {e}")
                break
    
    def stop_recording(self):
        if not self.recording:
            print("Not currently recording!")
            return b''
            
        self.recording = False
        
        if self.recording_thread:
            self.recording_thread.join()
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        
        audio_bytes = b''.join(self.audio_data)
        print(f"Recording stopped. Captured {len(audio_bytes)} bytes of audio.")
        return audio_bytes
    
    def is_recording(self):
        """Check if currently recording"""
        return self.recording
    
    def get_audio_info(self):
        """Get audio configuration info"""
        return {
            'chunk_size': self.CHUNK,
            'format': self.FORMAT,
            'channels': self.CHANNELS,
            'rate': self.RATE
        }
    
    def cleanup(self):
        """Clean up audio resources"""
        if self.recording:
            self.stop_recording()
        
        if self.stream:
            self.stream.close()
            self.stream = None
            
        if self.audio:
            self.audio.terminate()
            self.audio = None
        
        print("Audio resources cleaned up.")
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        self.cleanup()