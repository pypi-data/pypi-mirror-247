from bhaiapi.chatbot.open_app import speak_text

def search_wiki(query):
    # Search Wikipedia for the query and return summarized results 
    import wikipedia
    
    try:
        results = wikipedia.summary(query, sentences=2)
        speak_text(f"Here are the search results for {query}: {results}")
    except wikipedia.exceptions.PageError:
        speak_text(f"No results found for {query}")
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:3]
        speak_text(f"{query} may refer to: {', '.join(options)}")
