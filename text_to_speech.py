from gtts import gTTS
import os

text = "Hello, Sunil! How's your AI project going?"
tts = gTTS(text=text, lang='en')
tts.save("output.mp3")
os.system("afplay output.mp3")  # or use another media player
