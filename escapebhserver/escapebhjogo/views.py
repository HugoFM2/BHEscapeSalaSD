from django.shortcuts import render
from django.http import JsonResponse
from escapebhjogo.classes.logica_1 import Logica_1 # Classe com metodos da logica 1
from escapebhjogo.classes.logica_2 import Logica_2 # Classe com metodos da logica 2
from escapebhjogo.classes.logica_3 import Logica_3 # Classe com metodos da logica 3
from escapebhjogo.classes.logica_4 import Logica_4 # Classe com metodos da logica 4
from escapebhjogo.classes.escapedebug import debug # DEBUG ESCAPE
from escapebhjogo.classes.mcp23017 import MCP23017 as mcp # Classe para trabalhar com o MCP23017, referenciada como mcp
from . import views # Importa os metodos existentes neste arquivo

# Create your views here.

# View da pagina inicial
def pagina_inicial(request):
    # DICIONARIO PARA ENVIO DE INFORMAÇÕES DO PROGRAMA PARA A PAGINA HTML
    dicionario_para_html = {
        'logica1_duracao': views.conversaoDuracao(Logica_1.getDuracaoLogica()),
        'logica2_duracao': views.conversaoDuracao(Logica_2.getDuracaoLogica()),
        'logica3_duracao': views.conversaoDuracao(Logica_3.getDuracaoLogica()),
        'logica4_duracao': views.conversaoDuracao(Logica_4.getDuracaoLogica()),
        'logica1_status': Logica_1.concluida,
        'logica2_status': Logica_2.concluida,
        'logica3_status': Logica_3.concluida,
        'logica4_status': Logica_4.concluida,
    }

    # SE RECEBER UM FORMULARIO POST
    if request.method == 'POST':
        #print(request.POST) # DEBUG
        acao = request.POST.get('acao')
        forcar_logica1 = request.POST.get('forcar_logica1')
        forcar_logica2 = request.POST.get('forcar_logica2')
        forcar_logica3 = request.POST.get('forcar_logica3')
        forcar_logica4 = request.POST.get('forcar_logica4')

        if acao != None and acao == 'Iniciar Jogo':
            views.iniciar_jogo()
        elif acao != None and acao == 'Reiniciar Jogo':
            views.reiniciar_jogo() # EM TESTES AINDA

        if forcar_logica1 != None and forcar_logica1 == 'Forcar Abrir Gaveta':
            Logica_1.forcarAbrirGaveta()

        if forcar_logica2 != None and forcar_logica2 == 'Forcar Abrir Maleta':
            Logica_2.forcarAbrirMaleta()

        if forcar_logica3 != None and forcar_logica3 == 'Forcar Descer Aviao':
            Logica_3.forcarDescerAviao()
        elif forcar_logica3 != None and forcar_logica3 == 'Forcar Subir Aviao':
            Logica_3.forcarSubirAviao()

        if forcar_logica4 != None and forcar_logica4 == 'Forcar Descer Teto':
            Logica_4.forcarAbrirTeto()
    
    return render(request, 'escapebhhtml/pagina_inicial.html', dicionario_para_html )

# url .../escapedebug 
def escape_debug(request): # VIEW DE DEBUG
    #debug.logica_debug()
    debug.cronometro_debug()
    from django.http import HttpResponse
    return HttpResponse('')


# -------- METODOS PARA AUXILIAR A VIEWS -----------
def iniciar_jogo():
    print('Iniciando Jogo...') # imprime uma mensagem no terminal
    mcp.confRegistradoresComZero() # Escrevendo 0x00 nos registradores dos extensores de portas
    # Inicia as verificações dos sensores
    Logica_1.iniciarThread()
    Logica_2.iniciarThread()
    Logica_3.iniciarThread()
    Logica_4.iniciarThread()

def reiniciar_jogo(): # IMPLEMENTAR
    print('Reiniciando Jogo...') # imprime uma mensagem no terminal
    mcp.confRegistradoresComZero() # Escrevendo 0x00 nos registradores dos extensores de portas
    # Reinicia as verificações dos sensores
    Logica_1.reiniciarThread()
    Logica_2.reiniciarThread()
    Logica_3.reiniciarThread()
    Logica_4.reiniciarThread()

def conversaoDuracao(duracao_segundos): # Este metodo converte os segundos passados pela logica em uma string HH:MM:SS
    horas = duracao_segundos // 3600 # Retorna somente a parte inteira
    minutos = (duracao_segundos % 3600) // 60
    segundos = (duracao_segundos % 3600) % 60
    # Defini como sera montada a string de duracao
    if horas < 10 and minutos < 10 and segundos < 10:
        texto = '0{}:0{}:0{}'.format(round(horas), round(minutos), round(segundos) )
    elif horas < 10 and minutos < 10:
        texto = '0{}:0{}:{}'.format(round(horas), round(minutos), round(segundos) )
    elif horas < 10:
        texto = '0{}:{}:{}'.format(round(horas), round(minutos), round(segundos) )
    else:
        texto = '{}:{}:{}'.format(round(horas), round(minutos), round(segundos) )
    return texto
# ----------- FIM dos METODOS -----