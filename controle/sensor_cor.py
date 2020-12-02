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
    


NUM_CYCLES = 100


sensor_A = {"s2": 21, "s3": 19, "sinal": 23, 'led': 36}
sensor_B = {"s2": 26, "s3": 22, "sinal": 24, 'led': 32}

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 
GPIO.setup(sensor_A["sinal"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sensor_A["s2"], GPIO.OUT)
GPIO.setup(sensor_A["s3"], GPIO.OUT)
GPIO.setup(sensor_A["led"], GPIO.OUT)
GPIO.output(sensor_A["led"], False)
GPIO.setup(sensor_B["sinal"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sensor_B["s2"], GPIO.OUT)
GPIO.setup(sensor_B["s3"], GPIO.OUT)
GPIO.setup(sensor_B["led"], GPIO.OUT)
GPIO.output(sensor_B["led"], False)



def valor(sensor, filtro = Filtro.Sem_Filtro):
    
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
    
    duration = time.time() - start      #seconds to run for loop
    
    return(NUM_CYCLES / duration)   #in Hz


def cor(sensor):
    GPIO.output(sensor["led"], True)
    
    RESOLUCAO = 100
    vm = int(sum([valor(sensor, Filtro.Vermelho) for i in range(RESOLUCAO)])/RESOLUCAO)
    vd = int(sum([valor(sensor, Filtro.Verde) for i in range(RESOLUCAO)])/RESOLUCAO)
    az = int(sum([valor(sensor, Filtro.Azul) for i in range(RESOLUCAO)])/RESOLUCAO)
    sf = int(sum([valor(sensor, Filtro.Sem_Filtro) for i in range(RESOLUCAO)])/RESOLUCAO)
    print(vm, vd, az, sf, sep='\t')
    GPIO.output(sensor["led"], False)

    if(sensor == sensor_A):
        if(vm > 10000 and vd > 9000):
            return Cor.Amarelo
            
        elif(vm > 7000):
            return Cor.Vermelho
        
        elif(az > 5000):
            return Cor.Verde
    
        else:
            return None
        
    if(sensor == sensor_B):
        if(vm > 9000 and vd > 8000):
            return Cor.Amarelo
            
        elif(vm > 7000):
            return Cor.Vermelho
        
        elif(az > 4000):
            return Cor.Verde
    
        else:
            return None

'''
for i in range(900):
    c = cor(sensor_B)
    
    #
    print("\""+str(i)+"\"", c)
'''
