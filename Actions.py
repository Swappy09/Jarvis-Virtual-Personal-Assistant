import os
import pyautogui as py
import time
import Config
import datetime
import threading
import EntityExtractor
import Event
print("-[Loaded Event.py]")
from Speech import listen
from voice import notify
import ast
from voice import Speak
import random
from win32gui import GetForegroundWindow,ShowWindow,SetForegroundWindow,GetWindowText
import win32con 
import subprocess as sb
import random

# For Email 
import smtplib
import time
import imaplib
import email
import email.header

# Globals 
thread_locker = threading.Lock()
                      
class Personal:
     @staticmethod
     def my_actions():
         # Access Data file
         try:
             f = open("Data_1.json")
             action_list = ast.literal_eval(f.read())
             f.close()
             list_ = list( i for i in action_list.keys()  if not i.startswith("#") and not i.startswith("-") )
             work_list = "\n".join(list_)
             f = open("Tasks.txt",'w')
             f.write(work_list)
             f.close()
             Speak("Here is the full list:",just_text=work_list)
             os.system("start notepad Tasks.txt")
             Speak("Try saying:")
             Speak(action_list[random.choice(list_[:10])]['training'][0])
             Speak(action_list[random.choice(list_[10:15])]['training'][0])
             Speak("or "+action_list[random.choice(list_[15:])]['training'][0])
         except Exception as e:
             print(e)



class Time:
    @staticmethod
    def now():
        global Output
        import datetime
        s = datetime.datetime.now()
        s = datetime.datetime.ctime(s)[10:16]
        #Speak(s)
        # Output = s
        return {"TIME":[s]}
class Date:
    @staticmethod
    def tell():
        dt = datetime.date.today()
        # print("It's ", text)
        # Speak("It's {}".format(text))
        return {"DATE":[dt]}
class Video:
    @staticmethod
    def play():
        py.press("win")
        time.sleep(1)
        py.typewrite("folders:Videos")
        time.sleep(2)
        py.press('enter')
        time.sleep(2)
        py.hotkey('ctrl', 'a')
        time.sleep(1)
        py.press('enter')

    def pause():
        py.press('playpause')

    def next():
        py.press('nexttrack')

    def previous():
        py.press('prevtrack')
class Screenshot:
    def takeScreenshot():
        no = str(datetime.datetime.now())
        no = no.replace("-", "_")
        no = no.replace(":", "_")
        no = no.replace(".", "_")
        no = no.replace(" ","_")
        # print(no)
        py.screenshot("{}{}.png".format(Config.get('SCREENSHOT PATH'),no))
        os.system("{}{}.png".format(Config.get('SCREENSHOT PATH'),no))

def takePhoto():
    os.system("start microsoft.windows.camera:")
    time.sleep(2)
    Speak("Say cheeeeese.")
    time.sleep(2)
    py.press('enter')
def read_text():
    import pyperclip
    txt = pyperclip.paste()
    Speak(txt.replace("\n",". "))
def starting_screen():
    if(Event.isOnline(speak=False)):
        # Weather
        os.system("start bingweather:")
        time.sleep(1)
        py.keyDown('win')
        py.press('left')
        py.press('up')
        py.keyUp('win')
        Extra
        # News 
        os.system("start bingnews:")
        time.sleep(1)
        py.hotkey('win','right')
        time.sleep(1)
        py.press('esc')
        Extra.tell_weather()
        Extra.tell_news()
    Extra.tell_day_event({"DATE":[datetime.datetime.now()]},no_event_tell=True)
def open_app_and_tag(param):
    # ["name","cmd/path","type(APP/TAG)"]
    if param['APP|TAG'] != []:
        if param['APP|TAG'][2] == "APP" :
            Speak("Opening "+param['APP|TAG'][0])
            os.system("start "+param['APP|TAG'][1])
        else:
            Speak("Opening "+param['APP|TAG'][0])
            # Check if directory or file
            if os.path.isdir(param['APP|TAG'][1].strip("\"")):
                print("explorer "+param['APP|TAG'][1])
                os.system("start explorer "+param['APP|TAG'][1])
            else:
                os.system("start "+param['APP|TAG'][1])
    else:
        Speak("I don't know how the open that app or file")
