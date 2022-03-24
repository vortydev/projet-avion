########################################################
# Fichier :         avion.py
# Description :     Programme principal du projet avion.
# Auteur :          Étienne Ménard
# Création :        2022/03/18
# Modification :    2022/03/18
########################################################

# importations
import time
from time import sleep, strftime
from datetime import datetime

import RPi.GPIO as GPIO
from ADCDevice import *
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

# create adc object
adc = ADCDevice()

# define joystick pins
joystickZ = 21

# define L293D pins (DC motor)
motorRPin1 = 19
motorRPin2 = 26
enablePin = 13

# define servo variables
servoPin = 18                       # servo GPIO pin
OFFSET_DUTY = 0.5                   # pulse offset
SERVO_MIN_DUTY = 2.5 + OFFSET_DUTY  # pulse duty for minimum angle of the servo
SERVO_MAX_DUTY = 12.5 + OFFSET_DUTY # pulse duty for maximum angle of the servo

# lcd stuff
PCF8574_address = 0x27 # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)

# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

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
def joystick_callback(channel):
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
    return round(val)

# update the servo position
def servo(angle):
    value = map(angle, 0, 255, SERVO_MIN_DUTY, SERVO_MAX_DUTY)
    servoPWM.ChangeDutyCycle(value)   # map the angle to duty cycle and output it
    return round(map(angle, 0, 255, 0, 180))

def get_cpu_temp(): # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C'

def get_time_now(): # get system time
    return datetime.now().strftime('%H:%M:%S')

# main loop
def loop():
    lockedControls = False  # start with locked controls
    yVal = 128              # motor neutral state
    xVal = 128              # servo middle angle
    yBuffer = yVal
    xBuffer = xVal
    zStamp = time.localtime()
    zBuffer = time.localtime()

    mcp.output(3,1) # turn on LCD backlight
    lcd.begin(16,2) # set number of LCD lines and columns

    while (True):
        zVal = GPIO.input(joystickZ)

        zStamp = time.localtime()
        if GPIO.event_detected(joystickZ):
            if (time.asctime(zStamp) > time.asctime(zBuffer)):
                lockedControls = not lockedControls
                zBuffer = time.localtime()
            
        
        
        if not lockedControls:
            yBuffer = yVal = adc.analogRead(0)
            xBuffer = xVal = adc.analogRead(1)
        else:
            yVal = yBuffer
            xVal = xBuffer
        
        print("X: {}, Y: {}, Z: {}, Ctrl: {}".format(xVal, yVal, zVal, not lockedControls))

        vY = motor(yVal)   # runs the update
        vX = servo(xVal)   # runs the update

        lcd.setCursor(0,0) # set cursor position
        strY = str(vY).rjust(3, " ")
        strX = str(vX).rjust(3, " ")
        lcd.message("Mtr:" + strY+ "% Ang:" + strX)
        lcd.message("\nDestination: {}".format("POG"))
        # lcd.message( get_time_now() ) # display the time

        sleep(0.01)

# cleanup sequence
def destroy():
    lcd.clear()
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