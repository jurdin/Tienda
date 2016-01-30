import decimal
import random
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from Productos.admin import DetallePedidioAdmin
from Productos.models import Producto, Img_Producto, Categoria, Pedido, DetallePedido


def paginar_productos(request,n):
    p=Producto.objects.filter(categoria__id=n).order_by("id").reverse()
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

def filtro_categorias(request,n):
    usuario=request.user
    productos=paginar_productos(request,n)
    items=None
    try:
        pedido=Pedido.objects.get(procesado=False,usuario=usuario)
        items=DetallePedido.objects.filter(pedido=pedido)
        return render_to_response("shop-full-width.html",{"productos":productos,"items":items,"usuario":usuario})
    except:
        if usuario.is_anonymous():
            return render_to_response("shop-full-width.html",{"productos":productos})
        else:
            return render_to_response("shop-full-width.html",{"productos":productos,"items":items,"usuario":usuario})

def mas_producto(request,n):
    usuario=request.user
    categorias=Categoria.objects.all()
    producto=Producto.objects.get(id=n)
    imagenes=Img_Producto.objects.filter(producto=producto)
    prod_cat=Producto.objects.filter(categoria__id=producto.categoria.id)
    numeros=[]
    producto_footer=[]
    items=None
    for i in range(4):
        numero=random.randrange(len(Producto.objects.all()))
        if not numero in numeros:
            numeros.append(numero)
    todos=[p for p in Producto.objects.all()]
    print(todos)
    for j in numeros:
        producto_footer.append({"producto":todos[j]})

    try:
        pedido=Pedido.objects.get(procesado=False,usuario=usuario)
        items=DetallePedido.objects.filter(pedido=pedido)
        return render_to_response("shop-product-sidebar.html",{"pedido":pedido,"items":items,"producto":producto,"imagenes":imagenes,"categorias":categorias,"productos":prod_cat,"producto_footer":producto_footer,"usuario":usuario})
    except:
        if usuario.is_anonymous():
            print ("es anonimo")
            return render_to_response("shop-product-sidebar.html",{"producto":producto,"imagenes":imagenes,"categorias":categorias,"productos":prod_cat,"producto_footer":producto_footer})
        else:
            print("tiene login")
            return render_to_response("shop-product-sidebar.html",{"pedido":pedido,"items":items,"producto":producto,"imagenes":imagenes,"categorias":categorias,"productos":prod_cat,"producto_footer":producto_footer,"usuario":usuario})

def alcarrito(request):
    if not request.user.is_anonymous():
        pedido=None
        items=None
        pedidos=None
        usuario=request.user
        try:
            pedidos=Pedido.objects.filter(usuario=usuario).order_by("id").reverse()
            pedido=Pedido.objects.get(procesado=False,usuario=usuario)
            items=DetallePedido.objects.filter(pedido=pedido)
            return render_to_response("shop-cart.html",{"pedidos":pedidos,"pedido":pedido,"items":items,"usuario":usuario})
        except:
            return render_to_response("shop-cart.html",{"pedidos":pedidos,"pedido":pedido,"items":items,"usuario":usuario})
    else:
        return HttpResponse("/Usuario/login-register/")


def eliminar_del_carrito(request,id):
    usuario=request.user
    pedido=Pedido.objects.get(procesado=False,usuario=usuario)
    actualizarPrecio(pedido, id)
    return HttpResponseRedirect("/Productos/al-carrito/")

def actualizarPrecio(pedido,id):
    subtotal=0
    iva=0
    total=0
    detalle=DetallePedido.objects.get(id=id)
    ''' detalle '''
    subtotal+=detalle.subtotal
    iva+=detalle.iva
    total+=detalle.total
    ''' pedido '''
    try:
        pedido.subtotal-=decimal.Decimal(subtotal)
        pedido.iva-=decimal.Decimal(iva)
        pedido.total_pedido-=decimal.Decimal(total)
        detalle.delete()
        pedido.save()
        print(subtotal,iva,total, pedido.total_pedido)
    except Exception as error:
        print(error)


def add_carrito(request,n):
    if request.POST and not request.user.is_anonymous():
        usuario=request.user
        producto=Producto.objects.get(id=n)
        pedido=None
        try:
            pedido=Pedido.objects.get(usuario=usuario,procesado=False)
            print("ya existe")
        except:
            pedido=Pedido(usuario=usuario,procesado=False,subtotal=0,iva=0, total_pedido=0).save()
            print("se creo un nuevo pedido")
        try:
            print("intentando crear el articulo")
            pedido=Pedido.objects.get(usuario=usuario,procesado=False)
            print("encontro el pedido")
            detalle=DetallePedido.objects.get(producto=producto)
            print("encontro el detalle")
            cantidad=int(request.POST['cantidad'])
            precio=(producto.precio)/decimal.Decimal(1.12)
            subtotal=precio*decimal.Decimal(cantidad)
            iva=subtotal*decimal.Decimal(0.12)
            total=subtotal+iva
            print("modificando el detalle")
            detalle.cantidad+=cantidad
            detalle.subtotal+=subtotal
            detalle.iva=+iva
            detalle.total+=total
            detalle.save()
            print("calculos")
            pedido.subtotal+=subtotal
            pedido.iva+=iva
            pedido.total_pedido+=total
            print("guardando el pedido")
            pedido.save()
            return HttpResponse("Se guardo, en existente")
        except Exception as error:
            print("no encontro el detalle")
            pedido=Pedido.objects.get(usuario=usuario,procesado=False)
            cantidad=int(request.POST['cantidad'])
            precio=decimal.Decimal(producto.precio)/decimal.Decimal(1.12)
            subtotal=precio*decimal.Decimal(cantidad)
            iva=subtotal*decimal.Decimal(0.12)
            total=subtotal+iva
            print("guardando detalle")
            DetallePedido(pedido=pedido,producto=producto,cantidad=cantidad,subtotal=subtotal,iva=iva,total=total).save()
            print("calculando pedido")
            pedido.subtotal+=subtotal
            pedido.iva+=iva
            pedido.total_pedido+=total
            pedido.save()
            print("guardo el pedido")
            return HttpResponse("Se guardo, nuevo")
    else:
        return HttpResponse("render")