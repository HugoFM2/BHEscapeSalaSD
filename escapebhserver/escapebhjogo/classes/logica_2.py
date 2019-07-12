import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from escapebhjogo.classes.logica_1 import Logica_1 # Classe com metodos da logica 1
from .logica_geral import Logica_geral
from escapebhjogo.classes.reles import Reles

""" CLASSE LOGICA 2
Esta classe faz todo o controle dos itens relacionados a Logica 2

Verde -> Colocando as alavancas na sequência certa vai fazer o teto cair.
"""
class Logica_2(Logica_geral):
    
    # GPIO's
    gpio_chave1 = 35 # Primeira chave (raspberry)
    gpio_chave2 = 37 # Segunda chave (raspberry)
    gpio_chave3 = 40 # Terceira chave (raspberry)
    gpio_chave4 = 38 # Quarta chave (raspberry)
    gp_trava = 4 # Rele da trava do teto - GPB 4 (extensor 0x24)

    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls):
        GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
        GPIO.setwarnings(False) # Desativa avisos
        
        # Configurado GPIO's do raspberry
        GPIO.setup(cls.gpio_chave1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_chave2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_chave3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_chave4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

        # Desativar todos os reles
        Reles.desligarTodosReles()
        
        # Configurando GPIO's do Extensor 0x24
        mcp.setup(cls.gp_trava, mcp.GPB, mcp.OUT, mcp.ADDRESS2)

        # Inicialmente em nivel alto (Desativa o rele)
        mcp.output(cls.gp_trava, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

    # Metodo para destravar teto e fazer com que ele caia
    @classmethod
    def cairTeto(cls):
        cls._concluida = True
        mcp.setup(cls.gp_trava, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_trava, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
        time.sleep(0.5)
        mcp.output(cls.gp_trava, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

    # Sobreescrevendo metodo threadLogicas() da classe pai
    @classmethod
    def threadLogica(cls):
        while cls._concluida == False:
            if Logica_1._concluida == True:
                leituraSensor = []
                leituraSensor.append( GPIO.input(cls.gpio_chave1) )
                leituraSensor.append( GPIO.input(cls.gpio_chave2) )
                leituraSensor.append( GPIO.input(cls.gpio_chave3) )
                leituraSensor.append( GPIO.input(cls.gpio_chave4) )

                # Checa se as chaves estão na posição correta e se a logica 1 foi concluida
                if leituraSensor == [1,1,1,1]:
                    cls.cairTeto()
                    #print('Teto Aberto (Logica 2)') #DEBUG

                time.sleep(0.25)
                #print('Logica 2 Rodando')
        
        else:
            print('Logica 2 - Finalizada')

# ------ FIM DA LOGICA 2 ---------