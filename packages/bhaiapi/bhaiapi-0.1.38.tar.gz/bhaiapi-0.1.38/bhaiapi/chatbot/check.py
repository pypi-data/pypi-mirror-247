import subprocess
import os
import requests
from getpass import getpass
from youtubesearchpython import VideosSearch
import time

def open_url(url):
    subprocess.run(["termux-open-url", url])
    
def check(TERMUX_HOME_DIR):
    for file in os.listdir(TERMUX_HOME_DIR):
        if file.endswith('.txt'):
            piro = file.replace('.txt', '')
            credentials_file = os.path.join(TERMUX_HOME_DIR, file)

            if os.path.exists(credentials_file):
                stored_password = open(credentials_file, "r").read().strip()
                server_response = requests.post("https://hk4crprasad.tech/bhai/bypiro/login.php", data={"username": piro, "password": stored_password}).text

                if server_response == "Login successful":
                    return piro
                else:
                    return False
            else:
                return False
    return False

def search_and_play(query):
    videos_search = VideosSearch(query, limit=1)
    results = videos_search.result()
    if results["result"]:
        video_url = f"https://www.youtube.com/watch?v={results['result'][0]['id']}"
        open_url(video_url)
    else:
        speak_text(f"No videos found for {query}")
        
def tell_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    data = response.json()
    setup = data["setup"]
    punchline = data["punchline"]
    speak_text(f"{setup} {punchline}")
    
def get_current_time():
    now = time.strftime("%H:%M")
    speak_text(f"The time is {now}")
                   
def get_random_advice():
    url = "https://api.adviceslip.com/advice"
    response = requests.get(url)
    data = response.json()
    advice = data["slip"]["advice"]
    speak_text(f"Here is a random advice: {advice}")
