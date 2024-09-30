import requests
import wikipedia
import pywhatkit as kit


def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address['ip']

def search_on_wikipedia(query):
    res = wikipedia.summary(query, sentences=2)
    return results()

def search_on_google(query):
    kit.search(query)

def youtube(video):
    kit.search(video)
def get_news():
    news_headlines = []
    result = requests.get(f'https://newsapi.org/v2/everything?q=tesla&from=2024-08-30&sortBy=general&apiKey'
                          f'=4e26c21e00da4238886682d9f314f668').json()
    articles = result['articles']
    for article in articles:
        news_headlines.append(article['title'])
    return news_headlines[:6]

def weather_forcecast(city):
    res = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=813fab8bc08df455610c9c52d095c244"
    ).json()
    weather = res['weather'][0]['main']
    temp = res['main']['temp']
    feels_like = res['main']['feels_like']
    return weather,f'{temp}C',f'{feels_like}c'
