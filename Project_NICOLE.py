import speech_recognition as ear
import pyttsx3
import datetime
import wikipedia
import pyjokes
import pywhatkit
import warnings

warnings.filterwarnings("ignore")

# Initialize global variables
reap = False #To manage loops related to "Sleeping" vs. "Awake"
online = True

# Initialize speech recognition and text-to-speech
listener = ear.Recognizer()
mouth = pyttsx3.init()
voices = mouth.getProperty('voices')
mouth.setProperty('voice', voices[1].id)

def talk(text):
    mouth.say(text)
    mouth.runAndWait()

def listen():
    command = 'blank'
    try:
        with ear.Microphone() as source:
            print('Listening...')
            if reap:
                talk('BEEP')

            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source)
            command = listener.recognize_google(audio).lower()
            print(command)
            if 'nicole' in command:
                talk('Yes Sir')
                command = command.replace('nicole', '')
    except ear.UnknownValueError:
        if reap:
            talk('Sorry, I did not understand that.')
    except ear.RequestError:
        talk('Sorry, there is an issue with the speech recognition service.')

    return command

def Note():
    fileName = "Nicoles Note"
    note = open(fileName, "W")
    
    respond("Okay. Making a note")
    note.write(listen())
    note.close()
    return

def respond(text):
    print(' ' + text)
    talk(text)

def execute_command(command):
    global reap

    if 'are you' in command:
        respond("I am Nicole. Nkosie's Intelligent Coalescence Of Logical Effects, or something like that. " +
                "I don't know, I was made by a script kitty who doesn't know much and this is basically rocket science")

    elif 'what can you do' in command:
        respond('I can play music on YouTube with the "Play" command, tell the time, and retrieve information if asked.')

    elif 'play' in command:
        song = command.replace('play', '').strip()
        respond('Playing ' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%H:%M')
        respond('It is currently ' + current_time)

    elif 'what is' in command:
        search = command.replace('what is', '').strip()
        respond('Searching for ' + search)
        info = wikipedia.summary(search, 2)
        respond(info)
        respond('For more, say search for ' + search)

    elif 'who is' in command:
        search = command.replace('who is', '').strip()
        respond('Searching for ' + search)
        info = wikipedia.summary(search, 2)
        respond(info)
        respond('For more, say search for ' + search)

    elif 'search for' in command:
        search = command.replace('search for', '').strip()
        respond('Searching for ' + search)
        pywhatkit.search(search)

    elif 'tell me about' in command:
        thing = command.replace('tell me about', '').strip()
        info = wikipedia.summary(thing, 7)
        respond(info)

    elif 'sleep' in command:
        respond('Deactivating')
        reap = False

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        respond(joke)
        
    #elif ('text' or 'send a message') in command:
    #    pywhatkit.sendwhatmsg('+27xx xxx xxxx', 'This is Nicole <3', 16, 25)
    #    respond('Message sent')

    #else:
        #talk('Once more? Please repeat your request.')

def main():
    global reap
    respond('Sleeping..')
    #execute_command('')  # Initial dummy call

    while True:
        command = listen()
        if command == 'blank':
            print('No command detected')
            continue
        
        if reap:
            respond('Greetings. Nicole, at your service. Please wait for the beep to state your query.')
            execute_command(command)
            while reap:
                command = listen()
                execute_command(command)
        else:
            if 'wake up' in command:
                reap = True
                respond('I am awake. How can I assist you?')

if __name__ == "__main__":
    main()
