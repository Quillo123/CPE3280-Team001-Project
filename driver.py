from machine import Pin, PWM

MAX_DUTY_CYCLE = 2**16 - 1

class Driver : 
    left        : PWM
    speedLeft   : int
    right       : PWM
    speedRight  : int
    def __init__(self, left : int = 22, right : int = 21) :
        # Initialize Right Motor
        self.right = PWM(Pin(right, Pin.OUT))
        self.right.freq(1000)
        self.right.duty_u16(0)
        self.speedRight = 0

        # Initialize Left Motor
        self.left = PWM(Pin(left, Pin.OUT))
        self.left.freq(1000)
        self.left.duty_u16(0)
        self.speedLeft = 0
        
    def DriveRight(self, speed : int) :
        if(speed > 100) :
            speed = 100
        elif speed < 0 :
            speed = 0
        
        self.speedRight = speed
        self.right.duty_u16(int(MAX_DUTY_CYCLE * (speed/100)))
        
    def DriveLeft(self, speed : int) :
        if(speed > 100) :
            speed = 100
        elif speed < 0 :
            speed = 0
        
        self.speedLeft = speed
        self.left.duty_u16(int(MAX_DUTY_CYCLE * (speed / 100)))
    
    def DriveForward(self, speed : int) :
        if(speed > 100) :
            speed = 100
        elif speed < 0 :
            speed = 0

        self.DriveRight(speed)
        self.DriveLeft(speed)
    

    