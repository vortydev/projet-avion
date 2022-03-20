# importations
import RPi.GPIO as GPIO
import time
from time import sleep
from ADCDevice import *

# create adc object
adc = ADCDevice()

# define joystick pins
joystickZ = 21

# define L293D pins (DC motor)
motorRPin1 = 19
motorRPin2 = 26
enablePin = 6

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

# called when the joystick is clicked
def joystick_callback():
    print("CALLBACK: Controls toggled!")

# update motor spin
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

    val = map(abs(value), 0, 128, 0, 100)
    motorPWM.start(val)
    return round(value)

# update the servo position
def servo(angle):
    value = map(map(angle, 0, 255, 0, 180), 0, 180, SERVO_MIN_DUTY, SERVO_MAX_DUTY)
    servoPWM.ChangeDutyCycle(value)   # map the angle to duty cycle and output it
    return round(map(value, SERVO_MIN_DUTY, SERVO_MAX_DUTY, 0, 100))

# main loop
def loop():
    lockedControls = False  # start with locked controls
    yVal = 128              # motor neutral state
    xVal = 128              # servo middle angle
    zStamp = time.localtime()
    zBuffer = time.localtime()

    while (True):
        zVal = GPIO.input(joystickZ)

        zStamp = time.localtime()
        if GPIO.event_detected(joystickZ):
            if (time.asctime(zStamp) > time.asctime(zBuffer)):
                lockedControls = not lockedControls
                zBuffer = time.localtime()
            
        
        
        if not lockedControls:
            yVal = adc.analogRead(0)
            xVal = adc.analogRead(1)
        else:
            yVal = 128
            xVal = 128
        
        print("X: {}, Y: {}, Z: {}, Ctrl: {}".format(xVal, yVal, zVal, not lockedControls))

        motor(yVal)   # runs the update
        servo(xVal)   # runs the update

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