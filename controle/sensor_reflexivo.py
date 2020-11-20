import RPi.GPIO as GPIO

IO.setmode(GPIO.BOARD)
IO.setup(37, GPIO.IN)

def presente():
    return GPIO.input(37)