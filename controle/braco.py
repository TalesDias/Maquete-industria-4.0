import pigpio
import enum
from time import sleep

pwm = pigpio.pi()
atraso = 0.7

class Movimentos(enum.Enum):
    Mesa      = 1
    Concluido = 2
    Descarte  = 3
    

#Percorre um intervalo de jump partindo de X ate Y
def arange(x, y, jump):
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
        self.porta = porta
        
        pwm.set_mode(self.porta, pigpio.OUTPUT)
        pwm.set_PWM_frequency(self.porta, 50)
        pwm.set_servo_pulsewidth(self.porta, 0)

    def __exit__(self):
        pwm.set_dutcycle(self.porta, 0)
        pwm.set_PWM_frequency(self.porta, 0)
    
    def __call__(self, ang):
        duty = ang*11 + 500
        pwm.set_servo_pulsewidth(self.porta, duty)
        
    def parar(self):
        pwm.set_servo_pulsewidth(self.porta, 0)
    
    def deslizar(self, origem, destino):
        d_origem = origem*11 + 500
        d_destino = destino*11 + 500
        
        for i in arange(d_origem, d_destino, 0.1):
            pwm.set_servo_pulsewidth(self.porta, i)
            sleep(0.0001)
            pwm.set_servo_pulsewidth(self.porta, 0)
            sleep(0.0001)

#Declarando os servos motores
garra = Servo(5)
ext = Servo(6)
altura = Servo(13)
base = Servo(19)


def setup():
    garra(180)
    sleep(0.5)
    garra.parar()
    
    base(110)
    sleep(0.5)
    base.parar()
    
    ext(40)
    sleep(0.5)
    ext.parar()
    
    altura(80)
    sleep(0.5)
    altura.parar()
    
def executar(mov):
    sleep(2)
    if(mov == Movimentos.Mesa):
        base(174)
        sleep(atraso)
        garra(130)
        sleep(atraso)
        ext(70)
        sleep(atraso)
        altura(65)
        sleep(atraso)
        altura.parar()
        ext.deslizar(70,80)
        sleep(atraso)
        garra(180)
        sleep(atraso*2)
        altura(90)
        sleep(atraso)
        ext(40)
        sleep(atraso)
        base(110)
        sleep(atraso)
        ext(70)
        sleep(atraso)
        altura(50)
        sleep(atraso)
        altura.parar()
        garra(160)
        sleep(atraso)
        garra(130)
        sleep(atraso)
        ext(40)
        sleep(atraso)
        
    elif(mov == Movimentos.Concluido):
        garra(130)
        sleep(atraso)
        ext(60)
        sleep(atraso)
        altura(50)
        sleep(atraso)
        ext.deslizar(60, 80)
        sleep(atraso)
        garra(180) # Pega a Peca
        sleep(atraso)
        ext(20)
        sleep(atraso)
        altura(110)
        sleep(atraso*3)
        altura.parar()
        ext(40)
        sleep(atraso)
        base(180)
        sleep(atraso)
        garra(130)
        sleep(atraso*2)
        
    
    elif(mov == Movimentos.Descarte):
        garra(130)
        sleep(atraso)
        ext(60)
        sleep(atraso)
        altura(50)
        sleep(atraso)
        ext.deslizar(60, 80)
        sleep(atraso)
        garra(180) # Pega a Peca
        sleep(atraso)
        ext(20)
        sleep(atraso)
        altura(110)
        sleep(atraso*3)
        altura.parar()
        ext(40)
        sleep(atraso)
        base(50)
        sleep(atraso)
        ext(60)
        sleep(atraso)
        garra(130)
        sleep(atraso*2)    
    else:
        raise TypeError("Use apenas movimentos validos")
    setup()
'''
executar(Movimentos.Mesa)
'''