from voice import Speak
import datetime
import os
import BackgroundThread
print("-[Loaded BackgroundThread.py]")
import webbrowser
import time
import Config
import socket
# def isOnline():
#     flag = os.system("ping www.google.com -c 1")
#     os.system("clear")
#     if flag==0:
#         os.system("clear")
#         return True
#     else:
#         return False   
def greet():
    T = datetime.datetime.now()
    t = int(T.strftime("%H"))
    m = int(T.strftime("%M"))
    d = T.strftime("%D") 
    if Config.get('JARVIS BOOT')==d:
        resp = ['Good to see you again sir','Welcome back Sir','Its nice to see you again sir']
        import random
        Speak(random.choice(resp))
        return False
    else:
        Config.set("JARVIS BOOT",d)
        if t in range(4,10):
            Speak("Its Good to see you on early morning sir")
            return True
        elif t in range(10,12):
            Speak("Good Morning Sir")
            return True
        elif t in range(12,17):
            Speak("Good Afternoon Sir")
            return True
        elif t in range(16,24):
            Speak("Good Evening Sir")
    return False
            
def startEvents():
    BackgroundThread.startAllThreads()
def bye():
    T = datetime.datetime.now()
    t = int(T.strftime("%H"))
    import random
    if t in range(4,17):
            Speak(random.choice(["Have a wonderfull good day Sir",'Enjoy the day Sir','Have a good day Sir']))
    elif t in range(17,22):
            Speak("Bye Sir")
    elif t in range(22,4):
        Speak(random.choice(["Good Night Sir",'Good Night have good sleep Sir','Bye Sir take a rest']))
    Config.set("FIREBASE","OFF")

    

def stopEvents():
    BackgroundThread.stopAllThreads()

# Prerequisites before Actions Performs ----------------------------
# Format :
# Returns True -> Satisfied
# Returns False -> Didn't Satisfied
#-------------------------------------------------------------------
def isOnline(speak=True):
    try:
            # connect to the host -- tells us if the host is actually reachable
            socket.create_connection(("www.google.com", 80))
            return True
    except OSError:
        if speak==True:
            Speak("Sir we need Internet Connection")

    return False
def checkAttributes(var_agrs,msg=""):
    try:
        for i in var_agrs:
            c = Config.get(i)
            print(c)
            if c == None:
                raise Exception
            if c == "":
                Speak(msg)
                break
        else:
            return True
    except:
        Speak("No such attributes",just_text=""+str(var_agrs))

    return False


def getBatteryLevel():
    return BackgroundThread.ThreadControl['Battery']['value']
def getIpAddress():
    import socket    
    hostname = socket.gethostname()    
    IPAddr = socket.gethostbyname(hostname)    
    print("Your Computer Name is:" + hostname)    
    print("Your Computer IP Address is:" + IPAddr)
if __name__=="__main__":
    print(checkAttributes(["EMAIL","EMAIL_PWD"],"Sir the credential are missing for sending email. Please check the Settings"))