def is_new_day(param):
    if 'morning' in param['TEXT'][0].lower():
        Speak("Good Morning Sir")
    elif 'afternoon' in param['TEXT'][0].lower():
        Speak("Good Afternoon Sir")
    elif 'evening' in param['TEXT'][0].lower():
        Speak("Good Evening Sir")
    d = datetime.datetime.now().strftime("%D")    
    if Config.get('JARVIS BOOT') != d:
        starting_screen()
        Config.set('JARVIS BOOT',d)
def default_google_search(param={}):
    if Event.isOnline(speak=False):
        import webbrowser
        words = "+".join(param['TEXT'][0].split(" "))
        Speak("Searching on web Sir")
        webbrowser.open_new('https://www.google.com/search?q={}'.format(words))
        return -1
def locate_on_map(param):
    import webbrowser
    Address = param['TEXT'][0]
    if param['LOCATION'] != []:
        Address = param['LOCATION'][0]
    Speak("Finding on Map Sir")
    webbrowser.open("https://www.google.com/maps/?q={}".format(Address))   
def add_contact():
    Speak(random.choice(['Go ahead and add details','Please fill the details Sir','Here is the form. Fill it']))
    os.system('python add_contact_GUI.py')
    Speak(random.choice(['Contact Saved','Contact Added in Database']))
def remember(param):
    #[ TEXT ]
    token = param['TEXT'][0].split(" ")
    for index,i in enumerate(token):
        if 'that' == i.lower()  or 'remember' == i.lower():
            token[index]=""
    if len(token) >= 2 : 
        param['TEXT'] = " ".join(token)
        print(param['TEXT'])
        f = open('remembers.list')
        list_ = ast.literal_eval(f.read())
        list_.insert(0,param['TEXT'])
        f.close()
        f = open('remembers.list','w')
        f.write(str(list_))
        f.close()
    else:
        Speak("Context is unclear sir")
        return -1
def show_remembered_things():
    temp = open("Remember_Things.txt",'w')
    f = open('remembers.list')
    list_ = ast.literal_eval(f.read())
    f.close()
    if len(list_)==0:
        Speak("Sir you did not say anything to remember me")
        return -1
    temp.write("*"*100+"\n")
    for i in list_:
        s = "[*] "+i
        Speak(just_text=s)
        temp.write(s+"\n")
    temp.write("*"*100+"\n")
    temp.close()
    os.system('start notepad Remember_Things.txt')
        
    


class ShowFiles:
    @staticmethod
    def documents():
        py.press('win')
        time.sleep(2)
        py.typewrite("folders:Documents")
        time.sleep(2)
        py.press('enter')
    def photos(param={}):
        os.system("start ms-photos:")
        
