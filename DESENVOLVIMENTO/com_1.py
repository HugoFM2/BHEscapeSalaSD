import time

diretorio = '/home/pi/escapebh/DESENVOLVIMENTO/tmp/lista.txt'

#arq = open(diretorio, 'w')
contador = 0

try:
        while True:
                arq = open(diretorio, 'w')
                texto = str(contador)
                arq.write(texto)
                print('Gravado: ' + str(contador))
                contador = contador + 1
                #arq.close()
                time.sleep(1)

except KeyboardInterrupt:
    # Ao precionar Ctrl + C, encerra o programa.
    arq.close()
    print('\n --> Programa encerrado. <--')