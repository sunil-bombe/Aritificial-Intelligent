import speech_recognition as sr
import pyautogui
import pyttsx3
import webbrowser
import requests
from googlesearch import search
from bs4 import BeautifulSoup


engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Adjust speed
engine.setProperty("voice", engine.getProperty("voices")[2].id)  # Change voice if needed

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for 'Hey Jarvis'...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
            return command
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            speak("Sorry, I couldn't connect to the recognition service.")
            return None

def fetch_google_answer(query):
    try:
        search_results = list(search(query, num_results=1))
        if search_results:
            url = search_results[0]
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            if paragraphs:
                answer = paragraphs[0].get_text()
                return answer
            else:
                return "I couldn't find a direct answer, but you can check this link: " + url
        else:
            return "No results found."
    except Exception as e:
        return f"An error occurred: {e}"

def open_app(command):
    if "open notepad" in command:
        speak("Opening Notepad")
        pyautogui.hotkey("win", "r")
        pyautogui.write("notepad")
        pyautogui.press("enter")
    elif "open chrome" in command:
        speak("Opening Chrome")
        webbrowser.open("https://www.google.com")
    elif "search google for" in command:
        query = command.replace("search google for", "").strip()
        speak(f"Searching Google for {query}")
        answer = fetch_google_answer(query)
        speak(answer)
    else:
        speak("Command not recognized.")

# Always listening for "Hey Jarvis"
while True:
    wake_command = listen()
    if wake_command and "hey jarvis" in wake_command:
        speak("Yes, how can I help you?")
        command = listen()
        if command:
            open_app(command)