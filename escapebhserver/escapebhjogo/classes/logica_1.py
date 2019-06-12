import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads

""" CLASSE LOGICA 1
Esta classe faz todo o controle dos itens relacionados a Logica 1
"""
class Logica_1(object):
    # ATRIBUTOS DA CLASSE
    contador = 0 #DEBUG
    concluida = False # Atributo que guarda se a logica foi concluida
    leituraSensores = [] # Atributo que armazena leitura dos sensores
    tempo_inicial = None # Marca o tempo de inicio da Logica

    pinsensor = [3 , 5, 7] # Pinos dos sensores magneticos
    pinfechadura = 11 # Pino fechadura

    t = None # Variavel que ira armazenar a Thread da classe

    @classmethod
    def setup(cls):
        GPIO.setmode(GPIO.BOARD) # Modo BOARD (0 a 40)
        GPIO.setwarnings(False) # Desativa avisos

        # Loop para configurar os pinos dos sensores como entrada
        for i in range(0 , len(cls.pinsensor) ):
            GPIO.setup(cls.pinsensor[i], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
            #print("Pino: " + str(cls.pinsensor[i]) + " = INPUT")
        
        # Pino Fechadura como OUT e inicialmente em nivel baixo
        GPIO.setup(cls.pinfechadura,GPIO.OUT)
        GPIO.output(cls.pinfechadura, GPIO.LOW)
    
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
        GPIO.output(cls.pinfechadura, GPIO.HIGH)

    @classmethod
    def iniciarThread(cls):
        cls.setup()
        if cls.t == None: # Se o atributo t é Vazio
            cls.t = threading.Thread(target=cls.threadLogica)
        if cls.t.isAlive() == False and cls.concluida == False: # Verifica se a tread esta em execucao
            cls.tempo_inicial = time.time() # Defini o tempo incial da logica
            cls.t.start()
        elif cls.t.isAlive() == False and cls.concluida == True: # Verifica se a tread ja foi concluida alguma vez
            # CHECAR SE ESSA FUNCAO E NECESSARIA
            cls.t = threading.Thread(target=cls.threadLogica) # NOVA THREAD
            cls.tempo_inicial = time.time() # Defini o tempo incial da logica
            cls.contador = 0 #DEBUG
            cls.concluida = False
            cls.t.start()


    @classmethod
    def reiniciarThread(cls):
        cls.concluida = False
        cls.contador = 0 #DEBUG
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
            leituraSensor.append( GPIO.input(cls.pinsensor[0]) )
            leituraSensor.append( GPIO.input(cls.pinsensor[1]) )
            leituraSensor.append( GPIO.input(cls.pinsensor[2]) )
            cls.leituraSensores = leituraSensor

            # Checa se as condicoes dos sensores magneticos foi satisfeita
            if(leituraSensor == [1,1,1]):
                # Envia um pulso de 1 segundo para a fechadura
                GPIO.output(cls.pinfechadura, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(cls.pinfechadura, GPIO.LOW)
                cls.concluida == True
                print('Logica 1 - Finalizada')

            #print('\tLogica 1 - Rodando')
            time.sleep(0.5) # Delay do loop
            print(cls.getDuracaoLogica())
            
            print(cls.contador)
            cls.contador += 1
            if cls.contador >= 30:
                print('Logica 1 - Finalizada')
                cls.leituraSensores = []
                cls.concluida = True


# ------ FIM DA LOGICA 1 ---------