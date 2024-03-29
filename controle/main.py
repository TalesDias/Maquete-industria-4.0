from time import sleep
from datetime import datetime
from dateutil.parser import parse as parse_date
import enum, sqlite3, memcache

import braco, led_rgb, mesa, led_status
import sensor_cor as sc, sensor_reflexivo as sr, controle_geral as cg


class Estados (enum.Enum):
    Emergencia = 0
    Inativo    = 1
    Ativo      = 3
    Manutencao = 4
    Invalido   = 5

shared = None
estado = None
conn   = None
pc_conc = None
pc_retr = None
pc_refu = None
pc_tot  = None


def setup():
    global shared
    global estado
    global conn
    global pc_conc
    global pc_retr
    global pc_refu
    global pc_tot
    
    braco.setup()
    conn = sqlite3.connect('../maquete.db')
    c = conn.cursor()
    estado = Estados.Invalido
    atualizar_estado()
    shared = memcache.Client(['127.0.0.1:11211'])
    shared.set("Estado", estado.name)
    
    pc_conc = 0
    pc_retr = 0
    pc_refu = 0
    pc_tot  = 0
    for peca in c.execute('SELECT * FROM peca;'):
        if parse_date(peca[2]).day < datetime.now().day:
            pc_tot +=1
            if peca[1] == 'refugada':
                pc_refu += 1
            elif (peca[1] == 'retrabalhada'):
                pc_retr += 1
            else:
                pc_conc += 1
    c.close()

def atualizar_estado():
    global estado;
    c = conn.cursor()
    date = datetime.now()
    c.execute(f"INSERT INTO estado (nome, date_created) VALUES('{estado.name}', '{str(date)}');")
    conn.commit()
        

def log_file(msg):
    
    linha = str(datetime.now())
    linha += " @ System -> "
    linha += msg
    linha += "\n"
    
    with open("../log", 'a') as f:
        f.write(linha)
        f.close()
    
def executar():
    defeito = False
    mesa.setup()
    braco.setup()
    braco.executar(braco.Movimentos.Mesa)
    
    # verificando se existe uma parada de emergencia 
    if (not cg.ativado()): return 2
    
    cor = None
    while(cor != sc.Cor.Verde):
        # verificando se existe uma parada de emergencia 
        if (not cg.ativado()): return 2
        
        mesa.girar_para(mesa.Posicoes.Led_A)
        #led_rgb.gradiente(led_rgb.AMARELO, led_rgb.VERMELHO, led_rgb. LEDA)
        led_rgb.alternar(led_rgb.LED_A)
        sleep(6)
        led_rgb.alternar(led_rgb.LED_A)
        
        # verificando se existe uma parada de emergencia 
        if (not cg.ativado()): return 2
        
        mesa.girar_para_ponderado(mesa.Posicoes.Sensor_A, -4)
                
        tentativas = 0
        cor = None
        while (cor == None and tentativas < 9):
            cor = sc.cor(sc.sensor_A)
            tentativas += 1
            mesa.proximo_kappa()
            
        #caso no consiga identificar a cor
        if (tentativas == 9):
            for i in range(20):
                led_rgb.alternar(led_rgb.LED_B)
                sleep(0.2)
                led_rgb.alternar(led_rgb.LED_A)
                sleep(0.2)
                
            mesa.girar_para(mesa.Posicoes.Inicial)
        
            for i in range(20):
                led_rgb.alternar(led_rgb.LED_B)
                sleep(0.2)
                led_rgb.alternar(led_rgb.LED_A)
                sleep(0.2)
            return 2
        
        
        # verificando se existe uma parada de emergencia 
        if (not cg.ativado()): return 2
        
        if(cor == sc.Cor.Amarelo):
            defeito = True
            
        if(cor == sc.Cor.Vermelho):
            mesa.girar_para(mesa.Posicoes.Inicial)
            braco.executar(braco.Movimentos.Descarte)
            return 2
            
    cor = None
    while(cor != sc.Cor.Verde):
        # verificando se existe uma parada de emergencia 
        if (not cg.ativado()): return 2
    
        mesa.girar_para(mesa.Posicoes.Led_B)
        #led_rgb.gradiente(led_rgb.AMARELO, led_rgb.VERMELHO, led_rgb.LEDB)
        led_rgb.alternar(led_rgb.LED_B)
        sleep(6)
        led_rgb.alternar(led_rgb.LED_B)

        # verificando se existe uma parada de emergencia 
        if (not cg.ativado()): return 2

        mesa.girar_para_ponderado(mesa.Posicoes.Sensor_B, -4)
        
        tentativas = 0
        cor = None
        while (cor == None and tentativas < 9):
            cor = sc.cor(sc.sensor_B)
            mesa.proximo_kappa()
            tentativas += 1
        
        #caso no consiga identificar a cor
        if (tentativas == 9):
            for i in range(20):
                led_rgb.alternar(led_rgb.LED_B)
                sleep(0.2)
                led_rgb.alternar(led_rgb.LED_A)
                sleep(0.2)
                
            mesa.girar_para(mesa.Posicoes.Inicial)
        
            for i in range(20):
                led_rgb.alternar(led_rgb.LED_B)
                sleep(0.2)
                led_rgb.alternar(led_rgb.LED_A)
                sleep(0.2)
                
            return 2
        
        # verificando se existe uma parada de emergencia 
        if (not cg.ativado()): return 2
        
        if(cor == sc.Cor.Amarelo):
            defeito = True
            
        if(cor == sc.Cor.Vermelho):
            mesa.girar_para(mesa.Posicoes.Inicial)
            braco.executar(braco.Movimentos.Descarte)
            return 2
    
    # verificando se existe uma parada de emergencia 
    if (not cg.ativado()): return 2
        
    mesa.girar_para(mesa.Posicoes.Inicial)
    
    # verificando se existe uma parada de emergencia 
    if (not cg.ativado()): return 2
    
    braco.executar(braco.Movimentos.Concluido)
        
    if (defeito):
        return 1
    else:
        return 0
    
    
