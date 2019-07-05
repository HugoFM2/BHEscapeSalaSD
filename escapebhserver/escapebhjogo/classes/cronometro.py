"""Modulo com os metodos e atributos para cronometrar duração do escape.
"""

import time

class Cronometro(object):

    _tempoInicial = None
    _tempoDecorrido = None
    _tempoGravado = None

    @classmethod
    def iniciarCronometro(cls):
        if cls._tempoInicial == None:
            cls._tempoInicial = time.time()
        else:
            print('Cronometro ja iniciado!')

    @classmethod
    def resetarCronometro(cls):
        if cls._tempoInicial != None and cls._tempoDecorrido != None:
            cls.calculaTempoTotal()
            cls._tempoGravado = cls._tempoDecorrido
        cls._tempoInicial = None
        cls._tempoDecorrido = None
        print('Cronometro resetado! Inicie uma nova contagem!')

    @classmethod
    def getTempoTotal(cls):
        duracao = 0
        if cls._tempoInicial != None:
            cls.calculaTempoTotal()
            duracao = cls._tempoDecorrido

        return duracao

    @classmethod
    def calculaTempoTotal(cls):
        if cls._tempoInicial != None:
            cls._tempoDecorrido = (time.time() - cls._tempoInicial)
        else:
            print('Inicie o cronometro!')

    @classmethod
    def stringFormatada(cls):
        string = None
        if(cls._tempoInicial != None):
            cls.calculaTempoTotal()
            horas = cls._tempoDecorrido // 3600 # Retorna somente a parte inteira
            minutos = (cls._tempoDecorrido % 3600) // 60
            segundos = (cls._tempoDecorrido % 3600) % 60
            string = '{:02.0f}:{:02.0f}:{:02.0f}'.format(horas, minutos, segundos)
        else:
            string = '{:02.0f}:{:02.0f}:{:02.0f}'.format(0, 0, 0)
        return string