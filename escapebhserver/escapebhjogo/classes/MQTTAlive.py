import paho.mqtt.client as mqtt
import json
from threading import Thread, Timer
import time
from escapebhjogo.classes.logica_8 import Logica_8 

class MQTT_Th(Thread):
	

	# def __init__ (self,num, textTopic,automacoes):
	def __init__ (self,num):
		print("MQTT Iniciado: ",num)
		Thread.__init__(self)
		self.client = mqtt.Client()
		
		self.num = num
		self.Broker = "192.168.100.1"
		self.PortaBroker = 1883
		self.KeepAliveBroker = 60 
		self.client.on_connect = self.on_connect
		self.client.on_disconnect = self.on_disconnect
		self.client.on_message = self.on_message
		self.client.connect(self.Broker, self.PortaBroker)




	def run(self):

		print(f"Thread MQTT Iniciada: {self.num}")
		# self.client.loop_start()
		self.client.loop_forever(retry_first_connection=False)


	def on_connect(self, client, userdata,flags, rc):
		print("MQTT Conectado")
		self.client.subscribe("SalaSD/CaixaArma/Arma/#")
		self.client.subscribe("SalaSD/ESP_TUBO/Tubo/#")
		# self.client.subscribe(self.textTopic + "/") #subscribe to self.textTopic
		# self.SendMsgCheck()

	def on_disconnect(self, client, userdata, rc):
		print("MQTT DISCONNECT")
		# self.client.subscribe(self.textTopic + "/") #subscribe to self.textTopic
		# self.SendMsgCheck()

	def mqtt_publish(self,topic,msg,retain=False):
		self.client.publish(topic,msg,retain=retain)
		print(f"Mensagem enviada com retain {retain}")
		return "OK"

	def on_message(self, client, userdata, msg):
		print("---=== MENSAGEM MQTT RECEBIDA ===---")
		print(f"Mensagem: {msg.payload.decode()} -> Topico {msg.topic}\n")
		if (msg.topic == "SalaSD/CaixaArma/Arma/Status"):
			if msg.payload.decode() == 'true':
				print("Enviando comando de abrir caixa(ligar som)")
				Logica_8.abrirCaixa()

		if (msg.topic == "SalaSD/ESP_TUBO/Tubo/Status"):
			if msg.payload.decode() == 'true':
				print("Enviando comando de abrir Tubo(ligar som)")
				Logica_8.abrirTuboBrasao()				
		# if(msg.topic == self.textTopic + "/statusConn"):
		# 	self._lastConn = msg.payload.decode()
		# for i in range(len(self.automacoes)):
		# 	# print(self.textTopic + "/" + self.automacoes[i] + "/concluida")
		# 	if(msg.topic == self.textTopic + "/" + self.automacoes[i] + "/concluida"):
		# 		self._concluida[i] = bool(int(msg.payload.decode()))
		# 		print(self._concluida[i])		

	# def setDesc(self,nome,botoes,topico,mensagem):
	# 	self.desc = []
	# 	self.desc.clear()
	# 	self.desc = {
	# 		"Name"		: nome,
	# 		"Botoes"	: botoes,
	# 		"Topicos"	: topico,
	# 		"Mensagens"	: mensagem
	# 	}

	# def CheckConn(self):
	# 	if(self._lastConn == "1"):
	# 		# print("Modulo {} Conectado".format(self.textTopic))
	# 		self._ConnectStatus = 1
	# 	else:
	# 		# print("Modulo {} Desconectado".format(self.textTopic))
	# 		self._ConnectStatus = 0
	# 	Timer(5.0, self.SendMsgCheck).start()

	# def ConnectStatus(self):
	# 	self.x = [{
	# 		"Name" 			 : self.textTopic,
	# 		"Status"		 : self._ConnectStatus
	# 	}]
	# 	return self.x

	# def SendMsgCheck(self):
	# 	# print("Enviando requisicao de conexao")
	# 	self._lastConn = 0
	# 	Timer(2.0, self.CheckConn).start()
	# 	self.mqtt_publish(self.textTopic + "/sendCheck",self._lastConn)

	# def isConcluida(self):
	# 	self.x = []
	# 	self.x.clear()

	# 	for i in range(len(self.automacoes)):
	# 		self.x.append({
	# 	"Name" 			 : self.textTopic + "/" + self.automacoes[i],
	# 	"Status"		 : self._concluida[i]
	# 	}
	# 			)

	# 	return self.x

	def Reset(self):
		print("MQTT RESETADO")
		self.mqtt_publish("ESP32-1/cmnd","reset")
		self.mqtt_publish("SalaSD/CaixaArma/cmnd","reset")
		self.mqtt_publish("SalaSD/ESP_TUBO/cmnd","reset")
		self.mqtt_publish("SalaSD/Rpi/Gaveta/Status","false",retain=True)

	# def Descricao(self):
	# 	return self.desc


MQTTServer = MQTT_Th(3)
MQTTServer.start()
# Logica1 = MQTT_Th(5,"Automacao1",["Genius","Bicicleta"])
# Logica1.setDesc(["Automacao1/Bicicleta","Automacao1/Genius"],
# 				[["Concluir Bicicleta","Reiniciar Bicicleta"],["Abrir Tranca", "Reiniciar Genius"]],
# 				[["force","force"],["force","force"]],
# 				[["1","0"],["1","0"]])
# Logica1.start() 

# Logica2 = MQTT_Th(5,"Automacao2",["Einstein","Alavancas"])
# Logica2.start() 

# Logica2 = MQTT_Th(5,"Automacao2")
# Logica2.start() 

# Logicas = [Logica1,Logica2]

# Logicas = [Logica1]
# for i in range(1,100):
# 	t1 = MQTT_Th(i,"Automacao" + str(i))
# 	Logicas.append(t1)
# 	t1.start()



# def JSONConnStatus():
# 	LogicaStatus = []
# 	LogicaStatus.clear()
# 	for i in Logicas:
# 		LogicaStatus.append(i.ConnectStatus())
# 	return LogicaStatus

# def JSONConcluidoStatus(): # Retorna o status de conclusao de todas as automacoes
# 	LogicaConcluida = []
# 	LogicaConcluida.clear()
# 	for i in Logicas:
# 		for j in i.isConcluida():
# 			LogicaConcluida.append(j)
# 	return LogicaConcluida

def ResetALLMQTT():
	
	MQTTServer.Reset()


def PublishMQTT(topic,msg,retain=False):
	print(f"Mensagem MQTT {msg} Publicada no tópico {topic}")
	MQTTServer.mqtt_publish(topic,msg,retain)

# def merge_two_dicts(x, y):
#     """Given two dicts, merge them into a new dict as a shallow copy."""
#     z = x.copy()
#     z.update(y)
#     return z