# Requires PyAudio and PySpeech.
import speech_recognition as sr
from voice import Speak
import time
import Config
# Record Audio
# Gobals :

r = sr.Recognizer()


def listen(mode="",entity_mode=False):
   
    mode = Config.get("INPUT MODE")

    if mode=="TEXT":
                   
            return input("User   : ")

    if mode=="FIREBASE":
        Config.set("FIREBASE","ON")
        timeout = 5
        for i in range(timeout):
            msg = myfirebase.get_last_chat()
            if(msg==None):
                continue
            else:
                return msg
            time.sleep(1)
        return None;
    if mode=="LISTENING":
        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=800)
            print(r.recognize_google(audio))
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            Speak("Google Speech Recognition could not understand audio")
            return "ERROR"
        except sr.RequestError as e:
            Speak("Could not request results from Google Speech Recognition service; {0}".format(e))
            return "ERROR"
# def set_input_source(src):
#     global input_box
#     print(src)
#     input_box = src
#     print("Source Set")
if __name__ == "__main__":
    print(listen())