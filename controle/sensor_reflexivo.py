import RPi.GPIO as IO

IO.setmode(IO.BOARD)
IO.setup(37, IO.IN)

def presente():
    return IO.input(37)