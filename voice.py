# import pyttsx
# engine = pyttsx.init()
# engine.say('Good morning.')
# engine.runAndWait()
# Voice multiline pending........

import os
from win10toast import ToastNotifier
import threading
import pyttsx3
import myfirebase
import Config
eng = pyttsx3.init()
thread_lock = threading.Lock()
notify_lock = threading.Lock()

def Speak(text="",just_text=""):
    try:
        thread_lock.acquire()
        try:
            print("Jarvis : "+text+""+just_text)
            if Config.get("FIREBASE")=="ON":
                myfirebase.append_chat(text+" "+just_text)
            # print("cmd:"+"voice -m \""+text+"\"")
            os.system("voice -m \""+text+"\"")
        except Exception as e:
            print("Error in voice:"+e)
    except:
        pass
    finally:
        thread_lock.release()

# def Speak(text):
#     try:
#         thread_lock.acquire()
#         try:
#             print(text)
#             if Config.get("FIREBASE")=="ON":
#                 myfirebase.append_chat(text)
#             eng.say(text)
#             eng.runAndWait()
#         except Exception as e:
#             print("Error in voice:"+e)
#     except:
#         pass
#     finally:
#         thread_lock.release()    
    
def conform(text):
    thread_lock.acquire()
    print(text)
    os.system("voice -m '"+text+"'")
    out = input(">>")
    if out=="Yes":
        return True
    else:
        return False
    thread_lock.release()
def notify(text="",duration=5,icon_path=None,title="Notification",just_text=""):
    try:
        toast = ToastNotifier()
        toast.show_toast(title=title,msg=text+" "+just_text,duration=duration,icon_path=icon_path,threaded=True)
        if Config.get("INPUT MODE")=="FIREBASE":
                myfirebase.send_notification(text+" "+just_text)
        Speak(text=text)
               
    except Exception as e:
        print("notify:",e)
        
    
    

if __name__ == "__main__":
    # Speak("Nikhil")
    # Speak("Allow me to introduce myself. I am Jarvis. A Artificial Desktop Assisstant made by Nikhil  Devarkonda. I am there to help you in ur daily task, i can also notify on your mobile phones to stay updated. Try saying What can you do for me. For more information read the docs.")
    notify("Charging is down")
