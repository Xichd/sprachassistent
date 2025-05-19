
import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
import config
from speech_synthesis import sprich

q = queue.Queue()

model = Model(config.MODEL_PATH_VOSK)
rec = KaldiRecognizer(model, config.SAMPLERATE)

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def erkenne_sprachbefehl():
    with sd.RawInputStream(samplerate=config.SAMPLERATE, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("🎙️ Ich höre... Sag etwas.")
        sprich("Ich höre. Sag etwas.")

        audio_data = b""
        timeout = 4

        while True:
            try:
                data = q.get(timeout=timeout)
                audio_data += data
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result["text"]
                    print("📢 Du hast gesagt:", text)
                    return text
            except queue.Empty:
                print("⏳ Keine Sprache erkannt – Timeout.")
                sprich("Ich habe nichts verstanden.")
                return ""

