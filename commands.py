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
