import pigpio
import enum
from time import sleep

pwm = pigpio.pi()

class Movimentos(enum.Enum):
    Mesa      = 1
    Concluido = 2
    Descarte  = 3
    

#Percorre um intervalo de jump partindo de X ate Y
def arange(x, y, jump):
    if(x <= y):
        while x < y:
            yield x
            x += jump
            
    elif(x > y):
        while x >= y:
            yield x
            x -= jump


class Servo:
    def __init__(self, porta, posInicial,velocidade):
        self.porta = porta
        self.pos = posInicial
        self.velocidade = velocidade
        pwm.set_mode(self.porta, pigpio.OUTPUT)
        pwm.set_PWM_frequency(self.porta, 50)
        pwm.set_servo_pulsewidth(self.porta, 0)

    def __exit__(self):
        pwm.set_dutcycle(self.porta, 0)
        pwm.set_PWM_frequency(self.porta, 0)
    
    def __call__(self, ang):
        self.deslizar(self.pos, ang, self.velocidade)
        self.pos = ang
        
    def parar(self):
        pwm.set_servo_pulsewidth(self.porta, 0)
    
    def mover(self, ang):
        # move instantaneamente para o angulo
        # usar servo.parar() para finalizar
        self.pos = ang
        duty = ang*11 + 500
        pwm.set_servo_pulsewidth(self.porta, duty)
    
    def deslizar(self, origem, destino, velocidade):
        d_origem = origem*11 + 500
        d_destino = destino*11 + 500
        
        # torna velocidade diretamente proporcional
        # deixando o codigo mais intuitivo
        velocidade = 1/velocidade 
        
        for i in arange(d_origem, d_destino, 0.3):
            pwm.set_servo_pulsewidth(self.porta, i)
            sleep(velocidade * 1e-3)
            pwm.set_servo_pulsewidth(self.porta, 0)
            sleep(velocidade * 1e-3)

#Declarando os servos motores
garra = Servo(5, 180, 15)
base = Servo(19, 110, 1)
ext = Servo(6, 40, 1)
altura = Servo(13, 80, 1)

def setup():
    garra.mover(180)
    sleep(0.5)
    garra.parar()
    
    ext.mover(40)
    sleep(0.5)
    ext.parar()
    
    base.mover(110)
    sleep(0.5)
    base.parar()
    
    altura.mover(80)
    sleep(0.5)
    altura.parar()
    
def executar(mov):
    sleep(1)
    if(mov == Movimentos.Mesa):
        base(174)
        
        garra(130)
        
        ext(60)
        
        altura(63)
        
        ext(90)
        
        garra(180) # Pega a Peca
        
        altura(90)
        
        ext(40)
        
        base(110)
        
        ext(70)
        
        altura(50)
        
        garra(160)
        
        garra(130)
        
        ext(40)
        
        
    elif(mov == Movimentos.Concluido):
        garra(130)
        
        ext(40)
        
        altura(50)
        
        ext(80)
        
        garra(180) # Pega a Peca
        
        ext(20)
        
        altura(100)
        
        ext(40)
        
        base(180)
        
        garra(130)
        
    
    elif(mov == Movimentos.Descarte):
        garra(130)
        
        ext(40)
        
        altura(50)
        
        ext(80)
        
        garra(180) # Pega a Peca
        
        ext(20)
        
        altura(100)
        
        ext(40)
        
        base(50)
        
        ext(60)
        
        garra(130)
            
    else:
        raise TypeError("Use apenas movimentos validos")
    sleep(1)
    setup()
