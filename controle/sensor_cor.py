import RPi.GPIO as GPIO
import time, enum

class Filtro(enum.Enum):
    Verde    = 1
    Vermelho = 2
    Azul     = 3
    Sem_Filtro  = 4
    
class Cor(enum.Enum):
    Verde    = 1
    Vermelho = 2
    Amarelo  = 3
    


NUM_CYCLES = 50


sensorA = {"s2": 19, "s3": 21, "sinal": 23, 'led': 40 }
sensorB = {"s2": 24, "s3": 22, "sinal": 26, 'led': 36}

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 
GPIO.setup(sensorA["sinal"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sensorA["s2"], GPIO.OUT)
GPIO.setup(sensorA["s3"], GPIO.OUT)
GPIO.setup(sensorA["led"], GPIO.OUT)
GPIO.output(sensorA["led"], False)
GPIO.setup(sensorB["sinal"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sensorB["s2"], GPIO.OUT)
GPIO.setup(sensorB["s3"], GPIO.OUT)
GPIO.setup(sensorB["led"], GPIO.OUT)
GPIO.output(sensorB["led"], False)



def valor(sensor, filtro = Filtro.Sem_Filtro):
    
    GPIO.output(sensor["led"], True)
    
    if(filtro == Filtro.Vermelho):
        GPIO.output(sensor["s2"], GPIO.LOW)
        GPIO.output(sensor["s3"], GPIO.LOW)
        
    elif(filtro == Filtro.Verde):
        GPIO.output(sensor["s2"],GPIO.LOW)
        GPIO.output(sensor["s3"],GPIO.HIGH)
    
    elif(filtro == Filtro.Azul):
        GPIO.output(sensor["s2"],GPIO.HIGH)
        GPIO.output(sensor["s3"],GPIO.HIGH)
        
    elif(filtro == Filtro.Sem_Filtro):
        GPIO.output(sensor["s2"],GPIO.HIGH)
        GPIO.output(sensor["s3"],GPIO.LOW)
    
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
        GPIO.wait_for_edge(sensor["sinal"], GPIO.FALLING)
    
    GPIO.output(sensor["led"], False)
    duration = time.time() - start      #seconds to run for loop
    return(NUM_CYCLES / duration)   #in Hz


def cor(sensor):
    RESOLUCAO = 100
    vm = int(sum([valor(sensor, Filtro.Vermelho) for i in range(RESOLUCAO)])/RESOLUCAO)
    vd = int(sum([valor(sensor, Filtro.Verde) for i in range(RESOLUCAO)])/RESOLUCAO)
    az = int(sum([valor(sensor, Filtro.Azul) for i in range(RESOLUCAO)])/RESOLUCAO)
    sf = int(sum([valor(sensor, Filtro.Sem_Filtro) for i in range(RESOLUCAO)])/RESOLUCAO)
    print(vm, vd, az, sf)
    
    
    if(vm > 3500 and sf > 6000):
        return Cor.Amarelo
        
    elif(vm > 2000 and vd < 1400):
        return Cor.Vermelho
    
    elif(vm < 900 and az < 1200 and vd < 1000):
        return Cor.Verde
    
    else:
        return None
  
for i in range (20): cor(sensorA)