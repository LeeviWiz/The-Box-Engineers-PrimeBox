

"""
Coordinates the robot's control loops and mode switching.

This module manages the execution of both manual and autonomous 
control loops for a robot. It provides a central "conductor" that 
ensures commands are routed correctly to the RobotController and 
that the robot responds appropriately in real time.

Later this conductor will be used to merge the different modules like IR sensor reading, camera reading, detection
in the conductors loop
"""


# ============================================================
# 0. Importing libraries and modules
# ============================================================

import time
from manual_mode import ManualControl
from robot_control import RobotController
import curses

from object_detection import start_server
from linetracing_mode import LineTracing

# ============================================================
# 1. Conductor class and it's loop
# ============================================================

class Conductor():
    
    def __init__(self):
        self.stop_requested = False
        self.controller = RobotController()
        self.manual_mode = ManualControl(self.controller, self)
        self.linetracing_mode = LineTracing(self.controller, self)
        self.mode = None
        self.submode = None
        
    def stop(self):
        self.stop_requested = True
        print("Stopping the program")
    
    def conduct(self):
        try:
            self.mode = input("Type here manual or automatic to select mode")

            if self.mode == "manual":
                curses.wrapper(self.manual_mode.loop)

            elif self.mode == "automatic":
                self.submode = input("Type here line_trace to enter linetracing_mode")
                if self.submode == "line_trace":
                    self.linetracing_mode.line_trace()
                    #self.start_server()

        except KeyboardInterrupt:
            print("\nKeyboard interrupt received")

        finally:
            print("Stopping robot motors")
            self.controller.stop()
            