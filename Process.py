
import ast
import random
from threading import Lock
from voice import *
print("-[Loaded voice.py]")
from Actions import *
print("-[Loaded Actions.py]")
from EntityExtractor import Extractor
print("-[Loaded Extractor.py]")
Output = None
data_file_name = "Data.json"
def setOutput(out):
    global Output
    Output = out

    
class Process:
    def __init__(self):
        f = open(data_file_name)
        self.data_file = ast.literal_eval(f.read())
        self.extracated_ents = {}
    def start(self,intent_name,text):
        self.intent = self.data_file[intent_name]
        self.text = text
        # Event Check
        if not self.events():
            return
        # Entity Extraction
        self.entities = self.getEntities(self.intent['entities'],self.text)
        print("Extracted Entities:",self.entities)
        # Check if process is canceled
        if self.entities == "CANCELED":
            Speak(random.choice(["Cancelled","Process is canceled","As you wish"]))
            return
        # Pass entities and extecute action
        output = self.action(self.intent['action'],self.entities)
        if output==None:
            output = self.entities
        # [ Error or  Incomplete Action Ouputs ] ->  -1
        if output==-1:
            return 
        # Speak the response
        resp = self.response(self.intent['responses'],output)
        if resp!=None:
            Speak(resp)
    def events(self):
        try:
            e = self.intent['event']
            if e==[]:
                return True
            else:
                for i in e:
                    if i.endswith(")"):
                        print("setOutput( Event."+i+")")
                        exec("setOutput( Event."+i+")")
                    else:
                        print("setOutput( Event."+i+"() )")
                        exec("setOutput( Event."+i+"() )")
                return Output
        except Exception as e:
            print("Event",e)
    def getEntities(self,ents_list,text):
        E = Extractor(ents_list,text)
        output = E.getSpecifiedEntites()
        if output==None:
            return False
        print(output)
        self.extracated_ents = output
        return output
    def action(self,code="",parameters={}):
        global Output
        Output = None
        if code=="":
            if parameters!={}:
                Output=parameters 
            return Output

        try:
            # If function is statemet eg. os.system("notepad")
            if code[0]=="#":
                print(code)
                exec(code[1:])
            # If function needs a  thread lock eg. GUI automation(pyautiogui)
            elif code[0]=="*":
                th_lock = Lock()
                print("setOutput("+code[1:]+"())")
                exec("setOutput("+code[1:]+"())")
                th_lock.acquire()
            # If functions has no parameters
            elif parameters=={}:
                print("setOutput("+code+"())")
                exec("setOutput("+code+"())")
                return Output
            # If functions needs parameters
            elif parameters!={}:
                print("setOutput("+code+"("+str(parameters)+"))")
                exec("setOutput("+code+"("+str(parameters)+"))")
                return Output
        except Exception as e:
            print("Action did not found or error in action :"+code)
            print(e)
    def response(self,response_arr,ents):
        if response_arr==[]:
            return None
        resp = random.choice(response_arr)
        # Rendering {PERSON} -> Nikhil
        try:
            for i in ents:
                for j in ents[i]:
                    if type(j)==datetime.time:
                        j = j.strftime("%I:%M %p")
                    if type(j)==datetime.date:
                        j = str(j)
                    resp = resp.replace("{"+i+"}",j)
        except Exception as e:
            print("Respose:",e)
            pass
        return resp
def temp(param):
     print("Action Extecuted ",type(param))
     return True
if  __name__ == "__main__":
    P = Process()
    P.start("SEND EMAIL","remind me to go to office at 4 pm today")
    print(Output)
    # print(P.action("teddmp",{"TIME":"3:40 pm"}))
    # s = render({"TIME":"12:00 pm"},"The time is {TIME}")
    # print(s)
 
    