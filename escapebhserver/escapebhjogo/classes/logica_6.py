import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from .logica_geral import Logica_geral
from escapebhjogo.classes.logica_5 import Logica_5 # Classe com metodos da logica 5
# https://github.com/pimylifeup/MFRC522-python -> Biblioteca para trabalhar com RFID
from escapebhjogo.bibliotecas.MFRC522_python_master.mfrc522 import MFRC522

""" CLASSE LOGICA 6
Esta classe faz todo o controle dos itens relacionados a Logica 6

Preto -> Colocando todas as invenções nas prateleiras vai fazer com que o motor na segunda
sala ative, liberando a chave. (Explicando melhor essa parte: Ao invés de ser apenas a chave
caindo como é o atual avião que desce, será uma peça do teto que estará presa por uma
dobradiça e o motor. Quando o motor descer essa peça do teto vai abrir como se fosse uma
pequena gaveta e a chave irá deslizar)
"""

class Logica_6(Logica_geral):

    # GPIO's
    gpio_rfid = [None,None,None,None,None,None,None] # Criar um 'vetor'
    gpio_rfid[0] = 7 # Primeiro RFID (raspberry)
    gpio_rfid[1] = 11 # Segundo RFID (raspberry)
    gpio_rfid[2] = 13 # Terceiro RFID (raspberry)
    gpio_rfid[3] = 15 # Quarto RFID (raspberry)
    gpio_rfid[4] = 29 # Quinto RFID (raspberry)
    gpio_rfid[5] = 31 # Sexto RFID (raspberry)
    gpio_rfid[6] = 33 # Setimo RFID (raspberry)
    gp_motorDescer = 2 # Rele Desce Motor - GPB 2 (extensor 0x24)
    gp_motorSubir = 5 # Rele Sobe Motor - GPB 5 (extensor 0x24)

    # IMPLEMENTAR RFIDS DA SEGUNDA SALA
    pass

    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls):
        GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
        GPIO.setwarnings(False) # Desativa avisos
        
        # Configurado GPIO's do raspberry
        # Configura todos as GPIO ligada ao reset's como saida
        GPIO.setup(cls.gpio_rfid[0], GPIO.OUT)
        GPIO.setup(cls.gpio_rfid[1], GPIO.OUT)
        GPIO.setup(cls.gpio_rfid[2], GPIO.OUT)
        GPIO.setup(cls.gpio_rfid[3], GPIO.OUT)
        GPIO.setup(cls.gpio_rfid[4], GPIO.OUT)
        GPIO.setup(cls.gpio_rfid[5], GPIO.OUT)
        GPIO.setup(cls.gpio_rfid[6], GPIO.OUT)

        # Inicialmente todos os reset em nivel baixo (RFIDS desativados)
        GPIO.output(cls.gpio_rfid[0], GPIO.LOW)
        GPIO.output(cls.gpio_rfid[1], GPIO.LOW)
        GPIO.output(cls.gpio_rfid[2], GPIO.LOW)
        GPIO.output(cls.gpio_rfid[3], GPIO.LOW)
        GPIO.output(cls.gpio_rfid[4], GPIO.LOW)
        GPIO.output(cls.gpio_rfid[5], GPIO.LOW)
        GPIO.output(cls.gpio_rfid[6], GPIO.LOW)

        # Configurando GPIO's do Extensor
        mcp.setup(cls.gp_motorDescer, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
        mcp.setup(cls.gp_motorSubir, mcp.GPB, mcp.OUT, mcp.ADDRESS2)

        # Inicialmente em nivel alto (Desativado)
        mcp.output(cls.gp_motorDescer, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)
        mcp.output(cls.gp_motorSubir, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

    # Metodo para acionar o motor no sentindo de descer a "gaveta"
    @classmethod
    def descerMotor(cls):
        cls._concluida = True
        mcp.setup(cls.gp_motorDescer, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_motorDescer, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
        time.sleep(0.5)
        mcp.output(cls.gp_motorDescer, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

    # Metodo para acionar o motor no sentindo de subir a "gaveta"
    @classmethod
    def subirMotor(cls):
        mcp.setup(cls.gp_motorSubir, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_motorSubir, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
        time.sleep(0.5)
        mcp.output(cls.gp_motorSubir, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

    # Sobreescrevendo metodo threadLogica() da classe pai
    @classmethod
    def threadLogica(cls):
        
        # UID's dos cartões que possuem acesso liberado.
        CARTOES_CADASTRADOS = {
            '29:C5:92:55:2B' : 'CARTÃO A',
            '59:DD:C4:56:16' : 'CARTÃO B',
            'E9:2:C2:56:7F' : 'CARTÃO C',
        }

        # LISTA COM ORDEM CORRETA DOS ID'S DOS CARTOES PARA LIBERAR ACESSO
        ORDEM_CORRETA = ['29:C5:92:55:2B','59:DD:C4:56:16','E9:2:C2:56:7F']

        seletor = 0 # Variavel que ira escolher qual RFID ler
        lista_leitura = [None,None,None,None,None,None,None] # Lista que ira armazenar ordem de leitura,  inicialmente vazia

        print('Leitura Inciada! Aproxime seu cartão RFID')

        while cls._concluida == False:
            # Checa se a logica 5 já foi concluida
            if Logica_5._concluida == True:

                # Ativar algum RFID
                rfidAtivo = cls.ativarRfid(seletor)

                # Incrementa o seletor e se ele for maior que o numero de RFID's(7) volta para 0
                seletor = seletor + 1
                if seletor > 6:
                    seletor = 0

                # Verifica se existe uma tag proxima do módulo rfid.
                status, tag_type = rfidAtivo.MFRC522_Request(rfidAtivo.PICC_REQIDL)

                if status == rfidAtivo.MI_OK:

                    print('CARTÃO DETECTADO NO RFID ' + str(seletor) + '!')
                    
                    # Efetua leitura do UID do cartão.
                    status, uid = rfidAtivo.MFRC522_Anticoll()

                    if status == rfidAtivo.MI_OK:
                        uid = ':'.join(['%X' % x for x in uid])
                        print('UID do cartão: %s' % uid)
        
                        # Se o cartão está cadastrado, mostra a indentificacao
                        if uid in CARTOES_CADASTRADOS:
                            #print('Acesso Liberado!')
                            print('Identificação: %s.' % CARTOES_CADASTRADOS[uid])
                        else:
                            print('Cartao nao cadastrado!')

                        #Adicionar leitura na lista lista_leitura, o indice comeca em 0.
                        lista_leitura[seletor] = uid
                        
                        # Verifica se a lista foi totalmente preenchida (Não contem itens vazios)
                        if not None in lista_leitura:
                            print("Lista preenchida!")
                            print(lista_leitura)
                            
                            # Verifica se a lista de leitura é igual a lista de ORDEM_CORRETA
                            if lista_leitura == ORDEM_CORRETA:
                                print("Ordem correta!")
                                cls.descerMotor()
                            else:
                                print("Ordem incorreta!")
                        
                            lista_leitura = [None,None,None,None,None,None,None] # Apaga as leituras em ordem guardadas na lista

                        print('Aproxime o cartão RFID ')

                print('Logica 6 - Rodando')
                cls._concluida = True #Força a conclusao da logica
            time.sleep(1)
        
        else:
            print('Logica 6 - Finalizada')

    # Metodo para trabalhar com os reset's do RFID, deixando somente 1 ativo
    @classmethod
    def ativarRfid(cls, nRfid):
        """Este metodo recebe o parametro nRfid, que é um inteiro de 0 a 6
        Este parametro desabilita todos os rfids e deixa ativo somente o rfid passado
        como argumento.
        """
        for i in range(0,7): # 0,1,2,3,4,5,6
            if i == nRfid: # Coloca o pino reset em nivel alto, assim ativado o RFID
                GPIO.output(cls.gpio_rfid[i], GPIO.HIGH)
            else: # Coloca o pino reset em nivel baixo nos demais, assim desativado os outros RFID's
                GPIO.output(cls.gpio_rfid[i], GPIO.LOW)

        time.sleep(.05) # 50ms para o raspberry fazer as configuracoes
        LeitorRFID = MFRC522() # inicia o módulo RFID-RC522 com um novo RFID

        return LeitorRFID


# ------ FIM DA LOGICA 6 ---------