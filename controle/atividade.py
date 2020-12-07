import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

BOTAO_ATIVIDADE = 38

GPIO.setup(BOTAO_ATIVIDADE, GPIO.IN)

def ativado():
    return GPIO.input(BOTAO_ATIVIDADE)