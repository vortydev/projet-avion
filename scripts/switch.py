import time
from time import sleep
import RPi.GPIO as GPIO

# define switch pins
interrupteur = 12

def setup():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(interrupteur, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(interrupteur, GPIO.RISING, callback=interrupteurCallback)
    # GPIO.add_event_detect(interrupteur, GPIO.FALLING, callback=interrupteurOffCallback)

def loop():
    system = False
    zBuffer = time.localtime()
    while (True):
        interrupteurDetect(system, zBuffer)
        online = GPIO.input(interrupteur)
        print(online)
        sleep(0.1)

def interrupteurDetect(system, zBuffer):
    if GPIO.event_detected(interrupteur):
        zStamp = time.localtime()
        if time.asctime(zStamp) > time.asctime(zBuffer):
            system = True


def interrupteurCallback(channel):
    print("CALLBACK: SYSTEM ON")

# def interrupteurOffCallback(channel):
#     print("CALLBACK: SYSTEM OFF")

def destroy():
    GPIO.cleanup()

# main
if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Capture Ctrl-c, appelle destroy, puis quitte
        destroy()