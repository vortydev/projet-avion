########################################################
# Fichier :         avion.py
# Description :     Programme principal du projet avion.
# Auteur :          Étienne Ménard
# Création :        2022/03/18
# Modification :    2022/04/02
########################################################

# importations
import time
from time import sleep
from datetime import datetime

import RPi.GPIO as GPIO
from ADCDevice import *
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

####################

# CONDITIONS    # VRAI SI
C1 = False      # C2 est false
C2 = False      # code carte RFID autorisé par l'avion
C3 = False      # touche # appuyée
C4 = False      # C3 et C5 sont false
C5 = False      # interrupteur PWR position "ON"
C6 = False      # C7 est false
C7 = False      # interrupteur PWR position "OFF"

# create adc object
adc = ADCDevice()

# define LED pins
rLED = 16
yLED = 20
gLED = 21
onLED = GPIO.LOW
offLED = GPIO.HIGH
LEDs = {rLED, yLED, gLED}

# define switch pins
interrupteur = 12

# define joystick pins
joystickZ = 5

# define L293D pins (DC motor)
enablePin = 13
motorRPin1 = 19
motorRPin2 = 26

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
    print("Found LCD display")
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)

# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

####################

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

    # setup LEDs
    GPIO.setup(rLED, GPIO.OUT)
    GPIO.output(rLED, offLED)
    GPIO.setup(yLED, GPIO.OUT)
    GPIO.output(yLED, offLED)
    GPIO.setup(gLED, GPIO.OUT)
    GPIO.output(gLED, offLED)

    # interrupteur
    GPIO.setup(interrupteur, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(interrupteur, GPIO.RISING, callback=interrupteurCallback)

    # setup joystick
    GPIO.setup(joystickZ, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(joystickZ, GPIO.RISING, callback=joystickCallback)

    # setup DC motor
    GPIO.setup(enablePin, GPIO.OUT)
    GPIO.setup(motorRPin1, GPIO.OUT)
    GPIO.setup(motorRPin2, GPIO.OUT)

    # setup servo 
    GPIO.setup(servoPin, GPIO.OUT)
    GPIO.output(servoPin, GPIO.LOW)

    # set PWM frequencies
    global motorPWM
    global servoPWM
    motorPWM = GPIO.PWM(enablePin, 1000)    # set frequence to 1KHz
    servoPWM = GPIO.PWM(servoPin, 50)       # set frequence to 50Hz
    motorPWM.start(0)
    servoPWM.start(0)

def toggleLED(LED):
    for val in LEDs:
        if (val == LED):
            GPIO.output(val, onLED)
        else:
            GPIO.output(val, offLED)

# called when the slide switch is toggled
def interrupteurCallback(channel):
    print("CALLBACK: System toggled!")


# called when the joystick is clicked
def joystickCallback(channel):
    print("CALLBACK: Controls toggled!")

# update motor spin
def motor(ADC):
    value = ADC - 128
    # print(value)

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

# en attente
def E1():
    print("E1: En attente\n")
    toggleLED(rLED)
    # impossible de contrôler les moteurs (DC et servo)
    # clavier désactivé
    # interrupteur désactivé
    # LCD affiche "Scannez la carte"
    # attendre qu'une carte soit passée au lecteur RFID

# pré-vol
def E2():
    # print("E2: Pré-vol\n")
    toggleLED(yLED)

    # entrer code de destination

    # LCD affiche que l'on peut démarrer

    # interrupteur activé
    switchIn = GPIO.input(interrupteur)
    if (switchIn == 1):
        C5 = True
    else:
        C5 = False

# prêt à voler
def E3(controls, xBuffer, yBuffer, zBuffer):
    toggleLED(gLED)

    # GPIO.event_detected(interrupteur)
    
    zVal = GPIO.input(joystickZ)

    zStamp = time.localtime()
    if GPIO.event_detected(joystickZ):
        if (time.asctime(zStamp) > time.asctime(zBuffer)):
            controls = not controls
            zBuffer = time.localtime()
    
    if controls:
        yBuffer = yVal = adc.analogRead(0)
        xBuffer = xVal = adc.analogRead(1)
    else:
        yVal = yBuffer
        xVal = xBuffer
    
    print("X: {}, Y: {}, Z: {}, Ctrl: {}".format(xVal, yVal, zVal, controls))

    vY = motor(yVal)   # runs the update
    vX = servo(xVal)   # runs the update

    lcd.setCursor(0,0) # set cursor position
    strY = str(vY).rjust(3, " ")
    strX = str(vX).rjust(3, " ")
    lcd.message("Mtr:" + strY+ "% Ang:" + strX)
    lcd.message("\nDestination: {}".format("POG"))

    data = [controls, xBuffer, yBuffer, zBuffer]
    return data


def loop():
    currentstate = "E2"

    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns

    # prêt à voler
    controls = False    # start with locked controls
    yVal = 128          # motor neutral state
    xVal = 128          # servo middle angle
    yBuffer = yVal
    xBuffer = xVal
    zBuffer = time.localtime()

    while (True):

        if currentstate == "E1":
            E1()
            # Validation des conditions pour la mise à jour de l'état
        if C2 is True:
            currentstate = "E2"

        elif currentstate == "E2":
            E2()
            # Validation des conditions pour la mise à jour de l'état
            if C3 is True:
                currentstate = "E1"
            elif C4 is True:
                currentstate = "E3"

        elif currentstate == "E3":
            data = E3(controls, xBuffer, yBuffer, zBuffer)
            controls = data[0]
            xBuffer = data[1]
            yBuffer = data[2]
            zBuffer = data[3]

            # print(data)
            sleep(0.01)
            # Validation des conditions pour la mise à jour de l'état
            if C7 is True:
                currentstate = "E1"

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