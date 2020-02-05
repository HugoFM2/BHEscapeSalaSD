import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from escapebhjogo.classes.logica_6 import Logica_6 # Classe com metodos da logica 2
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
    gpio_degrau1 = 24 # Primeiro degrau (raspberry)
    gpio_degrau2 = 18 # Segundo degrau (raspberry)
    gpio_degrau3 = 29 # Terceiro degrau (raspberry)
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
        GPIO.setup(cls.gpio_degrau1, GPIO.IN)
        GPIO.setup(cls.gpio_degrau3, GPIO.IN)

        # Desativar todos os reles
        Reles.desligarTodosReles()

        # Configurando GPIO's dos Extensores
        mcp.setup(cls.gp_trava, mcp.GPA, mcp.OUT, mcp.ADDRESS2)

        # Inicialmente em nivel alto (Rele desativado)
        mcp.output(cls.gp_trava, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)

    # Metodo para destravar alcapao no chao
    @classmethod
    def abrirAlcapao(cls):
        cls._concluida = True
        mcp.setup(cls.gp_trava, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        # Ativa a trava com 3 pulsos de 2s cada
        #for i in range(3):
        #    mcp.output(cls.gp_trava, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
        #    time.sleep(2)
        #    mcp.output(cls.gp_trava, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
        #    time.sleep(2)
        # Trava magnetica
        mcp.output(cls.gp_trava, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
        time.sleep(12)
        mcp.output(cls.gp_trava, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
        time.sleep(0.250)
        print('Fim ativacao alcapao - Alçapão')

    # Sobreescrevendo metodo threadLogicas() da classe pai
    @classmethod
    def threadLogica(cls):
        # Ordem correta para pisar nos degraus
        ORDEM_CORRETA = [2,4,3,1]
        ordem_degrau = []
        tempoAnterior = time.time() # Inicia o tempo de referencia

        while cls._concluida == False:
            # Checa se a logica das Invenções já foi concluida
            if Logica_6._concluida == True:

                # Se for detectado uma pisada e o se o numero do degrau não estiver na lista, adiciona ele a lista
                leitura1 = GPIO.input(cls.gpio_degrau1)
                if leitura1 == 1 and (1 in ordem_degrau) == False:
                    ordem_degrau.append(1)
                
                leitura2 = GPIO.input(cls.gpio_degrau2)
                if leitura2 == GPIO.HIGH and (2 in ordem_degrau) == False:
                    ordem_degrau.append(2)

                leitura3 = GPIO.input(cls.gpio_degrau3)
                if leitura3 == 1 and (3 in ordem_degrau) == False:
                    ordem_degrau.append(3)

                leitura4 = GPIO.input(cls.gpio_degrau4)
                if leitura4 == GPIO.HIGH and (4 in ordem_degrau) == False:
                    ordem_degrau.append(4)

                print('5ª Logica - Rodando (Degraus/Porão)' + str(ordem_degrau) ) #DEBUG

                # Checa se todos os degrais já foram pisados e checa se foi na ordem correta.
                if len(ordem_degrau) == 4 and ordem_degrau == ORDEM_CORRETA :
                    cls.abrirAlcapao()
                    print('Porão Aberto') #DEBUG
                elif len(ordem_degrau) == 4 and ordem_degrau != ORDEM_CORRETA :
                    ordem_degrau = []
                    print('Ordem incorreta nos degrais') #DEBUG
                    time.sleep(1) # Pausa checagem por 1 segundos
                    tempoAnterior = time.time()

                # Timeout
                tempoAtual = time.time()
                tempoDecorrido = tempoAtual - tempoAnterior
                if tempoDecorrido > 20 and ordem_degrau != []: # Renova o tempo de referencia
                    print('Timeout Logica 3 - ' + str(tempoDecorrido)) #DEBUG
                    ordem_degrau = [] # Zera a leitura
                    tempoAnterior = time.time()
                elif ordem_degrau == []: # Se estiver vazio sempre zera tempo anterior
                    tempoAnterior = time.time()

                time.sleep(0.15)
        
        else:
            print('5ª Logica - Finalizada')

# ------ FIM DA LOGICA 3 ---------