"""Modulo com os metodos e atributos comuns de todas as logicas.
"""

import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads

class Logica_geral(object):
    """Classe Logica_geral, usada como classe Pai para herancas nas classes Logica_n do jogo.
    
    * Não serão criadas instancias das classes(Logica_n) herdadas desta classe(Logica_geral),
      pois a logica de programação desenvolvida prevê o uso de metodos de classe.

    Atributos da classe:
        _concluida (bool): Armazena o status da logica, False = Não Concluida e True = Concluida
        _leituraSensores (list(int)): Armazena leitura dos sensores referentes a logica
        _thread (Thread): Armazena a Thread da classe que faz a checagem dos estados dos sensores
    """

    _concluida = False
    _leituraSensores = []
    _thread = None

    # METODOS DE CLASSE

    @classmethod
    def setup(cls):
        """Metodo Setup
        Neste metodo serão configurados as GPIOS e outras configurações
        * Deve ser implementado na classe filha, se não gerará uma exceção `NotImplementedError`
        """
        raise NotImplementedError('É necessário implementar o metodo setup() na classe filha! ')

    @classmethod
    def isConcluida(cls):
        return cls._concluida

    @classmethod
    def getLeituraSensores(cls):
        return cls._leituraSensores

    @classmethod
    def iniciarThread(cls):
        # Se o atributo t é Vazio cria uma tread
        if cls._thread == None:
            cls._thread = threading.Thread(target=cls.threadLogica)
        
        # Verifica se a tread não esta em execucao e se ainda nao foi concluida
        if cls._thread.isAlive() == False and cls._concluida == False:
            cls.setup() # Executa o metodo setup()
            time.sleep(1) # Delay de 1 segundo
            cls.leituraSensores = [] # Limpa a variavel de leituras
            cls._thread.start() # Inicia a thread

        elif (cls._thread.isAlive() == True):
            print('Thread da ' + str(cls.__name__) + ' em execução, é necessario reinicia-la para executar do inicio.')
        else:
            print('Thread da ' + str(cls.__name__) + ' já concluida, é necessario reinicia-la para executar novamente.')

    @classmethod
    def reiniciarThread(cls):
        if cls._thread != None: # Se a thread existir, ou seja, diferente de vazia
            if cls._thread.isAlive() == True:
                cls._concluida = True # Finaliza a tread em execucao
                time.sleep(2)
        cls._concluida = False
        cls._leituraSensores = [] # Limpa a variavel de leituras
        cls._thread = threading.Thread(target=cls.threadLogica) # NOVA THREAD
        cls.iniciarThread() # Chama o metodo para iniciar thread

    @classmethod
    def threadIsAlive(cls):
        status = None
        if not cls._thread == None: # Se o atributo thread é diferente de Vazio
            status = cls._thread.isAlive()
        return status

    @classmethod
    def threadLogica(cls):
        """Thread threadLogica()
        Este metodo(Tarefa) ficará em loop checando os sensores
        * Deve ser implementado na classe filha, se não gerará uma exceção `NotImplementedError`
        """
        raise NotImplementedError('É necessário implementar o metodo threadLogica() na classe filha! ')

# ------ FIM CLASSE Logica_geral ------