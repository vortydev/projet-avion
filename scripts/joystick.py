import RPi.GPIO as GPIO
from time import sleep
from ADCDevice import *

adc = ADCDevice()

joystickZ = 13

def setup():
    global adc

    if (adc.detectI2C(0x4b)):
	    adc = ADS7830()
    elif (adc.detectI2C(0x48)):
        adc = PCF8591()
    else:
        print("No correct I2C address found.")
        exit(-1)
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(joystickZ, GPIO.IN, GPIO.PUD_UP)

def loop():
    while (True):
        zVal = GPIO.input(joystickZ)
        yVal = adc.analogRead(0)
        xVal = adc.analogRead(1)
        print("Value X: %d, Value Y: %d, Value Z: %d"%(xVal, yVal, zVal))
        sleep(0.01)

def destroy():
    adc.close()
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Capture Ctrl-c, appelle destroy, puis quitte
        destroy()