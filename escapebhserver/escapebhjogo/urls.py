from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('iniciarjogo', views.iniciar_jogo, name='iniciar_jogo'),
    path('escapedebug', views.escape_debug, name='escape_debug'),
]