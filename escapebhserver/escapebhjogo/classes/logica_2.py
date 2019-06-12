
import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays
import threading # Modulo para trabalhar com treads

# Classe Logica 2
class Logica_2(object):
    def __init__(self):
        # Diretorio do arquivo de trocas de informacoes
        self.dir_logica = '/home/pi/escapebh/escapebhserver/escapebhjogo/tmp/logica' + '2'

        # Pinos dos sensores magneticos
        self.pinsensor_1 = 13
        self.pinsensor_2 = 15
        self.pinsensor_3 = 19
        self.pinsensor_4 = 21
        self.pinMala = 23 # Pino da trava da mala

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        # Configurando Pinos como INPUT em Pull_Down
        GPIO.setup(self.pinsensor_1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(self.pinsensor_2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(self.pinsensor_3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(self.pinsensor_4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(self.pinMala,GPIO.OUT)

        GPIO.output(self.pinMala, GPIO.LOW) # Mala em nivel baixo

    # Metodo para leitura do arquivo onde estao gravadas as leituras dos sensores
    def getStatusSensores(self):
        leituraSensores = []
        arq = open(self.dir_logica, 'r')
        leitura = arq.readlines()

        if len(leitura) > 0:
            leituraSensores = leitura[0].split(',')
            leituraSensores.remove('\n')
            print(leituraSensores)
        
        return leituraSensores

    # Metodo para iniciar a thread
    def iniciarThread(self):
        threading.Thread(target=self.threadLogica).start()

    # Metodo para apagar o conteudo do arquivo de leituras do sensor
    def limparArquivoTemporario(self):
            arq = open(self.dir_logica, 'w')
            arq.write('') # Escrever uma string vazia no arquivo
            arq.close()

    # Metodo para forcar a abertura da mala
    def forcarAbrirMala(self):
        GPIO.output(self.pinMala, GPIO.HIGH)

    # Thread que verifica os sensores magneticos
    def threadLogica(self):
        concluida = False
        while concluida == False:
            leituraSensor_1 = GPIO.input(self.pinsensor_1)
            leituraSensor_2 = GPIO.input(self.pinsensor_2)
            leituraSensor_3 = GPIO.input(self.pinsensor_3)
            leituraSensor_4 = GPIO.input(self.pinsensor_4)
            
            # Escrevendo no arquivo de informacoes
            arq = open(self.dir_logica, 'w')
            texto = []
            texto.append(str(leituraSensor_1))
            texto.append(',')
            texto.append(str(leituraSensor_2))
            texto.append(',')
            texto.append(str(leituraSensor_3))
            texto.append(',')
            texto.append(str(leituraSensor_4))
            texto.append(',\n') # Ultimo caracter
            arq.writelines(texto)

            # Checa se as condicoes dos sensores magneticos foi satisfeita
            if(leituraSensor_1 == 1 and leituraSensor_2 == 1 and leituraSensor_3 == 1 and leituraSensor_4 == 1):
                GPIO.output(self.pinMala, GPIO.HIGH)
                time.sleep(1)
                concluida == True
                print('Logica 2 - Finalizada')
            #print('\tLogica 2 - Rodando')
            time.sleep(0.5)

# ------ FIM DA LOGICA 2 ---------