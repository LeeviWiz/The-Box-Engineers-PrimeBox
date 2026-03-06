

import RPi.GPIO as GPIO
import time




class LineTracing:
    def __init__(self, controller, conductor):
        # pins for the sensors
        self.LEFT_SENSOR = 5
        self.RIGHT_SENSOR = 13
        self.controller = controller
        self.conductor = conductor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LEFT_SENSOR, GPIO.IN)
        GPIO.setup(self.RIGHT_SENSOR, GPIO.IN)
        print("linetracing  initialized")

    def line_trace(self):
        while not self.conductor.stop_requested:
            
            self.left_measurement = GPIO.input(self.LEFT_SENSOR)
            self.right_measurement = GPIO.input(self.RIGHT_SENSOR)
            print(self.left_measurement, self.right_measurement)
            if self.left_measurement == 0 and self.right_measurement == 0:
                #both black = intersection
                self.controller.forward("005")
                self.controller.waituntil(self.controller.STOP)
            
            elif self.left_measurement == 1 and self.right_measurement == 0:
                # only left sees black
                self.controller.left("005")
                self.controller.waituntil(self.controller.STOP)
            
            elif self.left_measurement == 0 and self.right_measurement == 1:
                # only right sees black
                self.controller.right("005")
                self.controller.waituntil(self.controller.STOP)
            
            else:
                # We leave the robot spinning on its place until it finds a line again 
                self.controller.left("005")
                self.controller.waituntil(self.controller.STOP)
                self.controller.right("005")
                self.controller.waituntil(self.controller.STOP)
                #self.controller.spin_on_place()
                # TODO: If you found the line, go towards it
                # TODO: If you saw the logo aswell, go towards it
                # TODO: To prevent it from hitting walls and objects when left spinning
            if self.conductor.stop_requested:
                self.controller.waituntil(self.controller.STOP)
                self.controller.stop()
        
            
                
            