class Extra:
    @staticmethod
    def create_qrcode():
        Speak("Creating Qrcode of copied text")
        import qrcode
        import pyperclip
        img = qrcode.make(pyperclip.paste())
        print(img.size)
        img.save('Screenshots/qrcode.png')
        os.system('"start Screenshots/qrcode.png"')
    def tell_weather(para={'LOCATION':[]}):
        try:
                import requests, json,webbrowser
                
                resp = ["Wait a second sir", "I am gathering  information"]
                Speak(random.choice(resp))
                api_key = "bb89f3e63dd62d3cf4fba03842b4b6ea"
                base_url = "http://api.openweathermap.org/data/2.5/weather?"

                if para["LOCATION"] == []:
                    city_name = "Solapur"
                else:
                    city_name = para["LOCATION"][0]

                complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                response = requests.get(complete_url)

                x = response.json()
                print(x)

                if x["cod"] != "404":
                    y = x["main"]
                    kelvin_temp = y["temp"]
                    celcious = int(kelvin_temp - 273.15)    #kelvin -> celcious
                    current_pressure = y["pressure"]
                    current_humidiy = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]
                    Speak("Sir, Its {} degree celcious in {}.".format(str(celcious), city_name))
                    Speak("and weather is {} . humidity is {} percentage"
                        .format(str(weather_description),str(current_humidiy)))

                        # "\n atmospheric pressure (in hPa unit) = " +
                        #           str(current_pressure) +
                        # "\n humidity (in percentage) = " +
                        #           str(current_humidiy) +
                        # "\n description = " +
                        #           str(weather_description))
                else:
                    Speak("City Not Found ")
        except:
            Speak("Cannot Fetch weather information .This might be due to internet problem")
            return -1
    def tell_news(param={}):
        try:
            import requests, json,webbrowser
            from bs4 import BeautifulSoup
            url = 'https://www.ndtv.com/'
            webbrowser.open(url)
            # py.sleep(2)
            # py.scroll(10, 0, 100)
            page = requests.get(url)
            # print(page.content)
            soup = BeautifulSoup(page.text, 'html.parser')
            # print(soup.prettify())
            # table = soup.find_all('h3', class_='newcont')
            # print("Table", table)
            c = 0
            headlines = []
            Speak("Heres top headlines from NDTV")    
            for head in soup.find_all(['h1', 'h3']):
            
                if c < 6:
                    # print(head.text.strip())
                    headlines.append(head.text.strip())
                    c += 1
            
            for i in headlines:
                Speak(i)
        except Exception as e:
            print("You are not connected to internet ",e)
    def tag_it(param={}):
        text = param['TEXT'][0].lower()
        # Remove words
        words = ['this','it','as','remember','the','tag','file','folder']
        for i in words:
            text = text.replace(i,"")
        print("Started")
        Speak("I hope explorer is open and file is selected")
        py.hotkey('alt','h')
        time.sleep(1)
        py.typewrite('cp')
        import pyperclip
        path = pyperclip.paste()
        print("PATH:",path)
        # Validate
        if os.path.isdir(path.strip("\"")) or os.path.isfile(path.strip("\"")) :
            notify(title="TAG",text=text+" Tagged",just_text=path)
            # DISPLAY GUI BOX -- > Atfer 
            Config.set_tag(text,path)
        else:
            Speak("I think you didn't select file properly Sir")
    def add_event(param={}):
        try:
            month = param['DATE'][0].strftime("%b")
            day = int(param['DATE'][0].strftime("%d"))
            # Key ['Jan 6']
            key = month+" "+str(day)
            f = open("calender_events.json")
            events = ast.literal_eval(f.read())
            f.close()
            if key in events:
                events[key] = events[key]+","+param['EVENT'][0]
            else:
                events[key] = param['EVENT'][0]
            import json
            events_j = json.dumps(events)
            f = open("calender_events.json",'w')
            f.write(events_j)
            f.close()
            # print(events_j)
        except Exception as e:
            print("Error in calender",e)
    def tell_day_event(param={},no_event_tell=False):
        try:
            month = param['DATE'][0].strftime("%b")
            day = int(param['DATE'][0].strftime("%d"))
            # Key ['Jan 6']
            key = month+" "+str(day)
            f = open("calender_events.json")
            events = ast.literal_eval(f.read())
            f.close()
            if key in events:
                Speak("Events for the day: "+str(param['DATE'][0].strftime("%D")))
                Speak(events[key])
            else:
                if no_event_tell==True:
                    return
                resp = ["Nothing Special Sir","No Event Found for this day ","No Events for this day"]
                Speak(random.choice(resp))
        except Exception as e:
            print("Error in calender",e)

class MusicPlayer:
    @staticmethod 
    def play_music():
        try:
            path = Config.get('SONG PATH')
            files = os.listdir(path)
            mp3_files = [ f for f in files if f.endswith(".mp3") ]
            mp3_selected = random.choice(mp3_files) 
            print(mp3_selected)
            mp3_selected = path+mp3_selected
            os.system('''start "explorer.exe shell:C:\Program Files\WindowsApps\Microsoft.ZuneMusic_3.6.25021.0_x64__8wekyb3d8bbwe!Microsoft.ZuneMusic" "{}"'''.format(mp3_selected))
        except:
            Speak("It seems that you specify path or folder is empty")
    def pause():
        py.press("playpause")
    def resume():
        py.press("playpause")
    def next():
        py.press("nexttrack")
    def previous():
        py.press("prevtrack")
    def resume():
        py.press("playpause")
