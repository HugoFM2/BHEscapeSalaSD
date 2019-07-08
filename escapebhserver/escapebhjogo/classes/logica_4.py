import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from escapebhjogo.classes.logica_3 import Logica_3 # Classe com metodos da logica 2
from .logica_geral import Logica_geral

""" CLASSE LOGICA 4
Esta classe faz todo o controle dos itens relacionados a Logica 4

Laranja -> Virando as duas chaves no móvel que fica no mezanino vai fazer com que o busto
abra. Dentro do busto vai ter um botão. Apertando o botão no busto vai fazer com que a porta
secreta abra.
"""
class Logica_4(Logica_geral):
    
    # GPIO's
    gpio_chave1 = 0 # Primeira chave (raspberry)
    gpio_chave2 = 0 # Segunda chave (raspberry)
    gpio_botao = 0 # Botao no busto (raspberry)
    gpio_servo = 0 # Servo motor do busto
    gp_porta = 0 # Rele da trava do alçapão (extensor)

    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls):
        GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
        GPIO.setwarnings(False) # Desativa avisos
        
        # Configurado GPIO's do raspberry
        GPIO.setup(cls.gpio_chave1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_chave2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        # GPIO SERVO ?

        # Configurando GPIO's do Extensor
        mcp.setup(cls.gp_porta, mcp.GPA, mcp.OUT, mcp.ADDRESS2)

        # Inicialmente em nivel baixo
        mcp.output(cls.gp_porta, mcp.GPA, mcp.LOW, mcp.ADDRESS2)

    # Metodo para destravar alcapao no chao
    @classmethod
    def abrirPorta(cls):
        cls._concluida = True
        mcp.setup(cls.gp_porta, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_porta, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
        time.sleep(30)
        mcp.output(cls.gp_porta, mcp.GPA, mcp.LOW, mcp.ADDRESS2)

    @classmethod
    def abrirBusto(cls):
        # Implementar
        pass

    # Sobreescrevendo metodo threadLogicas() da classe pai
    @classmethod
    def threadLogica(cls):
        while cls._concluida == False:
            # Checa se a logica 3 já foi concluida
            if Logica_3._concluida == True:

                if (GPIO.input(cls.gpio_chave1) == GPIO.HIGH and GPIO.input(cls.gpio_chave2) == GPIO.HIGH) :
                    cls.abrirBusto()

                if GPIO.input(cls.gpio_botao) == GPIO.HIGH :
                    cls.abrirPorta()

            time.sleep(1)
        
        else:
            print('Logica 4 - Finalizada')

# ------ FIM DA LOGICA 4 ---------