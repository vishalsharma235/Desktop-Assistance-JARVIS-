import pyttsx3 # For speak() function. pyttsx3 is the module for conversion of text to speech
import datetime # for wishMe() function
import speech_recognition as sr # for takeCommand() function. speech_recognition is the process of converting audio to text
import wikipedia
import webbrowser # for opening websites
import os # for playing music
from random import randint
from selenium import webdriver # For Web Scraping
import pyjokes
import requests # For weather, news requests module is used for making GET and POST requests
from pprint import pprint # for weather
import wolframalpha # For mathematical calculations and general knowledge questions

engine = pyttsx3.init('sapi5') # sapi -> Speech Application Programming Interface (to use inbuilt voice in windows)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) # voices[0] is for David(male) and voices[1] is for Zira(female)

def speak(audio): # speaks whatever we give it as an argument
    engine.say(audio)
    engine.runAndWait()
    return

def wishMe(): # wishes us according to the time
    hour = int(datetime.datetime.now().hour) # Returns the current hour between 0 and 24
    if (0 <= hour < 12):
        speak("Good Morning!")
    elif (12 <= hour < 18):
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Jarvis. How may I help you?")
    return


def takeCommand(): # takes command from us and executes it
    """
    Takes Microphone input from user and gives us string output
    """

    r = sr.Recognizer() # Recognizer class helps us in recognizing the audio
    with sr.Microphone() as source: 
        print("Listening...")
        r.pause_threshold = 1 # pause_threshold means seconds of non-speaking audio before a phrase is considered complete
        r.energy_threshold = 600
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in') # google engine is used for recognizing, en-in is english india
        print("User said :", query)

    except:
        print("I cannot understand...")
        query = input("Please type your query here : ")

    return query

def find_files(filename, search_path): # Returns the directory path in which file is there
    for root, dir, files in os.walk(search_path):
        if filename in files:
            return root

    return "None"

def openApp(app): # Opens the specified app from our Computer
    directory = find_files(app, "C:\\")
    if (directory == "None"):
        speak("Not found")
    else:
        files = os.listdir(directory)
        os.startfile(os.path.join(directory, files[files.index(app)]))
    return

def weather_data(query):
    res=requests.get('http://api.openweathermap.org/data/2.5/weather?'+query+'&APPID=b35975e18dc93725acb092f7272cc6b8&units=metric');
    return res.json()
        
def speak_weather(result,city):
    print("{}'s temperature: {}°C ".format(city,result['main']['temp']))
    print("Wind speed: {} m/s".format(result['wind']['speed']))
    print("Description: {}".format(result['weather'][0]['description']))
    print("Weather: {}".format(result['weather'][0]['main']))
    speak("{}'s temperature: {}°C ".format(city,result['main']['temp']))
    speak("Wind speed: {} m/s".format(result['wind']['speed']))
    speak("Description: {}".format(result['weather'][0]['description']))
    speak("Weather: {}".format(result['weather'][0]['main']))
    return
    
