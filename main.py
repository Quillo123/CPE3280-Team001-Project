from sensors import Thermometer, SmokeGasSensor, Buzzer
from driver import Driver
from machine import Pin, UART
import utime
import _thread

reportTime = 1

th = Thermometer(11)
sm = SmokeGasSensor(28)
buzzer = Buzzer(20, 100, 10)
LED = Pin(7, Pin.OUT)

bt = UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))
driver = Driver()

smokeLimit = 40000
tempMin = -17
tempMax = 35
humiditiyMax = 70


lastInterruptTime = 0
play = True

def debounce():
    # print("CHECK BOUNCE")
    global lastInterruptTime
    currentTime = utime.ticks_ms() # get current time in ms 
    if currentTime - lastInterruptTime < 400: # find difference in time between current and last interrupt time, check if less than 400ms 
        return False
    lastInterruptTime = currentTime
    return True # ready to be used again!



def callback(pin) :
    if(debounce()) :
        global play
        play = not play
        print("TOGGLE ENABLED TO " + str(play))



button = Pin(10)
button.irq(handler = callback)

time = utime.time()

speed = 50

def Begin() :
    buzzerPlay = False
    while(True) :
        if(play) :
            i = bt.read()
            if(i != None) :
                i = str(i).strip("b\'")
                if(len(i) < 1) :
                    continue
                if(i[0] == 'w') :
                    print("UP")
                    driver.DriveForward(speed)
                elif(i[0] == 's') :
                    print("DOWN")
                elif(i[0] == 'a') :
                    print("LEFT")
                    driver.DriveRight(speed)  
                elif(i[0] == 'd') :
                    print("RIGHT")
                    driver.DriveLeft(speed)
                else :
                    driver.DriveForward(0)

                if(i[0] == 'f'):
                    buzzerPlay = not buzzerPlay
                    print("BUZZER SWITCH")
                    bt.sendbreak()

                if(i[0] == 'p') :
                    print("READING SENSORS")
                    time = utime.time()

                    th.Update()

                    bt.write(f"Temperature: {th.temperature}C ")
                    bt.write(f"Humidity: {th.humidity} ")

                    sm.Update()

                    bt.write(f"Methane: {sm.methane} ")
                    bt.write(f"LPG: {sm.LPG} ")
                    bt.write(f"Hydrogen: {sm.hydrogen} ")
                    bt.write(f"Smoke: {sm.smoke}\n\r")
                    if(sm.smoke > smokeLimit or th.temperature > tempMax or th.humidity > humiditiyMax or th.temperature < tempMin or buzzerPlay) :
                        buzzer.on()
                        LED.on()
                    else :
                        buzzer.off()
                        LED.off()
                    
                    bt.sendbreak()
            else :
                driver.DriveForward(0)
            utime.sleep(0.1) 

Begin()