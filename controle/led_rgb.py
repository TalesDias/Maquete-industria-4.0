import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

LED_A = {'porta': 5, 'ativado': False}
LED_B = {'porta': 3, 'ativado': False}


GPIO.setup(LED_A['porta'], GPIO.OUT)
GPIO.output(LED_A['porta'], False)
GPIO.setup(LED_B['porta'], GPIO.OUT)
GPIO.output(LED_B['porta'], False)

def alternar(led):
    led['ativado'] = not led['ativado']
    GPIO.output(led['porta'], led['ativado'])

def desligar(led):
    led['ativado'] = False
    GPIO.output(led['porta'], led['ativado'])
    
def ligar(led):
    led['ativado'] = True
    GPIO.output(led['porta'], led['ativado'])


'''
drive foi queimado
logo não usamos mais o codigo abaixo

import smbus,time

bus = smbus.SMBus(1)
 
DEVICE = 0x20 # Device address (A0-A2)
INIT = 0x00 
LEDA  = 0x14
LEDB  = 0x13

PRETO    = 0b0000_0000
AZUL     = 0b0000_0001
VERDE    = 0b0000_0010
CIANO    = 0b0000_0011
VERMELHO = 0b0000_0100
VIOLETA  = 0b0000_0101
AMARELO  = 0b0000_0110
BRANCO   = 0b0000_0111

def setup():    
    # Set all GPA pins as outputs
    bus.write_byte_data(DEVICE, INIT,0x00)
     
    # Set output all 7 output bits to 0
    bus.write_byte_data(DEVICE, LEDA, 0)
    bus.write_byte_data(DEVICE, LEDB, 0)


def gradiente(cor_de, cor_para, endereco, duracao = 500):
    
    inicial = 1e-2
    final   = 1e-10
    step = (inicial - final)/duracao
    
    for i in range(duracao):
        time.sleep(inicial)
        bus.write_byte_data(DEVICE, endereco, cor_para)
        time.sleep(final)
        bus.write_byte_data(DEVICE, endereco, cor_de)
        
        inicial -= step
        final   += step
        
    bus.write_byte_data(DEVICE, endereco, PRETO)
'''
