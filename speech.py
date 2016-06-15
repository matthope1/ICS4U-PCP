import smtplib
import speech_recognition
import pyttsx
from random import randint
import time
#printer stuff
import tempfile
import win32api
import win32print

speech_engine = pyttsx.init('sapi5')  # see http://pyttsx.readthedocs.org/en/latest/engine.html#pyttsx.init
speech_engine.setProperty('rate', 150)

contact_dict = {"MATTHEW":"matthew.hope16@ycdsbk12.ca", "MATT": "matt-hope@hotmail.com",
                "ANDREW": "andrewhope772@gmail.com"}

user_dict = {"MATTHEW":"matthew.hope16@ycdsbk12.ca" ,"ANDREW": "andrewhope772@gmail.com"}

pass_dict = {"MATTHEW":"Mh1097465", "ANDREW": "temp"}

def speak(text):
    """

    :rtype: object
    """
    
    speech_engine.say(text)
    speech_engine.runAndWait()


recognizer = speech_recognition.Recognizer()


def listen():

    with speech_recognition.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)

    except speech_recognition.UnknownValueError:
        print("Could not understand audio")
        speak("could not understand audio")
        speak("Im listening again")
        listen()
    except speech_recognition.RequestError as e:
        print("Recog Error; {0}".format(e))

    return ""

def user_prompt():

    prompt = False

    while prompt == False:

        usage_list = ["EMAIL","PRINTER","JOKE"]
        print "what would you like to do? Email,? Check printer?"
        speak("what would you like to do?")
        user_res = listen().upper()
        print user_res

        if "EMAIL" in user_res:
            email_prompt()
            prompt = True

        elif "JOKE" in user_res:
            joke()
            prompt = True

        elif "TIME" in user_res or "DATE" in user_res:
            date_time()
            prompt = True

        elif "PRINT" in user_res:
            send_to_printer()
            prompt = True


        else:
            print "invalid command"
            prompt = False


def email_prompt():

    print "do you want to send an email"
    speak("do you want to send an email? ")
    ans = listen()
    print ans

    if ans == "yes":
        print ans
        print "get ready to email:"
        speak("get ready to email")
        send_email()
    else:

        print ans
        print "okay, no email then"
        speak("okay, no email then")
        user_prompt()

def send_email():

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    user_valid = False

    while user_valid == False:

        speak("what is your username ")
        print "what is your username "
        user = listen().upper()
        print user

        if user in contact_dict:
            user_valid = True

        else:
            user_valid = False



    server.login(user_dict[user],pass_dict[user]) # logs into the gmail server

    speak("who do you want to send this to")
    send_to = listen().upper()
    print send_to
# you need a while loop here
    if send_to in contact_dict:

        speak("what do you want to say to" + contact_dict[send_to])
        msg = listen()
        print msg
        server.sendmail(user_dict[user], contact_dict[send_to], msg)
        print "email sent"

    else:
        print "that name is not in your contacts "

    server.quit()
    user_prompt()

def joke():
    joke_num = randint(1,3)

    if joke_num == 1:
        print"why are there fences in a grave yard? because people were dying to get in "
        speak("why are there fences in a grave yard?.. because people are dying to get in")

    elif joke_num == 2:
        print "how did the frog die? he kermit suicide"
        speak("how did the frog die?... he kermit suicide ")

    elif joke_num == 3:
        print "I sold my vacuum the other day, all it was doing was collecting dust "
        speak("I sold my vacuum the other day... all it was doing was collecting dust")

#user_prompt()
# tells user 1 of three random jokes

def date_time():

    localtime = time.asctime(time.localtime(time.time()))
    print "the current time is: ", localtime
    speak("the current time is" + localtime)
    user_prompt()
     #tells user the date and time
def send_to_printer():

    print "what do you want to print"
    speak("what do you want to print")
    ans = listen()
    print ans

    filename = tempfile.mktemp (".txt")
    open (filename, "w").write (ans)
    win32api.ShellExecute (
      0,
      "print",
      filename,
      #
      # If this is None, the default printer will
      # be used anyway.
      #
      '/d:"%s"' % win32print.GetDefaultPrinter (),
      ".",
      0
    )

    # sends something to default printer
    print "sent",ans,"to printer"

def main():
    user_prompt()

main()