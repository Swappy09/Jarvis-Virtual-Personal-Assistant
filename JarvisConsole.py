from threading import Thread
#Load Process--------------------------------------------------------------
def load_process():
    global Process
    import Process
    print("*[Process Module Loaded]")
T_Process = Thread(target=load_process)
T_Process.start()
#Load Classifier---------------------------------------------------------------
def load_classifer():
    global intentClassifier
    from Classifer_3 import intentClassifier
    print("*[Classifier Loaded]")
T_Classifier = Thread(target=load_classifer)
T_Classifier.start()
#-----------------------------------------------------------------------------
from voice import Speak
import Config
import myfirebase
import playsound

# Load Activation Model in Background -------------------------------------
def load():
    global is_activated,activation_stream,activation_run
    from jarvis_activate import is_activated,stream,run
    activation_stream = stream
    activation_run = run
    print("*[Voice Activation Loaded]")
# T = Thread(target=load)
# T.start()

from Speech import *
import ast

T_Process.join()


class Jarvis:
    def __init__(self):
        self.process = Process.Process()
        self.classify = intentClassifier  # Function
        self.context = {}                 # Format of Context -> [ { 'set_context': "intent_name" , "entities":{}" } , ......]
        
        
    def start(self):
        Speak("Jarvis at your service sir")
        Config.set("INPUT MODE","TEXT")
        while True:
                # if(Process.Event.isOnline()):
                #     text = listen('online')
                # else:
                    # text = listen('text')
                # text = listen('text')    
                text = listen()
                # Set the mode of input to jarvis
                if "firebase mode"==text:
                    Speak("Switching to Firebase mode")
                    Config.set("INPUT MODE","FIREBASE")
                    continue
                if(text=="listening mode"):
                    mode = 'listening'
                    Speak("Switching to Listening mode")
                    Config.set("INPUT MODE","LISTENING")
                    continue
                if(text=="text mode"):
                    Speak("Switching to text mode")
                    Config.set("INPUT MODE","TEXT")
                    mode = 'text'
                    continue
                if text == "ERROR" :
                    
                    Speak("Sir i am unable to hear you") 
                if text == None :
                    # print("Retrying for firebase")
                    continue
                if text == "exit" or text=="bye":
                   break 
                else:    
                    # print(text)
                        intent,self.context = self.classify(text,self.context)
                        print(intent,self.context)
                        if intent == None:
                            Speak("Unable to understand what you said")
                        else:
                            try:     
                                self.process.start(intent,text)
                            except Exception as e:
                                Speak("i found an internal error in my system:")
                                print(e)

   
if __name__ == "__main__":
    T_Classifier.join()
    Process.init()
    J = Jarvis()
    J.start()
    Process.terminate()

