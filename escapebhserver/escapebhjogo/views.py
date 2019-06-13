from django.shortcuts import render
from django.http import JsonResponse
from escapebhjogo.classes.logica_1 import Logica_1 # Classe com metodos da logica 1
from escapebhjogo.classes.logica_2 import Logica_2 # Classe com metodos da logica 2
from escapebhjogo.classes.logica_3 import Logica_3 # Classe com metodos da logica 3
from escapebhjogo.classes.logica_4 import Logica_4 # Classe com metodos da logica 4
from escapebhjogo.classes.escapedebug import debug # DEBUG ESCAPE 

# Create your views here.

# Metodo da pagina inicial - Antigo
def pagina_inicial(request):
    return render(request, 'escapebhhtml/pagina_inicial.html', {} )

def pagina_inicial_OLD(request):
    # Dicionario de valores que serao passados para a pagina HTML
    dicionario = {
        'logica1_sensor_1': None,
        'logica1_sensor_2': None,
        'logica1_sensor_3': None,
        'logica2_sensor_1': None,
        'logica2_sensor_2': None,
        'logica2_sensor_3': None,
        'logica2_sensor_4': None,
        'logica3_sensor_1': None,
        'logica3_sensor_2': None,
        'logica3_sensor_3': None,
        'logica4_sensor_1': None,
        'logica4_sensor_2': None,
        'logica4_sensor_3': None,
        'logica4_sensor_4': None,
    }

     # Se receber um formulario
    if request.method == "POST":
        leituraPostTrava = request.POST.get("trava", "")
        leituraPostMala = request.POST.get("mala", "")
        leituraPostMotor = request.POST.get("motor", "")
        leituraPostFechadura = request.POST.get("fechadura", "")

        if leituraPostTrava == "True":
            print('--> Trava Forcada a abrir')
            Logica_1().forcarAbrirTrava()
        if leituraPostMala == "True":
            print('--> Mala Forcada a abrir')
            Logica_2().forcarAbrirMala()
        if leituraPostMotor == "True":
            print('--> Motor Forcado a acionar')
            Logica_3().forcarAcionarMotor()
        if leituraPostFechadura == "True":
            print('--> Fechaduras Forcadas a abrir')
            Logica_4().forcarAbrirFechaduras()

        return render(request, 'escapebhhtml/pagina_inicial.html', dicionario)

    # Caso seja uma requisicao comum
    else:
        # Recebe as leituras do sensores
        leituraLogica_1 = Logica_1.getStatusSensores()
        leituraLogica_2 = Logica_2().getStatusSensores()
        leituraLogica_3 = Logica_3().getStatusSensores()
        leituraLogica_4 = Logica_4().getStatusSensores()
        
        # Se ha leituras, armazena em uma chave do dicionario
        if len(leituraLogica_1) > 0:
            dicionario['logica1_sensor_1'] = leituraLogica_1[0]
            dicionario['logica1_sensor_2'] = leituraLogica_1[1]
            dicionario['logica1_sensor_3'] = leituraLogica_1[2]

        if len(leituraLogica_2) > 0:
            dicionario['logica2_sensor_1'] = leituraLogica_2[0]
            dicionario['logica2_sensor_2'] = leituraLogica_2[1]
            dicionario['logica2_sensor_3'] = leituraLogica_2[2]
            dicionario['logica2_sensor_4'] = leituraLogica_2[3]

        if len(leituraLogica_3) > 0:
            dicionario['logica3_sensor_1'] = leituraLogica_3[0]
            dicionario['logica3_sensor_2'] = leituraLogica_3[1]
            dicionario['logica3_sensor_3'] = leituraLogica_3[2]

        if len(leituraLogica_4) > 0:
            dicionario['logica4_sensor_1'] = leituraLogica_4[0]
            dicionario['logica4_sensor_2'] = leituraLogica_4[1]
            dicionario['logica4_sensor_3'] = leituraLogica_4[2]
            dicionario['logica4_sensor_4'] = leituraLogica_4[3]

        return render(request, 'escapebhhtml/pagina_inicial.html', dicionario )

def iniciar_jogo(request):
    print('Iniciando Jogo...') # imprime uma mensagem no terminal
    # Inicia as verificações dos sensores
    Logica_1.iniciarThread()
    Logica_2.iniciarThread()
    Logica_3.iniciarThread()
    Logica_4.iniciarThread()
    return render(request, 'escapebhhtml/iniciar_jogo.html',{})

# url .../escapedebug 
def escape_debug(request): # VIEW DE DEBUG
    debug.mcp23017debug()
    #from django.http import HttpResponse
    #return HttpResponse('')
    return render(request, 'escapebhhtml/escape_debug.html',{})