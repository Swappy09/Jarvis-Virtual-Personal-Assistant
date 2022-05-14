import psutil
import time
import threading
import os
from voice import notify,Speak
import socket


def Battery():
    global ThreadControl
    control = 1
    trigger = [1,1,1,1,1]
    while ThreadControl['Battery']['enable']:
        
        battery = psutil.sensors_battery()
        percent = battery.percent
        plugged = battery.power_plugged

        ThreadControl['Battery']['value'] = percent
        # State Changed
        if plugged and control == 1:
            left_time = (battery.secsleft / 60) // 60
            notify("Sir the Power Source is Back")
            control = 0
            trigger[0]=1
            trigger[1]=1
        if not plugged and control==0:
            notify("Power source Disconnected")
            control = 1
            trigger[2]= 1
            trigger[3]= 1
            trigger[4]= 1
        # On Charging 
        if percent >= 100 and plugged and trigger[0]==1 :
            notify("The Battery is fully charged to 100%")
            Speak(" I recommend to unplug the source now")
            trigger[0]=0
        elif percent > 95 and plugged and trigger[1]==1:
            notify("The Battery status is good now. You may unplug the source")
            trigger[1]=0
        # Off Charging
        if percent<=7 and (not plugged) and trigger[4]==1:
            notify("Sir the System may shutdown at any movement")
            Speak("Only 5% left .Need immediate power backup")    
            trigger[4]=0
        elif percent <= 10 and (not plugged) and trigger[3]==1:
            notify("We are running on very low battery power")
            Speak("10% left . I recommend to charge immediatly")    
            trigger[3]=0 
        elif percent<=35 and (not plugged) and trigger[2]==1:
            notify("The battery is reduced to {}%".format(percent))
            Speak("I recommend to charge it")
            trigger[2]=0   
        time.sleep(1)
    
def Online():
    global ThreadControl
    status = 0
    counter=0
    while ThreadControl['Online']['enable']:
        try:
            # connect to the host -- tells us if the host is actually reachable
            socket.create_connection(("www.google.com", 80))
            output=0
        except OSError:
            output=1
        if(output==0 and status==0):
            notify("Sir we  are back online")
            ThreadControl['Online']['status'] = True
            status=1
        if(output==1 and status==1):
            notify("Sir we lost the connection")
            ThreadControl['Online']['status'] = False
            status=0
        time.sleep(5)
        

def DetectUSB():
    import win32file
    global ThreadControl
    device_count = 0
    drive_list = []
    
    while ThreadControl['DetectUSB']['enable']:
        drive_list.clear()
        drivebits = win32file.GetLogicalDrives()
        for d in range(1, 26):
            mask = 1 << d
            if drivebits & mask:
                # here if the drive is at least there
                drname = '%c:\\' % chr(ord('A') + d)
                t = win32file.GetDriveType(drname)
                if t == win32file.DRIVE_REMOVABLE:
                    drive_list.append(drname)
        c = len(drive_list)
        # print(device_count,drive_list)
        if(c>0 and device_count!=c):
            notify(title="USB",text="Sir {0} usb Device detected".format(len(drive_list)))
            device_count = c
            ThreadControl["DetectUSB"]['devices'] = drive_list.copy()
        time.sleep(2)

# def FileTransfer():
#     import win32file
#     global ThreadControl
#     device_count = 0
#     drive_list = []
    
#     while ThreadControl['DetectUSB']['enable']:
#         drive_list.clear()
#         drivebits = win32file.GetLogicalDrives()
#         for d in range(1, 26):
#             mask = 1 << d
#             if drivebits & mask:
#                 # here if the drive is at least there
#                 drname = '%c:\\' % chr(ord('A') + d)
#                 t = win32file.GetDriveType(drname)
#                 if t == win32file.DRIVE_REMOVABLE:
#                     drive_list.append(drname)
#         c = len(drive_list)
#         # print(device_count,drive_list)
#         if(c>0 and device_count!=c):
#             notify(title="USB",text="Sir {0} usb Device detected".format(len(drive_list)))
#             device_count = c
#             ThreadControl["DetectUSB"]['devices'] = drive_list.copy()
#         time.sleep(2)
# ThreadControl Methods
def stopThread(thread_name):
    global ThreadControl
    if  thread_name in ThreadControl:
        ThreadControl[thread_name]['enable'] = False
    
def startThread(thread_name):
    global ThreadControl
    if  thread_name in ThreadControl:
        ThreadControl[thread_name]['enable'] = True
def startAllThreads():
    global ThreadControl
    for i in ThreadControl:
        T = threading.Thread(target=ThreadControl[i]['function'])
        T.setName(i)
        T.start()
def stopAllThreads():
    global ThreadControl
    for i in ThreadControl:
        ThreadControl[i]['enable']=False

ThreadControl = {
    "Battery": {
        'enable':True,
        'function':Battery,
        'value': -1 
    },
    "Online":{
        'enable':True,
        'function':Online,
        'status':False
    },
    "DetectUSB":{
        'enable':True,
        'function':DetectUSB,
        'devices':[]
    }
    
}


if __name__ == "__main__":
    startAllThreads()
    input(">>")
    stopAllThreads()
    # startThread("DetectUSB")
    # input(">>")
    # stopThreads("DetectUSB")

    
   
    
    


