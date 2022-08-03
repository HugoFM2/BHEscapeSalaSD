var mqtt;
var reconnectTimeout = 2000;
var host="10.0.0.51"; //change this
var port=9001;


function randomInt(min, max) { // Retorna um cliente random, para nao haver conflito
	return min + Math.floor((max - min) * Math.random());
}

function onConnect() {		
	// Once a connection has been made, make a subscription and send a message.
	console.log("Conectado! ");
	mqtt.subscribe("ESP32-1/#");
	mqtt.subscribe("SalaSD/CaixaArma/Arma/#");
	mqtt.subscribe("SalaSD/CaixaArma/Connected");

	mqtt.subscribe("SalaSD/ESP_TUBO/Tubo/#");
	mqtt.subscribe("SalaSD/ESP_TUBO/Connected");

	getAllStatus();
	// message = new Paho.MQTT.Message("Hello World");
	// message.destinationName = "sensor1";
	// mqtt.send(message);
}

function MQTTconnect() {
	console.log("connecting to "+ host +" "+ port);
	mqtt = new Paho.MQTT.Client(host,port, randomInt( 10, 200).toString() );
	//document.write("connecting to "+ host);
	var options = {
		timeout: 3,
		onSuccess: onConnect,
		onFailure: onFailure,
		 };
	mqtt.onMessageArrived = onMessageArrived
	mqtt.onConnectionLost = onConnectionLost;

	mqtt.connect(options); //connect
}

function onFailure(message) {
	console.log("Connection Attempt to Host "+host+" Failed");
	setTimeout(MQTTconnect, reconnectTimeout);
	FixedAlert("DANGER","Conexao MQTT Perdida, Atualizar pagina, caso a mensagem permaneça reinicializar raspberry","lost-Connection");
}

function onConnectionLost(){
	console.log("connection lost");
	FixedAlert("DANGER","Conexao MQTT Perdida, Atualizar pagina, caso a mensagem permaneça reinicializar raspberry","lost-Connection");
	
}
function onMessageArrived(msg){
	out_msg="Message received "+msg.payloadString;
	out_msg=out_msg+"Message received Topic "+msg.destinationName;
	console.log(out_msg);
    if(msg.destinationName == "ESP32-1/LWT"){
      var statusbuff = (msg.payloadString === 'true');
      if(statusbuff){
        toggleConnStatusON("ESP32-1");
        // DeleteAlert("ESP32-1");
      }else{
        toggleConnStatusOFF("ESP32-1");
        // FixedAlert("DANGER","ESP32-1 Desconectada!","ESP32-1");
      }
    }
    else if(msg.destinationName == "ESP32-1/Bicicleta/concluida"){
	  console.log(msg.payloadString);
	  var statusbuff = (msg.payloadString === 'true');
	  if(statusbuff){
	    toggleStatusON("Bicicleta");
	    // $('#Linha-Automacao1').removeClass("table-success");
	  }
	  else{
	    toggleStatusOFF("Bicicleta");
	  }
	}
    else if(msg.destinationName == "ESP32-1/Genius/concluida"){
	  console.log(msg.payloadString);
	  var statusbuff = (msg.payloadString === 'true');
	  if(statusbuff){
	    toggleStatusON("Genius");
	    // $('#Linha-Automacao1').removeClass("table-success");
	  }
	  else{
	    toggleStatusOFF("Genius");
	  }
	}
	else if(msg.destinationName == "SalaSD/CaixaArma/Arma/Status"){
		if(msg.payloadString.toLowerCase() === 'true'){
			toggleStatusON("Caixa");
		} else {
			toggleStatusOFF("Caixa");
		}
	}
	else if(msg.destinationName == "SalaSD/CaixaArma/Connected"){
		if(msg.payloadString.toLowerCase() === 'true'){
			toggleConnStatusON("ESP32Caixa");
		} else {
			toggleConnStatusOFF("ESP32Caixa");
		}
	}	

	// ESP TUBO
	else if(msg.destinationName == "SalaSD/ESP_TUBO/Tubo/Status"){
		if(msg.payloadString.toLowerCase() === 'true'){
			toggleStatusON("Tubo");
		} else {
			toggleStatusOFF("Tubo");
		}
	}
	else if(msg.destinationName == "SalaSD/ESP_TUBO/Connected"){
		if(msg.payloadString.toLowerCase() === 'true'){
			toggleConnStatusON("ESP32Tubo");
		} else {
			toggleConnStatusOFF("ESP32Tubo");
		}
	}	

}

function getAllStatus(){
	// retorna o Status de todas as automacoes(enviado por dispositivo)
	// ESP CAIXA
	message = new Paho.MQTT.Message("getAllStatus");
	message.destinationName = "SalaSD/CaixaArma/cmnd";
	mqtt.send(message);

	// ESP TUBO
	message = new Paho.MQTT.Message("getAllStatus");
	message.destinationName = "SalaSD/ESP_TUBO/cmnd";
	mqtt.send(message);	

}

function toggleConnStatusON(id){
	$('.statusConn-' + id).attr("src", "static/imagens/icon-ok.svg");
}
function toggleConnStatusOFF(id){
	$('.statusConn-' + id).attr("src", "static/imagens/icon-fail.svg");
}

function toggleStatusON(id){
  console.log(id)
  document.getElementById("status-Conclusao-"+id).className = "dot dotVerde";
}

function toggleStatusOFF(id){
  console.log(id)
  document.getElementById("status-Conclusao-"+id).className = "dot dotCinza";
}



function FixedAlert(type,text,id){
  if(type == "DANGER"){
    $('#Alertas').append('<div id="Alerta-'+id+'" class="alert alert-danger alert-dismissible position-relative" >'+text+'</div>')
  }
}

function DeleteAlert(id){
  $('#Alerta-' +id).remove();
  $('#Alerta-' +id).remove();
  $('#Alerta-' +id).remove();
}

function concluir_Bicicleta(){
	message = new Paho.MQTT.Message("BicicletaForce");
	message.destinationName = "ESP32-1/cmnd";
	mqtt.send(message);
}

function concluir_Genius(){
	message = new Paho.MQTT.Message("GeniusForce");
	message.destinationName = "ESP32-1/cmnd";
	mqtt.send(message);
}

function ForcarESP32_Caixa_Cilindro(){
	message = new Paho.MQTT.Message("force");
	message.destinationName = "SalaSD/CaixaArma/Arma/cmnd";
	mqtt.send(message);
	console.log("[MQTT] Comando de reiniciar EspTubo enviado!");
}

function ForcarESP32_Tubo(){
	message = new Paho.MQTT.Message("force");
	message.destinationName = "SalaSD/ESP_TUBO/Tubo/cmnd";
	mqtt.send(message);
	console.log("[MQTT] Comando de Forcar tubo enviado!");
}

function ReiniciarESP321(){
	message = new Paho.MQTT.Message("reset");
	message.destinationName = "ESP32-1/cmnd";
	mqtt.send(message);
}

function ReiniciarESP32_Caixa(){
	message = new Paho.MQTT.Message("reset");
	message.destinationName = "SalaSD/CaixaArma/cmnd";
	mqtt.send(message);
	console.log("Comando de reiniciar EspCaixa enviado!");
}

function ReiniciarESP32_Tubo(){
	message = new Paho.MQTT.Message("reset");
	message.destinationName = "SalaSD/ESP_TUBO/cmnd";
	mqtt.send(message);
	console.log("Comando de reiniciar EspTubo enviado!");
}