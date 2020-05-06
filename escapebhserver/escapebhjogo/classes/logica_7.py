import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from .logica_geral import Logica_geral
from escapebhjogo.classes.logica_5 import Logica_5 # Classe com metodos da logica 5

""" CLASSE LOGICA 7
Esta classe faz todo o controle dos itens relacionados a Logica 7

Azul claro -> Colocando as quatro peças de madeira na ordem correta (similar ao puzzle de
letras) vai fazer com que uma gaveta na própria mesa abra.
"""

class Logica_7(Logica_geral): # Logica 7 no site

    # GPIO's
    gpio_peca2 = 21 # Segunda peça (raspberry)
    gpio_peca3 = 19 # Terceira peça (raspberry)
    gpio_peca4 = 15 # Quarta peça (raspberry)
    gp_trava = 6 # Rele da trava da gaveta - GPA 6 (extensor 0x24)
    executarSomLogica7 = False
    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls):
        GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
        GPIO.setwarnings(False) # Desativa avisos

        # Configurado GPIO's do raspberry
        GPIO.setup(cls.gpio_peca2, GPIO.IN)
        GPIO.setup(cls.gpio_peca3, GPIO.IN)
        GPIO.setup(cls.gpio_peca4, GPIO.IN)

        # Configurando GPIO's do Extensor 0x24
        mcp.setup(cls.gp_trava, mcp.GPA, mcp.OUT, mcp.ADDRESS2)

        # Inicialmente em nivel alto, Desligado
        mcp.output(cls.gp_trava, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)

    # Metodo para destravar o bau
    @classmethod
    def abrirGaveta(cls):
        cls._concluida = True
        cls.executarSomLogica7 = True
        # Ativa a trava com 3 pulsos de 2s cada
        for i in range(3):
            mcp.setup(cls.gp_trava, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
            mcp.output(cls.gp_trava, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
            time.sleep(0.050)
            mcp.output(cls.gp_trava, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
            time.sleep(2)
        cls.executarSomLogica7 = False

    # Sobreescrevendo metodo threadLogicas() da classe pai
    @classmethod
    def threadLogica(cls):
        while cls._concluida == False:
            # Checa se a logica 6 já foi concluida
            if Logica_5._concluida == True:

                leitura = [None, None, None, None]
                #leitura[0] = primeiro sensor desativado
                leitura[0] = 1 # Ignorando o primeiro sensor
                leitura[1] = GPIO.input(cls.gpio_peca2)
                leitura[2] = GPIO.input(cls.gpio_peca3)
                leitura[3] = GPIO.input(cls.gpio_peca4)

                if (leitura == [1,1,1,1]):

                    cls.abrirGaveta()
                    print('Gaveta 2ª Sala Aberta!')

                print('7ª Logica - Rodando (Puzzle 2ª Sala)')
                print(leitura)

            time.sleep(0.25)

        else:
            print('7ª Logica - Finalizada')

# ------ FIM DA LOGICA 7 ---------
