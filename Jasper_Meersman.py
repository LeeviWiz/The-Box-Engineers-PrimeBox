import RPi.GPIO as GPIO
import time
import opencvtest

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG = 23
ECHO = 24
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)
print ('Waiting a few seconds for the sensor to settle')
time.sleep(2)
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
    
# Implementing a safe distance
if distance <= 30:
    object_seen = 1
    print("object detected")
else:
    object_seen = 0
    print("fine to move")

time.sleep(0.5)

GPIO.cleanup()

opencvtest.decoded