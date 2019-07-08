import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from .logica_geral import Logica_geral
from escapebhjogo.classes.logica_7 import Logica_7 # Classe com metodos da logica 7

""" CLASSE LOGICA 8
Esta classe faz todo o controle dos itens relacionados a Logica 8

Roxo -> Colocando a invenção dentro do tubo pneumático, fechando e apertando o botão vai
fazer com que a porta deste tubo tranque, as luzes pisquem e o barulho de sucção. Ao mesmo
tempo vai soltar a trava de um dos outros tubos pneumáticos, que vai ter o brasão dentro.
"""

class Logica_8(Logica_geral):

    # GPIO's
    gpio_invencao = 0 # Sensor do tubo que detecta a Invencao (raspberry)
    gpio_botao = 0 # Botao do tubo
    #gp_luzes = 0 # Rele das luzes da sala
    gp_trava = 0 # Rele da trava da gaveta (extensor)

    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls):
        GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
        GPIO.setwarnings(False) # Desativa avisos
        
        # Configurado GPIO's do raspberry
        GPIO.setup(cls.gpio_invencao, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_botao, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

        # Configurando GPIO's do Extensor
        mcp.setup(cls.gp_trava, mcp.GPA, mcp.OUT, mcp.ADDRESS2)

        # Inicialmente em nivel baixo
        mcp.output(cls.gp_trava, mcp.GPA, mcp.LOW, mcp.ADDRESS2)

    # Metodo abrir o tubo que contem o brasão
    @classmethod
    def abrirTuboBrasao(cls):
        cls._concluida = True
        mcp.setup(cls.gp_trava, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_trava, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
        # --> Barulho de sucção <--
        time.sleep(30)
        mcp.output(cls.gp_trava, mcp.GPA, mcp.LOW, mcp.ADDRESS2)

    # Sobreescrevendo metodo threadLogicas() da classe pai
    @classmethod
    def threadLogica(cls):
        while cls._concluida == False:
            # Checa se a logica 7 já foi concluida
            if Logica_7._concluida == True:

                if (GPIO.input(cls.gpio_invencao) == GPIO.HIGH and GPIO.input(cls.gpio_botao) == GPIO.HIGH):

                    cls.abrirTuboBrasao()

            time.sleep(1)
        
        else:
            print('Logica 8 - Finalizada')

# ------ FIM DA LOGICA 8 ---------