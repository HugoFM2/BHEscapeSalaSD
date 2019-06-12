#!/usr/bin/env python
# -*- coding: utf8 -*-
 
import time
import RPi.GPIO as GPIO
#import MFRC522
#Corrigindo Import
import sys
sys.path.append('/home/pi/guilhermeweb/controlegpio/bibliotecas/MFRC522-python')
from mfrc522 import MFRC522
 
# UID dos cartões que possuem acesso liberado.
CARTOES_LIBERADOS = {
    '69:E0:FE:20:57': 'Tag Chaveiro',
    '59:DD:C4:56:16': 'Tag Cartao',
}

try:
    # Inicia o módulo RC522.
    #LeitorRFID = MFRC522.MFRC522()
    #->Corrigindo import
    LeitorRFID = MFRC522()
    
    print('Aproxime seu cartão RFID')
 
    while True:
        # Verifica se existe uma tag próxima do módulo.
        status, tag_type = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)
 
        if status == LeitorRFID.MI_OK:
            print('Cartão detectado!')
 
            #Efetua leitura do UID do cartão.
            status, uid = LeitorRFID.MFRC522_Anticoll()
 
            if status == LeitorRFID.MI_OK:
                uid = ':'.join(['%X' % x for x in uid])
                print('UID do cartão: %s' % uid)
 
                # Se o cartão está liberado exibe mensagem de boas vindas.
                if uid in CARTOES_LIBERADOS:
                    print('Acesso Liberado!')
                    print('Olá %s.' % CARTOES_LIBERADOS[uid])
                else:
                    print('Acesso Negado!')
 
                print('\nAproxime seu cartão RFID ')
 
        time.sleep(.25)
except KeyboardInterrupt:
    # Se o usuário precionar Ctrl + C
    # encerra o programa.
    GPIO.cleanup()
    print('nPrograma encerrado.')