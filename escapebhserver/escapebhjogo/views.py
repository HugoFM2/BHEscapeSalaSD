from django.shortcuts import render
from django.http import JsonResponse
from escapebhjogo.classes.logica_1 import Logica_1 # Classe com metodos da logica 1
from escapebhjogo.classes.logica_2 import Logica_2 # Classe com metodos da logica 2
from escapebhjogo.classes.logica_3 import Logica_3 # Classe com metodos da logica 3
from escapebhjogo.classes.logica_4 import Logica_4 # Classe com metodos da logica 4
from escapebhjogo.classes.logica_5 import Logica_5 # Classe com metodos da logica 5
from escapebhjogo.classes.logica_6 import Logica_6 # Classe com metodos da logica 6
from escapebhjogo.classes.logica_7 import Logica_7 # Classe com metodos da logica 7
from escapebhjogo.classes.logica_8 import Logica_8 # Classe com metodos da logica 8
# from escapebhjogo.classes.escapedebug import debug # DEBUG ESCAPE
from . import views # Importa os metodos existentes neste arquivo
from django.http import HttpResponse
from escapebhjogo.classes.cronometro import Cronometro
from  escapebhjogo.classes import MQTTAlive

# View da pagina inicial
def pagina_inicial(request):
    # DICIONARIO PARA ENVIO DE INFORMAÇÕES DO PROGRAMA PARA A PAGINA HTML
    dicionario_para_html = {
        'logica1_status': Logica_1._concluida,
        'logica2_status': Logica_2._concluida,
        'logica3_status': Logica_3._concluida,
        'logica4_status': Logica_4._concluida,
        'logica5_status': Logica_5._concluida,
        'logica6_status': Logica_6._concluida,
        'logica7_status': Logica_7._concluida,
        'logica8_status': Logica_8._concluida,
    }

    # SE RECEBER UM FORMULARIO POST
    if request.method == 'POST':
        #print(request.POST) # DEBUG
        # Armazena o valor das query recebidas, se não houver armazena None
        acao = request.POST.get('acao')
        forcar_logica1 = request.POST.get('forcar_logica1')
        forcar_logica2 = request.POST.get('forcar_logica2')
        forcar_logica3 = request.POST.get('forcar_logica3')
        forcar_logica4 = request.POST.get('forcar_logica4')
        forcar_logica5 = request.POST.get('forcar_logica5')
        forcar_logica6 = request.POST.get('forcar_logica6')
        forcar_logica7 = request.POST.get('forcar_logica7')
        forcar_logica8 = request.POST.get('forcar_logica8')

        # Checagem dos botoes de Ação
        if acao != None and acao == 'Iniciar Jogo':
            views.iniciar_jogo()

        elif acao != None and acao == 'Reiniciar Jogo':
            views.reiniciar_jogo()

        # Checagem dos botoes da logica 1
        if forcar_logica1 != None and forcar_logica1 == 'Forcar Ligar Laser':
            Logica_1.ligarLaser()
        elif forcar_logica1 != None and forcar_logica1 == 'Forcar Abrir Gaveta':
            Logica_1.abrirGaveta()

        # Checagem dos botoes da logica 2
        if forcar_logica2 != None and forcar_logica2 == 'Forcar Cair Teto':
            Logica_2.cairTeto()

        # Checagem dos botoes da logica 3
        if forcar_logica3 != None and forcar_logica3 == 'Forcar Abrir Alcapao':
            Logica_3.abrirAlcapao()

        # Checagem dos botoes da logica 4
        if forcar_logica4 != None and forcar_logica4 == 'Forcar Giro Busto':
            Logica_4.abrirBusto()
        elif forcar_logica4 != None and forcar_logica4 == 'Forcar Abrir Porta':
            Logica_4.abrirPorta()
        elif forcar_logica4 != None and forcar_logica4 == 'Voltar Busto':
            Logica_4.voltarBusto()

        # Checagem dos botoes da logica 5
        if forcar_logica5 != None and forcar_logica5 == 'Forcar Abrir Bau':
            Logica_5.abrirBau()

        # Checagem dos botoes da logica 6
        if forcar_logica6 != None and forcar_logica6 == 'Forcar Descer Chave':
            Logica_6.descerMotor()
        elif forcar_logica6 != None and forcar_logica6 == 'Subir Chave':
            Logica_6.subirMotor()

        # Checagem dos botoes da logica 7
        if forcar_logica7 != None and forcar_logica7 == 'Forcar Destravar Gaveta':
            Logica_7.abrirGaveta()

        # Checagem dos botoes da logica 8
        if forcar_logica8 != None and forcar_logica8 == 'Forcar Liberar Brasao':
            Logica_8.abrirTuboBrasao()
        elif forcar_logica8 != None and forcar_logica8 == 'Forcar Liberar Lampada':
            Logica_8.abrirCaixa()

    return render(request, 'escapebhhtml/pagina_inicial.html', dicionario_para_html )

# url .../escapedebug
def escape_debug(request): # VIEW DE DEBUG
    #debug.logica_debug()
    debug.cronometro_debug()
    from django.http import HttpResponse
    return HttpResponse('')


# -------- METODOS PARA AUXILIAR A VIEWS -----------
def iniciar_jogo():
    print('Iniciando Jogo...')
    # Inicia as threads das logicas
    Logica_2.iniciarThread()
    Logica_1.iniciarThread()
    Logica_4.iniciarThread()
    Logica_6.iniciarThread()
    Logica_3.iniciarThread()
    Logica_5.iniciarThread()
    Logica_7.iniciarThread()
    Logica_8.iniciarThread()

