import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import requests  # Import requests for API calls

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

def deepseek_query(stext):
    """Fetches AI-generated response using DeepSeek API"""
  #  url = "https://api.deepseek.com"
    url = "https://api.deepseek.com/chat/completions"  # Replace with the actual DeepSeek API endpoint
    headers = {
        "Authorization": "Bearer ",  # Replace with your DeepSeek API key
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",  # Replace with the appropriate model name
        "messages": [{"role": "user", "content": stext}],
        "temperature": 0.7,
        "max_tokens": 256
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        print(f"DeepSeek Response: {reply}")
        return reply
    except requests.exceptions.RequestException as e:
        print(f"DeepSeek API error: {e}")
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
            response = deepseek_query(query)
            speak(response)