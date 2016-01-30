from django.conf.urls import url
from .views import *

Productos=[
    url(r'^ver_mas/(\d+)/$', mas_producto),
    url(r'^segun-cat/(\d+)/$', filtro_categorias),
    url(r'^al-carrito/$', alcarrito),
    url(r'^al-carrito/eliminar/(\d+)/$', eliminar_del_carrito),
    url(r'^al-carrito/add/(\d+)/$', add_carrito),
]