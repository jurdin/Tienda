from django.conf.urls import url
from .views import *

Usuarios=[
    url(r'^contactar/$', contactar),
    url(r'^login-register/$', loginUsuario),
    url(r'^close-sesion/$', cerrar_sesion),
    url(r'^login-register/register/$', registrar_usuario),
]