import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from .logica_geral import Logica_geral
from escapebhjogo.classes.logica_2 import Logica_2 # Classe com metodos da logica 2
from escapebhjogo.classes.reles import Reles

""" CLASSE LOGICA 1
Esta classe faz todo o controle dos itens relacionados a Logica 1

Vermelho -> Dentro do móvel do mezanino terá um botão. Apertando-o vai liberar um laser.
Direcionando o laser da forma correta para a gaveta na parte de baixo do palco vai abri-la.
"""
class Logica_1(Logica_geral):

    # GPA's e GPB's
    gpio_botao = 32 # Botao mezanino (raspberry)
    gpio_ldr = 33 # Sensor ldr (raspberry)
    gp_laser = 1 # Rele Laser - GPA 1 (Extensor 0x24)
    gp_gaveta = 2 # Rele Gaveta - GPA 2 (Extensor 0x24)

    # Variaveis
    laser_on = False

    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls):
        GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
        GPIO.setwarnings(False) # Desativa avisos
        
        # Configurado GPIO's do raspberry
        GPIO.setup(cls.gpio_botao, GPIO.IN)
        GPIO.setup(cls.gpio_ldr, GPIO.IN)
        
        # Desativar todos os reles
        Reles.desligarTodosReles()

        # Configurando Reles, GP's do Extensor 0x24 
        mcp.setup(cls.gp_laser, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.setup(cls.gp_gaveta, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        
        # Inicialmente em nivel alto (Desligado)
        mcp.output(cls.gp_laser, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
        mcp.output(cls.gp_gaveta, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
    
    # Metodo para abrir gaveta
    @classmethod
    def abrirGaveta(cls):
        cls._concluida = True
        mcp.output(cls.gp_laser, mcp.GPA, mcp.HIGH, mcp.ADDRESS2) # Desativa rele laser
        cls.laser_on = False
        mcp.setup(cls.gp_gaveta, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        # Ativa a trava com 3 pulsos de 2s cada
        for i in range(3):
            mcp.output(cls.gp_gaveta, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
            time.sleep(2)
            mcp.output(cls.gp_gaveta, mcp.GPA, mcp.HIGH, mcp.ADDRESS2) # Desativa rele gaveta
            time.sleep(2)

    # Metodo para acionar o lasers
    @classmethod
    def ligarLaser(cls):
        mcp.setup(cls.gp_laser, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_laser, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
        cls.laser_on = True

    # Sobreescrevendo metodo threadLogicas() da classe pai
    @classmethod
    def threadLogica(cls):
        
        while cls._concluida == False:
            if Logica_2._concluida == True:
                # Se o botao for pressionado ativa o Laser
                leitura_botao = GPIO.input(cls.gpio_botao)

                if leitura_botao == 1 and cls.laser_on == False:
                    cls.ligarLaser()
                    print('O laser foi acionado') #DEBUG

                # Se o ldr detectar a luz do laser abre a gaveta
                leitura_ldr = GPIO.input(cls.gpio_ldr)

                if leitura_ldr == 1 and cls.laser_on == True:
                    cls.abrirGaveta() # Abre a gaveta e marca a logica como concluida
                    print('A gaveta do chão foi aberta') #DEBUG
                    
                time.sleep(0.25) # Delay de 250ms segundo entre checagens
                print('2ª Logica Rodando (Laser)') #DEBUG
            
        else:
            print('2ª Logica - Finalizada')


# ------ FIM DA LOGICA 1 ---------