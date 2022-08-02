# -*- coding: utf-8 -*-
import time
gp_travaCaixa = 7 # Rele da trava da caixa - GPB 7 (extensor 0x24)
gp_travaTubo = 6 # Rele da trava do tubo - GPB 6 (extensor 0x24)


from mcp23017 import MCP23017 as mcp
print('ola')


def setup():
	print('RODANDO SETUP')
	mcp.setup(gp_travaCaixa, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
	mcp.setup(gp_travaTubo, mcp.GPB, mcp.OUT, mcp.ADDRESS2)


	mcp.output(gp_travaCaixa, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)
	mcp.output(gp_travaTubo, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)


def AbrirCaixa():
	mcp.setup(gp_travaCaixa, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
	mcp.output(gp_travaCaixa, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
	time.sleep(0.25)
	mcp.output(gp_travaCaixa, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)



def AbrirTuboBrasao():
	mcp.setup(gp_travaTubo, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
	mcp.output(gp_travaTubo, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
	time.sleep(0.25)
	mcp.output(gp_travaTubo, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)
	

setup()


#AbrirTuboBrasao()
AbrirCaixa()