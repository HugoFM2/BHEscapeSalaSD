import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from escapebhjogo.classes.logica_2 import Logica_2 # Classe com metodos da logica 2
from .logica_geral import Logica_geral
from escapebhjogo.classes.reles import Reles

""" CLASSE LOGICA 3
Esta classe faz todo o controle dos itens relacionados a Logica 3

Marrom -> Pisando nos degraus no padrão certo vai soltar a tranca do alçapão (ou uma gaveta
caso não tenha como abrir o alçapão).
"""
class Logica_3(Logica_geral):
    
    # GPIO's
    # Degraus contados de baixo para cima
    gpio_degrau1 = 3 # Primeiro degrau - GPA 3 (Extensor 0x22)
    gpio_degrau2 = 18 # Segundo degrau (raspberry)
    gpio_degrau3 = 1 # Terceiro degrau - GPA 1(Extensor 0x22)
    gpio_degrau4 = 16 # Quarto degrau (raspberry)
    gp_trava = 3 # Rele da trava do alçapão - GPA 3 (extensor 0x24)

    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls):
        GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
        GPIO.setwarnings(False) # Desativa avisos
        
        # Configurado GPIO's do raspberry
        GPIO.setup(cls.gpio_degrau2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_degrau4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

        # Desativar todos os reles
        Reles.desligarTodosReles()

        # Configurando GPIO's dos Extensores
        mcp.setup(cls.gpio_degrau1, mcp.GPA, mcp.IN, mcp.ADDRESS1)
        mcp.setup(cls.gpio_degrau3, mcp.GPA, mcp.IN, mcp.ADDRESS1)
        mcp.setup(cls.gp_trava, mcp.GPA, mcp.OUT, mcp.ADDRESS2)

        # Inicialmente em nivel alto (Rele desativado)
        mcp.output(cls.gp_trava, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)

    # Metodo para destravar alcapao no chao
    @classmethod
    def abrirAlcapao(cls):
        cls._concluida = True
        mcp.setup(cls.gp_trava, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        # Trava acionada por pulsos durante 20s
        for i in range(8):
            mcp.output(cls.gp_trava, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
            time.sleep(0.25)
            mcp.output(cls.gp_trava, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
            time.sleep(2)
        print('Fim dos pulsos - Alçapão')

    # Sobreescrevendo metodo threadLogicas() da classe pai
    @classmethod
    def threadLogica(cls):
        # Ordem correta para pisar nos degraus
        ORDEM_CORRETA = [4,3,2,1]
        ordem_degrau = []
        tempoAnterior = time.time() # Inicia o tempo de referencia

        while cls._concluida == False:
            # Checa se a logica 2 já foi concluida
            if Logica_2._concluida == True:

                # Se for detectado uma pisada e o se o numero do degrau não estiver na lista, adiciona ele a lista
                leitura1 = mcp.input(cls.gpio_degrau1, mcp.GPA, mcp.ADDRESS1)
                if leitura1 == 1 and (1 in ordem_degrau) == False:
                    ordem_degrau.append(1)
                
                leitura2 = GPIO.input(cls.gpio_degrau2)
                if leitura2 == GPIO.HIGH and (2 in ordem_degrau) == False:
                    ordem_degrau.append(2)

                leitura3 = mcp.input(cls.gpio_degrau3, mcp.GPA, mcp.ADDRESS1)
                if leitura3 == 1 and (3 in ordem_degrau) == False:
                    ordem_degrau.append(3)

                leitura4 = GPIO.input(cls.gpio_degrau4)
                if leitura4 == GPIO.HIGH and (4 in ordem_degrau) == False:
                    ordem_degrau.append(4)

                print('Logica 3 - Rodando ' + str(ordem_degrau) ) #DEBUG

                # Checa se todos os degrais já foram pisados e checa se foi na ordem correta.
                if len(ordem_degrau) == 4 and ordem_degrau == ORDEM_CORRETA :
                    cls.abrirAlcapao()
                    print('Alçapão Aberto (Logica 3)') #DEBUG
                elif len(ordem_degrau) == 4 and ordem_degrau != ORDEM_CORRETA :
                    ordem_degrau = []
                    print('Ordem incorreta (Logica 3)') #DEBUG
                    time.sleep(1) # Pausa checagem por 1 segundos

                # Timeout
                tempoAtual = time.time()
                tempoDecorrido = tempoAtual - tempoAnterior
                if tempoDecorrido > 5 and ordem_degrau != []: # Renova o tempo de referencia
                    print('Timeout Logica 3 - ' + str(tempoDecorrido)) #DEBUG
                    ordem_degrau = [] # Zera a leitura
                    tempoAnterior = time.time()
                elif ordem_degrau == []: # Se estiver vazio sempre zera tempo anterior
                    tempoAnterior = time.time()

                time.sleep(0.25)
        
        else:
            print('Logica 3 - Finalizada')

# ------ FIM DA LOGICA 3 ---------