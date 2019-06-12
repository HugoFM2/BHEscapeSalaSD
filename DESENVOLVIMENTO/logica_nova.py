
# LOGICA 5
# Se um botao for ativado, acionar laser por 5 segundos
# Se o laser refletir no ldr, ai destrava fechadura gaveta

# LOGICA 6
# Se as duas fechadura estiverem na rotação correta, abre o busto do Dr.Gero
# Dentro do Dr.Gero ha um botao.

# Logica 7
# Se o botao do Dr.Gero for pressionado, destrava a fechadura da porta

# Logica 8
# Substitui logica 1 do codigo antigo
# Se as 7 invecoes RFID forem posicionadas no local correto, desce uma cordinha(Acionamento de motor)

# Logica 9
# Se o sensor de fechamento(magnetico) for acionado e o botao for ativado
# e Se a peca correta estiver encaixada, aciona fechadura para travar o sistema (Servo). 
# Se servo acionado, piscagemn da lampada da sala via rele
# Destrave de outra gaveta onde estara o brasao 

# Logica 10
# Se brasao na posicao correta(magnetico), destrava uma porta

"""---------------------------------------------------------------------"""

# Codigo antigo como 2,3,4

# Logica 2 - Posicinnamento de Letras
# Ler 4 sensores nmagneticos
# Caso os quatro estejam em HIGH destrava maleta


# Logica 3 - Posicionamento Livros
# Le tres sensores magneticos
# Caso os tres estejam em HIGH aciona um motor

# Logica 4 - Sistema de alavancas
# C
# caso as alavancas estejam na posicao correta, destrava duas fechaduras.