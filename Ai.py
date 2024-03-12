import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha
import openai
import os

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
activate_word = "computer"

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))

def search_wiki(query = ''):
    search_results = wikipedia.search(query)
    if not search_results:
        print('No results found')
        return "No results found"
    try:
        wiki_page = wikipedia.page(search_results[0])
    except wikipedia.DisambiguationError as error:
        wiki_page = wikipedia.page(error.options[0])
    print(wiki_page.title)
    wiki_summary = str(wiki_page.summary)
    return wiki_summary


def speak(text, rate = 200):
    engine.setProperty("rate", rate)
    engine.say(text)
    engine.runAndWait()

def parseCommand():
    listener = sr.Recognizer()
    print("listening for a command")

    with sr.Microphone() as source:
        listener.pause_threshold = 1
        input_speech = listener.listen(source)

    try:
        print("recognizing speech")
        query = listener.recognize_google(input_speech, language="en_us")
        print("the input speech was: " + query)
    except Exception as exception:
        print("Couldn't catch that")
        speak("Couldn't catch that")
        print(exception)
        return 'None'

    return query

if __name__ == '__main__':
    speak("All systems nominal.")

    while True:
        query = parseCommand().lower().split()

        if query[0] == activate_word:
            query.pop(0)

            if query[0] == 'say':
                if 'hello' in query:
                    speak("Greetings")
                else:
                    query.pop(0)
                    speech = ' '.join(query)
                    speak(speech)
            if query[0] == "go" and query[1] == 'to':
                print("Opening...")
                query = " ".join(query[2:])
                webbrowser.get("chrome").open_new(query)

            #wiki
            if query[0] == "wikipedia":
                query = ' '.join(query[1:])
                speak('Querying the universal databank.')
                speak(search_wiki(query))
            
            #wolframalpha


            #notes
                
            if query[0] == 'log':
                speak("Ready to record")
                new_note = parseCommand().lower()
                now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                with open('note_%s.txt' % now, 'w') as newfile:
                    newfile.write(new_note)
                speak("Note written")

