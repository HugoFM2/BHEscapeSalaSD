import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo



gpio_chave2 = 22 # Segunda chave (Direita) (raspberry)
enable_buttonpress_chave2 = False # Habilita ao apertar o botao da chave 2 libera a porta
GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
GPIO.setwarnings(False) # Desativa avisos
GPIO.setup(gpio_chave2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)	

while True:


	if GPIO.input(gpio_chave2) == False: 
		print("Chave girada, aguardando apertar seu botao")
		enable_buttonpress_chave2 = True
		time.sleep(0.1)
		continue

	if enable_buttonpress_chave2:

		if GPIO.input(gpio_chave2):
			print("LIBERAR SISTEMA")
			



	# print(GPIO.input(gpio_chave2))
	time.sleep(0.1)

GPIO.cleanup()