import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

#led indicador
LED = 12
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, False)

def ligar():
    GPIO.output(LED, True)
    
def desligar():
    GPIO.output(LED, False)