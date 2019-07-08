import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from escapebhjogo.classes.logica_2 import Logica_2 # Classe com metodos da logica 2
from .logica_geral import Logica_geral

""" CLASSE LOGICA 3
Esta classe faz todo o controle dos itens relacionados a Logica 3

Marrom -> Pisando nos degraus no padrão certo vai soltar a tranca do alçapão (ou uma gaveta
caso não tenha como abrir o alçapão).
"""
class Logica_3(Logica_geral):
    
    # GPIO's
    gpio_degrau1 = 0 # Primeiro degrau (raspberry)
    gpio_degrau2 = 0 # Segundo degrau (raspberry)
    gpio_degrau3 = 0 # Terceiro degrau (raspberry)
    gpio_degrau4 = 0 # Quarto degrau (raspberry)
    gp_trava = 0 # Rele da trava do alçapão (extensor)

    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls):
        GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
        GPIO.setwarnings(False) # Desativa avisos
        
        # Configurado GPIO's do raspberry
        GPIO.setup(cls.gpio_degrau1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_degrau2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_degrau3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_degrau4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

        # Configurando GPIO's do Extensor
        mcp.setup(cls.gp_trava, mcp.GPA, mcp.OUT, mcp.ADDRESS2)

        # Inicialmente em nivel baixo
        mcp.output(cls.gp_trava, mcp.GPA, mcp.LOW, mcp.ADDRESS2)

    # Metodo para destravar alcapao no chao
    @classmethod
    def abrirAlcapao(cls):
        cls._concluida = True
        mcp.setup(cls.gp_trava, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_trava, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
        time.sleep(30)
        mcp.output(cls.gp_trava, mcp.GPA, mcp.LOW, mcp.ADDRESS2)

    # Sobreescrevendo metodo threadLogicas() da classe pai
    @classmethod
    def threadLogica(cls):
        # Ordem correta para pisar nos degraus
        ORDEM_CORRETA = [4,3,2,1]
        ordem_degrau = []

        while cls._concluida == False:
            # Checa se a logica 2 já foi concluida
            if Logica_2._concluida == True:

                # Se for detectado uma pisada e o se o numero do degrau não estiver na lista, adiciona ele a lista
                if GPIO.input(cls.gpio_degrau1) == GPIO.HIGH and (1 in ordem_degrau) == False:
                    ordem_degrau.append(1)
                
                if GPIO.input(cls.gpio_degrau2) == GPIO.HIGH and (2 in ordem_degrau) == False:
                    ordem_degrau.append(2)

                if GPIO.input(cls.gpio_degrau3) == GPIO.HIGH and (3 in ordem_degrau) == False:
                    ordem_degrau.append(3)

                if GPIO.input(cls.gpio_degrau4) == GPIO.HIGH and (4 in ordem_degrau) == False:
                    ordem_degrau.append(4)

                # Checa se todos os degrais já foram pisados e checa se foi na ordem correta.
                if len(ordem_degrau) == 4 and ordem_degrau == ORDEM_CORRETA :
                    cls.abrirAlcapao()
                elif len(ordem_degrau) == 4 and ordem_degrau != ORDEM_CORRETA :
                    ordem_degrau = []

            time.sleep(1)
        
        else:
            print('Logica 3 - Finalizada')

# ------ FIM DA LOGICA 3 ---------