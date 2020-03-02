# from mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
# import smbus

# gpio_botao = 1 # Botao mezanino - GPB 1 (Extensor 0x22)
# mcp.setup(gpio_botao, mcp.GPB, mcp.IN, mcp.ADDRESS1)
# while True:
# 	leitura_botao = mcp.input(gpio_botao, mcp.GPB, mcp.ADDRESS1)
# 	if(leitura_botao == 1):
# 		print("Botao pressionado")