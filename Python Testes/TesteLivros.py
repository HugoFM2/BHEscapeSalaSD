import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo

gpio_livro1 = 10 # Primeiro livro (raspberry)
gpio_livro2 = 13 # Segundo livro (raspberry)
gpio_livro3 = 12 # Terceiro livro (raspberry)
GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
GPIO.setwarnings(False) # Desativa avisos
GPIO.setup(gpio_livro1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(gpio_livro2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)	
GPIO.setup(gpio_livro3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)	
while True:
	# print(GPIO.input(gpio_arma))
	leitura = [GPIO.input(gpio_livro1), GPIO.input(gpio_livro2), GPIO.input(gpio_livro3)]
	print(leitura)
	time.sleep(0.3)

GPIO.cleanup()