import RPi.GPIO as GPIO
import time, enum, json

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


constantes = None
with open('constantes_cor.json','r') as fp:
    constantes = json.load(fp)
    

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
    time.sleep(0.1)
    GPIO.output(sensor["led"], True)
    RESOLUCAO = 500
    vm = int(sum([valor(sensor, Filtro.Vermelho) for i in range(RESOLUCAO)])/RESOLUCAO)
    vd = int(sum([valor(sensor, Filtro.Verde) for i in range(RESOLUCAO)])/RESOLUCAO)
    az = int(sum([valor(sensor, Filtro.Azul) for i in range(RESOLUCAO)])/RESOLUCAO)
    sf = int(sum([valor(sensor, Filtro.Sem_Filtro) for i in range(RESOLUCAO)])/RESOLUCAO)
    print(vm, vd, az, sf, sep='\t')
    GPIO.output(sensor["led"], False)

    if(sensor == sensor_A):
        
        if(vm < constantes['sensor_A']['vermelho']['vmMax'] and vm > constantes['sensor_A']['vermelho']['vmMin'] and
           vd < constantes['sensor_A']['vermelho']['vdMax'] and vd > constantes['sensor_A']['vermelho']['vdMin'] and
           az < constantes['sensor_A']['vermelho']['azMax'] and az > constantes['sensor_A']['vermelho']['azMin'] and
           sf < constantes['sensor_A']['vermelho']['sfMax'] and sf > constantes['sensor_A']['vermelho']['sfMin']):
           
           return Cor.Vermelho
        
        elif(vm < constantes['sensor_A']['amarelo']['vmMax'] and vm > constantes['sensor_A']['amarelo']['vmMin'] and
           vd < constantes['sensor_A']['amarelo']['vdMax'] and vd > constantes['sensor_A']['amarelo']['vdMin'] and
           az < constantes['sensor_A']['amarelo']['azMax'] and az > constantes['sensor_A']['amarelo']['azMin'] and
           sf < constantes['sensor_A']['amarelo']['sfMax'] and sf > constantes['sensor_A']['amarelo']['sfMin']):
           
           return Cor.Amarelo
        
        elif(vm < constantes['sensor_A']['verde']['vmMax'] and vm > constantes['sensor_A']['verde']['vmMin'] and
           vd < constantes['sensor_A']['verde']['vdMax'] and vd > constantes['sensor_A']['verde']['vdMin'] and
           az < constantes['sensor_A']['verde']['azMax'] and az > constantes['sensor_A']['verde']['azMin'] and
           sf < constantes['sensor_A']['verde']['sfMax'] and sf > constantes['sensor_A']['verde']['sfMin']):
           
           return Cor.Verde
                
        else:
            return None
        
    if(sensor == sensor_B):
        if(vm < constantes['sensor_B']['vermelho']['vmMax'] and vm > constantes['sensor_B']['vermelho']['vmMin'] and
           vd < constantes['sensor_B']['vermelho']['vdMax'] and vd > constantes['sensor_B']['vermelho']['vdMin'] and
           az < constantes['sensor_B']['vermelho']['azMax'] and az > constantes['sensor_B']['vermelho']['azMin'] and
           sf < constantes['sensor_B']['vermelho']['sfMax'] and sf > constantes['sensor_B']['vermelho']['sfMin']):
           
           return Cor.Vermelho
        
        elif(vm < constantes['sensor_B']['amarelo']['vmMax'] and vm > constantes['sensor_B']['amarelo']['vmMin'] and
           vd < constantes['sensor_B']['amarelo']['vdMax'] and vd > constantes['sensor_B']['amarelo']['vdMin'] and
           az < constantes['sensor_B']['amarelo']['azMax'] and az > constantes['sensor_B']['amarelo']['azMin'] and
           sf < constantes['sensor_B']['amarelo']['sfMax'] and sf > constantes['sensor_B']['amarelo']['sfMin']):
           
           return Cor.Amarelo
        
        elif(vm < constantes['sensor_B']['verde']['vmMax'] and vm > constantes['sensor_B']['verde']['vmMin'] and
           vd < constantes['sensor_B']['verde']['vdMax'] and vd > constantes['sensor_B']['verde']['vdMin'] and
           az < constantes['sensor_B']['verde']['azMax'] and az > constantes['sensor_B']['verde']['azMin'] and
           sf < constantes['sensor_B']['verde']['sfMax'] and sf > constantes['sensor_B']['verde']['sfMin']):
           
           return Cor.Verde
                
        else:
            return None

def leituraMaxMin(sensor, amostras, timeout):
    time.sleep(0.1)
    GPIO.output(sensor["led"], True)
    RESOLUCAO = 100
    
    start = time.time()
    
    vmMax = int(sum([valor(sensor, Filtro.Vermelho) for i in range(RESOLUCAO)])/RESOLUCAO)
    vmMin = vmMax
    vdMax = int(sum([valor(sensor, Filtro.Verde) for i in range(RESOLUCAO)])/RESOLUCAO)
    vdMin = vmMax
    azMax = int(sum([valor(sensor, Filtro.Azul) for i in range(RESOLUCAO)])/RESOLUCAO)
    azMin = azMax
    sfMax = int(sum([valor(sensor, Filtro.Sem_Filtro) for i in range(RESOLUCAO)])/RESOLUCAO)
    sfMin = sfMax

    for j in range(amostras):
        vm = int(sum([valor(sensor, Filtro.Vermelho) for i in range(RESOLUCAO)])/RESOLUCAO)
        vd = int(sum([valor(sensor, Filtro.Verde) for i in range(RESOLUCAO)])/RESOLUCAO)
        az = int(sum([valor(sensor, Filtro.Azul) for i in range(RESOLUCAO)])/RESOLUCAO)
        sf = int(sum([valor(sensor, Filtro.Sem_Filtro) for i in range(RESOLUCAO)])/RESOLUCAO)
        print(str(j) +" =>" ,vm, vd, az, sf, sep='\t')
        
        if(vm > vmMax): vmMax = vm
        elif(vm < vmMin): vmMin = vm
        if(vd > vdMax): vdMax = vd
        elif(vd < vdMin): vdMin = vd
        if(az > azMax): azMax = az
        elif(az < azMin): azMin = az
        if(sf > sfMax): sfMax = sf
        elif(sf < sfMin): sfMin = sf
        
        delta = time.time() - start
        if (delta > timeout): break
    
    vmDelta = vmMax - vmMin
    vmMax += int(vmDelta/2)
    vmMin -= int(vmDelta/2)
        
    vdDelta = vdMax - vdMin
    vdMax += int(vdDelta/2)
    vdMin -= int(vdDelta/2)
        
    azDelta = azMax - azMin
    azMax += int(azDelta/2)
    azMin -= int(azDelta/2)
        
    sfDelta = sfMax - sfMin
    sfMax += int(sfDelta/2)
    sfMin -= int(sfDelta/2)
    
    GPIO.output(sensor["led"], False)
    
    return {"vmMax":vmMax, "vmMin":vmMin, "vdMax":vdMax, "vdMin":vdMin, "azMax":azMax, "azMin":azMin, "sfMax":sfMax, "sfMin":sfMin}


def sense():
    for i in range(900):
        c = cor(sensor_A)
        
        #
        print(str(i), c, sep='\t')


#sense()