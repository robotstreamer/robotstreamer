import time
import RPi.GPIO as GPIO 

movementSystemActive = False

class l298n_driver:


    def __init__(self, defs):

        #setup pins
        self.defs = defs 

        self.enable  = self.defs[0]
        self.l1 = self.defs[1]
        self.l2 = self.defs[2]
        self.r1 = self.defs[3]
        self.r2 = self.defs[4] 
        print (defs)
        #pin setups
        GPIO.setmode(GPIO.BCM) #pin mode
        GPIO.setup(self.enable, GPIO.OUT)   #set as out
        GPIO.setup(self.l1, GPIO.OUT)       #set as out
        GPIO.setup(self.l2, GPIO.OUT)       #set as out
        GPIO.setup(self.r1, GPIO.OUT)       #set as out
        GPIO.setup(self.r2, GPIO.OUT)       #set as out
        
        GPIO.output(self.r1, 0)  
        GPIO.output(self.r2, 0)  
        GPIO.output(self.l1, 0)  
        GPIO.output(self.l2, 0) 

        #pwm COULD be used for speed although its better for current limit
        self.pwm = GPIO.PWM(self.enable, 1)  
        self.pwm.ChangeFrequency(10000)   
        self.pwm.start(100)

        self.movementSystemActive = False
        print("l298n_driver initialised")
 
    def move(self, dir):

        if self.movementSystemActive == False:
            self.movementSystemActive = True

            print("Move: ", dir) 

            if dir == "R":
                GPIO.output(self.r1, 0)  
                GPIO.output(self.r2, 1)  
                GPIO.output(self.l1, 1)  
                GPIO.output(self.l2, 0) 
                time.sleep(0.3)

            if dir == "L":

                GPIO.output(self.r1, 1)  
                GPIO.output(self.r2, 0)  
                GPIO.output(self.l1, 0)  
                GPIO.output(self.l2, 1)  
                time.sleep(0.3)

            if dir == "F":
            #t
                GPIO.output(self.r1, 1)  
                GPIO.output(self.r2, 0)  
                GPIO.output(self.l1, 1)  
                GPIO.output(self.l2, 0) 
                time.sleep(0.5)

            if dir == "B":

                GPIO.output(self.r1, 0)  
                GPIO.output(self.r2, 1)  
                GPIO.output(self.l1, 0)  
                GPIO.output(self.l2, 1) 
                time.sleep(0.5)

            #all stop
            GPIO.output(self.r1, 0)  
            GPIO.output(self.r2, 0)  
            GPIO.output(self.l1, 0)  
            GPIO.output(self.l2, 0) 

            #prevents sharp change
            #if dir == "F":
            #    time.sleep(1)
            #if dir == "B":
            #    time.sleep(1)

        self.movementSystemActive = False


    def burnIn(self, dir):

        if dir == "R":
            GPIO.output(self.r1, 0)  
            GPIO.output(self.r2, 1)  
            GPIO.output(self.l1, 1)  
            GPIO.output(self.l2, 0) 

        if dir == "L":

            GPIO.output(self.r1, 1)  
            GPIO.output(self.r2, 0)  
            GPIO.output(self.l1, 0)  
            GPIO.output(self.l2, 1)  

        if dir == "F":

            GPIO.output(self.r1, 1)  
            GPIO.output(self.r2, 0)  
            GPIO.output(self.l1, 1)  
            GPIO.output(self.l2, 0) 


        if dir == "B":

            GPIO.output(self.r1, 0)  
            GPIO.output(self.r2, 1)  
            GPIO.output(self.l1, 0)  
            GPIO.output(self.l2, 1) 





def init():
    global l298n
    l298n = l298n_driver([5, 6, 13, 19, 26])    
    #5 in a row = 5,6,13,19,26


def handleCommand(command, keyPosition):

                print("handleCommand", command)
                if keyPosition == 'down':
                    l298n.move(command)


def inputFromKeyboard():

    while True:
        data = input(">")

        if data == "w":
            handleCommand('F', 'down')

        if data == "s":
            handleCommand('B', 'down')

        if data == "a":
            handleCommand('R', 'down')

        if data == "d":
            handleCommand('L', 'down')


        if data == "B":
            print("burn in B")
            l298n.burnIn("B")

        if data == "F":
            print("burn in F")
            l298n.burnIn("F")
            
        if data == "S":
            print("burn in sim")
            l298n.burnIn("sim")

if __name__ == "__main__":

    init()
    inputFromKeyboard()  
