from django.urls import path
from . import views

urlpatterns = [
    path('dashboard2', views.pagina_inicial, name='pagina_inicial'),
    path('escapedebug', views.escape_debug, name='escape_debug'),
    path('', views.nova_dashboard, name='nova_dashboard'),
    path('ajaxdashboard', views.ajaxdashboard, name='ajaxdashboard'),
    path('ajaxcronometro', views.ajaxcronometro, name='ajaxcronometro'),
    path('ajaxstatus', views.ajaxstatus, name='ajaxstatus'),
    path('ajaxsom', views.ajaxsom, name='ajaxsom'),
]