if (__name__ == "__main__"):
    wishMe()

    while True:
        query = takeCommand().lower() # Converting the user inputed string to lower case string

        # Logic to execute user command
        if "wikipedia" in query: # give command as "Actor aamir khan wikipedia or Scientist Newton wikipedia"
            speak("Searching Wikipedia...")
            try:
                query = query.replace("wikipedia", "") # Delete wikipedia from the query string
                results = wikipedia.summary(query, sentences = 3)
                speak("According to Wikipedia...")
                speak(results)
            except:
                speak("Sorry. No results found")

        elif 'google' in query: # Performs a google search. Give command as Search on Google
            speak("sir. what should i search on google")
            cm =takeCommand().lower()
            webbrowser.open('https://google.com/?#q='+ cm)

        elif 'youtube' in query: # Performs a youtube search. GIve command as Search on Youtube
            speak("What should I search on youtube")
            command = takeCommand().lower()
            webbrowser.open('https://www.youtube.com/results?search_query= ' + command)

        elif "facebook" in query: # Logs in to Facebook. GIve command as Log in to facebook please
            driver = webdriver.Chrome("Your_Driver_Path")
            driver.get("https://facebook.com")
            searchbox = driver.find_element_by_xpath('//*[@id="email"]')
            searchbox.send_keys("Your_Login_ID")
            searchPassword = driver.find_element_by_xpath('//*[@id="pass"]')
            searchPassword.send_keys("Your_Password")
            searchButton = driver.find_element_by_xpath('//*[@id="u_0_b"]')
            searchButton.click()

        elif "outlook" in query: # Opens Outlook
            driver = webdriver.Chrome("Your_Driver_Path")
            driver.get("https://outlook.live.com")
    
            searchButton = driver.find_element_by_xpath('/html/body/header/div/aside/div/nav/ul/li[2]/a')
            searchButton.click()

            searchbox = driver.find_element_by_xpath('//*[@id="i0116"]')
            searchbox.send_keys("Your_Email")

            searchButton = driver.find_element_by_xpath('//*[@id="idSIButton9"]')
            searchButton.click()

        elif "moodle" in query: # Command : Take me to moodle Jarvis
            driver = webdriver.Chrome("Your_Driver_Path")
            driver.get("https://moodle.coep.org.in")

            searchbox = driver.find_element_by_xpath('//*[@id="username"]')
            searchbox.send_keys("Your_MIS")

            searchPassword = driver.find_element_by_xpath('//*[@id="password"]')
            searchPassword.send_keys("Your_Password")

            searchButton = driver.find_element_by_xpath('//*[@id="loginbtn"]')
            searchButton.click()

        elif "mis" in query: # Command : Open mis portal Jarvis
            driver = webdriver.Chrome("Your_Driver_Path")
            driver.get("http://portal.coep.org.in:9093/SignUp?ReturnUrl=%2f")

            searchbox = driver.find_element_by_xpath('//*[@id="UserName"]')
            searchbox.send_keys("Your_MIS")

            searchPassword = driver.find_element_by_xpath('//*[@id="Password"]')
            searchPassword.send_keys("Your_Password")

            searchButton = driver.find_element_by_xpath('//*[@id="btnSignIn"]')
            searchButton.click()

        elif "play music" in query:
            speak("Loading Music")
            musicDirectory = "YourDirectoryPathHere"
            songs = os.listdir(musicDirectory) # returns a list which contains the contents of directory
            os.startfile(os.path.join(musicDirectory, songs[randint(0, len(songs) - 1)])) # plays any random song in the directory

        elif "what is your name" in query:
            speak("My name is Jarvis")

        elif "thank you" in query:
            speak("You are Welcome!!")

        elif "weather" in query:
            speak("please tell me your city name")
            city = takeCommand()
            #city = "mumbai"
            print()
            try:
                query='q='+city;
                w_data=weather_data(query);
                speak_weather(w_data, city)
                print()
            except:
                speak('City name not found')

        elif "news" in query:
            # BBC news api 
            main_url = " https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=YOUR_API_ID_HERE"
  
            # fetching data in json format 
            open_bbc_page = requests.get(main_url).json() 
      
            # getting all articles in a string article 
            article = open_bbc_page["articles"] 
  
            # empty list which will  
            # contain all trending news 
            results = [] 
              
            for ar in article: 
                results.append(ar["title"]) 
                  
            for i in range(len(results)): 
                  
                # printing all trending news
                print(results[i])
                speak(results[i])

        elif "day" in query: # What day is it today
            day = datetime.datetime.today().weekday() + 1
      
            #this line tells us about the number  
            # that will help us in telling the day 
            Day_dict = {1: 'Monday', 2: 'Tuesday',  
                        3: 'Wednesday', 4: 'Thursday',  
                        5: 'Friday', 6: 'Saturday', 
                        7: 'Sunday'}
            if day in Day_dict.keys(): 
                day_of_the_week = Day_dict[day] 
                speak("The day is " + day_of_the_week) 

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak("The time is")
            speak(strTime)

        elif "date" in query: # Tell me what date it is Jarvis
            strDate = str(datetime.date.today())
            speak("The date is")
            speak(strDate)

        elif 'open command prompt' in query:
            speak("Opening Command Prompt")
            os.system("start cmd")

        elif "open python" in query:
            speak("Opening Python IDLE")
            openApp("IDLE (Python 3.9 64-bit).lnk")

        elif "open microsoft teams" in query:
            speak("Opening Microsoft Teams")
            openApp("Microsoft Teams.lnk")

        elif "open" in query: # Open apps like Paint, Word, Notepad, Wordpad, Excel, Outlook
            list1 = query.split(" ")
            index = list1.index("open")
            speak("opening " + list1[index + 1])
            app = list1[index + 1] + ".lnk"
            app = app.capitalize()
            openApp(app)

        elif "start data structures lecture" in query:
            driver = webdriver.Chrome("Your_Driver_Path_Here")
            driver.get('https://moodle.coep.org.in/moodle/login/index.php') # Fire up a get request

            username = driver.find_element_by_xpath('//*[@id="username"]')
            username.send_keys('YourMIS')
            password = driver.find_element_by_xpath('//*[@id="password"]')
            password.send_keys('YourPassword')
            login = driver.find_element_by_xpath('//*[@id="loginbtn"]')
            login.click()
            driver.get('https://moodle.coep.org.in/moodle/course/view.php?id=1152')
            driver.get('https://moodle.coep.org.in/moodle/mod/url/view.php?id=10838')

        elif "write a note" in query: 
            speak("What should i write, sir") 
            note = takeCommand() 
            file = open('ntoes.txt', 'a') 
            speak("Sir, Should i include date and time") 
            snfm = takeCommand() 
            if 'yes' in snfm or 'sure' in snfm: 
                strTime = str(datetime.datetime.now())
                file.write(strTime) 
                file.write(" :- ") 
                file.write(note) 
            else: 
                file.write(note)
            file.write("\n")
          
        elif "show note" in query: 
            speak("Showing Notes") 
            file = open("notes.txt", "r")  
            string = file.read()
            print(string)
            speak(string)

        elif "delete note" in query:
            speak("Which note do you want to delete?")
            delete = takeCommand()
            with open("notes.txt", "r") as f:
                lines = f.readlines()
            with open("notes.txt", "w") as f:
                for line in lines:
                    if delete not in line:
                        f.write(line)

        elif "joke" in query:
            speak(pyjokes.get_joke())

        elif ("good bye" in query) or ("goodbye" in query):
            speak("It was nice serving you...")
            speak("Goodbye... See you soon, have a nice day ahead")
            break

        elif ("calculate" in query) or ("who is" in query) or ("what is" in query): # Calculate sin(30), What is Capital Of India, who is president of India, US
            app_id = 'YOUR_API_ID_HERE'
            client = wolframalpha.Client(app_id)
            res = client.query(query)
            try: 
                print (next(res.results).text) 
                speak (next(res.results).text) 
            except StopIteration: 
                speak("No results")
