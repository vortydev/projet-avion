# importations
import RPi.GPIO as GPIO
from time import sleep

# servo
servoPin = 18                       # servo GPIO pin
OFFSET_DUTY = 0.5                   # pulse offset
SERVO_MIN_DUTY = 2.5 + OFFSET_DUTY  # pulse duty for minimum angle of the servo
SERVO_MAX_DUTY = 12.5 + OFFSET_DUTY # pulse duty for maximum angle of the servo

# map a value from one range to another
def map(value, fromLow, fromHigh, toLow, toHigh):
    return (toHigh - toLow) * (value - fromLow) / (fromHigh - fromLow) + toLow

def setup():
    global p
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPin, GPIO.OUT)
    GPIO.output(servoPin, GPIO.LOW)

    p = GPIO.PWM(servoPin, 50)  # set frequence to 50Hz
    p.start(0)                  # set initial duty cycle to 0

def servoWrite(angle):
    # making sure the angle isn't over the servo's capacity
    if (angle < 0):
        angle = 0
    elif (angle > 180):
        angle = 180
    
    print(map(angle, 0, 180, SERVO_MIN_DUTY, SERVO_MAX_DUTY))
    p.ChangeDutyCycle(map(angle, 0, 180, SERVO_MIN_DUTY, SERVO_MAX_DUTY))   # map the angle to duty cycle and output it

def loop():
    while True:
        for dc in range(0, 181, 1):
            servoWrite(dc)
            sleep(0.001)
        sleep(0.5)

        for dc in range(180, -1, -1):
            servoWrite(dc)
            sleep(0.001)
        sleep(0.5)

def destroy():
    p.stop()
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()