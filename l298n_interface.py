import time
import RPi.GPIO as GPIO 

movementSystemActive = False
speed = 15000


def handleCommand(command, keyPosition):
 
    global movementSystemActive
    global speed

    if keyPosition == "down":

            if command == 'F':
                l298n.move("left", speed, "false"); 
                print("move interface F")
            if command == 'B':
                l298n.move("right", speed, "false"); 
                print("move interface B")
            if command == 'L':
                l298n.move("forward", speed, "false"); 
                print("move interface L")
            if command == 'R':
                l298n.move("backward", speed, "false"); 
                print("move interface R")


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

        print("l298n_driver initialised")
        self.pwm = GPIO.PWM(self.enable, 1)  
        self.pwm.ChangeFrequency(10000)   
        self.pwm.start(90)

        self.movementSystemActive = False
 
    def move(self, dir):


        #self.pwm = GPIO.PWM(self.l1, 1)  
        #self.pwm.ChangeFrequency(1000) 
        #pwm.start(50) #50/50 duty  

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


            GPIO.output(self.r1, 0)  
            GPIO.output(self.r2, 0)  
            GPIO.output(self.l1, 0)  
            GPIO.output(self.l2, 0) 

            if dir == "F":
                time.sleep(1)
            if dir == "B":
                time.sleep(1)



        self.movementSystemActive = False


def init():
    global l298n
    l298n = l298n_driver([5, 6, 13, 19, 26])    
    #6 in a row = 5,6,13,19,26


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


if __name__ == "__main__":

    init()
    inputFromKeyboard()  
