import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN)

def presente():
    return not GPIO.input(37)