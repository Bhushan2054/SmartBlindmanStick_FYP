import RPi.GPIO as GPIO
import time
import datetime
from gtts import gTTS
import pyttsx3
import os
 
GPIO.setmode(GPIO.BOARD)

GPIO_TRIGGER = 18
GPIO_ECHO = 24
buzzer = 16
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
time1= datetime.time
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
   
 
try:
    while True:
        dist = distance()
        dis = str (dist)
        print ("Measured Distance = %.1f cm" % dist)
        if (dist<=15.0):
            GPIO.output(buzzer,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(buzzer,GPIO.LOW)
            print("Soo near")
            tts_en = gTTS('the object is '+ dis + 'cm ahead ! be alert!!', lang='hi')
            # tts_en.write_to_fp(mp3_fp)
            tts_en.save("distance.mp3")
            os.system("mpg321 -q distance.mp3")
            time.sleep(2)
            time.sleep(2)
            


        else:
            print("far")
            time.sleep(2)



            
            
except KeyboardInterrupt:
    GPIO.cleanup()