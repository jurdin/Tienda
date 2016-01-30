from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from Productos.models import Producto, Pedido, DetallePedido


def paginar_productos(request):
    p=Producto.objects.all().order_by("id").reverse()
    paginator=Paginator(p,12)
    try:
        pagina=int(request.GET.get("page","1"))
    except ValueError:
        pagina=1
    try:
        p=paginator.page(pagina)
    except(InvalidPage, EmptyPage):
        p=paginator.page(paginator.num_pages)
    return p

def index(request):
    usuario=request.user
    pedido=None
    try:
        productos=paginar_productos(request)
        pedido=Pedido.objects.get(procesado=False,usuario=usuario)
        items=DetallePedido.objects.filter(pedido=pedido)
        print(usuario)
        return render_to_response("shop-full-width.html",{"productos":productos,"items":items,"usuario":usuario,"pedido":pedido})
    except:
        if not usuario.is_anonymous():
            return  render_to_response("shop-full-width.html",{"productos":productos,"usuario":usuario})
        else:
            return  render_to_response("shop-full-width.html",{"productos":productos,"pedido":pedido})


def contactar(request):
    if request.user.is_anonymous():
        return render_to_response("contact-us.html")
    else:
        pedido=Pedido.objects.get(procesado=False,usuario=request.user)
        items=DetallePedido.objects.filter(pedido=pedido)
        return render_to_response("contact-us.html",{"usuario":request.user,"pedido":pedido,"items":items})


def loginUsuario(request):
    if not request.user.is_authenticated() and request.POST:
        user = auth.authenticate(username=request.POST['usuario'], password=request.POST['password'])
        if user is not None and user.is_active:
            auth.login(request, user)
            print (user)
            return render_to_response("login-register.html",{"usuario":user})
        else:
            print(request.user)
            return render_to_response("login-register.html",{"usuario":request.user})
    else:
        return render_to_response("login-register.html")


def registrar_usuario(request):
    print("entro a registrar")
    if request.POST:
        usuario=User.objects.create_user(username=request.POST['usuario'],email=request.POST['email'],password=request.POST['password'])
        usuario.is_staff=True
        usuario.first_name=request.POST['nombres']
        usuario.last_name=request.POST['apellidos']
        usuario.save()
        return render_to_response("login-register.html")


def cerrar_sesion(request):
    auth.logout(request)
    return HttpResponseRedirect("/")