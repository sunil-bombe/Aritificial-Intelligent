import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
print(voices)
engine.setProperty('voice', voices[1])  # Choose the second voice (usually female)
engine.setProperty('rate', 150)  # Adjust speed (Lower value = slower speech)
engine.say("Hello, Sunil! How are you?")
engine.runAndWait()
