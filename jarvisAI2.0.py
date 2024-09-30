import pyttsx3
import requests
import speech_recognition as sr
import keyboard
import os
import wolframalpha
import pyautogui
import subprocess as sp
import imdb
from datetime import datetime
from decouple import config, text_type
from random import choice
from pyttsx3 import speak
from conv import random_text
from online import find_my_ip,search_on_google,search_on_wikipedia,youtube,get_news,weather_forcecast

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 225)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

USER = config('USER')
HOSTNAME = config('BOT')


def speak(text):
    engine.say(text)
    engine.runAndWait()

def great_me():
    hour = datetime.now().hour
    if (hour>=6) and (hour < 12):
        speak(f'Good Morning {USER}')
    elif (hour >= 12) and (hour < 16):
        speak(f'Good Afternoon {USER}')
    elif (hour >= 16) and (hour < 19):
        speak(f'Good Evening {USER}')
    speak(f'I am {HOSTNAME}. How may i assist you? {USER}')

listening = False

def start_listening():
    global listening
    listening = True
    print('started listening')

def pause_listening():
    global listening
    listening = False
    print('stopped listening')

keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p',pause_listening)

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing....')
        queri = r.recognize_google(audio, language='en-in')
        print(queri)
        if not 'stop' in queri or 'exit' in queri:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour>=21 and hour<6:
                speak(f'Good night sir,take care!')
            else:
                speak(f'Have a good day sir!')
            exit()


    except Exception:
        speak(f'Sorry i could not understand. Can you reapet that?')
        queri = 'None'
    return queri

if __name__ == '__main__':
      great_me()
      while True:
          if listening:
              query = take_command().lower()
              if 'how are you' in query:
                  speak(f'I am absolutely fine sir. What about you')
              elif 'open command promt' in query:
                  speak('open command promt')
                  os.system('start command promt')
              elif 'open camera' in query:
                  speak('open camera')
                  sp.run('start microsoft.windows.camera:', shell=True)
              elif 'ip address' in query:
                  ip_address = find_my_ip()
                  speak(f'your ip address is {ip_address}')
                  print(f'your io address is{ip_address}')
              elif 'open youtube' in query:
                  speak('what do you want to play on youtube sir?')
                  video = take_command().lower()
                  youtube(video)
              elif 'open google' in query:
                  speak(f'what do you want search on google{USER}')
                  query = take_command().lower()
                  search_on_google(query)

              elif 'open wikipedia' in query:
                  speak(f'what do you want search on wikipedia sir?')
                  search = take_command().lower()
                  result = search_on_wikipedia(search)
                  speak(f'According to wikipedia {result}')
                  speak('I am printing in on terminal')
                  print(result)

              elif "give me news" in query:
                  speak(f"I am reading out the headline of today,sir")
                  speak(get_news())
                  speak('I am printing it on screen sir')
                  print(*get_news(),sep='\n')

              elif 'weather' in query:
                  ip_address = find_my_ip()
                  speak('tell me the name of your city:')
                  city = input('Enter the city name')
                  speak(f'Getting weather report of your city{city}')
                  weather,temp,feels_like = weather_forcecast(city)
                  speak(f'The current temperature is {temp},but it feel like {feels_like}')
                  speak(f'Also the weather talks about {weather}')
                  speak("I am printing info om scereen")
                  print(f'Description:{weather}\nTemperature:{temp}\nFeels Like:{feels_like}')

              elif 'movie' in query:
                  movies_db = imdb.IMDb()
                  speak('Please tell the movie name:')
                  text = take_command()
                  movies = movies_db.search_movir(text)
                  speak('searching for' + text)
                  speak('I found these')
                  for movie in movies:
                      title = movie['title']
                      year = movie['year']
                      speak(f'{title}-{year}')
                      info = movie.getID()
                      movie_info = movies_db.ge_movie(info)
                      rating = movie_info['rating']
                      cast = movie_info['cast']
                      actor = cast[0:5]
                      plot = movie_info.get('plot outline','plot summary not available')
                      speak(f'{title} was released in{year}has imdb rating of {rating}. It has a cast of{actor}.The'
                            f'plot summary of movie is{plot}')
                      print(f'{title} was released in{year}has imdb rating of {rating}. It has a cast of{actor}.The'
                            f'plot summary of movie is{plot}')

              elif 'calculate' in query:
                  app_id = 'ET2TU2-A52X8JVHKL'
                  client = wolframalpha.Client(app_id)
                  ind = query.lower().split().index('calculate')
                  text = query.split()[ind + 1:]
                  result = client.query(" ".join(text))
                  try:
                      ans = next(result.results).text
                      speak('The answer is' + ans)
                      print('The answer is' + ans)
                  except StopIteration:
                      speak('I could not find that. Please try again')
              elif 'what is' in query or 'who is' in query or 'which is' in query:
                  app_id = 'ET2TU2-A52X8JVHKL'
                  client = wolframalpha.Client(app_id)
                  try:
                      ind = query.lower().index('what is') if 'what is' in query.lower() else\
                          query.lower().index('who is') if 'who is' in query.lower() else\
                            query.lower().index('which is') if 'which is' in query.lower() else None

                      if ind is not None:
                          text = query.split()[ind + 2:]
                          result = client.query(" ".join(text))
                          ans = next(result.results).text
                          speak('The answer is' + ans)
                          print('The answer is' + ans)
                      else:
                          speak('I could not find that')
                  except StopIteration:
                      speak('I could not find that. Please try again')