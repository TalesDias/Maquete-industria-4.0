from time import sleep
from datetime import datetime
from dateutil.parser import parse as parse_date
import enum, memcache, json

import braco, led_rgb, mesa, led_status
import sensor_cor as sc, sensor_reflexivo as sr, controle_geral as cg


shared = memcache.Client(['127.0.0.1:11211'])
    

DELTA_DISTANCIA = 40
    
while True:
    
    if(not (shared.get("Estado") == "Calibracao" and cg.ativado())):
        sleep(0.1)
        continue
    
    modo = "Lento" #shared.get("Modo")
    amostras = None
    timeout  = None
    configuracoes = {}
    
    
    if modo == "Rapido":
        amostras = 10
        timeout  = 50
        
    elif modo == "Moderado":
        amostras = 20
        timeout  = 100
        
    elif modo == "Lento":
        amostras = 15
        timeout  = 2000
        
    
    mesa.setup()
    braco.setup()
    
    '''
    #Colocando as 3 pecas na mesa
    while(not sr.presente()):
        sleep(0.3)
        led_rgb.alternar(led_rgb.LED_A)
        led_rgb.alternar(led_rgb.LED_B)
                
    led_rgb.desligar(led_rgb.LED_A)
    led_rgb.desligar(led_rgb.LED_B)
    braco.executar(braco.Movimentos.Mesa)
    mesa.girar(DELTA_DISTANCIA,1)
            
    while(not sr.presente()):
        sleep(0.3)
        led_rgb.alternar(led_rgb.LED_A)
        led_rgb.alternar(led_rgb.LED_B)
                
    led_rgb.desligar(led_rgb.LED_A)
    led_rgb.desligar(led_rgb.LED_B)
    braco.executar(braco.Movimentos.Mesa)
    mesa.girar(DELTA_DISTANCIA,1)
            
    while(not sr.presente()):
        sleep(0.3)
        led_rgb.alternar(led_rgb.LED_A)
        led_rgb.alternar(led_rgb.LED_B)
                
    led_rgb.desligar(led_rgb.LED_A)
    led_rgb.desligar(led_rgb.LED_B)
    braco.executar(braco.Movimentos.Mesa)
    '''
    shared.set("Progresso", "1")
    
    #Pegando dados das pecas no sensor A
    configuracoes['sensor_A'] = {}
    mesa.girar_para(mesa.Posicoes.Sensor_A)
    configuracoes['sensor_A']['vermelho'] = sc.leituraMaxMin(sc.sensor_A, amostras, timeout) 
    shared.set("Progresso", "2")
    
    mesa.girar(DELTA_DISTANCIA,-1)
    configuracoes['sensor_A']['amarelo'] = sc.leituraMaxMin(sc.sensor_A, amostras, timeout)
    shared.set("Progresso", "3")
    
    mesa.girar(DELTA_DISTANCIA,-1)
    configuracoes['sensor_A']['verde'] = sc.leituraMaxMin(sc.sensor_A, amostras, timeout) 
    shared.set("Progresso", "4")
    '''
    
    #Pegando dados das pecas no sensor B
    configuracoes['sensor_B'] = {}
    mesa.girar_para(mesa.Posicoes.Sensor_B)
    configuracoes['sensor_B']['verde'] = sc.leituraMaxMin(sc.sensor_B, amostras, timeout) 
    shared.set("Progresso", "5")
    
    mesa.girar(DELTA_DISTANCIA,1)
    configuracoes['sensor_B']['amarelo'] = sc.leituraMaxMin(sc.sensor_B, amostras, timeout) 
    shared.set("Progresso", "6")
    
    mesa.girar(DELTA_DISTANCIA,1)
    configuracoes['sensor_B']['vermelho'] = sc.leituraMaxMin(sc.sensor_B, amostras, timeout) 
    shared.set("Progresso", "7")
    
    mesa.girar_para(mesa.Posicoes.Inicial)
    shared.set("Progresso", "0")
    '''
    # Salvando Dados
    with open("constantes_cor.json", 'w') as f:
        json.dump(configuracoes, f)
        f.close()
        
    shared.set("Estado","Invalido")
