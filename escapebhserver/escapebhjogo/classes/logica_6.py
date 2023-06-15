import RPi.GPIO as GPIO # Modulo de controle da GPIOs
import time # Modulo para delays e contagem de tempo
import threading # Modulo para trabalhar com treads
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from .logica_geral import Logica_geral
from escapebhjogo.classes.logica_4 import Logica_4 # Classe com metodos da logica 4

""" CLASSE LOGICA 6
Esta classe faz todo o controle dos itens relacionados a Logica 6

Preto -> Colocando todas as invenções nas prateleiras vai fazer com que o motor na segunda
sala ative, liberando a chave. (Explicando melhor essa parte: Ao invés de ser apenas a chave
caindo como é o atual avião que desce, será uma peça do teto que estará presa por uma
dobradiça e o motor. Quando o motor descer essa peça do teto vai abrir como se fosse uma
pequena gaveta e a chave irá deslizar)
"""

class Logica_6(Logica_geral): # Logica 4 no site

	# GPIO's
	gp_arduinoInvecoes = 31 # GPIO que recebe sinal sobre a leitura das 7 invecoes. (raspberry)
	gp_motorDescer = 2 # Rele Desce Motor - GPB 2 (extensor 0x24)
	gp_motorSubir = 5 # Rele Sobe Motor - GPB 5 (extensor 0x24)
	executarSomLogica4 = False
	# Sobreescrevendo metodo setup() da classe pai
	@classmethod
	def setup(cls):
		GPIO.setmode(GPIO.BOARD) # Contagem de (0 a 40)
		GPIO.setwarnings(False) # Desativa avisos

		# Configurado GPIO's do raspberry
		# GPIO.setup(cls.gp_arduinoInvecoes, GPIO.IN) # DESABILITADO - AGORA É UMA AUTOMACAO INDEPENDENTE, POR MQTT

		# Configurando GPIO's do Extensor
		mcp.setup(cls.gp_motorDescer, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
		mcp.setup(cls.gp_motorSubir, mcp.GPB, mcp.OUT, mcp.ADDRESS2)

		# Inicialmente em nivel alto (Desativado)
		mcp.output(cls.gp_motorDescer, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)
		mcp.output(cls.gp_motorSubir, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

	# Metodo para acionar o motor no sentindo de descer a "gaveta"
	@classmethod
	def descerMotor(cls):
		print("Descendo motor teto")
		cls.executarSomLogica4 = True
		# cls._concluida = True
		time.sleep(1) # Delay Adicional para detectar o som
		cls.executarSomLogica4 = False
		mcp.setup(cls.gp_motorDescer, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
		mcp.output(cls.gp_motorDescer, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
		time.sleep(10)
		mcp.output(cls.gp_motorDescer, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)
		



	# Metodo para acionar o motor no sentindo de subir a "gaveta"
	@classmethod
	def subirMotor(cls):
		mcp.setup(cls.gp_motorSubir, mcp.GPB, mcp.OUT, mcp.ADDRESS2)
		mcp.output(cls.gp_motorSubir, mcp.GPB, mcp.LOW, mcp.ADDRESS2)
		time.sleep(10.5)
		mcp.output(cls.gp_motorSubir, mcp.GPB, mcp.HIGH, mcp.ADDRESS2)

	@classmethod
	def descerSubirMotor(cls):# Utilizado durante a automação para descer o motor e subir apos X segundos
		cls.descerMotor()
		time.sleep(5)
		cls.subirMotor()

	# Sobreescrevendo metodo threadLogica() da classe pai
	@classmethod
	def threadLogica(cls):
		while cls._concluida == False:
			# Checa se a logica 4 já foi concluida - AUTOMACAO INDEPENDENTE, POR MQTT
			if Logica_4._concluida == True:
			# 	print("Logica Arduino RFID rodando")
			# 	if GPIO.input(cls.gp_arduinoInvecoes) == GPIO.HIGH:
			# 		# cls.descerMotor()
			# 		cls.descerSubirMotor()
			# 		print("MotorDescendo e subindo apos x segundos")
				print('4ª Logica - Rodando (Invenções/Teto 2ª Sala)')

			time.sleep(0.25)

		else:
			print('4ª Logica - Finalizada')

# ------ FIM DA LOGICA 6 ---------
