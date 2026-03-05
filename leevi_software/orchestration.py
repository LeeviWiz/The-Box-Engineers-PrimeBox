

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
from leevi_software.manual_mode import ManualController

# ============================================================
# 1. Conductor class and it's loop
# ============================================================

class Conductor():
    
    def __init__(self):
        self.stop_requested = False
        self.yeah = "yeah"
        
    def stop(self):
        self.stop_requested = True
        print("Stopping the program")
    
    def conduct(self):
        while not self.stop_requested:
            self.print_this(self.yeah)
            
            

            