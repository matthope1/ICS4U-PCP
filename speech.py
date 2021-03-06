import smtplib
import speech_recognition
import pyttsx #text to speech
from random import randint
import time
# printer stuff
import tempfile
import win32api
import win32print
import os


speech_engine = pyttsx.init('sapi5')  # see http://pyttsx.readthedocs.org/en/latest/engine.html#pyttsx.init
speech_engine.setProperty('rate', 150)

contact_dict = {"MATTHEW": "matthew.template@mail.ca"}

user_dict = {"MATTHEW": "matthew.template@mail.ca", "ANDREW": "temp"}

pass_dict = {"MATTHEW": "temp", "ANDREW": "temp"}

music_dict = {"SONG ONE":"C:\Users\Matthew\Desktop\song1.mp3", "SONG TWO" : ""}

program_dict = {"NOTES":"C:\Users\Matthew\Desktop\openme.txt", "SUBLIME TEXT": "C:\Program Files\Sublime Text 3\sublime_text.exe" }




def speak(text):
    """
    :param text: string : text that the computer will say to the user
    :return: None
    """

    speech_engine.say(text)
    speech_engine.runAndWait()


recognizer = speech_recognition.Recognizer()


def listen():
    """
    listens for user input
    :return: the user input as a string
    """

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
    """
    asks user what they would like the computer to do
    :return: None
    """

    prompt = False

    while prompt == False:

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

        elif "RUN" in user_res or "FILE" in user_res or "PROGRAM" in user_res:
            open_program()
            prompt = True

        elif "SONG" in user_res or "MUSIC" in user_res:
            play_music()
            prompt = True

        elif "HELP" in user_res:
             user_help()
             prompt = True

        elif "EXIT" in user_res:
            print "hi"
            exit_program()
            prompt = True

        else:
            print "invalid command"
            speak("invalid command")
            prompt = False


def email_prompt():
    """
    prompts user for if they want to send email
    :return: None
    """

    print "do you want to send an email"
    speak("do you want to send an email? ")
    ans = listen()
    print ans

    if ans == "yes":
        print "get ready to email:"
        speak("get ready to email")
        send_email()
    else:

        print ans
        print "okay, no email then"
        speak("okay, no email then")
        user_prompt()


def send_email():
    """
    connects to gmail server, sends email from users address to one of their contacts
    :return: None
    """

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

    server.login(user_dict[user], pass_dict[user])  # logs into the gmail server

    speak("who do you want to send this to")
    send_to = listen().upper()
    print send_to

    if send_to in contact_dict:

        speak("what do you want to say to" + contact_dict[send_to])
        msg = listen()
        print msg
        server.sendmail(user_dict[user], contact_dict[send_to], msg)
        print "email sent"
        speak("email sent")

    else:
        print "that name is not in your contacts "
        speak("that name is not in your contacts ")

    server.quit()
    user_prompt()


def joke():
    """
    ramdomly picks one of three different jokes and tells to  user
    :return: None
    """
    joke_num = randint(1, 3)

    if joke_num == 1:
        print"why are there fences in a grave yard? because people were dying to get in "
        speak("why are there fences in a grave yard?.. because people are dying to get in")

    elif joke_num == 2:
        print "how did the frog die? he kermit suicide"
        speak("how did the frog die?... he kermit suicide ")

    elif joke_num == 3:
        print "I sold my vacuum the other day, all it was doing was collecting dust "
        speak("I sold my vacuum the other day... all it was doing was collecting dust")


    user_prompt()

def date_time():
    """
    tells user what the date and time are
    :return: None
    """

    localtime = time.asctime(time.localtime(time.time()))
    print "the current time is: ", localtime
    speak("the current time is" + localtime)
    user_prompt()
    # tells user the date and time


def send_to_printer():
    """
    creates temporary file and prints text to the default printer
    :return: None
    """

    print "what do you want to print"
    speak("what do you want to print")
    ans = listen()
    print ans.upper

    filename = tempfile.mktemp(".txt")
    open(filename, "w").write(ans)
    win32api.ShellExecute(
            0,
            "print",
            filename,
            #
            # If this is None, the default printer will
            # be used anyway.
            #
            '/d:"%s"' % win32print.GetDefaultPrinter(),
            ".",
            0
    )

    # sends something to default printer
    print "sent", ans, "to printer"
    user_prompt()

def open_program():
    """
    opens a program of the users choice
    :return:
    """

    print "which program or file do you want to open?"
    speak("which program or file do you want to open?")
    ans = listen().upper()
    print ans

    if ans == "NOTEPAD":
        try:
            print "yes"
            os.startfile("C:\Users\Matthew\Desktop\openme.txt")

        except Exception, e:
            print "no"
            print str(e)

    elif ans == "SUBLIME TEXT":
        try:
            print "yes"
            os.startfile("C:\Program Files\Sublime Text 3\sublime_text.exe")

        except Exception, e:
            print"no"
            print str(e)

    user_prompt()

def play_music():
    """
    prompts user for which song they want to play and opens it
    :return: None
    """

    print "which song do you want to play"
    speak("which song do you want to play")
    ans = listen().upper()
    print ans

    if ans.upper() in music_dict:

        try:
            if ans == "SONG ONE":

                print "playing", ans
                speak("playing" + ans)
                os.startfile("C:\Users\Matthew\Desktop\song One.mp3") # fix space problem

            elif ans == "SONG TWO":
                print "playing", ans
                speak("playing" + ans)
                os.startfile("C\Users\Matthew\Desktop\song Two.mp3")

        except Exception, e:
            print"no"
            print str(e)

    else:
        print "that song is not on the list"
        speak("That song is not on the list ")
        play_music()


def user_help():
    """
    tells user what the program can do
    :return: None
    """

    print "You can send emails, print, check the time, ask for a joke, if mic cant pick up audio, try changing locations or checking internet connection"
    speak("You can send emails, print, check the time, ask for a joke," +
          " if mic cant pick up audio, try changing locations or checking internet connection")

    user_prompt()

def exit_program():
    """
    exits program by not calling the user prompt function at the end
    :return: None
    """

    print "exiting program, goodbye"
    speak("exiting program, goodbye")


def main():
    user_prompt()


main()
