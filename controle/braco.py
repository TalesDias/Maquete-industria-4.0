import RPi.GPIO as GPIO
import enum
from time import sleep

GPIO.setmode(GPIO.BOARD)

class Movimentos(enum.Enum):
    Mesa      = 1
    Concluido = 2
    Descarte  = 3
    

#Percorre um intervalo de jump partindo de X ate Y
def arange(x, y, jump):
    print(x,y,jump)
    if(jump > 0):
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
        self.posF = 6.0 # Guarda a posicao anterior

    def __exit__(self):
        self.pwm.stop()
        GPIO.cleanup()
    
    def __call__(self, ang):
        freq = ang/18 + 2
        
        self.posF = freq
        self.pwm.ChangeDutyCycle(freq)
        
    def stop(self):
        self.pwm.ChangeDutyCycle(0)


#Declarando os servos motores
garra = Servo(29)

ext = Servo(31)
ext.posF = 1.0

altura = Servo(33)
altura.posF = 6.0

base = Servo(35)
base.posF = 6.0


def setup():
    sleep(0.5)
    garra(200)
    ext(30)
    altura(110)
    base(110)
    
    sleep(0.5)
    
    garra.stop()
    ext.stop()
    altura.stop()
    base.stop()


def executar(mov):
    if(mov == Movimentos.Mesa):
        '''
        garra(120)
        base(174)
        sleep(0.5)
        base.stop()
        garra.stop()
        sleep(0.2)        
        altura(66)
        ext(50)
        sleep(0.4)
        ext(70)
        sleep(0.4)
        altura.stop()
        sleep(0.8)
        ext(85)
        sleep(0.3)
        ext.stop()
        sleep(0.6)
        garra(200) # pega a peca
        sleep(1.5)
        ext(40)
        altura(90)
        sleep(0.8)
        ext.stop()
        altura.stop()
        base(110)
        sleep(0.6)
        base.stop()
        '''
        altura(60)
        ext(70)
        sleep(0.4)
        altura.stop()
        ext.stop()
        sleep(0.5)
        garra(120)# solta a peca
        sleep(1)
        ext(60)
        altura(100)
        sleep(0.3)
        altura.stop()
        ext.stop()
        
        
    elif(mov == Movimentos.Concluido):
        pass
    
    elif(mov == Movimentos.Descarte):
        pass
    
    else:
        raise TypeError("Use apenas movimentos validos")
    setup()

for i in range (1):
    executar(Movimentos.Mesa)
