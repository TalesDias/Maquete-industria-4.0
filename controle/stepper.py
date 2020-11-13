import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT) # STEP
GPIO.setup(10, GPIO.OUT) #DIR
GPIO.setwarnings(False)
GPIO.output(8, True)

GPIO.setup(11, GPIO.OUT) #MS3
GPIO.output(11, True)
GPIO.setup(13, GPIO.OUT) #MS2
GPIO.output(13, True)
GPIO.setup(15, GPIO.OUT) #MS1
GPIO.output(15, True)

#iemand anders 500 

step = GPIO.PWM(8, 5000)

def SpinMotor(direcao, num_steps):
    step.ChangeFrequency(5000)
    GPIO.output(10, direcao)
    while num_steps > 0:
        step.start(1)
        time.sleep(0.01)
        num_steps -= 1
    step.stop()
    GPIO.cleanup()
    return True

direction_input = input('Please enter 0 or C Open or Close:')
num_steps = int(input('Please enter the number of steps: '))

if direction_input == 'C':
    SpinMotor(False, num_steps)
else:
    SpinMotor(True, num_steps)

