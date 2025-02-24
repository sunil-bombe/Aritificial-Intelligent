import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
from openai import OpenAI

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Ensure there are voices available
if voices:
    engine.setProperty('voice', voices[1])  # Choose the second voice (usually female)
    engine.setProperty('rate', 150)  # Adjust speed (Lower value = slower speech)
else:
    print("No voices found! Using the default voice.")

def speak(audio):
    """Converts text to speech"""
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Greets the user based on the time of day"""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Boss")
    elif 12 <= hour < 18:
        speak("Good Afternoon Boss")
    else:
        speak("Good Evening Boss")

def takeCommand():
    """Takes voice input from the microphone and converts it to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  # Adjust pause threshold
        try:
            audio = r.listen(source, timeout=5)  # Add timeout to prevent indefinite listening
            print("Recognizing...")
            query = r.recognize_google(audio)
            print(f"User said: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            print("Could not understand audio, please try again.")
            return "Could not understand audio"
        except sr.RequestError:
            print("Could not request results, check your internet connection.")
            return "Could not request results"
        except Exception as e:
            print(f"Error: {e}")
            return "Error occurred"

def gpt3(stext):
    """Fetches AI-generated response using DeepSeek API"""
    client = OpenAI(api_key="Bearer ", base_url="https://api.deepseek.com")

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": stext},
            ],
            stream=False
        )
        reply = response.choices[0].message.content.strip()
        print(f"AI Response: {reply}")
        return reply
    except Exception as e:
        print(f"API error: {e}")
        return "Sorry, I couldn't process that request."

if __name__ == "__main__":
    wishMe()
    speak("I am Jarvis. How may I help you?")

    while True:
        query = takeCommand()
        if "exit" in query or "quit" in query:
            speak("Goodbye! Have a great day.")
            break
        elif query:
            response = gpt3(query)
            speak(response)
