import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo

import sys
sys.path.append('/home/pi/escapebh/escapebhserver/escapebhjogo/classes')
from mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp


""" MAPEAMENTO LOGICA 1

Vermelho -> Dentro do móvel do mezanino terá um botão. Apertando-o vai liberar um laser.
Direcionando o laser da forma correta para a gaveta na parte de baixo do palco vai abri-la.
"""

GPIO_RASPBERRY = [35,37,40,38,36,32,26,22,18,16,12,10,8]

print('Mapeamento 1 Iniciado!')

# Extensor
mcp.confRegistradoresComZero()

# Sensores do extensor como INPUT
time.sleep(2)
for i in range(0,8):
    mcp.setup(i, mcp.GPA, mcp.IN, mcp.ADDRESS1)
    mcp.setup(i, mcp.GPB, mcp.IN, mcp.ADDRESS1)

# Reles como OUTPUT (Modulo desativa em nivel alto)
time.sleep(2)
for i in range(0,8):
    mcp.setup(i, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
    mcp.setup(i, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
    mcp.output(i, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
    mcp.output(i, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

# Raspberry
GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
GPIO.setwarnings(False) # Desativa avisos

# Definindo pinos como input
for gpio in GPIO_RASPBERRY:
    GPIO.setup(gpio, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    
# Loop
while True:
    leitura = []
    leitura.append('GPA:')
    for i in range(0,8):
        leitura.append(mcp.input(i,mcp.GPA, mcp.ADDRESS1))

    leitura.append('GPB:')
    for i in range(0,8):
        leitura.append(mcp.input(i,mcp.GPB, mcp.ADDRESS1))

    print('\n Leituras Extensor:')
    print(leitura)
    time.sleep(1)

    leiura_rasp = []
    for gpio in GPIO_RASPBERRY:
        leiura_rasp.append(GPIO.input(gpio)) #
    
    print('\n Leituras Raspberry:')
    print(leitura)
    time.sleep(1)

# # GPIO's
# gpio_botao = 0 # Botao mezanino (Raspberry)
# gpio_ldr = 0 # Sensor ldr (Raspberry)
# gp_laser = 0 # Rele Laser (Extensor 0x)s
# gp_gaveta = 0 # Rele Gaveta (Extensor)



# # Configurado GPIO's do raspberry
# GPIO.setup(cls.gpio_botao, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
# GPIO.setup(cls.gpio_ldr, GPIO.IN)

# # Configurando GPIO's do Extensor
# mcp.setup(cls.gp_laser, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
# mcp.setup(cls.gp_gaveta, mcp.GPA, mcp.OUT, mcp.ADDRESS2)

# # Inicialmente em nivel baixo
# mcp.output(cls.gp_laser, mcp.GPA, mcp.LOW, mcp.ADDRESS2)
# mcp.output(cls.gp_gaveta, mcp.GPA, mcp.LOW, mcp.ADDRESS2)