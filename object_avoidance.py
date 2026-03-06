import RPi.GPIO as GPIO
import time
import object_detection

detectionRange = 30

def objectInit():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    TRIG = 23
    ECHO = 24
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG, False)

def objectAvoid():
    #measuring the distance
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
    pulse_start = time.time()
    while GPIO.input(ECHO)==1:
    pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17165
    distance = round(distance, 1)
    print ('Distance:',distance,'cm')


    # check if the object is near and decide what to do next
    if distance <= detectionRange and opencvtest.decoded == True:
        #object is the logo
        object_seen = 1
        print("object detected")
    else if distance <= detectionRange:
        #random object
    else:
        return
