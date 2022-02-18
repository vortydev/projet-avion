# importations
import RPi.GPIO as GPIO
from time import sleep
from ADCDevice import *

# create adc object
adc = ADCDevice()

# define joystick pins
joystickZ = 13

# define L293D pins (DC motor)
motorRPin1 = 27
motorRPin2 = 17
enablePin = 22

# define servo variables
servoPin = 18                       # servo GPIO pin
OFFSET_DUTY = 0.5                   # pulse offset
SERVO_MIN_DUTY = 2.5 + OFFSET_DUTY  # pulse duty for minimum angle of the servo
SERVO_MAX_DUTY = 12.5 + OFFSET_DUTY # pulse duty for maximum angle of the servo

# map a value from one range to another
def map(value, fromLow, fromHigh, toLow, toHigh):
    return (toHigh - toLow) * (value - fromLow) / (fromHigh - fromLow) + toLow

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

    # setup joystick
    GPIO.setup(joystickZ, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(joystickZ, GPIO.RISING, callback=joystick_callback)

    # setup DC motor
    GPIO.setup(motorRPin1, GPIO.OUT)
    GPIO.setup(motorRPin2, GPIO.OUT)
    GPIO.setup(enablePin, GPIO.OUT)

    # setup servo 
    GPIO.setup(servoPin, GPIO.OUT)
    GPIO.output(servoPin, GPIO.LOW)

    # set PWM frequencies
    global motorPWM
    global servoPWM
    motorPWM = GPIO.PWM(enablePin, 1000)   # set frequence to 1KHz
    servoPWM = GPIO.PWM(servoPin, 50)   # set frequence to 50Hz
    motorPWM.start(0)
    servoPWM.start(0)

def joystick_callback(channel):
    print("Controls toggled")

def motor(ADC):
    value = ADC - 128
    if (value > 0):
        GPIO.output(motorRPin1, GPIO.HIGH)
        GPIO.output(motorRPin2, GPIO.LOW)
        # print("Turning forward")
    elif (value < 0):
        GPIO.output(motorRPin1, GPIO.LOW)
        GPIO.output(motorRPin2, GPIO.HIGH)
        # print("Turning backward")
    else:
        GPIO.output(motorRPin1, GPIO.LOW)
        GPIO.output(motorRPin2, GPIO.LOW)
        # print("Motor stopped")

    motorPWM.start(map(abs(value), 0, 128, 0, 100))
    # print("The PWM duty cycle is %d%%\n"%(abs(value)*100/127))

def servo(angle):
    servoPWM.ChangeDutyCycle(map(map(angle, 0, 255, 0, 180), 0, 180, SERVO_MIN_DUTY, SERVO_MAX_DUTY))   # map the angle to duty cycle and output it
    # print(angle, map(angle, 0, 255, 0, 180), map(map(angle, 0, 255, 0, 180), 0, 180, SERVO_MIN_DUTY, SERVO_MAX_DUTY))

def loop():
    lockedControls = False
    yVal = 128
    xVal = 90

    while (True):
        zVal = GPIO.input(joystickZ)

        if GPIO.event_detected(joystickZ):
            lockedControls = not lockedControls
        
        if not lockedControls:
            yVal = adc.analogRead(0)
            xVal = adc.analogRead(1)
        
        print("Value X: %d, Value Y: %d, Value Z: %d"%(xVal, yVal, zVal))

        servo(xVal)
        motor(yVal)

        sleep(0.01)

# cleanup sequence
def destroy():
    motorPWM.stop()
    servoPWM.stop()
    adc.close()
    GPIO.cleanup()

# main
if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Capture Ctrl-c, appelle destroy, puis quitte
        destroy()