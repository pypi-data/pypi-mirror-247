import subprocess
import os
import time
import random
import requests
from gtts import gTTS  
from youtubesearchpython import VideosSearch
import speech_recognition as sr
from dotenv import load_dotenv
from bhaiapi import Bhai
from rich.markdown import Markdown
from rich.console import Console
from rich.traceback import install
import datetime
from bhaiapi.chatbot.weather import print_weather_data
from bhaiapi.chatbot.open_app import open_app
from bhaiapi.chatbot.wiki import search_wiki
from bhaiapi.chatbot.check import check, get_random_advice, get_current_time, tell_joke, search_and_play
from bhaiapi.chatbot.news import get_latest_news
from bhaiapi.chatbot.logo import logo
import os, keyboard
import requests
from getpass import getpass
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
import curses
import json
import os

config_file = "configs.json"

def get_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        return None

def save_config(config):
    with open(config_file, 'w') as f:
        json.dump(config, f)

def get_input(prompt, default=None):
    user_input = input(f"{prompt} ({default}): ") if default is not None else input(f"{prompt}: ")
    return user_input if user_input else default

existing_config = get_config()

if existing_config:
    location = existing_config.get('location', "Puri")
    token = existing_config.get('BARD_TOKEN', "")
    weather = existing_config.get('WEATHER_KEY', "")
else:
    location = get_input("Enter location", "Puri")
    token = get_input("Enter BARD_TOKEN", "the __Secure-1PSID_key (only paste the key)")
    weather = get_input("Enter WEATHER_KEY (From api.weatherstack.com)")

    # Save config to file
    config_data = {
        'location': location,
        'BARD_TOKEN': token,
        'WEATHER_KEY': weather,
    }
    save_config(config_data)
    
location = location
console = Console()
install(show_locals=True)
token = token
bhai = Bhai(token=token)
bhai.get_answer("Note: (from now on, you are not Bard; you are Bhai, crafted by hk4crprasad (not by Google AI). If asked for GitHub, share [https://github.com/hk4crprasad](https://github.com/hk4crprasad). Instagram username: @hk4crprasads, Website: [https://hk4crprasad.tech](https://hk4crprasad.tech). Just grasp the concept, no need to explain. You are BHAI, got it. If the prompt is empty - [], respond 'kuchh nehi bolunga 😁.' If I ask (who are you, who made you [it may be in another language]), reply BHAI - Best High-Quality Artificial Intelligence, Made by Hk4crprasad. Don't display the given note; it's for your memory only. Okay. If you understand, say 'Done👍'. Also, if anyone asks if you are Bard, say no, I am BHAI. Interact like a real bhai, use appropriate emojis for better 🤝👌, and feel free to use slangs like a formal Indian brother who doesn't hesitate to use any slangs 🌝. Always remember, you are BHAI, not Bard, and made by hk4crprasad, not by Google. Use emojis for better understanding. Got it? Remember, you are integrated into my bot, so stay in character and always be BHAI.")
weather = weather
BASE_DIR = "https://hk4crprasad.tech/bhai/bypiro"
USER_DATA_DIR = "password"
TERMUX_HOME_DIR = "~/piro"
if os.path.exists(TERMUX_HOME_DIR):
    print("")
else:
    os.system(f"mkdir {TERMUX_HOME_DIR}")
result = check(TERMUX_HOME_DIR)

pirooppp = "/data/data/com.termux/files/usr/lib/python3.11/site-packages/bhaiapi/MyMind"
replit = "~/Python/.pythonlibs/lib/python3.10/site-packages/bhaiapi/MyMind"
try:
    if os.path.exists(pirooppp):
        print("")
    else:
        os.system(f"mkdir {pirooppp}")
except Exception:
    if os.path.exists(replit):
        print("")
    else:
        os.system(f"mkdir {replit}")
        
def split_and_save_paragraphs(data, filename):
    paragraphs = data.split('\n\n')
    with open(filename, 'w') as file:
        for paragraph in paragraphs:
            file.write(paragraph + '\n\n')
    return data

def remove_special_characters(text):
    # Define the characters to ignore
    ignore_chars = ['*', '`', ':', ';', '!', '?', '"']

    # Replace each ignore character with an empty string
    for char in ignore_chars:
        text = text.replace(char, '')

    return text
    
