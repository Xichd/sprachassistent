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

