import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo

gpio_arma = 36 # Sensor que detecta o encaixe da arma (raspberry)
GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
GPIO.setwarnings(False) # Desativa avisos
GPIO.setup(gpio_arma, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)		
while True:
	print(GPIO.input(gpio_arma))
	time.sleep(1)

GPIO.cleanup()