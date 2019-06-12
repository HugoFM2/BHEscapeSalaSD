""" Leitura de GPIOs como INPUT
Autor: Salamaker
Data: 07/06/2019
"""
# modulos de controle de GPIO e de tempo
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# 1,17 -> 3.3v
# 2,4 -> 5v
# 6,9,14,20,25,30,34,39 -> GND
# Nao pode ser INPUT, 27 e 28
pinosImpares = [3,5,7,11,13,15,19,21,23,29,31,33,35,37] # Nao INPUT 27
pinosPares = [8,10,12,16,18,22,24,26,32,36,38,40] # Nao INPUT 28

for i in range(0 , len(pinosImpares)):
    print(pinosImpares[i], end=' ')
    GPIO.setup(pinosImpares[i] , GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    time.sleep(0.05)

for i in range(0 , len(pinosPares)):
    print(pinosPares[i], end=' ')
    GPIO.setup(pinosPares[i] , GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    time.sleep(0.05)

# Inicia o loop, e se pressionado Ctrl + C finaliza o programa.
try:
    contador = 1
    while True:
        print('\n -------------- Leitura Nº ' + str(contador) )
        contador = contador + 1
        
        # Leitura das GPIO's definidas como INPUT
        for i in range(0 , len(pinosImpares)):
            print('Leitura digital pino %d = %d' % (pinosImpares[i], GPIO.input(pinosImpares[i])) )

        for i in range(0 , len(pinosPares)):
            print('Leitura digital pino %d = %d' % (pinosPares[i], GPIO.input(pinosPares[i])) )
        time.sleep(2) # Pausa de 2 segundos entre impressoes
        
except KeyboardInterrupt:
    # Ao precionar Ctrl + C, encerra o programa.
    #GPIO.cleanup() # Reseta ao padrão as GPIOs
    print('\n --> Leitura encerrada. <--')