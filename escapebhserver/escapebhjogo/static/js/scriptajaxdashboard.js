const pCronometro = document.querySelector('#p-cronometro')

const btnIniciarJogo = document.querySelector('#btnIniciarJogo')
const btnReiniciarJogo = document.querySelector('#btnReiniciarJogo')
const btnDesligarRaspberry = document.querySelector('#btnDesligarRaspberry')

const btnAlcapao = document.querySelector('#btnAlcapao')

const btnLaser = document.querySelector('#btnLaser')
const btnGavetaLaser = document.querySelector('#btnGavetaLaser')

const btnGirarBusto = document.querySelector('#btnGirarBusto')
const btnVoltarBusto = document.querySelector('#btnVoltarBusto')
const btnPorta = document.querySelector('#btnPorta')

const btnSubirTeto = document.querySelector('#btnSubirTeto')
const btnDescerTeto = document.querySelector('#btnDescerTeto')
const btnDescerSubirTeto = document.querySelector('#btnDescerSubirTeto')

const btnPorao = document.querySelector('#btnPorao')

const btnBau = document.querySelector('#btnBau')

const btnGavetaMesa = document.querySelector('#btnGavetaMesa')

const btnCilindroEnergia = document.querySelector('#btnCilindroEnergia')
// const btnTubo = document.querySelector('#btnTubo')

const dotlogica2 = document.querySelector('#status-logica2')
const dotlogica1 = document.querySelector('#status-logica1')
const dotlogica4 = document.querySelector('#status-logica4')
const dotlogica6 = document.querySelector('#status-logica6')
const dotlogica3 = document.querySelector('#status-logica3')
const dotlogica5 = document.querySelector('#status-logica5')
const dotlogica7 = document.querySelector('#status-logica7')
const dotlogica8 = document.querySelector('#status-logica8')

// ---- SONS ----
const audio1 = document.querySelector("#myAudio1");
const btnAudio1 = document.querySelector('#btnAudio1')
// const audio2 = document.querySelector("#myAudio2-BR");
// const audio2_ES = document.querySelector("#myAudio2-ES");
// const audio2_EN = document.querySelector("#myAudio2-EN");
const btnAudio2 = document.querySelector('#btnAudio2')
const btnConfirmarIdioma = document.getElementById("ConfirmarIdioma");
var fazerRequestSom = false

// ---- VARIAVEIS ----
var segundos = 0
var intervalo = null

// ---- FUNCOES ----
function cronometro() {
    var h, min, seg
    var tH, tMin, tSeg
    var texto = ''
    seg = (segundos % 60) // 3700
    min = ((segundos - seg) / 60) % 60 // 1
    h = (((segundos - seg) / 60) - min) / 60

    if (h < 10) {
        tH = `0${h.toFixed(0)}`
    } else {
        tH = h.toFixed(0)
    }

    if (min < 10) {
        tMin = `0${min.toFixed(0)}`
    } else{
        tMin = min.toFixed(0)
    }
    
    if (seg < 10) {
        tSeg = `0${seg.toFixed(0)}`
    } else {
        tSeg = seg.toFixed(0)
    }

    texto = `${tH}:${tMin}:${tSeg}`
    pCronometro.innerHTML = texto
    console.log(segundos.toFixed(0))
    segundos += 1
    intervalo = setTimeout(cronometro, 1000)
}

function getRequestCronometro() {
    var xhttp = new XMLHttpRequest()
    var url = "ajaxcronometro"

    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        segundos = Number(this.responseText)
        if (intervalo === null) {
            cronometro()
        }
      }
    }
    xhttp.open("GET", url, true)
    xhttp.send()
}

function getRequestStatus() {
    var xhttp = new XMLHttpRequest()
    var url = "ajaxstatus"

    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var resposta = JSON.parse(this.responseText)
        //console.log(JSON.parse(this.responseText))

        if (resposta.logica1_status == true) {
            dotlogica1.className = "dot dotVerde"
        }
        if (resposta.logica2_status == true) {
            dotlogica2.className = "dot dotVerde"
        }
        if (resposta.logica3_status == true) {
            dotlogica3.className = "dot dotVerde"
        }
        if (resposta.logica4_status == true) {
            dotlogica4.className = "dot dotVerde"
        }
        if (resposta.logica5_status == true) {
            dotlogica5.className = "dot dotVerde"
        }
        if (resposta.logica6_status == true) {
            dotlogica6.className = "dot dotVerde"
        }
        if (resposta.logica7_status == true) {
            dotlogica7.className = "dot dotVerde"
            if (fazerRequestSom == false) {
                requestSom()
                fazerRequestSom = true
            }
        }
        // if (resposta.logica8_status == true) {
        //     dotlogica8.className = "dot dotVerde"
        // }
        
        setTimeout(getRequestStatus, 5000)
      }
    }
    xhttp.open("GET", url, true)
    xhttp.send()
}

function requestForcaLogica(acao) {
    var xhttp = new XMLHttpRequest()
    var url = "ajaxdashboard?acao=" + acao

    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        //console.log(this.responseText)
        criarAlerta(`Comando Executado! (${this.responseText})`, 'corpo')
      }
    }
    xhttp.open("GET", url, true)
    xhttp.send()
}