def reiniciar_jogo():
    import os
    print('Reiniciando Jogo...')
    # Matar o server da porta 8000 e 4 segundos depois inicia um novo server
    os.system('sudo fuser -k 8000/tcp && sleep 4 && . /home/pi/escapebh/escapeiniciar')

def desligarRaspberry():
    # Desliga a raspberry
    import os
    os.system('sudo shutdown -h now')

# ----------- FIM dos METODOS -----

# ----------- AJAX ----------------

def nova_dashboard(request):
    return render(request, 'escapebhhtml/nova_dashboard.html', {})

def ajaxcronometro(request):
    #Cronometro.iniciarCronometro()
    texto = Cronometro.getTempoTotal()
    return HttpResponse(texto)

def ajaxstatus(request):
    dicionario_para_html = {
        'logica1_status': Logica_1._concluida,
        'logica2_status': Logica_2._concluida,
        'logica3_status': Logica_3._concluida,
        'logica4_status': Logica_4._concluida,
        'logica5_status': Logica_5._concluida,
        'logica6_status': Logica_6._concluida,
        'logica7_status': Logica_7._concluida,
        'logica8_status': Logica_8._concluida,
    }
    return JsonResponse(dicionario_para_html)

def ajaxdashboard(request):
    acao = None
    # SE RECEBER UM REQUEST GET
    if request.method == 'GET':
        acao = request.GET.get('acao', None)

        # Checagem dos botoes de Ação
        if acao != None and acao == 'iniciarjogo':
            Cronometro.iniciarCronometro()
            views.iniciar_jogo()
        elif acao != None and acao == 'reiniciarjogo':
            views.reiniciar_jogo()
        elif acao != None and acao == 'desligarraspberry':
            views.desligarRaspberry()

        # Checagem dos botoes da logica 1
        elif acao != None and acao == 'ativarlaser':
            Logica_1.ligarLaser()
        elif acao != None and acao == 'abrirgavetalaser':
            Logica_1.abrirGaveta()

        # Checagem dos botoes da logica 2
        elif acao != None and acao == 'cairalcapao':
            Logica_2.cairTeto()

        # Checagem dos botoes da logica 3
        elif acao != None and acao == 'abrirporao':
            Logica_3.abrirAlcapao()

        # Checagem dos botoes da logica 4
        elif acao != None and acao == 'girarbusto':
            Logica_4.abrirBusto()
        elif acao != None and acao == 'abrirporta':
            Logica_4.abrirPorta()
        elif acao != None and acao == 'voltarbusto':
            Logica_4.voltarBusto()

        # Checagem dos botoes da logica 5
        elif acao != None and acao == 'abrirbau':
            Logica_5.abrirBau()

        # Checagem dos botoes da logica 6
        elif acao != None and acao == 'descerteto':
            Logica_6.descerMotor()
        elif acao != None and acao == 'subirteto':
            Logica_6.subirMotor()

        # Checagem dos botoes da logica 7
        elif acao != None and acao == 'abrirgavetamesa':
            Logica_7.abrirGaveta()

        # Checagem dos botoes da logica 8
        elif acao != None and acao == 'abrirtubo':
            Logica_8.abrirTuboBrasao()
        elif acao != None and acao == 'liberarcilindroenergia':
            Logica_8.abrirCaixa()

    texto = acao
    return HttpResponse(texto)

# Essa rotina sicroniza o executar do som na sala
def ajaxsom(request):
    sinaisSom = {
        'executarSom1': Logica_8.executarSom1,
        'executarSom2': Logica_8.executarSom2,
    }
    return JsonResponse(sinaisSom)

# ---=== SONS REMOTOS ===---

def nova_dashboard_Sons(request):
    return render(request, 'escapebhhtml/nova_dashboard_Sons.html', {})

def ajaxsomVirtual(request):
    sinaisSom = {
        'executarSom1': Logica_8.executarSom1,
        'executarSom2': Logica_8.executarSom2,
        'executarSomLogica1' : Logica_2.executarSomLogica1,
        'executarSomLogica2' : Logica_1.executarSomLogica2,
        'executarSomLogica3_1' : Logica_4.executarSomLogica3_1,
        'executarSomLogica3_2' : Logica_4.executarSomLogica3_2,
        'executarSomLogica4' : Logica_6.executarSomLogica4,
        'executarSomLogica5' : Logica_3.executarSomLogica5,
        'executarSomLogica6' : Logica_5.executarSomLogica6,
        'executarSomLogica7' : Logica_7.executarSomLogica7,
    }
    return JsonResponse(sinaisSom)

# ---=== FIM SONS REMOTOS ===---


# ---=== AUTOMACOES MQTT ===---

def pings(request):
    # return HttpResponse(MQTTAlive.Logica1.ConnectStatus())
    # return JsonResponse(MQTTAlive.Logica1.ConnectStatus(),safe=False)
    return JsonResponse(MQTTAlive.JSONConnStatus(),safe=False)
    # return JsonResponse(ping.IsUp(),safe=False)
    # return HttpResponse(ping.IsUp())

def status(request):
    return JsonResponse(MQTTAlive.JSONConcluidoStatus(),safe=False)

def send(request, msg=None,topic=None):
    msg = request.GET.get('msg')
    topic = request.GET.get('topic')
    MQTTAlive.Logica1.mqtt_publish(topic,msg)
    return HttpResponse(msg)

def reset(request):
    MQTTAlive.ResetALLMQTT()
    return HttpResponse("Dispositivos MQTT Resetados")


def descricao(request):
    return JsonResponse(MQTTAlive.Logica1.Descricao(),safe=False)
