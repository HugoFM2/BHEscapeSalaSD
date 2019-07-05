
#from escapebhjogo.classes.mcp23017 import MCP23017 as mcp
from .logica_geral import Logica_geral
from .cronometro import Cronometro
import time

# Classe criada para testes de desenvolvimento

class debug(object):

    # DEBUG logica_geral.py
    @staticmethod
    def logica_debug():
        #Logica_N1.setup()
        Logica_N1.iniciarThread()

    # DEBUG cronometro.py
    @staticmethod
    def cronometro_debug():
        Cronometro.iniciarCronometro()
        print('Inicio - Tempo Total: {}'.format(Cronometro.getTempoTotal()) ) 
        print('Inicio - String Formatada: {}'.format(Cronometro.stringFormatada()) )
        i = 0
        while True:
            print('Loop - String Formatada: {}'.format(Cronometro.stringFormatada()) )
            i += 1
            if i >= 10:
                Cronometro.resetarCronometro()
                print('Loop - Tempo Gravado: {}'.format(Cronometro._tempoGravado) )
                print('Loop - Tempo Decorrido: {}'.format(Cronometro._tempoDecorrido) )
                Cronometro.iniciarCronometro()
                i = 0
            time.sleep(1)


class Logica_N1(Logica_geral):

    @classmethod
    def setup(cls):
        print('Execucao do setup da {}'.format(cls.__name__))
        #print('Concluida =' + cls.isConcluida())

    @classmethod
    def threadLogica(cls):
        i = 0
        while cls._concluida == False:
            print( 'Thread implementada! i = {}'.format(i) )
            i += 1
            
            if (i > 10):
                break
            
            time.sleep(1)