class System:
    @staticmethod 
    def shutdown(param={}):
        sec = 5
        Speak("System will shutdown in 10 seconds")
        terminate()
        os.system("shutdown /s /t 5 ")
    @staticmethod 
    def restart(param={}):
        
        Speak("System restart in 5 seconds")
        terminate()
        os.system("shutdown /r /t  5 ")
    @staticmethod     
    def sleep(param={}):
        Speak(random.choice(["System going in sleep mode",'Sleeping.','As you wish Sir','System sleeping.']))
        py.hotkey("win","x")
        time.sleep(0.5)
        py.press("u")
        py.press("s")
    @staticmethod 
    def hibernate(param={}):
        sec = 5
        # if param['TIME'] != [] :
        #     sec = param['TIME'][0]
        # os.system("shutdown /h /t {} ".format(sec))
    @staticmethod 
    def logOff(param={}):
        sec = 5
        if param['TIME'] != [] :
            sec = param['TIME'][0]
        os.system("shutdown /s /t {} ".format(sec))
    def tell_battery_status():
        import psutil
        battery = psutil.sensors_battery()
        percent = battery.percent
        plugged = battery.power_plugged
        if(plugged):
            plugged = " and its on Charging "
        else:
            plugged = ""
        notify(title="Battery",text="Sir the battery level is "+str(percent)+" "+plugged)
    def locate_usb():
        import win32file
        drive_list = []
        drivebits = win32file.GetLogicalDrives()
        for d in range(1, 26):
            mask = 1 << d
            if drivebits & mask:
                # here if the drive is at least there
                drname = '%c:\\' % chr(ord('A') + d)
                t = win32file.GetDriveType(drname)
                if t == win32file.DRIVE_REMOVABLE:
                    drive_list.append(drname)
        print(len(drive_list))
        notify(title="USB",text="Sir {0} usb detected".format(len(drive_list)))
    def eject_usb(drive_name):
        os.system("start powershell")
        time.sleep(2)
        cmd = '''$driveEject = New-Object -comObject Shell.Application ; $driveEject.Namespace(17).ParseName('{}:').InvokeVerb("Eject")'''.format(drive_name)
        py.typewrite(cmd+"\n")
        time.sleep(1)
        py.typewrite("exit\n")
    def show_sys_info():
        import platform
        import psutil
        py.press('win')
        py.sleep(2)
        py.typewrite("System Information")
        py.sleep(2)
        py.press('enter')
        name = platform.uname()
        Speak("Sir, your System is running on {} and version is {}".format(str(name.system), str(name.version)))
        # print("Machine = ",name.machine)
        Speak("Processor is {}".format(str(name.processor)))
        Speak("Systems Boot time is {}".format(datetime.datetime.fromtimestamp(psutil.boot_time())))

        memory = psutil.virtual_memory()
        Speak("Total Memory in System is {} out of {} is free".format(System.get_size(memory.total),
                                                                      System.get_size(memory.available)))
        # Speak("Memory used is {} ".format(System.get_size(memory.used)))
        # Speak("Memory free is {}".format(System.get_size(memory.available)))
        # print("Available = ",System.get_size(memory.available))
        # print("Used = ", System.get_size(memory.used))
        # print("Percentage = ", memory.percent)

        total = 0
        used = 0
        free = 0
        disk = psutil.disk_partitions()
        for d in disk:
            # print("Device = ",d.device)
            # print("Type = ", d.fstype)
            try:
                part_usg = psutil.disk_usage(d.mountpoint)
            except:
                continue
            # print("Total = ", System.get_size(part_usg.total))
            total += part_usg.total
            # print("Used = ", System.get_size(part_usg.used))
            used += part_usg.used
            # print("Available = ", System.get_size(part_usg.free))
            free += part_usg.free
            # print("Percentage = ", part_usg.percent)

        Speak("Total disk space is {} out of {} is available".format(str(System.get_size(total)),
                                                                     str(System.get_size(free))))
        # Speak("Used disk space is {}".format(str(System.get_size(used))))
        # Speak("Available free disk space is {}".format(System.get_size(free)))
    def get_size(bytes, suffix="B"):
        fact = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < fact:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= fact

# class Wifi:
#     @staticmethod 
#     def on_off_wifi(para):

