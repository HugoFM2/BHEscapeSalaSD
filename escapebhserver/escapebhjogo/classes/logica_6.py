import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from .logica_geral import Logica_geral
from escapebhjogo.classes.logica_5 import Logica_5 # Classe com metodos da logica 5

""" CLASSE LOGICA 6
Esta classe faz todo o controle dos itens relacionados a Logica 6

Preto -> Colocando todas as invenções nas prateleiras vai fazer com que o motor na segunda
sala ative, liberando a chave. (Explicando melhor essa parte: Ao invés de ser apenas a chave
caindo como é o atual avião que desce, será uma peça do teto que estará presa por uma
dobradiça e o motor. Quando o motor descer essa peça do teto vai abrir como se fosse uma
pequena gaveta e a chave irá deslizar)
"""

class Logica_6(Logica_geral):

    # GPIO's
    gp_motorDescer = 2 # Rele Desce Motor - GPB 2 (extensor 0x24)
    gp_motorSubir = 5 # Rele Sobe Motor - GPB 5 (extensor 0x24)

    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls):
        # Configurando GPIO's do Extensor
        mcp.setup(cls.gp_motorDescer, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
        mcp.setup(cls.gp_motorSubir, mcp.GPB, mcp.OUT, mcp.ADDRESS2)

        # Inicialmente em nivel alto (Desativado)
        mcp.output(cls.gp_motorDescer, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)
        mcp.output(cls.gp_motorSubir, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

    # Metodo para acionar o motor no sentindo de descer a "gaveta"
    @classmethod
    def descerMotor(cls):
        cls._concluida = True
        mcp.setup(cls.gp_motorDescer, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_motorDescer, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
        time.sleep(0.5)
        mcp.output(cls.gp_motorDescer, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

    # Metodo para acionar o motor no sentindo de subir a "gaveta"
    @classmethod
    def subirMotor(cls):
        mcp.setup(cls.gp_motorSubir, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_motorSubir, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
        time.sleep(0.5)
        mcp.output(cls.gp_motorSubir, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

    # Sobreescrevendo metodo threadLogica() da classe pai
    @classmethod
    def threadLogica(cls):
        # *A Logica 6 é acionada manualmente
        while cls._concluida == False:
            # Checa se a logica 5 já foi concluida
            if Logica_5._concluida == True:
                print('Logica 6 - Rodando')

            time.sleep(1)
        
        else:
            print('Logica 6 - Finalizada')

# ------ FIM DA LOGICA 6 ---------