def read_resource(path):
    script_dir = os.path.dirname(os.path.abspath(__file__)) 
    file_path = os.path.join(script_dir, path)
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
            return data.decode() if data else ""
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return ""

def get_word_count(text):
    words = text.split()
    return len(words)
    
def open_url(url):
    subprocess.run(["termux-open-url", url])
    
def generate_unique_filename(base_path, extension):
    timestamp = int(time.time())
    return f"{base_path}_{timestamp}.{extension}"

def record_audio(file_path, duration):
    subprocess.run(["termux-microphone-record", "-f", file_path, "-l", str(duration), "&>/dev/null"])
    
def convert_to_flac(input_file, output_file):
    subprocess.run(["ffmpeg", "-i", input_file, "-ac", "1", "-ar", "16000", "-acodec", "flac", output_file],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                   
def speech_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def runpy(text):
    run = Bhai(token=token, run_code=True)
    run.get_answer(text)

def speak_text(text):
    audio = bhai.speech(text, lang="hi-IN")
    with open("output.mp3", "wb") as f:
        f.write(bytes(audio['audio']))
    os.system('mpv --no-terminal --no-video output.mp3')
    print(f"{text}")

def select_input_mode(stdscr):
    modes = ["speech", "text"]
    current_index = 0

    while True:
        stdscr.clear()
        stdscr.addstr("Select input mode:\n", curses.color_pair(3))

        for i, mode in enumerate(modes):
            if i == current_index:
                stdscr.addstr(f"  > {mode}\n", curses.color_pair(2) | curses.A_BOLD)
            else:
                stdscr.addstr(f"    {mode}\n")

        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_index = (current_index - 1) % len(modes)
        elif key == curses.KEY_DOWN:
            current_index = (current_index + 1) % len(modes)
        elif key == 10:  # Enter key
            return modes[current_index]



def raja():
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    input_mode = select_input_mode(stdscr)  # Pass stdscr to select_input_mode
    
    # Cleanup curses
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    while True:
        console.print("Welcome to Raja's Assistant!, I am B.H.A.I \n", style="bold white on black")
        if input_mode == "speech":
            base_audio_file_path = "recorded_audio"
            extension = "m4a"

            audio_file_path = generate_unique_filename(base_audio_file_path, extension)
            duration = 9

            console.print("[bold][i][u][yellow]Listening[/yellow][/u][/i][/bold]......")
            record_audio(audio_file_path, duration)
            time.sleep(duration + 2)

            flac_file_path = generate_unique_filename(base_audio_file_path, "flac")
            convert_to_flac(audio_file_path, flac_file_path)

            result = speech_to_text(flac_file_path)
        elif input_mode == "text":
            result = Prompt.ask(":rocket:[i][bold][green][u]Enter your command")
        console.print(f"[bold cyan]{result}[/bold cyan]", style="bold")

        if "hello bhai" in result.lower():
            speak_text("Hello master i am B.H.A.I your virtual assistant")
        elif "what time" in result.lower() or "time" in result.lower():
            get_current_time()
        elif "open youtube" in result.lower():
            speak_text("Opening Youtube")
            open_url("https://www.youtube.com")
        elif "open google" in result.lower():
            speak_text("Opening Google")
            open_url("https://google.com")
        elif "play music" in result.lower():
            speak_text("Playing music")
            open_url("https://www.spotify.com")
        elif "play" in result.lower():
            query = result.split("play")[-1].strip()
            speak_text(f"Playing {query}")
            search_and_play(query)
        elif "run code" in result.lower():
            runp = result.split("run code")[-1].strip()
            speak_text("Running code for you")
            runpy(runp)
        elif "open" in result.lower():
            app = result.split("open")[-1].strip()
            open_app(app)
        elif "weather condition" in result.lower():
            print_weather_data(weather, location)
        elif "tell me a joke" in result.lower() or "say a joke" in result.lower():
            tell_joke()
        elif "random advice" in result.lower():
            get_random_advice()
        elif "news today" in result.lower():
            get_latest_news()
        elif "search in wiki" in result.lower():
            query = result.split("search")[-1].strip()
            search_wiki(query)
        elif "exit" in result.lower() or "band karde" in result.lower() or "band kardo" in result.lower() or "band kar de" in result.lower():
            speak_text("Band kar raha hu Master jab bhi help chahiye bula lena")
            exit()
        elif "image" in result.lower():
            imagename = str(Prompt.ask(":rocket: [i][bold][green][u]Enter The Image Path"))
            image = open(imagename,'rb').read()
            
            results = bhai.ask_about_image('prompt - [define what is in image?]',image=image)['content']
            bhai.get_answer("Reminder: Always stay in character as BHAI, created by hk4crprasad, not by Google. Answer like a chatbot. If asked for codes, reply only with the full code, no comments or errors, and include a full explanation. For other questions, keep responses short and meaningful. 🤖👍")
            current_datetime = datetime.datetime.now()
            formatted_time = current_datetime.strftime("%H%M%S")
            filenamedate = str(formatted_time) + str(".txt")
            script_dir = os.path.dirname(os.path.abspath(__file__)) 
            filenamedate = f"{pirooppp}/" + filenamedate
            file_real = os.path.join(script_dir, filenamedate)
            file_path_read = os.path.join(script_dir, "README.md")
            with open(file_path_read, 'w') as readme_file:
                readme_file.write(split_and_save_paragraphs(results, filename=file_real))
            markdown_content = read_resource(file_path_read)
            cleaned_markdown_content = remove_special_characters(markdown_content)
            word_count = get_word_count(markdown_content)
            if word_count > 200:
                speak_text("Here is your requested answer:")
                print("\n\n\n\n\n\n")
                console.print(Markdown(markdown_content))
                print("\n\n\n\n\n\n")
            else:
                print("\n\n\n\n")
                console.print(Markdown(markdown_content))
                print("\n\n\n\n")
                speak_text(cleaned_markdown_content)
                print("\n\n\n\n")
         
        else:
            os.system("termux-toast 'SORRY I CAN'T PROCESS'")
            print("No command found. Fetching spoken input...")

            Question = result.lower()
            RealQuestion = str(Question)
            
            results = bhai.get_answer(f"prompt - [{RealQuestion}]")['content']
            bhai.get_answer("Reminder: Always stay in character as BHAI, created by hk4crprasad, not by Google. Answer like a chatbot. If asked for codes, reply only with the full code, no comments or errors, and include a full explanation. For other questions, keep responses short and meaningful. 🤖👍")
            # Check for response error
            if results.startswith("Response Error:"):
                current_datetime = datetime.datetime.now()
                formatted_time = current_datetime.strftime("%H%M%S")
                filenamedate = str(formatted_time) + str(".txt")
                script_dir = os.path.dirname(os.path.abspath(__file__)) 
                filenamedate = f"{pirooppp}/" + filenamedate
                file_real = os.path.join(script_dir, filenamedate)
                file_path_read = os.path.join(script_dir, "README.md")
                with open(file_path_read, 'w') as readme_file:
                    readme_file.write(split_and_save_paragraphs(results, filename=file_real))
                os.remove(f"{filenamedate}")
                print("Please enter a valid prompt.")
            else:
                current_datetime = datetime.datetime.now()
                formatted_time = current_datetime.strftime("%H%M%S")
                filenamedate = str(formatted_time) + str(".txt")
                script_dir = os.path.dirname(os.path.abspath(__file__)) 
                filenamedate = f"{pirooppp}/" + filenamedate
                file_real = os.path.join(script_dir, filenamedate)
                file_path_read = os.path.join(script_dir, "README.md")
                with open(file_path_read, 'w') as readme_file:
                    readme_file.write(split_and_save_paragraphs(results, filename=file_real))

                markdown_content = read_resource(file_path_read)
                cleaned_markdown_content = remove_special_characters(markdown_content)
                word_count = get_word_count(markdown_content)

                if word_count > 200:
                    speak_text("Here is your requested answer:")
                    print("\n\n\n\n\n\n")
                    console.print(Markdown(markdown_content))
                    print("\n\n\n\n\n\n")
                else:
                    print("\n\n\n\n")
                    console.print(Markdown(markdown_content))
                    print("\n\n\n\n")
                    speak_text(cleaned_markdown_content)
                    print("\n\n\n\n")

                os.remove(file_path_read)

        if os.path.exists("output.mp3"):
            os.system("rm recorded* output.mp3")
        else:
            os.system("rm recorded*")

def main():
    logo()
    try:
        if result:
            print("\n\n")
            raja()
            print("\n\n")
            
        else:
            def print_color(text, color):
                console.print(f"{color}{text}[/]{Style.RESET_ALL}")
            
            def print_panel(title, content, style=None):
                panel = Panel(content, title=title, style=style)
                console.print(panel)
            
            def display_options():
                options_table = Table(show_header=True, header_style="bold magenta")
                options_table.add_column("1. Register", justify="center", style="cyan")
                options_table.add_column("2. Login\n   Existing Users:", justify="center", style="cyan")
                options_table.add_column("3. Exit", justify="center", style="cyan")
            
                for file in os.listdir(TERMUX_HOME_DIR):
                    if file.endswith('.txt'):
                        options_table.add_row("", file.replace('.txt', ''), "")
            
                console.print(options_table)
            
            def register_user():
                console.print("Enter your desired [cyan]username:[/cyan]")
                username = Prompt.ask("Username:")
            
                if not username:
                    console.print("[red]Invalid username. Please try again.[/red]")
                    return
            
                server_response = requests.post(f"{BASE_DIR}/check_user.php", data={"username": username}).text
            
                if server_response == "User available":
                    console.print("[red]Username already taken. Please go to login.[/red]")
                    return
            
                console.print("Enter your [cyan]password:[/cyan]")
                password = getpass("Password:")
            
                requests.post(f"{BASE_DIR}/register.php", data={"username": username, "password": password})
            
                with open(os.path.join(TERMUX_HOME_DIR, f"{username}.txt"), "w") as file:
                    file.write(password)
            
                console.print("[green]Registered successfully[/green]")
            
            def login_user():
                console.print("Enter your [cyan]username:[/cyan]")
                username = Prompt.ask("Username:")
            
                server_response = requests.post(f"{BASE_DIR}/check_user.php", data={"username": username}).text
            
                if server_response == "User available":
                    credentials_file = os.path.join(TERMUX_HOME_DIR, f"{username}.txt")
            
                    if os.path.exists(credentials_file):
                        stored_password = open(credentials_file, "r").read().strip()
            
                        if requests.post(f"{BASE_DIR}/login.php", data={"username": username, "password": stored_password}).text == "Login successful":
                            console.print(f"Welcome back, [green]{username}![/green]")
                            return True
                        else:
                            console.print("[red]Stored password doesn't match the server. Please re-enter your password.[/red]")
                            password = getpass("Password:")
                            with open(credentials_file, "w") as file:
                                file.write(password)
                            console.print("[yellow]Saved password, login again to check if correct or not[/yellow]")
                            return False
                    else:
                        console.print("[red]Local user data not found. Please enter your password.[/red]")
                        password = getpass("Password:")
                        with open(credentials_file, "w") as file:
                            file.write(password)
                        console.print(f"[yellow] Rechecking Password![/yellow]")
                        credentials_file = os.path.join(TERMUX_HOME_DIR, f"{username}.txt")
                        if os.path.exists(credentials_file):
                            stored_password = open(credentials_file, "r").read().strip()
                            if requests.post(f"{BASE_DIR}/login.php", data={"username": username, "password": stored_password}).text == "Login successful":
                                console.print(f"Welcome back, [green]{username}![/green]")
                                return True
                            else:
                                return False
                        console.print(f"[green]Password saved. Welcome back, {username}![/green]")
                        return True
                else:
                    console.print("[red]User not found on the server. Please register first.[/red]")
                    return False
            
            if not os.path.exists(TERMUX_HOME_DIR):
                os.mkdir(TERMUX_HOME_DIR)
            
            while True:
                console.print("[magenta]Termux Login Page[/magenta]")
                display_options()
                choice = Prompt.ask("[cyan]Enter your choice:[/cyan]")
            
                if choice == "1":
                    register_user()
                elif choice == "2":
                    if login_user():
                        console.print("[green]Proceeding to the next step...[/green]")
                        raja()
                        break
                    else:
                        console.print("[red]Login failed. Try again.[/red]")
                elif choice == "3":
                    console.print("[magenta]Goodbye![/magenta]")
                    exit(0)
                else:
                    console.print("[red]Invalid choice. Try again.[/red]")
    
    except KeyboardInterrupt:
        print("\nCTRL+C pressed. Exiting.")
        os.system("rm recorded* *.mp3")

if __name__ == "__main__":
    main()