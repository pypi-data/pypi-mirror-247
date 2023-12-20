from bhaiapi.chatbot.open_app import speak_text
def get_latest_news():
    # Fetch top news headlines from newsapi.org 
    import requests
    
    url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=80e3e6880c3946498ae1f6c28954feee"
    response = requests.get(url)
    data = response.json()
    
    articles = data['articles'][:5]
    
    speak_text("Here are the top news headlines:")
    
    for article in articles:
        speak_text(article['title'])
        speak_text(article['description'])