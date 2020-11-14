import RPi.GPIO as GPIO
import time, enum

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


def reset():
    garra(200)
    ext(20)
    altura(10)
    base(110)
    
    time.sleep(0.5)
    
    garra.stop()
    ext.stop()
    altura.stop()
    base.stop()


def executar(mov):
    if(mov == Movimentos.Mesa):
        
        garra(120)
        base(174)
        time.sleep(0.5)
        base.stop()
        garra.stop()
        altura(-11)
        ext(60)
        time.sleep(0.4)
        ext(80)
        time.sleep(0.2)
        altura.stop()
        ext.stop()
        garra(200)
        time.sleep(1)
        ext(10)
        altura(10)
        time.sleep(0.8)
        ext.stop()
        altura.stop()
        base(110)
        time.sleep(0.6)
        base.stop()
        
        altura(0)
        ext(70)
        time.sleep(0.8)
        altura.stop()
        ext.stop()
        garra(120)
        time.sleep(0.4)
        ext(20)
        time.sleep(0.1)
        ext.stop()
        
        
        
        
    elif(mov == Movimentos.Concluido):
        pass
    
    elif(mov == Movimentos.Descarte):
        pass
    
    else:
        raise TypeError("Use apenas movimentos validos")
    reset()

reset()
for i in range(5):
    executar(Movimentos.Mesa)
