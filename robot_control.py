

"""
This module is used for writing data mainly to the ESP motor controlling. 

The controller is the hardware abstraction layer. 
All real control of the motors are happening inside
the ESP32 and because we don't have the source code
it's basically firmware that we send commands to right now and it
deterministically executes them until the end probably
because the firmware code tries to avoid resonance between motor steps

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

        self.bus = smbus.SMBus(self.BUS_KANAAL_1)

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
        byteValue = self.StringToBytes(value)
        self.bus.write_i2c_block_data(self.DEVICE_ADDRESS,0x01,byteValue)	#first byte is "1"-command byte (not used in ESP32)
        return -1

    def waituntil(self, ret_value):
        esp_prev_value = 0
        esp_ret_value = 0
        timeout = 5.0 # 5 seconds
        start_time = time.time() # start measuring time from here
        while esp_ret_value != ret_value:
            try:
                esp_ret_value = self.bus.read_byte(self.DEVICE_ADDRESS)
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
    
    """      
    # format of byte string sent to ESP32 motor control 
    #    "a,sss,eee,r,s,r,s" where following values are valid
    # a: = 1 (run a number of steps ) or 0 (run continuously)
    # sss: number of hectosteps to execute (from 001 to 999) when a = 1  
    # eee: motor end speed (from 000 to 030)
    # r: = 0 (run forward or 1 (run backward) for left motor
    # s: skip step (from 0 to 9) From available motor timing pulses, we skip 0 to max 9 to reduce motor speed for left motor
    # r: = 0 (run forward) or 1 (run backward) for right motor
    # s: skip step (from 0 to 9) From available motor timing pulses, we skip 0 to max 9 to reduce motor speed for right motor
    """
    
    def forward(self, steps):
        print ("FORWARD CONTINUOUS sending 0,steps,015,1,0,1,0")
        self.writeData(f"0,{steps},005,1,0,1,0")
        #self.waituntil(self.CONT)

    def backward(self, steps):
        print ("REVERSE STRAIGHT sending 1,steps,015,0,0,0,0")
        self.writeData(f"1,{steps},005,0,0,0,0")
        #self.waituntil(self.STRAI)
    
    def left(self, steps):
        print ("TURN LEFT sending 0,steps,020,1,4,1,0")
        self.writeData(f"0,{steps},005,1,4,1,0")
        #self.waituntil(self.LEFT)   
    
    def right(self, steps):
        print ("TURN RIGHT sending 0,200,020,1,0,1,4")
        self.writeData(f"0,{steps},005,1,0,1,4")
        #self.waituntil(self.RIGHT)
    
    def stop(self):
        print("EMERGENCY STOP SENT")
        self.writeData("1,000,000,1,0,1,0")
    
    def spin_on_place(self, direction="clockwise"):
        """
        Spins the robot in place without moving forward.
        
        Args:
            steps (int): Number of steps to rotate.
            direction (str): "clockwise" or "counterclockwise".
        """
        print(f"spinning on my place {direction}")
        
        

