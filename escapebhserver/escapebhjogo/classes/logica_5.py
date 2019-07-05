import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from .logica_geral import Logica_geral
from escapebhjogo.classes.logica_4 import Logica_4 # Classe com metodos da logica 4

""" CLASSE LOGICA 5
Esta classe faz todo o controle dos itens relacionados a Logica 4

Azul -> Colocando os livros na ordem correta vai fazer com que o baú abra.
"""

class Logica_5(Logica_geral):

    # GPIO's
    gpio_livro1 = 0 # Primeiro livro (raspberry)
    gpio_livro2 = 0 # Segundo livro (raspberry)
    gpio_livro3 = 0 # Terceiro livro (raspberry)
    gp_bau = 0 # Rele da trava do bau (extensor)

    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls):
        GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
        GPIO.setwarnings(False) # Desativa avisos
        
        # Configurado GPIO's do raspberry
        GPIO.setup(cls.gpio_livro1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_livro2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_livro3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

        # Configurando GPIO's do Extensor
        mcp.setup(cls.gp_bau, mcp.GPA, mcp.OUT, mcp.ADDRESS2)

        # Inicialmente em nivel baixo
        mcp.output(cls.gp_bau, mcp.GPA, mcp.LOW, mcp.ADDRESS2)

    # Metodo para destravar o bau
    @classmethod
    def abrirBau(cls):
        cls.concluida = True
        mcp.setup(cls.gp_bau, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_bau, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
        time.sleep(30)
        mcp.output(cls.gp_bau, mcp.GPA, mcp.LOW, mcp.ADDRESS2)

    # Sobreescrevendo metodo threadLogicas() da classe pai
    @classmethod
    def threadLogica(cls):
        while cls.concluida == False:
            # Checa se a logica 4 já foi concluida
            if Logica_4._concluida == True:

                if (GPIO.input(cls.gpio_livro1) == GPIO.HIGH and
                    GPIO.input(cls.gpio_livro2) == GPIO.HIGH and
                    GPIO.input(cls.gpio_livro3) == GPIO.HIGH ):
                    
                    cls.abrirBau()

            time.sleep(1)
        
        else:
            print('Logica 4 - Finalizada')

# ------ FIM DA LOGICA 4 ---------