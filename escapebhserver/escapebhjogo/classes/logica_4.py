import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from escapebhjogo.classes.logica_1 import Logica_1 # Classe com metodos da logica 1
from .logica_geral import Logica_geral
from escapebhjogo.classes.reles import Reles

""" CLASSE LOGICA 4
Esta classe faz todo o controle dos itens relacionados a Logica 4

Laranja -> Virando as duas chaves no móvel que fica no mezanino vai fazer com que o busto
abra. Dentro do busto vai ter um botão. Apertando o botão no busto vai fazer com que a porta
secreta abra.
"""
class Logica_4(Logica_geral):
    
    # GPIO's
    gpio_chave1 = 26 # Primeira chave (Esquerda) (raspberry)
    gpio_chave2 = 22 # Segunda chave (Direita) (raspberry)
    gp_botao = 0 # Botao no busto - GPA 0 (Extensor 0x22)
    gpio_servo = 8 # Servo motor do busto (raspberry)
    gp_trava_busto = 7 # Trava do busto - GPA 7 (Extensor 0x24)
    gp_porta = 0 # Rele da trava da porta - GPA 0(extensor 0x24)

    # Variaveis
    busto_girou = False
    pwmServo = None

    # Sobreescrevendo metodo setup() da classe pai
    @classmethod
    def setup(cls):
        GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
        GPIO.setwarnings(False) # Desativa avisos
        
        # Configurado GPIO's do raspberry
        GPIO.setup(cls.gpio_chave1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_chave2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.gpio_servo, GPIO.OUT)

        # Desativar todos os reles
        Reles.desligarTodosReles()

        # Configurando GPIO's do Extensor
        mcp.setup(cls.gp_botao, mcp.GPA, mcp.IN, mcp.ADDRESS1)
        mcp.setup(cls.gp_porta, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.setup(cls.gp_trava_busto, mcp.GPA, mcp.OUT, mcp.ADDRESS2)

        # Inicialmente em nivel baixo
        GPIO.output(cls.gpio_servo, GPIO.LOW)
        # Rele em nivel alto (Para iniciar desativado)
        mcp.output(cls.gp_porta, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
        mcp.output(cls.gp_trava_busto, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)

        cls.busto_girou = False

    # Metodo para destravar alcapao no chao
    @classmethod
    def abrirPorta(cls):
        cls._concluida = True
        mcp.setup(cls.gp_porta, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_porta, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
        time.sleep(0.25)
        mcp.output(cls.gp_porta, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
        cls.busto_girou = False

    @classmethod
    def abrirBusto(cls):
        mcp.setup(cls.gp_trava_busto, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        mcp.output(cls.gp_trava_busto, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
        time.sleep(0.25)
        mcp.output(cls.gp_trava_busto, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
        time.sleep(0.5)

        cls.setup()
        #Servo MG90: Pulse Cycle -> 20ms (50Hz), Pulse Width: 0.4ms a 2.4ms (2% a 12%)
        if cls.pwmServo == None:
            cls.pwmServo = GPIO.PWM(cls.gpio_servo, 50) # GPIO inicia PWM de 50HZ, periodo 20ms, no pino do servo
            cls.pwmServo.start(0) # Inicio com DutyCycle em 0%
            time.sleep(0.5)

        cls.pwmServo.ChangeDutyCycle(2.5) # Aberto
        time.sleep(1.5)
        
        cls.pwmServo.ChangeDutyCycle(0) # Caso o servo fique tremendo
        #cls.pwmServo.stop()

    @classmethod
    def voltarBusto(cls):
        cls.setup()

        if cls.pwmServo == None:
            cls.pwmServo = GPIO.PWM(cls.gpio_servo, 50) # GPIO inicia PWM de 50HZ, periodo 20ms, no pino do servo
            cls.pwmServo.start(0) # Inicio com DutyCycle em 0%
            time.sleep(0.5)
        
        cls.pwmServo.ChangeDutyCycle(11.4) # Fechado
        time.sleep(1.5)
        cls.pwmServo.ChangeDutyCycle(0) # Caso o servo fique tremendo
        #cls.pwmServo.stop()
        cls.busto_girou = False

    # Sobreescrevendo metodo threadLogicas() da classe pai
    @classmethod
    def threadLogica(cls):
        while cls._concluida == False:
            # Checa se a logica 3 já foi concluida
            if Logica_1._concluida == True:
                
                #leitura = [GPIO.input(cls.gpio_chave1), GPIO.input(cls.gpio_chave2)]

                if GPIO.input(cls.gpio_chave1) == GPIO.HIGH and GPIO.input(cls.gpio_chave2) == GPIO.HIGH and cls.busto_girou == False :
                    cls.abrirBusto()
                    cls.busto_girou = True
                    print('Girando Busto e liberando botão.') #DEBUG

                leituraBotao = mcp.input(cls.gp_botao, mcp.GPA, mcp.ADDRESS1)
                if leituraBotao == 1 :
                    cls.abrirPorta()
                    print('Abrindo a Porta secreta') #DEBUG

                time.sleep(0.25)
                #print(leitura)
                print('3ª Logica - Rodando (Busto/Porta)') #DEBUG
        
        else:
            print('3ª Logica - Finalizada')

# ------ FIM DA LOGICA 4 ---------