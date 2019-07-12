import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo

import sys
sys.path.append('/home/pi/escapebh/escapebhserver/escapebhjogo/classes')
from mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp

# Importando a biblioteca MFRC522 que esta em uma pasta especifica
sys.path.append('/home/pi/escapebh/escapebhserver/escapebhjogo/bibliotecas/MFRC522_python_master')
from mfrc522 import MFRC522

# Trava Porta
# print('Iniciando trava porta')
# gp = 0
# mcp.output(gp, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
# time.sleep(2)
#mcp.output(gp, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)


reset_1 = 36 # GPIO ligada ao reset do RFID 1 - 2ª Sala
reset_2 = 32 # GPIO ligada ao reset do RFID 2 - 2ª Sala
reset_3 = 33 # GPIO ligada ao reset do RFID 7 - 1ª Sala

GPIO.setmode(GPIO.BOARD) # Configuras as GPIO como BOARD(Contagem de 1 a 40). www.pinout.xyz
GPIO.setwarnings(False)

# Configura todos as GPIO ligada a reset's como saida
GPIO.setup(reset_1, GPIO.OUT)
GPIO.setup(reset_2, GPIO.OUT)
GPIO.setup(reset_3, GPIO.OUT)

# Inicialmente todos os reset em nivel baixo (RFIDS desativados)
GPIO.output(reset_1, GPIO.LOW)
GPIO.output(reset_2, GPIO.LOW)
GPIO.output(reset_3, GPIO.LOW)

# Inicia variaveis usadas ao longo do loop
seletor = 0 # Variavel que diz qual RFID ler
contador = 0 # Variavel que contador o numero de leituras

print('Leitura Inciada! Aproxime seu cartão RFID')

while True:
    # Incrementa o seletor e se ele for maior que o numero de RFID's volta para 1
    seletor = seletor + 1
    if seletor > 3:
        seletor = 1

    # Faz o ajuste do pino de reset de acordo com o RFID
    if seletor == 1: # Reset do RFID 1 Ativado
        GPIO.output(reset_1, GPIO.HIGH)
        GPIO.output(reset_2, GPIO.LOW)
        GPIO.output(reset_3, GPIO.LOW)
        time.sleep(.2)
        LeitorRFID = MFRC522() # inicia o novo módulo RFID-RC522.
    elif seletor == 2: # Reset do RFID 2 Ativado
        GPIO.output(reset_1, GPIO.LOW)
        GPIO.output(reset_2, GPIO.HIGH)
        GPIO.output(reset_3, GPIO.LOW)
        time.sleep(.2)
        LeitorRFID = MFRC522() # inicia o novo módulo RFID-RC522.
    elif seletor == 3: # Reset do RFID 3 Ativado
        GPIO.output(reset_1, GPIO.LOW)
        GPIO.output(reset_2, GPIO.LOW)
        GPIO.output(reset_3, GPIO.HIGH)
        time.sleep(.2)
        LeitorRFID = MFRC522() # inicia o novo módulo RFID-RC522.

    time.sleep(.1) # 50ms para o raspberry fazer as configuracoes

    # Verifica se existe uma tag proxima do módulo rfid.
    status, tag_type = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)

    if status == LeitorRFID.MI_OK:

        # Efetua leitura do UID do cartão.
        status, uid = LeitorRFID.MFRC522_Anticoll()

        if status == LeitorRFID.MI_OK:
            contador = contador + 1
            print('CARTÃO DETECTADOR NO RFID ' + str(seletor) + "! Leitura: " + str(contador))

            uid = ':'.join(['%X' % x for x in uid])
            print('UID do cartão: %s' % uid)
            
            print('\nAproxime o cartão RFID ')

        print('Cartao detectado')
    
    #time.sleep(1)