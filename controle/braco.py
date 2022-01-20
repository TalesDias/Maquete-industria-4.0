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
    def __init__(self, porta, posInicial, velocidade):
        self.porta = porta
        self.pos = posInicial
        self.velocidade = velocidade
        pwm.set_mode(self.porta, pigpio.OUTPUT)
        pwm.set_PWM_frequency(self.porta, 50)
        pwm.set_servo_pulsewidth(self.porta, 0)

    def __exit__(self):
        pwm.set_dutcycle(self.porta, 0)
        pwm.set_PWM_frequency(self.porta, 0)
        pwm.stop()
     
    def __call__(self, ang):
        self.deslizar(self.pos, ang, self.velocidade)
        
    def parar(self):
        pwm.set_servo_pulsewidth(self.porta, 0)
    
    def mover(self, ang):
        # move instantaneamente para o angulo
        # usar servo.parar() para finalizar
        self.pos = ang
        duty = ang*11 + 500
        pwm.set_servo_pulsewidth(self.porta, duty)

    def deslizar(self, origem, destino, velocidade):
        d_origem  = origem  *11 + 500
        d_destino = destino *11 + 500
        
        # torna velocidade diretamente proporcional
        # deixando o codigo mais intuitivo
        velocidade = 1/velocidade 
        
        for i in arange(d_origem, d_destino, 0.3):
            pwm.set_servo_pulsewidth(self.porta, i)
            sleep(velocidade * 1e-3)
        
        #ajuda a garantir que o servo chege ate local correto
        pwm.set_servo_pulsewidth(self.porta, d_destino)
        sleep(0.1)
        pwm.set_servo_pulsewidth(self.porta,0)

        self.pos = destino



#Declarando os servos motores
garra  = Servo(5, 180, 6)
base   = Servo(19, 110, 10)
ext    = Servo(13, 40, 2.5)
altura = Servo(6, 80, 3)

setup()

def setup():
    # E necessario mover o extensor primeiro
    # para evitar colisoes com a maquete
    ext.mover(40)
    sleep(0.3)
    ext.parar()
    
    garra.mover(180)
    altura.mover(100)
    base.mover(95)
    
    sleep(0.3)

    garra.parar()
    altura.parar()
    base.parar()
    
    
def executar(mov):
    sleep(0.5)
    if(mov == Movimentos.Mesa):
        base(154)
        
        garra(130)
        
        ext(80)
        
        altura(65)
        
        ext(105)
        
        garra(180) # Pega a Peca
        
        altura(80)
        
        ext(40)
        
        base(95)
        
        ext(70)
        
        altura(50)
        
        ext(95)
        
        garra(130) # Solta a Peca
        
        altura(25)
        
        garra(150)
        
        ext(70)
        
        altura(75)
        
        ext(40)
        
        
    elif(mov == Movimentos.Concluido):
        ext(60)
        
        garra(130)
        
        altura(55)
        
        ext(105)
        
        garra(180) # Pega a Peca
        
        ext(70)
        
        altura(70)
        
        ext(60)
        
        altura(90)
        
        base(165)
        
        ext(50)
        
        garra(130)
        
        
    elif(mov == Movimentos.Descarte):
        ext(60)
        
        garra(130)
        
        altura(55)
        
        ext(105)
        
        garra(180) # Pega a Peca
        
        ext(50)
        
        altura(70)
        
        ext(40)
        
        altura(90)
        
        base(20)
        
        ext(90)
        
        garra(130)
            
    else:
        raise TypeError("Use apenas movimentos validos")
    
    sleep(0.5)
    setup()