function criarAlerta(texto, idElementoPai) {
    var pai = document.getElementById(idElementoPai)

    // Criando a div do alerta
    var divMsgAlerta = document.createElement('div')
    divMsgAlerta.className = 'alert alert-info alert-dismissible fade show'
    
    // Criando o botao de fechar o alerta
    var btnFechar = document.createElement('button')
    btnFechar.type = 'button'
    btnFechar.className = 'close'
    btnFechar.dataset.dismiss = "alert"
    btnFechar.appendChild(document.createTextNode("×")) //&times;
    divMsgAlerta.appendChild(btnFechar)

    // Adicionando o texto ao alerta
    divMsgAlerta.appendChild(document.createTextNode(texto))

    // Adicionando o alerta ao elemento pai
    pai.appendChild(divMsgAlerta)
}
// ---- ACOES ----
//Inicia as atualizacoes dos status das logicas
getRequestStatus()

pCronometro.addEventListener('click', getRequestCronometro)

// Eventos ao aperta os botoes
btnIniciarJogo.addEventListener('click', function(){
    setTimeout(getRequestCronometro, 1500);
    requestForcaLogica('iniciarjogo');
    $.get("reset", function (data) { // Reinicia as Automacoes MQTT
        console.log(data)
    });
})
btnReiniciarJogo.addEventListener('click', function(){
    setTimeout(function() {
        console.log("Reiniciando automações RPI")
        requestForcaLogica('reiniciarjogo');
        $.get("reset", function (data) { // Reinicia as Automacoes MQTT
            console.log(data)
        });
    },500)

    setTimeout(function () {
        window.location.href = "http://10.0.0.51:8000/"
    },2000)
})
btnDesligarRaspberry.addEventListener('click', function(){
    requestForcaLogica('desligarraspberry')

    setTimeout(function () {
        window.location.href = "http://10.0.0.51:8000/"
    },2000)
})

btnAlcapao.addEventListener('click', function(){ requestForcaLogica('cairalcapao') })

btnLaser.addEventListener('click', function(){ requestForcaLogica('ativarlaser') })
btnGavetaLaser.addEventListener('click', function(){ requestForcaLogica('abrirgavetalaser') })

btnGirarBusto.addEventListener('click', function(){ requestForcaLogica('girarbusto') })
btnVoltarBusto.addEventListener('click', function(){ requestForcaLogica('voltarbusto') })
btnPorta.addEventListener('click', function(){ requestForcaLogica('abrirporta') })

btnSubirTeto.addEventListener('click', function(){ requestForcaLogica('subirteto') })
btnDescerTeto.addEventListener('click', function(){ requestForcaLogica('descerteto') })
btnDescerSubirTeto.addEventListener('click', function(){ requestForcaLogica('descersubirteto') })

btnPorao.addEventListener('click', function(){ requestForcaLogica('abrirporao') })

btnBau.addEventListener('click', function(){ requestForcaLogica('abrirbau') })

btnGavetaMesa.addEventListener('click', function(){ requestForcaLogica('abrirgavetamesa') })

btnCilindroEnergia.addEventListener('click', function(){
    // requestForcaLogica('liberarcilindroenergia')
    audio1.play()
})
// btnTubo.addEventListener('click', function(){
//     // requestForcaLogica('abrirtubo')
//     // audio2.play()
//     PlayNarracao();
// })

// ---- SONS ----

function requestSom() {
    var xhttp = new XMLHttpRequest()
    var url = "ajaxsom"

    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var resposta = JSON.parse(this.responseText)

        // console.log(resposta)

        if (resposta.executarSom1 == true && audio1.paused == true) {
            audio1.play()
            console.log('executando som 1')
        }
        // if (resposta.executarSom2 == true && audio2.paused == true) {
        //     // audio2.play()
        //     // PlayNarracao();
        //     console.log('executando som 2')
        // }

        setTimeout(requestSom, 700)
      }
    }
    xhttp.open("GET", url, true)
    xhttp.send()
}

btnAudio1.addEventListener('click', function() {
    audio1.play()
})

btnAudio2.addEventListener('click', function() {
    // audio2.play()
    PlayNarracao();
})


// ---===MUDAR IDIOMA ===---
btnConfirmarIdioma.addEventListener('click', function(){


    // console.log("Funcao Mudar idioma chamada!")
    if (document.getElementById("IdiomaPortugues").checked){
        document.getElementById("h1-titulo").innerHTML = "Sala Santos Dumont Português"
        document.getElementById("sourceMyAudio2").src = "{% static 'sons/SomCompleto-Portugues.mp3' %}"
    }
    else if(document.getElementById("IdiomaIngles").checked){
        // console.log("Selecionado Ingles")
        document.getElementById("h1-titulo").innerHTML = "Sala Santos Dumont Inglês"
        document.getElementById("sourceMyAudio2").src = "{% static 'sons/SomCompleto-Ingles.mp3' %}"
    }
    else if(document.getElementById("IdiomaEspanhol").checked){
        // console.log("Selecionado Espanhol")
        document.getElementById("h1-titulo").innerHTML = "Sala Santos Dumont Espanhol"
        document.getElementById("sourceMyAudio2").src = "{% static 'sons/SomCompleto-Espanhol.mp3' %}"
    }

});



// function PlayNarracao(){
//     if (document.getElementById("IdiomaPortugues").checked){
//         audio2.play()
//     }
//     if (document.getElementById("IdiomaIngles").checked){
//         audio2_EN.play()
//     }
//     if (document.getElementById("IdiomaEspanhol").checked){
//         audio2_ES.play()
//     }
// }