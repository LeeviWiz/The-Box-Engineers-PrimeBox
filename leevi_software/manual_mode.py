

"""
Modes are just strategy layers.

This module and its control loop will be run if the
user has told the conductor to use manual mode. 

This determines the manual control logic for the robot: 
If you press up/forward arrow -> robot drives forward,
press left arrow -> turn left
press right arrow -> turn right
press down/back arrow -> turn left
and with esc or keyboardinterrupt it gracefully exits
and shuts the motors

This way you can control the robot in small steps you can
edit here and approximate "dynamic control" although
in reality when you press button the robot
will keep moving until the given amount of steps has
been taken. 
"""


# ============================================================
# 0. Importing libraries and modules
# ============================================================

import curses
import time


# ============================================================
# 1. Determine what happens when you press WASD or Arrows
# ============================================================

class ManualControl:
    
    def __init__(self, controller, stop_requested):
        self.controller = controller
        self.stop_requested = stop_requested
    
    def forward(self):
        # input the amount of steps taken when button pressed 
        # see the robot_control module for information
        steps = 100
        self.controller.forward(steps)
        
    def backward(self):
        steps = 100
        self.controller.backward(steps)
    
    def left(self):
        steps = 100
        self.controller.left(steps)
    
    def right(self):
        steps = 100
        self.controller.right(steps)
    
    def loop(self, stdscr):
        print("Manual control started. Use arrow keys (ESC to stop).")

        stdscr.nodelay(True)   # do not block waiting for key
        stdscr.keypad(True)    # enable arrow keys

        try:
            while not self.stop_requested:

                key = stdscr.getch()

                if key == curses.KEY_UP:
                    self.forward()

                elif key == curses.KEY_DOWN:
                    self.backward()

                elif key == curses.KEY_LEFT:
                    self.left()

                elif key == curses.KEY_RIGHT:
                    self.right()

                elif key == 27:   # ESC key
                    self.controller.writeData("1,000,000,1,0,1,0")
                    print("Exiting manual control.")
                    break

                time.sleep(0.05)

        except KeyboardInterrupt:
            self.controller.writeData("1,000,000,1,0,1,0")
            print("Manual control interrupted.")

