import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from .logica_geral import Logica_geral

""" CLASSE LOGICA 1
Esta classe faz todo o controle dos itens relacionados a Logica 1

Vermelho -> Dentro do móvel do mezanino terá um botão. Apertando-o vai liberar um laser.
Direcionando o laser da forma correta para a gaveta na parte de baixo do palco vai abri-la.
"""
class Logica_1(Logica_geral):

    # GPIO's
    gpio_botao = 0 # Botao mezanino (Raspberry)
    gpio_ldr = 0 # Sensor ldr (Raspberry)
    gp_laser = 0 # Rele Laser (Extensor 0x)s
    gp_gaveta = 0 # Rele Gaveta (Extensor)

    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls): 
        GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
        GPIO.setwarnings(False) # Desativa avisos

        # Configurado GPIO's do raspberry
        GPIO.setup(cls.gpio_botao, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_ldr, GPIO.IN)

        # Configurando GPIO's do Extensor
        mcp.setup(cls.gp_laser, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.setup(cls.gp_gaveta, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        
        # Inicialmente em nivel baixo
        mcp.output(cls.gp_laser, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
        mcp.output(cls.gp_gaveta, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
    
    # Metodo para abrir gaveta
    @classmethod
    def abrirGaveta(cls):
        cls.concluida = True
        mcp.setup(cls.gp_gaveta, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_gaveta, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
        time.sleep(30)
        mcp.output(cls.gp_gaveta, mcp.GPA, mcp.LOW, mcp.ADDRESS2)

    # Metodo para acionar o lasers
    @classmethod
    def ligarLaser(cls):
        mcp.setup(cls.gp_laser, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_laser, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)

    # Sobreescrevendo metodo threadLogicas() da classe pai
    @classmethod
    def threadLogica(cls):
        while cls.concluida == False:
            # Se o botao for pressionado ativa o Laser
            if GPIO.input(cls.gpio_botao) == GPIO.HIGH :
                cls.ligarLaser()

            # Se o ldr detectar a luz do laser abre a gaveta
            if GPIO.input(cls.gpio_ldr) == GPIO.HIGH:
                cls.abrirGaveta() # Abre a gaveta e marca a logica como concluidas
                
            time.sleep(1) # Delay de 1 segundo entre checagens
            
        else:
            print('Logica 1 - Finalizada')


# ------ FIM DA LOGICA 1 ---------