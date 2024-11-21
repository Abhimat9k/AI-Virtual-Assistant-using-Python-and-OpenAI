import speech_recognition as sr         
import webbrowser                      # voice command will get open in browser
import pyttsx3                         # python speech to text module/package
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

recognizer = sr.Recognizer()
engine = pyttsx3.init()                  # initializing text to speed i.e ttsx engine
newsapi = os.getenv('news_api')

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize the mixer and pygame
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")  # Replace with your MP3 file path

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running to let the music play
    while pygame.mixer.music.get_busy():  # Check if the music is playing
        pygame.time.Clock().tick(10)  # Wait for a short time

    pygame.mixer.music.unload()
    os.remove("temp.mp3")    

def aiProcess(command):
    client = OpenAI(
    api_key = os.getenv('API_KEY'),
    )

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks just like Alexa and Google Cloud. Give short responses please"},
        {
            "role": "user",
            "content": "What is programming."
        }
    ]
    )

    return completion.choices[0].message

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = " ".join(c.lower().split(" ")[1:])      # join all the words after "play" command and put it in song
        songLink = musicLibrary.music[song]
        if songLink:
            webbrowser.open(songLink) 
        else:
            print(f"Sorry, '{song}' is not present in the music Library")     
    
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            # Extract the articles
            articles = data.get('articles', [])

            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        pass            

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()

        # recognize speech using Google
        try:
            with sr.Microphone() as source:
                print("Listening..")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            
            if(word.lower() == "jarvis"):
                speak("Ya")

                #Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active..")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)  
              
        except Exception as e:
            print(e)
