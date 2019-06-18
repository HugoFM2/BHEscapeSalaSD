import sys
sys.path.append('/home/pi/escapebh/escapebhserver/escapebhjogo/classes/mcp23017.py')

from mcp23017 import MCP23017 as mcp
import time

#mcp.confRegistradoresComZero()
for i in range(8):
    mcp.setup(i, mcp.GPB, mcp.OUT, 0x24)
    time.sleep(0.2)
print("Comecando Loop")
while True:
    print("Digite a GPIO")
    gpio = int(input())
    print("Digie o Nivel - 0 ou 1")
    nivel = int(input())
    if nivel == 1:
        n = mcp.HIGH
    else:
        n = mcp.LOW
    
    print("\tGPIO " + str(gpio) + " = " + str(n) + "\n")

    mcp.output(gpio, mcp.GPB, n, 0x24)
