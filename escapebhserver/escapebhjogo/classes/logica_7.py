import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from .logica_geral import Logica_geral
from escapebhjogo.classes.logica_6 import Logica_6 # Classe com metodos da logica 6
from escapebhjogo.classes.logica_5 import Logica_5 # Classe com metodos da logica 5

""" CLASSE LOGICA 7
Esta classe faz todo o controle dos itens relacionados a Logica 7

Azul claro -> Colocando as quatro peças de madeira na ordem correta (similar ao puzzle de
letras) vai fazer com que uma gaveta na própria mesa abra.
"""

class Logica_7(Logica_geral):

    # GPIO's
    gpio_peca1 = 5 # Primeira peça - GPA 5(extensor 0x22)
    gpio_peca2 = 7 # Segunda peça - GPA 7 (extensor 0x22)
    gpio_peca3 = 6 # Terceira peça - GPA 6 (extensor 0x22)
    gpio_peca4 = 4 # Quarta peça - GPA 4 (extensor 0x22)
    gp_trava = 6 # Rele da trava da gaveta - GPA 6 (extensor 0x24)

    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls):
        # Configurado GPIO's do extensor 0x22
        mcp.setup(cls.gpio_peca1, mcp.GPA, mcp.IN, mcp.ADDRESS1)
        mcp.setup(cls.gpio_peca2, mcp.GPA, mcp.IN, mcp.ADDRESS1)
        mcp.setup(cls.gpio_peca3, mcp.GPA, mcp.IN, mcp.ADDRESS1)
        mcp.setup(cls.gpio_peca4, mcp.GPA, mcp.IN, mcp.ADDRESS1)

        # Configurando GPIO's do Extensor 0x24
        mcp.setup(cls.gp_trava, mcp.GPA, mcp.OUT, mcp.ADDRESS2)

        # Inicialmente em nivel alto, Desligado
        mcp.output(cls.gp_trava, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)

    # Metodo para destravar o bau
    @classmethod
    def abrirGaveta(cls):
        cls._concluida = True
        mcp.setup(cls.gp_trava, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_trava, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
        time.sleep(0.25)
        mcp.output(cls.gp_trava, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)

    # Sobreescrevendo metodo threadLogicas() da classe pai
    @classmethod
    def threadLogica(cls):
        while cls._concluida == False:
            # Checa se a logica 6 já foi concluida
            if Logica_6._concluida == True and Logica_5._concluida == True:

                leitura = [None, None, None, None]
                leitura[0] = mcp.input(cls.gpio_peca1, mcp.GPA, mcp.ADDRESS1)
                leitura[1] = mcp.input(cls.gpio_peca2, mcp.GPA, mcp.ADDRESS1)
                leitura[2] = mcp.input(cls.gpio_peca3, mcp.GPA, mcp.ADDRESS1)
                leitura[3] = mcp.input(cls.gpio_peca4, mcp.GPA, mcp.ADDRESS1)

                if (leitura == [1,1,1,1]):
                    
                    cls.abrirGaveta()
                    print('Logica 7 - Gaveta Aberta')
                
                print('Logica 7 - Rodando')
                print(leitura)
                
            time.sleep(0.25)
        
        else:
            print('Logica 7 - Finalizada')

# ------ FIM DA LOGICA 7 ---------