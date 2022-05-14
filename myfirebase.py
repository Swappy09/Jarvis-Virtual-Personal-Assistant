from  firebase import firebase

url  = 'https://jarvis-dddpfp.firebaseio.com/Jarvis/Chats/'
active = False
def append_chat(msg):
    global url
    try:
        fb  = firebase.FirebaseApplication(url,None)
        data = dict()
        data['Sender'] = "Jarvis"
        data['msg'] = msg
        result = fb.post("/Jarvis/Chats/",data)
        print("Sent:",msg)
        return True
    except Exception as e:
        print("Firebase Error:",e)
        return False
        
def get_last_chat():
    global url
    try: 
        fb = firebase.FirebaseApplication(url, None)
        result = fb.get('/Jarvis/Chats', '')
        l = list(result.values()) 
        if(l[-1]['Sender']=="Jarvis"):
            return None
        else:
            return l[-1]['msg']
    except Exception as e:
        print("Firebase Error",e)
        return None
def clear_chats():
    global url
    try: 
        fb = firebase.FirebaseApplication(url, None)
        fb.delete('/Jarvis/Chats/', '')
        result = fb.post("/Jarvis",'Chats','')
        return result
    except:
        return None
def send_notification(msg):
    # Send to single device.
    from pyfcm import FCMNotification
    push_service = FCMNotification(api_key="AAAACth0i78:APA91bFxgjTVUOnJ-OXDRHudZzpYPD4TFXwciGHe8E-oNR2gDyS-u7VR6YmPffcUxIFxhlHGussZHgzvNUZjW0eMp1k_Pc-5tdMzWzV7y7AkjlkUSUBelmaSD1Guc3mdlC6brSVwRzu9")
    registration_id = "ejXJ3rYDQreKZnbAYS1dAA:APA91bGqxu6TedvlyWR30HsXRffjwXjvOlWkhT59u5gvZmGBzXFCTV9yhJJ9ht7f3v16ML7Jd-QvsRivZZvLFlxhzcklYc7usAdY9c8jk7vR5UQkNPS2G1ylih14sEVeKscBWbTujMc0"
    message_title = "Jarvis"
    message_body = msg
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)


    print(result)
if __name__ == "__main__":
    print(send_notification("Battery Full"))
    # append_chat("Hello Sir")
    # print(clear_chats())
    pass
# result = get_chats()

# for i in result:
#     print(result[i])

