from machine import UART, Pin

bt = UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))

while(True) :
    i = bt.read()
    if(i != None) :
        i = str(i).strip("b\'")
        if(i[0] == 'w') :
            print("UP")
        elif(i[0] == 's') :
            print("DOWN")
        elif(i[0] == 'a') :
            print("LEFT")  
        elif(i[0] == 'd') :
            print("RIGHT")