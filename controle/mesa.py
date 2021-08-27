import RPi.GPIO as GPIO
from time import sleep
import enum

GPIO.setmode(GPIO.BOARD)
STEP = 16
DIR = 18
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)

''' Nao funciona, provavel problema de hardware
GPIO.setup(11, GPIO.OUT) #MS1
GPIO.output(11, True)
GPIO.setup(13, GPIO.OUT) #MS2
GPIO.output(13, True)
GPIO.setup(15, GPIO.OUT) #MS3
GPIO.output(15, False)
'''

class Posicoes(enum.Enum):
    Inicial  = 0
    Led_A    = 29
    Sensor_A = 78
    Led_B    = 125
    Sensor_B = 177

VELOCIDADE = 0.018
PASSOS_POR_REV = 200

pos_atual = None
#kappa e uma constante de erro que permite ajustar levemente a posicao da mesa
kappa = 0

def setup():
    global pos_atual
    pos_atual = Posicoes.Inicial


def sign(num): return 1 if num >= 0 else -1

def girar(passos, direcao):
    direcao = - direcao
    if (direcao < 0):
        GPIO.output(DIR, False)
    else:
        GPIO.output(DIR, True)
        
    for i in range(passos):
        GPIO.output(STEP, True)
        sleep(VELOCIDADE)
        GPIO.output(STEP, False)
        sleep(VELOCIDADE)


def girar_para(pos):
    global pos_atual
    global kappa
    
    delta = pos.value - pos_atual.value - kappa
    kappa = 0
    
    if (abs(delta) > (PASSOS_POR_REV/2)):
        delta = delta + PASSOS_POR_REV*sign(-delta)

    if(delta > 0):
        girar(abs(delta), 1)
    else:
        girar(abs(delta), -1)
    pos_atual = pos
    
def girar_para_ponderado(pos, K):
    global pos_atual
    global kappa
    
    kappa = K
    delta = pos.value - pos_atual.value + kappa
    
    if (abs(delta) > (PASSOS_POR_REV/2)):
        delta = delta + PASSOS_POR_REV*sign(-delta)

    if(delta > 0):
        girar(abs(delta), 1)
    else:
        girar(abs(delta), -1)
    pos_atual = pos

def proximo_kappa():
    global kappa 
    girar(1, 1)
    kappa += 1

def anterior_kappa():
    global kappa
    girar(1, -1)
    kappa -= 1
    
