import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo

import sys
sys.path.append('/home/pi/escapebh/escapebhserver/escapebhjogo/classes')
from mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp

# Extensor
#mcp.confRegistradoresComZero()

# Reles como OUTPUT (Modulo desativa em nivel alto)
#time.sleep(1)
for i in range(0,8):
    mcp.setup(i, mcp.GPA, mcp.OUT, mcp.ADDRESS2)
    mcp.setup(i, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
    mcp.output(i, mcp.GPA, mcp.HIGH, mcp.ADDRESS2)
    mcp.output(i, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

# TESTE
print('Iniciando teste trava')
gp = 4
while True:
    mcp.output(gp, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
    time.sleep(2)
    mcp.output(gp, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)
    time.sleep(2)