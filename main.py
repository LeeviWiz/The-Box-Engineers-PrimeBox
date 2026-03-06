

"""
This is the main entry point of the program
it controls:
- Starting the program
- Running all the core loops/modules/function of the program 
- Stopping it by command from user 
Here we this main is just used for starting and shutting down
and the entire program loop control and logic is delegated to the
orchestration.py module where we have the conductor deciding
everything like for example whether we'd like to use manual or 
autonomous mode. So head there if you want to read about how 
the different modules and their control loops
communicate with each other. 
  (Press ESC on keyboard or type CTRL+C on terminal)
"""


# ============================================================
# 0. Importing libraries and modules
# ============================================================

from orchestration import Conductor
import time

# ============================================================
# 1. Running the main loop of this software
# ============================================================

print("the file is running")

class Test:
    def run(self):
        print("Running test")

if __name__ == "__main__":

    print("Inside main")

    t = Test()
    t.run()

    print("the main is running")

    conductor = Conductor()

    try:
        conductor.conduct()

    except KeyboardInterrupt:
        print("Keyboard interrupt received")

    finally:
        conductor.controller.stop()