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
    gpio_lampada = 31 # Sensor da mesa que detecta o encaixe da lampada (raspberry)
    gpio_arma = 36 # Sensor que detecta o encaixe da arma (raspberry)
    gpio_ldr = 23 # Ldr da lampada (raspberry)
    gp_travaCaixa = 7 # Rele da trava da caixa - GPB 7 (extensor 0x24)
    gp_travaTubo = 6 # Rele da trava do tubo - GPB 6 (extensor 0x24)
    gp_fitaLed = 4 # Rele da fita de led - GPA 4 (extensor 0x24)
    gp_lampada127v = 3 # Rele da fita de led - GPB 3 (extensor 0x24)
    executarSom1 = False # Variavel que sera usada para sicronizar o som 1
    executarSom2 = False # Variavel que sera usada para sicronizar o som 2

    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls):
        GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
        GPIO.setwarnings(False) # Desativa avisos

        # Configurado GPIO's do raspberry
        GPIO.setup(cls.gpio_lampada, GPIO.IN)
        GPIO.setup(cls.gpio_arma, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_ldr, GPIO.IN)

        # Configurando GPIO's do Extensor 0x24
        mcp.setup(cls.gp_travaCaixa, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
        mcp.setup(cls.gp_travaTubo, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
        mcp.setup(cls.gp_fitaLed, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.setup(cls.gp_lampada127v, mcp.GPB, mcp.OUT, mcp.ADDRESS2)

        # Inicialmente em nivel alto (Rele desativado)
        mcp.output(cls.gp_travaCaixa, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)
        mcp.output(cls.gp_travaTubo, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)
        mcp.output(cls.gp_fitaLed, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
        mcp.output(cls.gp_lampada127v, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

    # Metodo abrir a caixa que contem a lampada
    @classmethod
    def abrirCaixa(cls):
        cls.executarSom1 = True # Sinal para executar o som

        mcp.setup(cls.gp_fitaLed, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        for i in range(5):
            mcp.output(cls.gp_fitaLed, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
            time.sleep(0.15)
            mcp.output(cls.gp_fitaLed, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
            time.sleep(0.15)
        mcp.output(cls.gp_fitaLed, mcp.GPA, mcp.LOW, mcp.ADDRESS2)

        mcp.setup(cls.gp_travaCaixa, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_travaCaixa, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
        time.sleep(0.25)
        mcp.output(cls.gp_travaCaixa, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

        cls.executarSom1 = False # Sinal para parar o som

    # Metodo abrir o tubo que contem o brasão
    @classmethod
    def abrirTuboBrasao(cls):
        cls._concluida = True

        cls.executarSom2 = True # Sinal para executar o som

        time.sleep(14) # Da um delay de 13 segundos para piscar a lampada e abrir o tubo

        # Pisca lampada 127v
        mcp.setup(cls.gp_lampada127v, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
        for i in range(5):
            mcp.output(cls.gp_lampada127v, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
            time.sleep(0.15)
            mcp.output(cls.gp_lampada127v, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)
            time.sleep(0.15)
        mcp.output(cls.gp_lampada127v, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

        # Abre o tubo
        mcp.setup(cls.gp_travaTubo, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_travaTubo, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
        time.sleep(0.25)
        mcp.output(cls.gp_travaTubo, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

        cls.executarSom2 = False # Sinal para parar o som
        # Desliga a fita de LED ao concluir a logica do tubo
        mcp.setup(cls.gp_fitaLed, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_fitaLed, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)

    # Sobreescrevendo metodo threadLogicas() da classe pai
    @classmethod
    def threadLogica(cls):
        caixaAberta = False
        while cls._concluida == False:
            # Checa se a logica 7 já foi concluida
            if Logica_7._concluida == True:

                if (GPIO.input(cls.gpio_arma) == 1 and caixaAberta == False):
                    cls.abrirCaixa()
                    caixaAberta = True
                    print('Caixa Aberta!')

                leitura = GPIO.input(cls.gpio_lampada)
                leituraLdr = GPIO.input(cls.gpio_ldr)
                # if (leitura == 1 and leituraLdr == 1 and caixaAberta == True):
                if (leitura == 1 and caixaAberta == True):
                    cls.abrirTuboBrasao()
                    print('Tubo de energia Aberto')

                print('8ª Logica - Rodando (Arma/Lampada Energia) Lampada: ' + str(leitura))

            time.sleep(0.25)

        else:
            print('8ª Logica - Finalizada')

# ------ FIM DA LOGICA 8 ---------
