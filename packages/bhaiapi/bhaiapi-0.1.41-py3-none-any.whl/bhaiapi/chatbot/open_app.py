import requests
from gtts import gTTS  
import os

def speak_text(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save('output.mp3')
    os.system('mpv --no-terminal --no-video output.mp3')
    print(f"{text}")

def open_app(app_name):
    if app_name.lower() == "chrome":
        speak_text("Opening Chrome")
        os.system("am start com.android.chrome/com.google.android.apps.chrome.Main")
    elif app_name.lower() == "whatsapp":
        speak_text("Opening WhatsApp")
        os.system("am start com.whatsapp/com.whatsapp.HomeActivity")
    elif app_name.lower() == "instagram":
        speak_text("Opening Instagram")
        os.system("am start com.instagram.android/com.instagram.mainactivity.LauncherActivity")
    elif app_name.lower() == "pubg" or app_name.lower() == "bgmi" or app_name.lower() == "bgm i":
        speak_text("Opening Battle Ground Mobile India")
        os.system("am start com.pubg.imobile/com.epicgames.ue4.SplashActivity")
    elif app_name.lower() == "mt manager" or app_name.lower() == "mt" or app_name.lower() == "manager":
        speak_text("Opening mt manager")
        os.system("am start bin.mt.plus/bin.mt.plus.Main")
    else:
        speak_text(f"Sorry, I don't know how to open {app_name}")
        