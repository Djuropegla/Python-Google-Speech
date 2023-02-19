from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

# Speech engine initialisation
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) # 0 = male, 1 =female
activationWord = 'computer' # single word

# Configure browser
# Set the path
chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# wolfram_aplha client
appId = '29H459-RE2K9P8UX2'
wolframClient = wolframalpha.Client(appId)

def speak(text, rate = 120):
    engine.setProperty('rate',rate)
    engine.say(text)
    engine.runAndWait()


def parseCommand():
    listener = sr.Recognizer()
    print('Listening for a command')

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)

    try:
        print('Recognizing speech...')
        query = listener.recognize_google(input_speech, language='en_gb')
        print(f'The input speech was: {query}')
    except Exception as exception:
        print('I did not quite catch that')
        speak('I did not quite catch that')
        print(exception)
        return 'None'
    
    return query


def search_wikipedia(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('No wikipedia result')
        return 'No result received'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.option[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']

def search_wolframAlpha(query = ''):

    response = wolframClient.query(query)

    # @success: wolfram was able to resolve the query
    # @numpods: number of results returned
    # pod: list of results. this can also contain subpods

    if response['@success'] == 'false':
        return 'Could not compute'
    else:
        result = ''
        # question
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]
        # may contain the answer, has the highest confidence value
        # if it's primary or has the title of reesult or definition, then it's the official result
        if (('result') in pod1['@title'].lower() or (pod1.get('@primary', 'false')=='true') or ('definition' in pod1['@title'].lower())):
            #get the result
            result = listOrDict(pod1['subpod'])
            # remove the bracketed section
            return result.split('(')[0]
        else:
            question = listOrDict(pod0['subpod'])
            #remove the bracketet section
            return question.split('(')[0]
            #search wikipedia instead
            speak('Computation failed. Querying universal databank')
            return search_wikipedia(question)




# main loop
if __name__ == '__main__':
    speak('All systems nominal.')

    while True:
        # parse as list
        query = parseCommand().lower().split()
    
        if query[0] == activationWord:
            query.pop(0)

            #list commands
            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greetings, all.')
                else:
                    query.pop(0) # remove say
                    speech = ' '.join(query)
                    speak(speech)

            # Navigation
            if query[0] == 'go' and query[1] == 'to':
                speak('Opening...')
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)
                # webbrowser.open_new(query)

            # Wikipedia

            if query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                speak('Querying the universal databank.')
                result = search_wikipedia(query)
                speak(result)

            # wolfram_alpha
            if query[0] == 'compute' or query[0] == 'computer':
                query = ' '.join(query[1:])
                speak('Computing')
                try:
                    result = search_wolframAlpha(query)
                    print(result)
                    speak(result)
                except:
                    speak('Unable to compute.')
            
            # note taking
            if query[0] == 'log':
                speak('Ready to record your note')
                newNote = parseCommand().lower()
                now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                with open('note_%s.txt' % now, 'w') as newFile:
                    newFile.write(now+': '+newNote)
                speak('Note written')
            
            if query[0] == 'goodbye':
                speak('Goodbye')
                break