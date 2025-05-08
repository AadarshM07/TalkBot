import sys
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

class SpeechRecognizer:
    def __init__(self, model_path="vosk-model-small-en-in-0.4", samplerate=16000):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, samplerate)
        self.q = queue.Queue()

    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def listen(self):
        print("🎤 Speak now...")
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=self.callback):
            while True:
                data = self.q.get()
                if self.recognizer.AcceptWaveform(data):
                    return json.loads(self.recognizer.Result())["text"]


