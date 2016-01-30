from Productos.models import Producto, Img_Producto, DetallePedido
from django import template

register = template.Library()

@register.filter(name='imagen')
def imagen(text, arg):
    p=""
    try:
        for i in Img_Producto.objects.filter(producto__id=int(arg)):
            p=i
        return p.imagen
    except:
        return ""

@register.filter(name='pedido')
def cantidad(text,arg):
    try:
        print("todo bien "+str(arg))
        return len(DetallePedido.objects.filter(pedido__id=arg))
    except Exception as error:
        print("todo bien "+ error)
        return 0


