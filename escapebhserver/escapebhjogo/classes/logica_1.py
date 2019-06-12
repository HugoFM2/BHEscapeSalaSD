
import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays
import threading # Modulo para trabalhar com treads

# Classe Logica 1
class Logica_1(object):
    
    contador = 0
    concluida = False
    leituraSensoresG = []

    # Pinos dos sensores magneticos
    pinsensor_1 = 3
    pinsensor_2 = 5
    pinsensor_3 = 7
    pinfechadura = 11

    @classmethod
    def setup(cls):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(cls.pinsensor_1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.pinsensor_2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.pinsensor_3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(cls.pinfechadura,GPIO.OUT)

        GPIO.output(cls.pinfechadura, GPIO.LOW)
    
    @classmethod
    def getLeituraSensores(cls):
        return cls.leituraSensoresG

    def iniciarThread(self):
        threading.Thread(target=self.threadLogica).start()

    def forcarAbrirTrava(self):
        GPIO.output(self.pinfechadura, GPIO.HIGH)

    def threadLogica(self):
        while Logica_1.concluida == False:
            leituraSensor_1 = GPIO.input(self.pinsensor_1)
            leituraSensor_2 = GPIO.input(self.pinsensor_2)
            leituraSensor_3 = GPIO.input(self.pinsensor_3)
            Logica_1.leituraSensoresG = [leituraSensor_1,leituraSensor_2,leituraSensor_3]

            # Checa se as condicoes dos sensores magneticos foi satisfeita
            if(leituraSensor_1 == 1 and leituraSensor_2 == 1 and leituraSensor_3 == 1):
                GPIO.output(self.pinfechadura, GPIO.HIGH)
                time.sleep(1)
                concluida == True
                print('Logica 1 - Finalizada')
            print('\tLogica 1 - Rodando')
            time.sleep(0.5)

# ------ FIM DA LOGICA 1 ---------