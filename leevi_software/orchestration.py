

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
from leevi_software.manual_mode import ManualControl
from leevi_software.robot_control import RobotController
import curses

# ============================================================
# 1. Conductor class and it's loop
# ============================================================

class Conductor():
    
    def __init__(self):
        self.stop_requested = False
        self.controller = RobotController()
        self.manual_mode = ManualControl(self.controller, self.stop_requested)
        self.mode = None
        
    def stop(self):
        self.stop_requested = True
        print("Stopping the program")
    
    def conduct(self):
        self.mode = input("Type here manual or automatic to select mode")
        
        if self.mode == "manual":
            # enter manual mode
            curses.wrapper(self.manual_mode.loop)
            

            