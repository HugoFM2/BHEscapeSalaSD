
#from escapebhjogo.classes.mcp23017 import MCP23017 as mcp
from .logica_geral import Logica_geral
import time

# Classe criada para testes de desenvolvimento

class debug(object):

    # DEBUG logica_geral.py
    @staticmethod
    def logica_debug():
        #Logica_N1.setup()
        Logica_N1.iniciarThread()

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