def loop():
    global shared
    global estado
    global conn
    global pc_conc
    global pc_retr
    global pc_refu
    global pc_tot
    
    while True:
        
        if(Estados[shared.get("Estado")] == Estados.Manutencao):
            if(estado != Estados.Manutencao):
                estado = Estados.Manutencao
                atualizar_estado()
            sleep(1)
            continue
       
        if (not cg.ativado()):
            if(estado != Estados.Emergencia):
                estado = Estados.Emergencia
                atualizar_estado()
                
            shared.set("Estado", estado.name)
            led_status.desligar()
            sleep(0.5)
            continue
        else:                
            led_status.ligar()
            sleep(0.5)
        
        if (not (sr.presente() and cg.ativado())):
            if(estado != Estados.Inativo):
                estado = Estados.Inativo
                atualizar_estado()
            
            #garante que o estado nao mudou antes de o atualizar 
            sleep(1)
            if(not Estados[shared.get("Estado")] == Estados.Manutencao):
                shared.set("Estado", estado.name)
            continue
        
        
        atualizar_estado()
        estado = Estados.Ativo
        
        shared.set("Estado", estado.name)
        
        log_file("Entrou em modo:ATIVO")
        log_file(f"iniciando {pc_tot} rotina do dia")
        
        resultado = executar()
        txt = ""
        
        print("resultado: ",resultado)
        
        if(resultado == 1):
            pc_retr += 1
            txt = "retrabalhada"
            log_file(f'defeito na peca {pc_tot}')
            log_file(f'finalizando {pc_tot} rotina do dia, {pc_retr} pecas retrabalhadas')
            
        elif(resultado == 2): 
            pc_refu += 1
            txt = "refugada"
            log_file(f'falha na peca {pc_tot}')
            log_file(f'finalizando {pc_tot} rotina do dia, {pc_refu} pecas refugadas')
            
        else:
            pc_conc += 1
            txt = "concluida"
            log_file(f'finalizando {pc_tot} rotina do dia, {pc_conc + pc_refu} pecas concluidas')
            
        c = conn.cursor()
        date = datetime.now()
        c.execute(f"INSERT INTO peca (resultado, date_created) VALUES('{txt}', '{str(date)}');")
        conn.commit()
        
        pc_tot += 1 
        atualizar_estado()
    
setup()
loop()


