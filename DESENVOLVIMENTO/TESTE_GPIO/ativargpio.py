""" Esse script server para colocar um determinado
pino da raspberry é em nivel alto ou baixo.

Autor: Salamaker
Data: 07/06/2019
"""

import RPi.GPIO as GPIO # Modulo de controle GPIO
import os # Modulo de controle do terminal
os.system('pinout') # Imprimi os pinos da raspberry na serial

# ---- MAPA DE PINOS ----
# 1,17 -> 3.3v
# 2,4 -> 5v
# 6,9,14,20,25,30,34,39 -> GND
pinosImpares = [3,5,7,11,13,15,19,21,23,27,29,31,33,35,37]
pinosPares = [8,10,12,16,18,22,24,26,28,32,36,38,40]

# Configura as GPIOs como BOARD, Contagem de 0 a 40
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

try:
    """ Loop para colocar em HIGH ou LOW uma GPIO """

    print('\n  ------ SCRIPT DE CONTROLE INICIADO - SALA MAKER ---------')
    while True:
        print('   Numero do pino (1 a 40): ', end='')
        pino = input() # Recebe o numero do pino BOARD
        print('   Definir estado 0 para LOW ou 1 para HIGH: ', end='')
        nivel = input() # Recebe o nivel que o pino sera setado
        print('\tPino ' + pino + ' colocado em nivel ' + nivel + '\n')
        print('  ------------------------------------\n')
        
        pino = int(pino)
        nivel = int(nivel)

        if pino in pinosImpares or pino in pinosPares:
            if nivel == 1:
                GPIO.setup(pino , GPIO.OUT)
                GPIO.output(pino, GPIO.HIGH)
            elif nivel == 0:
                GPIO.setup(pino , GPIO.OUT)
                GPIO.output(pino, GPIO.LOW)
            else:
                print('Nivel diferente de 0 e 1, pino nao setado')
        else:
            print('Pino não reconhecido, valor fora da lista de pinos')

except KeyboardInterrupt:
    #""" Ao precionar Ctrl + C, encerra o programa. """
    #GPIO.cleanup() # Reseta ao padrão as GPIOs
    print('\n --> Teste encerrado. <--')