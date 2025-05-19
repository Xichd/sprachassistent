import os
import zipfile

project_files = {
    "main.py": '''\
from config import MODEL_PATH_LLAMA, MODEL_FILE_LLAMA
from llama_model import frage_llama
from speech_recognition import erkenne_sprachbefehl
from speech_synthesis import sprich
from commands import verarbeite_befehl

while True:
    befehl = erkenne_sprachbefehl()

    if befehl == "":
        continue

    if "ende" in befehl:
        sprich("Ich beende mich. Tschüss.")
        break

    verarbeite_befehl(befehl)
''',

    "config.py": '''\
MODEL_PATH_VOSK = "models/vosk-model-small-de-0.15"
MODEL_PATH_LLAMA = "models"
MODEL_FILE_LLAMA = "TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"
SAMPLERATE = 16000
''',

    "llama_model.py": '''\
from ctransformers import AutoModelForCausalLM
import config

llama = AutoModelForCausalLM.from_pretrained(
    config.MODEL_PATH_LLAMA,
    model_file=config.MODEL_FILE_LLAMA,
    model_type="llama",
    gpu_layers=0  # wichtig für Raspberry Pi
)

def frage_llama(frage):
    print("💭 TinyLLaMA denkt nach...")
    prompt = f"User: {frage}\\nAssistant:"
    antwort = llama(prompt, max_new_tokens=100)
    antwort = antwort.strip().split("User:")[0].strip()
    print("🦙 TinyLLaMA sagt:", antwort)
    return antwort
''',

    "speech_recognition.py": '''\
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
''',

    "speech_synthesis.py": '''\
import pyttsx3

def sprich(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
''',

    "commands.py": '''\
from speech_synthesis import sprich
from llama_model import frage_llama

def verarbeite_befehl(befehl):
    if any(phrase in befehl for phrase in ["was ist", "erklär", "erkläre", "wer ist", "was bedeutet"]):
        antwort = frage_llama(befehl)
        sprich(antwort)

    elif "vorwärts" in befehl:
        sprich("Ich fahre vorwärts.")

    elif "stop" in befehl:
        sprich("Ich bleibe stehen.")

    elif "links" in befehl:
        sprich("Ich drehe mich nach links.")

    elif "rechts" in befehl:
        sprich("Ich drehe mich nach rechts.")

    else:
        sprich("Diesen Befehl kenne ich leider nicht.")
''',

    "install.sh": '''\
#!/bin/bash

# Sprachassistent Setup-Skript für Raspberry Pi

echo "🔧 Starte Installation..."

# Systempakete aktualisieren
sudo apt update && sudo apt upgrade -y

# Abhängigkeiten installieren
echo "📦 Installiere Abhängigkeiten..."
sudo apt install -y python3-pip python3-venv portaudio19-dev espeak unzip wget

# Projektverzeichnis vorbereiten
mkdir -p ~/sprachassistent/models
cd ~/sprachassistent || exit

# Virtuelle Umgebung erstellen
python3 -m venv venv
source venv/bin/activate

# Python-Pakete installieren
pip install --upgrade pip
pip install sounddevice vosk pyttsx3 ctransformers

# Vosk-Modell herunterladen
cd models || exit
wget -q https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip
unzip vosk-model-small-de-0.15.zip && rm vosk-model-small-de-0.15.zip

# Hinweis zu LLaMA-Modell
echo "📁 Bitte kopiere dein TinyLLaMA GGUF-Modell in das models/ Verzeichnis."
echo "🟡 Name z.B.: TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"

echo "✅ Installation abgeschlossen. Starte mit:"
echo "    cd ~/sprachassistent && source venv/bin/activate && python main.py"
''',

    "README.md": '''\
# 🗣️ Sprachassistent für Raspberry Pi

Ein offlinefähiger Sprachassistent mit Spracheingabe (Vosk), Sprachausgabe (pyttsx3) und TinyLLaMA als KI-Modell.

## 🔧 Voraussetzungen
- Raspberry Pi 4 oder 5
- Mikrofon (USB)
- Lautsprecher

## 📦 Installation

```bash
git clone <dieses-repo> sprachassistent
cd sprachassistent
chmod +x install.sh
./install.sh
