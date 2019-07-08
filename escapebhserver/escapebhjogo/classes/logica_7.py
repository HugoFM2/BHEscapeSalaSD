import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from .logica_geral import Logica_geral
from escapebhjogo.classes.logica_6 import Logica_6 # Classe com metodos da logica 6

""" CLASSE LOGICA 7
Esta classe faz todo o controle dos itens relacionados a Logica 7

Azul claro -> Colocando as quatro peças de madeira na ordem correta (similar ao puzzle de
letras) vai fazer com que uma gaveta na própria mesa abra.
"""

class Logica_7(Logica_geral):

    # GPIO's
    gpio_peca1 = 0 # Primeira peça (raspberry)
    gpio_peca2 = 0 # Segunda peça (raspberry)
    gpio_peca3 = 0 # Terceira peça (raspberry)
    gpio_peca4 = 0 # Quarta peça (raspberry)
    gp_trava = 0 # Rele da trava da gaveta (extensor)

    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls):
        GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
        GPIO.setwarnings(False) # Desativa avisos
        
        # Configurado GPIO's do raspberry
        GPIO.setup(cls.gpio_peca1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_peca2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_peca3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_peca4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

        # Configurando GPIO's do Extensor
        mcp.setup(cls.gp_trava, mcp.GPA, mcp.OUT, mcp.ADDRESS2)

        # Inicialmente em nivel baixo
        mcp.output(cls.gp_trava, mcp.GPA, mcp.LOW, mcp.ADDRESS2)

    # Metodo para destravar o bau
    @classmethod
    def abrirGaveta(cls):
        cls._concluida = True
        mcp.setup(cls.gp_trava, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_trava, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
        time.sleep(30)
        mcp.output(cls.gp_trava, mcp.GPA, mcp.LOW, mcp.ADDRESS2)

    # Sobreescrevendo metodo threadLogicas() da classe pai
    @classmethod
    def threadLogica(cls):
        while cls._concluida == False:
            # Checa se a logica 4 já foi concluida
            if Logica_6._concluida == True:

                if (GPIO.input(cls.gpio_peca1) == GPIO.HIGH and
                    GPIO.input(cls.gpio_peca2) == GPIO.HIGH and
                    GPIO.input(cls.gpio_peca3) == GPIO.HIGH and
                    GPIO.input(cls.gpio_peca4) == GPIO.HIGH ):
                    
                    cls.abrirGaveta()

            time.sleep(1)
        
        else:
            print('Logica 7 - Finalizada')

# ------ FIM DA LOGICA 7 ---------