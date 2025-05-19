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
```

## 🧠 Modelle

- **Vosk (STT):** Wird automatisch heruntergeladen (`vosk-model-small-de-0.15`)
- **LLaMA (LLM):** GGUF-Modell muss manuell ins `models/`-Verzeichnis kopiert werden
  - Empfohlen: `TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf`

## ▶️ Starten
```bash
cd ~/sprachassistent
source venv/bin/activate
python main.py
```

## 📁 Projektstruktur
```
sprachassistent/
├── main.py
├── config.py
├── llama_model.py
├── speech_recognition.py
├── speech_synthesis.py
├── commands.py
├── install.sh
├── README.md
└── models/
```

## 🚀 Autostart (optional)
Füge in `crontab` folgendes hinzu:
```bash
crontab -e
```
Dann z. B.:
```bash
@reboot /home/pi/sprachassistent/venv/bin/python /home/pi/sprachassistent/main.py
```

## ✅ Sprachbefehle
- "vorwärts"
- "stop"
- "links"
- "rechts"
- "ende"
- Wissensfragen (an LLaMA)

---

Für Fragen: [Deine Kontaktinfo hier]

