
diretorio = '/home/pi/escapebh/DESENVOLVIMENTO/tmp/lista.txt'

# Escrever em arquivo
arq = open(diretorio, 'w')
texto = """Lista de Alunos
---
João da Silva
José Lima
Maria das Dores"""
arq.write(texto)
arq.close()

#Escrever linha a linha
# arq = open('/tmp/lista.txt', 'w')
# texto = []
# texto.append('Lista de Alunos\n')
# texto.append('---\n')
# texto.append('João da Silva\n')
# texto.append('José Lima\n')
# texto.append('Maria das Dores')
# arq.writelines(texto)
# arq.close()

# Ler arquivo inteiro
arq = open(diretorio, 'r')
texto = arq.read()
print(texto)
arq.close()

# Ler aquivo linha a linha
arq = open(diretorio, 'r')
texto = arq.readlines()
for linha in texto :
    print(linha, end='')
arq.close()