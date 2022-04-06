# importations
import RPi.GPIO as GPIO
from time import sleep
from ADCDevice import *

# create adc object
adc = ADCDevice()

# define L293D pins
motorRPin1 = 27
motorRPin2 = 17
enablePin = 22

# define joystick pins
joystickZ = 13

# séquence d'initialisation
def setup():
    # init adc
    global adc
    if (adc.detectI2C(0x4b)):
	    adc = ADS7830()
    elif (adc.detectI2C(0x48)):
        adc = PCF8591()
    else:
        print("No correct I2C address found.")
        exit(-1)
    
    # setup GPIO
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(motorRPin1, GPIO.OUT)
    GPIO.setup(motorRPin2, GPIO.OUT)
    GPIO.setup(enablePin, GPIO.OUT)

    GPIO.setup(joystickZ, GPIO.IN, GPIO.PUD_UP)

    global p
    p = GPIO.PWM(enablePin, 1000)   # create PWM and set frequence to 1KHz
    p.start(0)

# mapNUM function: map the value from a range of mapping to another range.
def mapNUM(value, fromLow, fromHigh, toLow, toHigh):
    return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow

def motor(ADC):
    value = ADC - 128
    if (value > 0):
        GPIO.output(motorRPin1, GPIO.HIGH)
        GPIO.output(motorRPin2, GPIO.LOW)
        print("Turning forward")
    elif (value < 0):
        GPIO.output(motorRPin1, GPIO.LOW)
        GPIO.output(motorRPin2, GPIO.HIGH)
        print("Turning backward")
    else:
        GPIO.output(motorRPin1, GPIO.LOW)
        GPIO.output(motorRPin2, GPIO.LOW)
        print("Motor stopped")

    p.start(mapNUM(abs(value), 0, 128, 0, 100))
    print("The PWM duty cycle is %d%%\n"%(abs(value)*100/127))

def loop():
    while (True):
        zVal = GPIO.input(joystickZ)
        yVal = adc.analogRead(0)
        xVal = adc.analogRead(1)
        print("Value X: %d, Value Y: %d, Value Z: %d"%(xVal, yVal, zVal))

        motor(yVal)

        sleep(0.01)

# cleanup sequence
def destroy():
    adc.close()
    GPIO.cleanup()

# main
if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Capture Ctrl-c, appelle destroy, puis quitte
        destroy()