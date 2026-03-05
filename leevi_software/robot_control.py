

"""
This module implements object-oriented programming for robot control.

The `RobotController` class provides a reusable interface for controlling the robot,
including moving forward, turning left or right, and stopping. It can be used in both
manual control (e.g., keyboard or GUI commands) and autonomous control loops.

Using a class reduces redundancy and repetition in the code. Instead of creating a
new controller for every task, the same `RobotController` object can be reused and
extended. This makes the system more scalable and maintainable for future development.

In essence, classes allow you to create objects that encapsulate both data (attributes)
and behavior (methods). 

Conceptually/analoguous, it’s like a game controller: you can use a single controller to operate 
your PlayStation, or create another one if a friend wants to join for multiplayer. 
Similarly, a RobotController object can be reused for different tasks - manual control or autonomous control
Same controller, different users. 
"""


# ============================================================
# 0. Importing libraries we will use
# ============================================================

import smbus
import time
import sys


# ============================================================
# 1. Defining the class that will be used by the conductor
# ============================================================

class RobotController():
    
    def __init__(self):
        # make a list of available channels by typing "i2cdetect -l" from terminal
        self.BUS_KANAAL_0 = 0
        self.BUS_KANAAL_1 = 1
        #esp_ret_value = 0
        #esp_prev_value = 0

        self.bus = smbus.SMBus(BUS_KANAAL_1)

        # Address = 9 for our ESP32 microcontroller we are talking to
        self.DEVICE_ADDRESS = 0x09
        # Values received from ESP32
        self.NOS = 48    # not started (or no change)
        self.ACC = 49	# accelerating
        self.CONT = 50	# constant speed
        self.DEC = 51	# decelerating
        self.LEFT = 52	# turning left
        self.RIGHT = 53	# turning right
        self.STRAI = 54   # continuous straight again
        self.STOP = 57	# stopped

    def writeData(self, value):
        byteValue = StringToBytes(value)
        bus.write_i2c_block_data(DEVICE_ADDRESS,0x01,byteValue)	#first byte is "1"-command byte (not used in ESP32)
        return -1

    def waituntil(self, ret_value):
        esp_prev_value = 0
        esp_ret_value = 0
        timeout = 5.0 # 5 seconds
        start_time = time.time() # start measuring time from here
        while esp_ret_value != ret_value:
            try:
                esp_ret_value = bus.read_byte(DEVICE_ADDRESS)
            except OSError:
                print("I2C read error")
                break
            if esp_ret_value != esp_prev_value:
                esp_prev_value = esp_ret_value
                if esp_ret_value == self.ACC:
                    print(esp_ret_value,"ACCELERATE")
                elif esp_ret_value == self.CONT:
                    print(esp_ret_value,"CONSTANT")
                elif esp_ret_value == self.DEC:
                    print(esp_ret_value,"DECELERATE")
                elif esp_ret_value == self.LEFT:
                    print(esp_ret_value,"TURNING LEFT")
                elif esp_ret_value == self.RIGHT:
                    print(esp_ret_value,"TURNING RIGHT")
                elif esp_ret_value == self.STRAI:
                    print(esp_ret_value,"STRAIGHT")
                elif esp_ret_value == self.STOP:
                    print(esp_ret_value,"STOPPED")
                elif esp_ret_value == self.NOS:
                    print(esp_ret_value,"NOT STARTED / NO CHANGE")
            time.sleep(0.02)  # 20 ms polling
            if time.time() - start_time > timeout: # check the timer's measurement
                print("Timeout waiting for", ret_value) 
                break
            
    def StringToBytes(self, val):
        retVal =[]

        for c in val:
            retVal.append(ord(c))
        return retVal

