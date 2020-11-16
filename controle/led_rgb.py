import smbus,time

bus = smbus.SMBus(1)
 
DEVICE = 0x20 # Device address (A0-A2)
INIT = 0x00 
ADDRA  = 0x14
ADDRB  = 0x13
 
# Set all GPA pins as outputs
bus.write_byte_data(DEVICE, INIT,0x00)
 
# Set output all 7 output bits to 0
bus.write_byte_data(DEVICE, ADDRA, 0)
bus.write_byte_data(DEVICE, ADDRB, 0)


PRETO    = 0b0000_0000
AZUL     = 0b0000_0001
VERDE    = 0b0000_0010
CIANO    = 0b0000_0011
VERMELHO = 0b0000_0100
VIOLETA  = 0b0000_0101
AMARELO  = 0b0000_0110
BRANCO   = 0b0000_0111

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

