import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

def arange(x, y, jump):
    if(jump>0):
        while x < y:
            yield x
            x += jump
    else:
        while x > y:
            yield x 
            x+= jump

class Servo:
    def __init__(self, porta):
        GPIO.setup(porta, GPIO.OUT)
        self.pwm = GPIO.PWM(porta, 50) # pulsos de 50Hz 
        self.pwm.start(0)
        self.posF = 6.0

    def __exit__(self):
        self.pwm.stop()
        GPIO.cleanup()

garraS = Servo(29) #verificado

extS = Servo(31) #verificado
extS.posF = 1.0

alturaS = Servo(33) #verificado
alturaS.posF = 6.0

baseS = Servo(35)
baseS.posF = 6.0


def abrirGarra():
    garraS.pwm.ChangeDutyCycle(8)   
    time.sleep(0.5)
    garraS.pwm.ChangeDutyCycle(0)

def fecharGarra():
    garraS.pwm.ChangeDutyCycle(12)  
    time.sleep(0.5)
    garraS.pwm.ChangeDutyCycle(0)

def ext(ang):
    angF = ang/18 + 2
    delta = angF - extS.posF
    if (delta == 0):
        return

    dir = (int) (delta / abs(delta)) 

    for k in arange(extS.posF, angF, dir/10000): 
        print("E: "+ str(k))
        extS.pwm.ChangeDutyCycle(k)
        time.sleep(5e-5)

    extS.posF = angF
    extS.pwm.ChangeDutyCycle(0)

def base(ang):
    angF = ang/18 + 2
    delta = angF - baseS.posF
    if (delta == 0):
        return

    dir = (int) (delta / abs(delta)) 

    for k in arange(baseS.posF, angF, dir/10000): 
        print("B: "+str(k))
        baseS.pwm.ChangeDutyCycle(k)
        time.sleep(5e-5)


    baseS.posF = angF
    baseS.pwm.ChangeDutyCycle(0)