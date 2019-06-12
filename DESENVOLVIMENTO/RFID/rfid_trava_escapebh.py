#!/usr/bin/env python
# -*- coding: utf8 -*-

# Importa as bibliotecas de tempo e controle da GPIO 
import time
import RPi.GPIO as GPIO

# Importando a biblioteca MFRC522 que esta em uma pasta especifica
import sys
sys.path.append('/home/pi/guilhermeweb/controlegpio/bibliotecas/MFRC522-python')
from mfrc522 import MFRC522

# UID's dos cartões que possuem acesso liberado.
CARTOES_LIBERADOS = {
    '29:C5:92:55:2B' : 'CARTÃO A',
    '59:DD:C4:56:16' : 'CARTÃO B',
    'E9:2:C2:56:7F' : 'CARTÃO C',
}

# LISTA COM ORDEM CORRETA DOS ID'S DOS CARTOES PARA LIBERAR ACESSO
ORDEM_CORRETA = ['29:C5:92:55:2B','59:DD:C4:56:16','E9:2:C2:56:7F']

try:
    # Esquema de ligacao GPIO, placa no modo BOARD(Contagem de 1 a 40). Pinngaem: www.pinout.xyz
    # A biblioteca MFRC522 adota a contagem como BOARD
    # RESET do RFID 01 no pino 12 = BCM18
    # RESET do RFID 02 no pino 16 = BCM23
    # RESET do RFID 03 no pino 18 = BCM24
    # *Com o reset em HIGH o rfid recebe dados
    # *Com o reset em LOW o rfid nao recebe dados
    # *Jamais dois RESET's devem estar em alto ao mesmo tempo

    reset_1 = 12 # GPIO ligada ao reset do RFID 1
    reset_2 = 16 # GPIO ligada ao reset do RFID 2
    reset_3 = 18 # GPIO ligada ao reset do RFID 3
    pino_trava = 3 # GPIO ligada ao modulo rele (Pois a trava trabalha com 12v)
    
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

    # --Ajuste do pino que aciona o modulo rele ligado a TRAVA
    GPIO.setup(pino_trava, GPIO.OUT)
    GPIO.output(pino_trava,GPIO.LOW)

    # Inicia variaveis usadas ao longo do loop
    seletor = 0 # Variavel que diz qual RFID ler
    lista_leitura = [None,None,None] # Lista que ira armazenar ordem de leitura,  inicialmente vazia
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
            time.sleep(.05)
            LeitorRFID = MFRC522() # inicia o novo módulo RFID-RC522.
        elif seletor == 2: # Reset do RFID 2 Ativado
            GPIO.output(reset_1, GPIO.LOW)
            GPIO.output(reset_2, GPIO.HIGH)
            GPIO.output(reset_3, GPIO.LOW)
            time.sleep(.05)
            LeitorRFID = MFRC522() # inicia o novo módulo RFID-RC522.
        elif seletor == 3: # Reset do RFID 3 Ativado
            GPIO.output(reset_1, GPIO.LOW)
            GPIO.output(reset_2, GPIO.LOW)
            GPIO.output(reset_3, GPIO.HIGH)
            time.sleep(.05)
            LeitorRFID = MFRC522() # inicia o novo módulo RFID-RC522.
 
        time.sleep(.05) # 50ms para o raspberry fazer as configuracoes

        # Verifica se existe uma tag proxima do módulo rfid.
        status, tag_type = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)
 
        if status == LeitorRFID.MI_OK:
            contador = contador + 1
            print('CARTÃO DETECTADOR NO RFID ' + str(seletor) + "! Leitura: " + str(contador))
 
            # Efetua leitura do UID do cartão.
            status, uid = LeitorRFID.MFRC522_Anticoll()
 
            if status == LeitorRFID.MI_OK:
                uid = ':'.join(['%X' % x for x in uid])
                print('UID do cartão: %s' % uid)
 
                # Se o cartão está cadastrado, mostra a indentificacao
                if uid in CARTOES_LIBERADOS:
                    #print('Acesso Liberado!')
                    print('Cartão: %s.' % CARTOES_LIBERADOS[uid])
                else:
                    print('Cartao nao cadastrado!')

                #Adicionar leitura na lista lista_leitura, o indice comeca em 0.
                lista_leitura[seletor - 1] = uid
                
                # Verifica se a lista foi totalmente preenchida 
                if not None in lista_leitura:
                    print("\n=============\nLista preenchida!")
                    print(lista_leitura)
                    
                    # Verifica se as lista de leitura foi igual a lista de ordem correta
                    if lista_leitura == ORDEM_CORRETA:
                        print("\tOrdem correta!\n\tTRAVA LIBERADA!")
                        GPIO.output(pino_trava, GPIO.HIGH)
                        time.sleep(.2)
                        GPIO.output(pino_trava, GPIO.LOW)
                        #GPIO.cleanup() # Volta as GPIO para modo padrão
                        break # Finaliza o loop
                    else:
                        print("\tOrdem incorreta!")
                
                    print("\n\n")
                    lista_leitura = [None,None,None] # Apaga as leituras em ordem guardadas na lista

                    
                    #break 
                
                print('\nAproxime o cartão RFID ')                
            
except KeyboardInterrupt:
    # Ao precionar Ctrl + C, encerra o programa.
    #GPIO.cleanup()
    print('\n --> Programa encerrado. <--')
