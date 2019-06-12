import time

diretorio = '/home/pi/escapebh/DESENVOLVIMENTO/tmp/lista.txt'

arq = open(diretorio, 'r')


#try:
while True:
    arq = open(diretorio, 'r')
    texto = arq.readlines()
    print(texto)
    #arq.close()
    time.sleep(2)
                
# except KeyboardInterrupt:
#     # Ao precionar Ctrl + C, encerra o programa.
#     arq.close()
#     print('\n --> Programa encerrado. <--')