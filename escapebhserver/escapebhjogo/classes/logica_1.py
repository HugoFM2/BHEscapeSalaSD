import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp

""" CLASSE LOGICA 1
Esta classe faz todo o controle dos itens relacionados a Logica 1
"""
class Logica_1(object):
    # ATRIBUTOS DA CLASSE
    concluida = False # Atributo que guarda se a logica foi concluida
    leituraSensores = [] # Atributo que armazena leitura dos sensores
    tempo_inicial = None # Marca o tempo de inicio da Logica
    duracao_total = None # Guarda o tempo total da logica
    t = None # Variavel que ira armazenar a Thread da classe

    @classmethod
    def setup(cls):
        # Esta Logica nao usa GPIOS do raspberry, somente extensor
        # GPB2 e GPB3 do 0x22 - (invencao 2 e Invencao 1)
        # ADDRESS1 e o 0x22 (ADDRESS1)
        # CONFIGURAS SENSORES COMO INPUT
        mcp.setup(2, mcp.GPB, mcp.IN, mcp.ADDRESS1)
        mcp.setup(3, mcp.GPB, mcp.IN, mcp.ADDRESS1) 

        # GPA3 do 0x24 (ADDRESS2) - Abre a maleta
        # GAVETA COMO OUT e inicialmente em nivel baixo
        #mcp.setup(3, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
        #mcp.output(3, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
    
    @classmethod
    def getLeituraSensores(cls):
        return cls.leituraSensores

    @classmethod
    def getDuracaoLogica(cls):
        duracao = 0
        if not cls.tempo_inicial == None:
            duracao = time.time() - cls.tempo_inicial
        return duracao

    @classmethod
    def forcarAbrirTrava(cls):
        #mcp.output(3, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
        #time.sleep(4)
        #mcp.output(3, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
        pass

    @classmethod
    def iniciarThread(cls):
        cls.setup() # Executa on metodo setup
        time.sleep(1) # Delay de 1 segundo
        # Se o atributo t é Vazio cria uma tread
        if cls.t == None:
            cls.t = threading.Thread(target=cls.threadLogica)
        # Verifica se a tread não esta em execucao e se ainda nao foi concluida
        if cls.t.isAlive() == False and cls.concluida == False:
            cls.leituraSensores = [] # Limpa a variavel de leituras
            cls.duracao_total = None # Limpa a varivel de contagem
            cls.tempo_inicial = time.time() # Defini o tempo incial da logica
            cls.t.start()
        else:
            print('Logica 1 ja concluida, é necessario reicia-la para executar novamente.')

    @classmethod
    def reiniciarThread(cls):
        cls.concluida = False
        cls.t = threading.Thread(target=cls.threadLogica) # NOVA THREAD
        cls.iniciarThread()

    @classmethod
    def thread_isAlive(cls):
        status = None
        if not cls.t == None: # Se o atributo t é diferente de Vazio
            status = cls.t.isAlive()
        return status

    @classmethod
    def threadLogica(cls):
        while cls.concluida == False:
            leituraSensor = []
            leituraSensor.append( mcp.input(2, mcp.GPB, mcp.ADDRESS1) )
            leituraSensor.append( mcp.input(3, mcp.GPB, mcp.ADDRESS1) )
            cls.leituraSensores = leituraSensor
            print(cls.leituraSensores)

            # Checa se as condicoes dos sensores magneticos foi satisfeita
            if leituraSensor == [1,1]:
                # chama o metodo para abrir a gaveta
                cls.forcarAbrirTrava()
                cls.concluida = True
                cls.duracao_total = time.time() - cls.tempo_inicial
                print('Logica 1 - Finalizada - Tempo: ' + str(cls.duracao_total) + 'segundos')
            
            time.sleep(1)

# ------ FIM DA LOGICA 1 ---------