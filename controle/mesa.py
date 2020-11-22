import RPi.GPIO as GPIO
from time import sleep
import enum

GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT) # STEP
GPIO.setup(16, GPIO.OUT) #DIR
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
    Led_B    = 260
    Sensor_B = 345

VELOCIDADE = 0.018
pos_atual = Posicoes.Inicial

def sign(num): return 1 if num >= 0 else -1


def girar(passos, direcao):
    if (direcao < 0):
        GPIO.output(16, False)
    else:
        GPIO.output(16, True)
    
        
    for i in range(passos):
        GPIO.output(18, True)
        sleep(VELOCIDADE)
        GPIO.output(18, False)
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
    
    
    
    