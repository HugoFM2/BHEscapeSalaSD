# -*- coding: utf-8 -*-

# Autor: Sala Maker

# PINOUT GPIOs MC23017
# -----------|_U_|------------
# GPB0 <--*1 |--| 28 --> GPA7
# GPB1 <-- 2 |--| 27 --> GPA6
# GPB2 <-- 3 |--| 26 --> GPA5
# GPB3 <-- 4 |--| 25 --> GPA4
# GPB4 <-- 5 |--| 24 --> GPA3
# GPB5 <-- 6 |--| 23 --> GPA2
# GPB6 <-- 7 |--| 22 --> GPA1
# GPB7 <-- 8 |--| 21 --> GPA0
# -----------------------------

# Importar biblioteca para registro I2C
import smbus
# Importar sleep para delay do programa
from time import sleep

n_barramento = 0x01 # Numero do Barramento I2C do raspberry (No nosso caso é 1)
ADDRESS = 0x20 # Endereco do chip MC23017 (Definido pela configuracao A0,A1,A2

barramento = smbus.SMBus(n_barramento) # Instancia o barramento

# Enderecos de alguns registradores do chip MC23017 em hexadecimal
# Etrada ou saida de dados, 0=OUTPUT e 1=INPUT
IODIRA = 0x00
IODIRB = 0x01
#Protecao contra oscilacao de pinos configurados como INPUT,
# 1=Resitor de 10k interno habilitado, 0=Desabilitado
GPPUA = 0x0C
GPPUB = 0x0D
# Configuracao dos pino de INPUT como PULL UP ou PULL DOWN
# 0=PULL DOWN , 1=PULL UP
IPOLA = 0x02
IPOLB = 0x03
# Configuracao dos pinos de OUTPUT, similar ao digitalWrite do arduino
# 0=LOW e 1=HIGH
OLATA = 0x14
OLATB = 0x15
# Leitura dos pinos INPUT e OUTPUT, similar ao digitalRead do arduino
GPIOA = 0x12
GPIOB = 0x13

# Definindo metodos
# Le o valor do BIT referente a GPIOA recebida como argumento
def ler_GPIOA(gpioa):
    if gpioa > 7: gpioa = 7 # Evita resultados inesperados
    leitura = barramento.read_byte_data(ADDRESS, GPIOA)
    #print("Leitura HEX: " + str(hex(leitura)) + " BIN: " + str(bin(leitura)) + " INT:" + str(leitura))
    comparador = 0b00000001 << gpioa # gera um byte comparador
    valor = leitura & comparador # Faz uma operacao logica and com a leitura
    if valor == comparador:
        valor = 1
    else:
        valor = 0

    #print(valor)
    return valor

def ler_GPIOB(gpiob):
    if gpiob > 7: gpiob = 7 # Evita resultados inesperados
    leitura = barramento.read_byte_data(ADDRESS, GPIOB)
    #print("Leitura HEX: " + str(hex(leitura)) + " BIN: " + str(bin(leitura)) + " INT:" + str(leitura))
    comparador = 0b00000001 << gpiob # gera um byte comparador
    valor = leitura & comparador # Faz uma operacao logica and com a leitura
    if valor == comparador:
        valor = 1
    else:
        valor = 0

    print(valor)
    return valor

def setup():
    # Definir pinos como OUTPUT e INPUT
    barramento.write_byte_data(ADDRESS, IODIRA, 0b10000000) #GPIO A
    barramento.write_byte_data(ADDRESS, IODIRB, 0b00000001) #GPIO B

    # Definir protecao contra oscilacao do sinal para as GPIO configuradas como INPUT
    barramento.write_byte_data(ADDRESS, GPPUA, 0b10000000) #GPIO A
    barramento.write_byte_data(ADDRESS, GPPUB, 0b00000001) #GPIO B

    # Configurar os pino de INPUT PULL UP ou PULL DOWN
    barramento.write_byte_data(ADDRESS, IPOLA, 0b10000000) #GPIO A
    barramento.write_byte_data(ADDRESS, IPOLB, 0b00000000) #GPIO B
    # ---FIM DO SETUP

# Chamadas antes do loop
setup()
print("\n\t--> Programa MC23017 Iniciado. ")

# Loop infinito
while True:
    # Bit mais a direita representa o GPIO0 e o mais a esquerda o GPIO7
    if ler_GPIOA(7) == 1:
        barramento.write_byte_data(ADDRESS, OLATA, 0b00000001)
    else:
        barramento.write_byte_data(ADDRESS, OLATA, 0b00000000)
    #print( "LED = " + str(ler_GPIOA(0)) )
    ler_GPIOB(0)
    sleep(0.05)