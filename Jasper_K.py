import RPi.GPIO as GPIO
import time

#pins for sensors
LEFT_SENSOR = 5
RIGHT_SENSOR = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_SENSOR, GPIO.IN)
GPIO.setup(RIGHT_SENSOR, GPIO.IN)

try:
    while True:
        left_state = GPIO.input(LEFT_SENSOR)
        right_state = GPIO.input(RIGHT_SENSOR)
        
        # 0 = zwart, 1 = wit
        print(f"Links: {left_state}  Rechts: {right_state}")
        
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()