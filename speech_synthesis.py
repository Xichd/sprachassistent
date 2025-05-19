import pyttsx3

def sprich(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
