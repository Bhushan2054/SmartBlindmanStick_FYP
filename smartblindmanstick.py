import RPi.GPIO as GPIO
import time
import datetime
 
GPIO.setmode(GPIO.BOARD)
 
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
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
        print ("Measured Distance = %.1f cm" % dist)
        if (dist<=15.0):
            print("Soo near")
            time.sleep(2)
            


        else:
            print("far")
            time.sleep(2)



            
            
except KeyboardInterrupt:
    GPIO.cleanup()