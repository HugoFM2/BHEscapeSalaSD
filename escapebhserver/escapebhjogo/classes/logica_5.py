import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from .logica_geral import Logica_geral
from escapebhjogo.classes.logica_4 import Logica_4 # Classe com metodos da logica 4

""" CLASSE LOGICA 5
Esta classe faz todo o controle dos itens relacionados a Logica 5

Azul -> Colocando os livros na ordem correta vai fazer com que o baú abra.
"""

class Logica_5(Logica_geral): # Logica 6 no site

    # GPIO's
    gpio_livro1 = 12 # Primeiro livro (raspberry)
    gpio_livro2 = 10 # Segundo livro (raspberry)
    gpio_livro3 = 13 # Terceiro livro (raspberry)
    gp_bau = 5 # Rele da trava do bau - GPA 5 (extensor 0x24)
    executarSomLogica6 = False

    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls):
        GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
        GPIO.setwarnings(False) # Desativa avisos

        # Configurado GPIO's do raspberry
        GPIO.setup(cls.gpio_livro1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_livro2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_livro3, GPIO.IN)

        # Configurando GPIO's do Extensor
        mcp.setup(cls.gp_bau, mcp.GPA, mcp.OUT, mcp.ADDRESS2)

        # Inicialmente em nivel alto (Desligado)
        mcp.output(cls.gp_bau, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)

    # Metodo para destravar o bau
    @classmethod
    def abrirBau(cls):
        cls.executarSomLogica6 = True
        cls._concluida = True
        mcp.setup(cls.gp_bau, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_bau, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
        time.sleep(0.25)
        mcp.output(cls.gp_bau, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
        cls.executarSomLogica6 = False

    # Sobreescrevendo metodo threadLogicas() da classe pai
    @classmethod
    def threadLogica(cls):
        while cls._concluida == False:
            # Checa se a logica da porta já foi concluida
            if Logica_4._concluida == True:

                leitura = [GPIO.input(cls.gpio_livro1), GPIO.input(cls.gpio_livro2), GPIO.input(cls.gpio_livro3)]
                print(leitura)
                if ( leitura[0] == GPIO.HIGH and leitura[1] == GPIO.HIGH and leitura[2] == 1 ) :

                    cls.abrirBau()

                    print('Bau Aberto!')

                print('6ª Logica - Rodando (Livros)')

            time.sleep(0.25)

        else:
            print('6ª Logica - Finalizada')

# ------ FIM DA LOGICA 5 ---------
