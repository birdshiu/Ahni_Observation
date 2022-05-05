import requests
from datetime import datetime
import os
import time

#record last time take image
last_minute=-1
last_hour=-1

# take a image, save in current folder, file name is ahni.jpg
def take_image():
    #https://lbhtran.github.io/Camera-setting-and-photo-taking-schedule-to-get-the-best-result/
    command='sudo fswebcam -D 2 -S 20 -r 1280x720 --no-banner ./ahni.jpg'
    os.system(command)

#send image to line notify 
def send_line_message():
    token='my token'
    url='https://notify-api.line.me/api/notify'
    headers={
        'Authorization':'Bearer '+token
    }
    #a space
    data={
        'message':' '
    }
    image=open('./ahni.jpg', 'rb')
    imageFile={'imageFile':image}
    requests.post(url, headers=headers, data=data, files=imageFile)

#check if now can execute, program will execute every 'number' minute
def can_act_now(number):
    global last_minute
    global last_hour
    
    now=datetime.now()
    hour=now.hour
    minute=now.minute

    #run from 5am to 6pm
    if(hour < 5 or hour > 18):
        return False
        
    if(minute % number !=0):
        return False
        
    if(not(last_hour == hour and last_minute == minute)):
        last_hour=hour
        last_minute=minute
        return True
    else:
        return False

if __name__ == '__main__':
    while True:
        #just prevent program stop if any error occur
        try:
            #take image and send every 10 minutes
            if(can_act_now(10)):
                take_image()
                send_line_message()
        except:
            print('error')
        #check time every 5 seconds
        time.sleep(5)