#         # py.hotkey("win","r")
#         # py.typewrite("cmd")
#         # py.hotkey("ctrl","shift","enter")
#         # time.sleep(2)
#         # py.typewrite("netsh interface set interface 'Wifi' disabled"))
#         os.system("netsh interface set interface 'Wifi' disabled")
class Window:
    win_list = []
    opreation_running = None
    window_hwd = 0
    last_window = 0
    win_for_launch = None
    thread_stop = True
    cmd = '''Add-Type @"
   using System;
  using System.Runtime.InteropServices;
  public class SFW {
     [DllImport("user32.dll")]
     [return: MarshalAs(UnmanagedType.Bool)]
     public static extern bool SetForegroundWindow(IntPtr hWnd);
  }
"@\n'''
    cmd_hwd = '[SFW]::SetForegroundWindow({})'
    @staticmethod
    def start_thread():
        Window.thread_stop = False
        threading.Thread(target=Window.windowThread).start()
    def minimize():
        Window.window_hwd = GetForegroundWindow()
        ShowWindow(Window.window_hwd, win32con.SW_MINIMIZE)
    def maximize():
        ShowWindow(Window.window_hwd, win32con.SW_RESTORE)
    def move():
        py.hotkey("alt","space")
        py.press("m")
        py.press("up",presses=5)
        time.sleep(1)
        py.press("down",presses=5)
    def operation_notify(): 
        for i in Window.win_list:
            if i.find('complete')!=-1:
                    Window.opreation_running = "YES"
                    break
        else:
            if Window.opreation_running=="YES":
                notify("File Transfer Completed")
                Window.opreation_running = None

    def windowThread():
        import ctypes
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))    
        curr = GetForegroundWindow()
        while not Window.thread_stop:
            # Store Current windows -> winlist
            Window.win_list.clear()
            EnumWindows(EnumWindowsProc(Window.foreach_window), 0)
            # If any operation found copying,etc
            Window.operation_notify()
            # 
            w = GetForegroundWindow()
            if curr != w :
                # print(w,GetWindowText(w))
                Window.last_window = curr
                curr = w
            time.sleep(1)
        
    def previous_window():
        sb.check_call(['powershell',Window.cmd+Window.cmd_hwd.format(Window.last_window)])
        ShowWindow(Window.last_window, win32con.SW_RESTORE)
    def close():
        pass
    def arrange():
        pass
    def foreach_window(hwnd, lParam):
            import ctypes
            IsWindowVisible = ctypes.windll.user32.IsWindowVisible       
            GetWindowText = ctypes.windll.user32.GetWindowTextW
            GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
            if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
                if buff.value!='':
                    Window.win_list.append(buff.value)
                # For launchning if window exists
                # if((buff.value.lower()).find(Window.win_for_launch)):
                #     print(Window.cmd+Window.cmd_hwd.format(hwnd))
                #     sb.check_call(['powershell',Window.cmd+Window.cmd_hwd.format(hwnd)])
                #     ShowWindow(Window.last_window, win32con.SW_RESTORE)
            return True
    def isOpen(window_name,duration_to_check=1,launch=False):
        import ctypes
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))    
        if(launch):
            Window.win_for_launch = window_name
        for i in range(duration_to_check):
            Window.win_list.clear()
            EnumWindows(EnumWindowsProc(Window.foreach_window), 0)
            for win in Window.win_list:
                if (win.lower()).find(window_name)!=-1:
                    return True
            print(Window.win_list)
            time.sleep(1)
        return False       
class Desktop:
    @staticmethod 
    def create():
        py.hotkey("ctrl","win","d")
    def switch_previous():
        py.hotkey("ctrl","win","left")
    def switch_next():
        py.hotkey("ctrl","win","right")
    def switch_to(param):
        py.hotkey("win","tab")
    def setWallpaper(param):
        path = param['FILE']
        if '\n' in path :
            print("Select only one")
            return
        if path == pervious_clipboard:
            print("Please Select the file")
            return
        if path[:-1].endswith(".jpg") or path[:-1].endswith(".png"):
            cmd = """ Set-ItemProperty -path 'HKCU:\Control Panel\Desktop\' -name wallpaper -value {} """
            sb.call(["powershell",cmd.format(path)+"; rundll32.exe user32.dll, UpdatePerUserSystemParameters, 1, True"])
            print(cmd.format(path))
            pervious_clipboard = path
        else:
            print("File not supported")
