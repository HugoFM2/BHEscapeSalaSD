#!/usr/bin/env python
# -*- coding: utf8 -*-
 
import time
import RPi.GPIO as GPIO
# import MFRC522
# Corrigindo Import
import sys
sys.path.append('/home/pi/guilhermeweb/controlegpio/bibliotecas/MFRC522-python')
from mfrc522 import MFRC522

# UID dos cartões que possuem acesso liberado.
CARTOES_LIBERADOS = {
    '29:C5:92:55:2B' : 'CARTÃO A',
    '59:DD:C4:56:16' : 'CARTÃO B',
    'E9:2:C2:56:7F' : 'CARTÃO C',
}

# ORDEM CORRETA DOS CARTOES PARA LIBERAR ACESSO
ORDEM_CORRETA = ['29:C5:92:55:2B','59:DD:C4:56:16','E9:2:C2:56:7F']

# COMANDO EXTERNO do terminal
#import os
#print("\n\tReiniciando comunicacao SPI\n")
#os.system("lsmod")
#os.system("sudo rmmod spi_bcm2835 && sudo modprobe spi_bcm2835")
#time.sleep(1)
#print("\t->OK!\n")

try:
    # *RESET FORÇADO, RFID 02 usa modo BOARD. 18=BCM24
    # *RESET FORÇADO, RFID 03 usa modo BOARD. 16=BCM23
    # *RESET FORÇADO, RFID 01 usa modo BOARD. 12=BCM18
    # *Com o reset em HIGH o rfid recebe dados
    # *Com o reset em LOW o rfid nao recebe dados

    reset_1 = 12 # GPIO ligada ao reset do RFID 1
    reset_2 = 18 # GPIO ligada ao reset do RFID 2
    reset_3 = 16 # GPIO ligada ao reset do RFID 3
    pino_trava = 3 # GPIO ligada ao rele da trava
    
    GPIO.setmode(GPIO.BOARD) # Configuras as GPIO como BOARD(Contagem de 1 a 40). www.pinout.xyz
    
    GPIO.setup(reset_1, GPIO.OUT)
    GPIO.setup(reset_2, GPIO.OUT)
    GPIO.setup(reset_3, GPIO.OUT)

    # Inicialmente todos os reset em nivel baixo (RFIDS desativados)
    GPIO.output(reset_1, GPIO.LOW)
    GPIO.output(reset_2, GPIO.LOW)
    GPIO.output(reset_3, GPIO.LOW)

    # ------TRAVA
    GPIO.setup(pino_trava, GPIO.OUT)
    GPIO.output(pino_trava,GPIO.LOW)
    
    # Inicia o módulo RC522.
    # LeitorRFID = MFRC522.MFRC522()
    # ->Corrigindo import
    LeitorRFID = MFRC522()

    # IMPRIMI O MODO QUE AS GPIO ESTAO CONFIGURADAS, 11=BCM e 10 = BOARD
    if GPIO.getmode() == 10:
        print("Modo GPIO: BOARD")
    elif GPIO.getmode() == 11:
        print("Modo GPIO: BCM")
    else:
        print("Modo desconhecido: " + GPIO.getmode())

    print('Leitura Inciada! Aproxime seu cartão RFID')

    seletor = 0 # Variavel que diz qual RFID ler
    lista_leitura = [None,None,None] # Lista que ira armazenar ordem de leitura
    contador = 0

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
            time.sleep(.05)
            LeitorRFID = MFRC522()
        elif seletor == 3: # Reset do RFID 2 Ativado
            GPIO.output(reset_1, GPIO.LOW)
            GPIO.output(reset_2, GPIO.HIGH)
            GPIO.output(reset_3, GPIO.LOW)
            time.sleep(.05)
            LeitorRFID = MFRC522()
        elif seletor == 2: # Reset do RFID 3 Ativado
            GPIO.output(reset_1, GPIO.LOW)
            GPIO.output(reset_2, GPIO.LOW)
            GPIO.output(reset_3, GPIO.HIGH)
            time.sleep(.05)
            LeitorRFID = MFRC522()
 
        time.sleep(.05) # 50ms para o raspberry fazer as configuracoes

        # Verifica se existe uma tag próxima do módulo.
        status, tag_type = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)
 
        if status == LeitorRFID.MI_OK:
            contador = contador + 1 # Contador de leitura
            print('CARTÃO DETECTADOR NO RFID ' + str(seletor) + "! Leitura: " + str(contador))
 
            # Efetua leitura do UID do cartão.
            status, uid = LeitorRFID.MFRC522_Anticoll()
 
            if status == LeitorRFID.MI_OK:
                uid = ':'.join(['%X' % x for x in uid])
                print('UID do cartão: %s' % uid)
 
                # Se o cartão está cadastrado, mostra a indentificacao
                if uid in CARTOES_LIBERADOS:
                    print('Acesso Liberado!')
                    print('Cartão: %s.' % CARTOES_LIBERADOS[uid])
                else:
                    print('Cartao nao cadastrado!')

                #Adicionar leitura na lista lista_leitura
                lista_leitura[seletor - 1] = uid
                
                # Verifica se a lista foi totalmente preenchida 
                if not None in lista_leitura:
                    print("\n=============\nLista preenchida!")
                    print(lista_leitura)
                    
                    # Verifica se as lista de leitura foi igual a lista de ordem correta
                    if lista_leitura == ORDEM_CORRETA:
                        print("\tOrdem correta!")
                        GPIO.output(pino_trava, GPIO.HIGH)
                        time.sleep(.2)
                        GPIO.output(pino_trava, GPIO.LOW)
                        break
                    else:
                        print("\tOrdem incorreta!")
                
                    print("\n\n")
                    lista_leitura = [None,None,None] # Apaga as leituras em ordem guardadas na lista

                    #GPIO.cleanup()
                    #break # Finaliza o programa
                
                print('\nAproxime o cartão RFID ')                
            
except KeyboardInterrupt:
    # Ao precionar Ctrl + C
    # encerra o programa.
    #GPIO.cleanup()
    print('nPrograma encerrado.')
