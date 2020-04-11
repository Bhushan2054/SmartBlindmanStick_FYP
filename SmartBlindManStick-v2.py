# importing required Libraries
import RPi.GPIO as GPIO
import time
import datetime
import serial
from gtts import gTTS
import pyttsx3
import os
import sys

# connection of hardwares with GPIO pin of Raspberry Pi
GPIO.setmode(GPIO.BOARD)

GPIO_TRIGGER = 18
GPIO_ECHO = 24
buzzer = 16
button_date = 22
GPIO.setup(buzzer, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(button_date, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# code for obstactle ditection
def distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance


# code for sending message
def sms1():
    serial_port = "/dev/serial0"
    mob_num = "9804089456"
    
    # Enable Serial Communication
    ser = serial.Serial(serial_port, baudrate = 9600, timeout = 5)
    
    # Transmitting AT Commands to the Modem
    # '\r' indicates the Enter key
    ser.write(('AT'+'\r').encode())

    # Disable the Echo
    ser.write(('ATE0'+'\r').encode())
    #  Select Message format as Text mode      
    ser.write(("AT+CMGF=1"+"\r").encode())  
    print ("Text mode enabled....")
    time.sleep(1)
    # Sending a message to a particular Number
    ser.write(('AT+CMGS='+mob_num+'\r').encode())   
    msg = "Pannic button integration testing1"
    print ("sending message")
    time.sleep(2)
    ser.write((msg+chr(50)).encode())


# code for alerting about the object and the distance in the form of sound
try:
    while True:
        button_state_date= GPIO.input(button_date)
        dist = distance()
        distt = round(dist, 2)
        dis = str(distt)
        now = datetime.datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        engine = pyttsx3.init()

        if button_state_date == False:
            print('Button Pressed date...')
            engine.say('The Current Date and Time is ' + current_date +'and'+ current_time)
            engine.runAndWait()	
            engine.stop()
            # tts_en = gTTS('The Current Date and Time is ' + current_date_time , lang='hi')
            # tts_en.save("CurrentDateTime.mp3")
            # os.system("mpg321 -q CurrentDateTime.mp3")
            time.sleep(0.1) 
            sms1()   

        elif (dist < 15):
            GPIO.output(buzzer, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(buzzer, GPIO.LOW)
            print("Measured Distance = "+dis + " cm")
            print("Soo near")
            time.sleep(0.1)
        
        elif (dist > 15.0 and dist <= 25) :
            GPIO.output(buzzer, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(buzzer, GPIO.LOW)
            print("Measured Distance = "+dis + " cm")
            print("near")
            time.sleep(0.1)

        elif(dist > 25 and dist <=100):
            print("Measured Distance = "+dis + " cm")
            print("Far")
            engine.say('the object is ' + dis + 'cm ahead ! be alert!')
            engine.runAndWait()	
            engine.stop()
            #tts_en = gTTS('the object is ' + dis + 'cm ahead ! be alert!!', lang='hi')
            #tts_en.save("distance.mp3")
            #os.system("mpg321 -q distance.mp3")
            time.sleep(0.1)
        


except KeyboardInterrupt:
    GPIO.cleanup()
