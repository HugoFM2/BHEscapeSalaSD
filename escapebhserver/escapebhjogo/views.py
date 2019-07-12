from django.shortcuts import render
from django.http import JsonResponse
from escapebhjogo.classes.logica_1 import Logica_1 # Classe com metodos da logica 1
from escapebhjogo.classes.logica_2 import Logica_2 # Classe com metodos da logica 2
from escapebhjogo.classes.logica_3 import Logica_3 # Classe com metodos da logica 3
from escapebhjogo.classes.logica_4 import Logica_4 # Classe com metodos da logica 4
# from escapebhjogo.classes.escapedebug import debug # DEBUG ESCAPE
# from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from . import views # Importa os metodos existentes neste arquivo

# Create your views here.

# View da pagina inicial
def pagina_inicial(request):
    # DICIONARIO PARA ENVIO DE INFORMAÇÕES DO PROGRAMA PARA A PAGINA HTML
    dicionario_para_html = {
        'logica1_status': Logica_1._concluida,
        'logica2_status': Logica_2._concluida,
        'logica3_status': Logica_3._concluida,
        'logica4_status': Logica_4._concluida,
        'logica5_status': False,
        'logica6_status': False,
        'logica7_status': False,
        'logica8_status': False,
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
            pass

        # Checagem dos botoes da logica 6
        if forcar_logica6 != None and forcar_logica6 == 'Forcar Descer Chave':
            pass
        elif forcar_logica5 != None and forcar_logica5 == 'Subir Chave':
            pass

        # Checagem dos botoes da logica 7
        if forcar_logica7 != None and forcar_logica7 == 'Forcar Destravar Gaveta':
            pass

        # Checagem dos botoes da logica 8
        if forcar_logica8 != None and forcar_logica8 == 'Forcar Liberar Brasao':
            pass
    
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
    Logica_1.iniciarThread()
    Logica_2.iniciarThread()
    Logica_3.iniciarThread()
    Logica_4.iniciarThread()
    #Logica_5.iniciarThread()
    #Logica_6.iniciarThread()
    #Logica_7.iniciarThread()
    #Logica_8.iniciarThread()

def reiniciar_jogo(): # EM TESTES
    print('Reiniciando Jogo...')
    # Reinicia as threads das logicas
    Logica_1.reiniciarThread()
    Logica_2.reiniciarThread()
    Logica_3.reiniciarThread()
    Logica_4.reiniciarThread()
    #Logica_5.reiniciarThread()
    #Logica_6.reiniciarThread()
    #Logica_7.reiniciarThread()
    #Logica_8.reiniciarThread()

# ----------- FIM dos METODOS -----