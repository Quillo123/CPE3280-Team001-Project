from machine import Pin, PWM
from picobricks import DHT11
from mq2 import MQ2
import time

MAX_DUTY_CYCLE = 2**16 - 1 #unsigned int (65535)

class Thermometer : 
    temperature :   float
    humidity :      float
    readTime :      int
    sensor :        DHT11
    pin :           int
    def __init__(self, pin : int) :
        self.sensor = DHT11(Pin(pin))  
        self.pin = pin  
        self.temperature = 0
        self.humidity = 0
        self.readTime = 0
        
    def Update(self) : 
        if time.time() - self.readTime >= 3 : #only checks again after 3 seconds have passed
            self.readTime = time.time() 
            try:
                self.sensor.measure()
                self.temperature = self.sensor.temperature
                self.humidity = self.sensor.humidity
            except Exception as e:
                print("Warning: could not measure: " + str(e))
                
class SmokeGasSensor :
    pin :           int
    readTime :      int
    sensor :        MQ2
    smoke :         float
    LPG :           float
    hydrogen :      float
    methane :       float
    def __init__(self, pin) :
        self.pin = pin
        self.sensor = MQ2(Pin(pin, Pin.IN))
        self.readTime = 0
        self.smoke = 0
        self.LPG = 0
        self.hydrogen = 0
        self.methane = 0      
        self.sensor.calibrate()
          
    def Update(self) :
        if time.time() - self.readTime >= 3 : #only checks again after 3 seconds have passed
            self.readTime = time.time()
            try:
                self.smoke = self.sensor.readSmoke()
                self.LPG = self.sensor.readLPG()
                self.hydrogen = self.sensor.readHydrogen()
                self.methane = self.sensor.readMethane()
            except Exception as e:
                print("Warning: could not measure: " + str(e))

class Buzzer : 
    pin :           int
    buzzer :        PWM
    frequency :     int
    volume :        int
    def __init__(self, pin : int, frequency : int, volume : int) :
        self.pin = pin
        self.buzzer = PWM(Pin(pin, Pin.OUT))
        self.frequency = frequency
        self.volume = volume
        self.off()
    
    def on(self) :
        self.buzzer.freq(self.frequency)
        duty_cycle_percentage = self.volume #percentage of the time the pin is high
        duty_cycle = MAX_DUTY_CYCLE * (duty_cycle_percentage/100)   
        self.buzzer.duty_u16(int(duty_cycle))
    
    def off(self) :
        self.buzzer.duty_u16(0)