# Hardware Section ********************************************************'
class Volume:
    @staticmethod
    def set_volume(param):
        # Volume limit 65535
        if param['VALUE']!=[]:
            param['VALUE'] = param['VALUE'][0]
            if param['VALUE'] == "+" :
                # increment by default 20% 
                os.system("nircmd.exe changesysvolume 13107")
            elif param['VALUE'] == "-" :
                # decrement by default 20%
                os.system("nircmd.exe changesysvolume -13107")
            elif param['VALUE'].startswith("+") :
                v = ( int(param['VALUE'][1:])*65535 ) // 100
                os.system("nircmd.exe changesysvolume {0} ".format(v))
            elif param['VALUE'].startswith("-") :
                v = ( int(param['VALUE'][1:])*65535 ) // 100
                os.system("nircmd.exe changesysvolume -{0} ".format(v))
            elif param['VALUE'].startswith("=") :
                v = ( int(param['VALUE'][1:])*65535 ) // 100
                os.system("nircmd.exe setsysvolume {0} ".format(v))
    def mute_volume():
        os.system("nircmd.exe mutesysvolume 1")
    def unmute_volume():
        os.system("nircmd.exe mutesysvolume 0")
class Brightness:
    @staticmethod
    def set_brightness(param):
        current = os.popen("powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness").read()
        current = int(current)
        value = 0
        cmd = "powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness({0},{1})"
        if param['VALUE']!=[]:
            param['VALUE'] = param['VALUE'][0]
            if param['VALUE'] == "+" :
                # increment by default 20
                value = current+20
            elif param['VALUE'] == "-" :
                # decrement by default 20%
                value = current-20
            elif param['VALUE'].startswith("+") :
                value = current+int(param["VALUE"][1:])
            elif param['VALUE'].startswith("-") :
                value = current-int(param["VALUE"][1:])
            elif param['VALUE'].startswith("=") :
                value=int(param["VALUE"][1:])
            # Limiting values between 0 - 100
            if value < 0:
                value = 0
            if value > 100:
                value = 100
            
            os.system(cmd.format(1,value))    
class Network:
    @staticmethod
    def tell_my_ip():
        import socket    
        hostname = socket.gethostname()    
        IPAddr = socket.gethostbyname(hostname)       
        print("Your Computer IP Address is:" + IPAddr)
        if(IPAddr=="127.0.0.1"):
            Speak("Sir we are in the localhost")
        else:
            notify(title="IP Address",text="Sir your IP Address is "+IPAddr,duration=10)    
class Wifi:
    @staticmethod 
    def on_off_wifi(para):

        # py.hotkey("win","r")
        # py.typewrite("cmd")
        # py.hotkey("ctrl","shift","enter")
        # time.sleep(2)
        # py.typewrite("netsh interface set interface 'Wifi' disabled"))
        os.system("netsh interface set interface 'Wifi' disabled")
class SnipAndDetect:
     thread_stop = True
     @staticmethod
     def start_thread():
          pass
     def scanner():
          while not SnipAndDetect.thread_stop :
               pass
     def snip():
          Speak(random.choice(["Capturing Screen.","Mark the region","Go ahead and snip a section","Screen Capturing Ready"]))
          if os.system("python snipping_tool.py Screenshots/snipped.png") == 0 :
               Speak(random.choice(["Ok i will notify you if i see some changes","Sure if i detect something i will inform you Sir"]))
               while py.locateOnScreen("Screenshots/snipped.png") != None :
                    time.sleep(1)
               res = random.choice(["Sir i detected some changes","I found that something is changed on Screen","Changes found in marked region","It appears that snipped section is no longer"])
               notify(res)
          else:
               Speak("You didn't snipped it correctly sir")
