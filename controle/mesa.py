import RPi.GPIO as GPIO
from time import sleep
import enum

GPIO.setmode(GPIO.BOARD)
STEP = 16
DIR = 18
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
''' Nao funciona por algum motivo,
provavel problema de hardware
GPIO.setup(15, GPIO.OUT) #MS1
GPIO.output(15, False)
GPIO.setup(13, GPIO.OUT) #MS2
GPIO.output(13, False)
'''
GPIO.setup(11, GPIO.OUT) #MS3
GPIO.output(11, True)

class Posicoes(enum.Enum):
    Inicial  = 0
    Led_A    = 58
    Sensor_A = 150
    Led_B    = 265
    Sensor_B = 351

VELOCIDADE = 0.018
pos_atual = Posicoes.Inicial

def sign(num): return 1 if num >= 0 else -1


def girar(passos, direcao):
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
    
    if (abs(delta) > 200):
        delta = delta + 400*sign(-delta)

    if(delta > 0):
        girar(abs(delta), 1)
    else:
        girar(abs(delta), -1)
    pos_atual = pos
    
    
