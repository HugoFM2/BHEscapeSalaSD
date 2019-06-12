
# Classe criada para testes de desenvolvimento

class debug(object):
    total_classes = 0

    def __init__(self):
        self.total_classes = self.total_classes + 1
        print('Objeto instanciado')
        print(self.total_classes)
        pass

    @staticmethod
    def mensagem():
        print('Debug Escape BH - Mensagem')