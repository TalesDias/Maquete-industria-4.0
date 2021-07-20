# Essa classe funciona apenas como um Wrapper
# do RFID. O que faz sentido pois o sensor
# RFID simularia um sensor de cor.

from mfrc522 import SimpleMFRC522 as SM
import RPi.GPIO as G
from enum import Enum
from time import sleep
import json



class Cor(Enum):
    Verde    = 0
    Amarelo  = 1
    Vermelho = 2
    
sensor_A = 0 #CE0
sensor_B = 1 #CE1
led_A = 32
led_B = 36

G.setmode(G.BOARD)
G.setup(led_A, G.OUT)
G.output(led_A, False)
G.setup(led_B, G.OUT)
G.output(led_B, False)

mapeamento = None
with open('mapeamento_tag_cor.json','r') as fp:
   mapeamento = json.load(fp) 


# Todo: Verificar a necessidade de colocar um try-catch na leitura

def cor(sensor):
    leitor = SM(bus=0,device=sensor)
    limite = 10
    ligar_led(sensor)
    sleep(2) # da a sensação de que algum trabalho foi feito 
   
    while limite > 0:
        limite -= 1
        id = str(leitor.read_id())
        if(id in mapeamento):
            desligar_led(sensor)
            return Cor(mapeamento[id])
        
    
    desligar_led(sensor)    
    #Caso o sensor não reconheca, retorna como padrão vermelho
    return Cor.Vermelho

    
def ligar_led(sensor):
    if sensor == sensor_A:
        G.output(led_A, True)
    else:
        G.output(led_B,True)

def desligar_led(sensor):
    if sensor == sensor_A:
        G.output(led_A, False)
    else:
        G.output(led_B, False)