# Threads Classes *********************************************************   
class Reminder:
    thread_stop = False
    reminder_list = []
    @staticmethod
    def start_thread():
        f = open('reminders.list')
        Reminder.reminder_list = ast.literal_eval(f.read())
        f.close()
        threading.Thread(target=Reminder.running).start()
    def set(param):
        # [ TIME[ %H:%M:%S ],DATE[ %D ], MESSAGE ]
        d = {}
        d['TIME'] = param["TIME"][0].strftime("%H:%M")
        d['DATE'] = param['DATE'][0].strftime("%D")
        d['MESSAGE'] = param['MESSAGE'][0]
        Reminder.reminder_list.append(d)
        f = open("reminders.list",'w')
        f.write(str(Reminder.reminder_list))
        f.close()
    def running():
        import playsound
        while not Reminder.thread_stop:
            current_time = datetime.datetime.now()
            for index,i in enumerate(Reminder.reminder_list):
                if i['DATE'] == current_time.strftime("%D"):
                    if i['TIME'] == current_time.strftime("%H:%M"):
                        Speak("Sir your reminder")
                        notify(title="Reminder",just_text=i['MESSAGE'],duration=10)
                        playsound.playsound(Config.get('ALARM SOUND'))
                        break
            else:
                continue
            # Write to File Again
            Reminder.reminder_list.pop(index)
            f = open("reminders.list",'w')
            f.write(str(Reminder.reminder_list))
            f.close()
class Alarm:
    alarm_list = []
    thread_stop = False
    @staticmethod
    def start_thread():
        f = open("alarms.list")
        Alarm.alarm_list = ast.literal_eval(f.read())
        f.close()
        t = threading.Thread(target=Alarm.running)
        t.start()
    @staticmethod
    def set_alarm(param):
        add_time = lambda t1,t2: t1+datetime.timedelta(hours=t2.hour,minutes=t2.minute,seconds=t2.second)
        if param['TIME'][1]!=None :
            param['TIME'][0] = add_time(datetime.datetime.now(),param['TIME'][1])
        # Set Alarm Details
        alarm_time = param['TIME'][0].strftime("%H:%M")
        new_alarm = {}
        new_alarm['id']=len(Alarm.alarm_list)+1
        new_alarm['TIME']= alarm_time
        if param['MESSAGE'] != []:
            new_alarm['MESSAGE'] = param['MESSAGE'][0]
        else:
            new_alarm['MESSAGE'] = "Your Alarm Sir"
        # Add to Running Alarm List
        Alarm.alarm_list.append(new_alarm)
        # Store Alarm in File
        f = open("alarms.list",'w')
        f.write(str(Alarm.alarm_list))
        f.close()
    def running():
        while not Alarm.thread_stop:
            alarm_tiggered = False
            # Go through each index number
            for i in range(len(Alarm.alarm_list)):
                current_time = datetime.datetime.now().strftime("%H:%M") # --> 12:45
                # print(current_time)
                if Alarm.alarm_list[i]['TIME']==current_time :
                    notify(title="Alarm:",text=Alarm.alarm_list[i]["MESSAGE"],just_text=" [Alarm]")
                    print("Your Alarm : ",Alarm.alarm_list[i]['MESSAGE'])
                    import playsound
                    playsound.playsound(Config.get('ALARM SOUND'))
                    alarm_tiggered = True
                    break
            # if alarm was tiggered -> remove that alarm from list and file
            if alarm_tiggered:
                alarm_tiggered = False
                Alarm.alarm_list.pop(i)
                # Store Alarm in File
                f = open("alarms.list",'w')
                f.write(str(Alarm.alarm_list))
                f.close()
            # print("Alarm working.",)
            time.sleep(1)
