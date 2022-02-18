import RPi.GPIO as GPIO
from time import sleep
from ADCDevice import *

adc = ADCDevice()

# define L293D pins
motorRPin1 = 27
motorRPin2 = 17
enablePin = 22

def setup():
    global adc

    if (adc.detectI2C(0x4b)):
	    adc = ADS7830()

    global p

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motorRPin1, GPIO.OUT)
    GPIO.setup(motorRPin2, GPIO.OUT)
    GPIO.setup(enablePin, GPIO.OUT)

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
        value = adc.analogRead(0)
        print("ADC value: %d"%(value))
        motor(value)
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