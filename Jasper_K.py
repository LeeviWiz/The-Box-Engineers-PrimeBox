import RPi.GPIO as GPIO
import time

#pins for sensors
LEFT_SENSOR = 5
RIGHT_SENSOR = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_SENSOR, GPIO.IN)
GPIO.setup(RIGHT_SENSOR, GPIO.IN)

if linetracing == true 

    #both black = intersection
    if LEFT_SENSER == 0 and RIGHT_SENSOR == 0
        #code go straight

    # only left sees black
    elif LEFT_SENSER == 1 and RIGHT_SENSOR == 0
        #code turn left

    #only right sees black
    elif LEFT_SENSER == 0 and RIGHT_SENSOR == 1
        #code turn right   
    
    #both don't see black
    else 
        #code to go straight

GPIO.cleanup()