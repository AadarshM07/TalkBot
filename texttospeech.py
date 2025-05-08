import os
import subprocess
import pygame
import time

class TextToSpeech:
    def __init__(self):
        self.piper_path = "./piper/piper"
        self.model_path = "./piper/voices/en_US-hfc_female-medium.onnx"
        self.output_file = "./piper/output.wav"
        
    
        pygame.mixer.init()

    def speak(self, text):
        command = [
            self.piper_path,
            "--model", self.model_path,
            "--output_file", self.output_file
        ]
        
        try:
            subprocess.run(
                command,
                input=text,
                text=True,
                check=True,
                timeout=10  
            )
            
            self._play_audio()
            
        except subprocess.CalledProcessError as e:
            print("Error running Piper:", e)
        except subprocess.TimeoutExpired:
            print("Piper TTS timed out.")
        except Exception as e:
            print("Unexpected error:", e)

    def _play_audio(self):
        try:
            pygame.mixer.music.load(self.output_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        except Exception as e:
            print("Pygame playback error:", e)
        finally:
            pygame.mixer.music.stop()

    def __del__(self):
        """Clean up Pygame when done."""
        pygame.mixer.quit()