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
    Led_A    = 28
    Sensor_A = 76
    Led_B    = 126
    Sensor_B = 178

VELOCIDADE = 0.018
PASSOS_POR_REV = 206

pos_atual = None


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
    delta = pos.value - pos_atual.value
    
    if (abs(delta) > (PASSOS_POR_REV/2)):
        delta = delta + PASSOS_POR_REV*sign(-delta)

    if(delta > 0):
        girar(abs(delta), 1)
    else:
        girar(abs(delta), -1)
    pos_atual = pos
    
def teste():
    setup()
    girar_para(Posicoes.Led_A)
    sleep(3)
    girar_para(Posicoes.Sensor_A)
    sleep(3)
    girar_para(Posicoes.Led_B)
    sleep(3)
    girar_para(Posicoes.Sensor_B)
    sleep(3)
    girar_para(Posicoes.Inicial)
    