class Email:
    last_email_time = ""
    last_email = None
    thread_stop = True
    @staticmethod
    def start_thread():
        Email.thread_stop = False
        threading.Thread(target=Email.check_thread).start()
    def check_thread():
        print("Email checking started")
        while not Email.thread_stop:
            if not Event.isOnline(speak=False) :
                time.sleep(5)
                continue
            # GET ONLY ONE LATEST EMAIL
            mails = Email.check_for_email(1)
            if mails!=None:
                if len(mails)==0:
                    Speak("We not no new emails sir")
                else:
                    # Checking we this email was spoke before
                    if Email.last_email_time!=mails[0]['DATE'] :
                        Speak("Sir we got an email from "+mails[0]['EMAIL_NAME'])
                        notify(title=mails[0]['EMAIL_NAME'],just_text=mails[0]['SUBJECT'])
                        Email.last_email_time = mails[0]['DATE']
                        Email.last_email = mails[0]
            # print("Emai Check Runing ",mails)
            time.sleep(10)
    def reply_incoming_email():
        # GUI Email Box Launch
        param = {'EMAIL_ADDRESS':[],"MESSAGE":[],'SUBJECT':['Subject:\n']}
        #
        if Email.last_email != None :
            Email.last_email['MESSAGE'] = []
            return Email.send_email(Email.last_email)
        return Email.send_email(param)
    def show_emails():
        # Open Website of Gmail  
        import webbrowser
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox",autoraise=True) 
    def send_email(param={}):
        import ssl
        port , smtp_server  =  465 , "smtp.gmail.com"
        # Show Email GUI Box
        # Take Neccessray Details
        while True:
            if param['EMAIL_ADDRESS']==[]:
                Speak("to whom do you want to send it?")
                addr = EntityExtractor.extractMail(listen())        
                if addr==[]:
                    Speak("I could not found any one in Contacts")
                    continue
                else:
                    param['EMAIL_ADDRESS'] = [addr]
            if param['MESSAGE']==[]:
                Speak("Whats the message?")
                msg = listen()
                if msg==None:
                    Speak("I could not find any message")
                    continue
                else:
                    param['MESSAGE']=[msg]
                    break
            else:
                break
                
        # Send mail
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(Config.get("EMAIL"),Config.get('EMAIL_PWD'))
                server.sendmail(Config.get("EMAIL"),param['EMAIL_ADDRESS'][0],param["MESSAGE"][0])
        except Exception as e:
            Speak("Someting went wrong Please re try again")
            if Config.get("EMAIL")=="" or Config.get("EMAIL_PWD")=="":
                Speak("Sir your credential are missing.Go ot settings")
            return -1
        
        return param

    def check_for_email(show_mail=3): 
        try:
            mail_list = []
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(Config.get('EMAIL'),Config.get('EMAIL_PWD'))
            mail.select('inbox')
            type, data = mail.search(None, 'All')
            mail_ids = data[0]
            id_list = mail_ids.split()   
            typ, data = mail.fetch(id_list[-show_mail], '(RFC822)' )
            for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(str(response_part[1],encoding='utf-8'))
                        email_subject, encoding = email.header.decode_header(msg['subject'])[0]
                        email_from , encoding = email.header.decode_header(msg['from'])[0]
                        email_date , encoding = email.header.decode_header(msg['date'])[0]
                        if isinstance(email_subject,bytes):
                            email_subject = str(email_subject,encoding='utf-8')
                        # Printing
                        # print('From : ['+email_from+']')
                        # print('Subject : ',email_subject)
                        mail_info = dict()
                        mail_info['EMAIL_NAME'] = email_from.split('<')[0]
                        mail_info['EMAIL_ADDRESS'] = email_from.split('<')[1][:-1]
                        mail_info['SUBJECT'] = email_subject
                        mail_info['DATE'] = email_date
                        mail_list.append(mail_info)
                        
            return mail_list
        except Exception as  e:
            # print("Error-Email_Read:",e)
            return None

# Controlling all the Threads and Events : Start and Stop *****************
def start_threads():
    Event.startEvents()
    Alarm.start_thread()
    Window.start_thread()
    Reminder.start_thread()
    Email.start_thread()
def init():
    t = Event.greet()
    start_threads()
    if t:
        starting_screen()
def terminate():
    Event.bye()
    Event.stopEvents()
    Alarm.thread_stop  = True
    Window.thread_stop = True
    Email.thread_stop  = True
    Reminder.thread_stop = True
if __name__ == "__main__":
    # Wifi.on_off_wifi("")
    # SnipAndDetect.snip()
    # add_contact()
    # init()
    # input(">>>>")
    # print(remember({"TEXT":["remember that Its an event today"]}))
    # show_remembered_things()
    # Reminder.start_thread()
    # Reminder.set({'DATE':[datetime.datetime.now()],'TIME':[datetime.datetime(1900, 1, 1, 15, 0), datetime.datetime(1, 1, 1, 0, 15)],"MESSAGE":["Wake Up"]})
    # terminate()
    # Email.send_email({'SENDER':"nikhildev0076@gmail.com","MESSAGE":"HI is is the Jarvis Test2"})
    # time.sleep(5)
    # # Extra.tag_it({'TEXT':["web project"]})
    # open_app_and_tag({"APP|TAG":['softwares', '"E:\\SOFWARES"', 'TAG']})
    # Personal.my_actions()
    # starting_screen()
    pass
    
