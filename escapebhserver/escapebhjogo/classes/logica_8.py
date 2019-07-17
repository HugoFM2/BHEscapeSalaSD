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
*Errata: Ao colocar as duas partes da arma na caixa do lado parede (cada parte possui uma tag rfid),
o rfid lerá se as armas estao na ordem certa e assim irá destravar a parte de baixo da caixa que contera
a lampada de acampamento. Esta lampada ao ser colocada no outro lado da sala sobre um encaixe com
sensor magnetico abrira um tubo pneumatico que contera uma chave para a caixa que contem o brassao.
"""

class Logica_8(Logica_geral):

    # GPIO's
    gpio_lampada = 5 # Sensor da mesa que detecta o encaixe da lampada - GPB 5 (extensor 0x22)
    gp_travaCaixa = 7 # Rele da trava da caixa - GPB 7 (extensor 0x24)
    gp_travaTubo = 6 # Rele da trava do tubo - GPB 6 (extensor 0x24)

    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls):
        # Configurando GPIO's do Extensor 0x22
        mcp.setup(cls.gpio_lampada, mcp.GPB, mcp.IN, mcp.ADDRESS1)

        # Configurando GPIO's do Extensor 0x24
        mcp.setup(cls.gp_travaCaixa, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
        mcp.setup(cls.gp_travaTubo, mcp.GPB, mcp.OUT, mcp.ADDRESS2)

        # Inicialmente em nivel alto (Rele desativado)
        mcp.output(cls.gp_travaCaixa, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)
        mcp.output(cls.gp_travaTubo, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

    # Metodo abrir a caixa que contem a lampada
    @classmethod
    def abrirCaixa(cls):
        mcp.setup(cls.gp_travaCaixa, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_travaCaixa, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
        time.sleep(0.25)
        mcp.output(cls.gp_travaCaixa, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

    # Metodo abrir o tubo que contem o brasão
    @classmethod
    def abrirTuboBrasao(cls):
        cls._concluida = True
        mcp.setup(cls.gp_travaTubo, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_travaTubo, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
        time.sleep(0.25)
        mcp.output(cls.gp_travaTubo, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

    # Sobreescrevendo metodo threadLogicas() da classe pai
    @classmethod
    def threadLogica(cls):
        while cls._concluida == False:
            # Checa se a logica 7 já foi concluida
            if Logica_7._concluida == True:

                leitura = mcp.input(cls.gpio_lampada, mcp.GPB, mcp.ADDRESS1)
                if (leitura == 1):

                    cls.abrirTuboBrasao()
                    print('Logica 8 - Tubo Aberto')

                print('Logica 8 - Rodando, Lampada: ' + str(leitura))

            time.sleep(0.25)
        
        else:
            print('Logica 8 - Finalizada')

# ------ FIM DA LOGICA 8 ---------