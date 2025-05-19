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

