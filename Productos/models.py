from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre=models.CharField(max_length=50)
    estado=models.BooleanField(default=True)

    def __str__(self):
        return "%s"%(self.nombre)

class Marca(models.Model):
    nombre=models.CharField(max_length=50)
    estado=models.BooleanField(default=True)

    def __str__(self):
        return "%s"%(self.nombre)


class Producto(models.Model):
    categoria=models.ForeignKey(Categoria)
    nombre=models.TextField()
    descripcion=models.TextField()
    caracteristicas=models.TextField(default="")
    marca=models.ForeignKey(Marca)
    stock=models.IntegerField()
    precioant=models.DecimalField(max_digits=15,decimal_places=2, default=0.00)
    precio=models.DecimalField(max_digits=15,decimal_places=2, default=0.00)
    tamanio=models.CharField(max_length=60, default="Sin Descripción")
    color=models.CharField(max_length=40, default="Sin Especificar")
    estado=models.BooleanField(default=True)
    es_nuevo=models.BooleanField(default=True)

    def __str__(self):
        return "%s"%(self.nombre)


class Img_Producto(models.Model):
    imagen=models.FileField(upload_to="Productos/")
    producto=models.ForeignKey(Producto)


class Pedido(models.Model):
    fecha=models.DateField(auto_now=True)
    usuario=models.ForeignKey(User)
    subtotal=models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    iva=models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_pedido=models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    procesado=models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s - %s"%(self.fecha, self.usuario,self.procesado)


class DetallePedido(models.Model):
    pedido=models.ForeignKey(Pedido)
    producto=models.ForeignKey(Producto)
    cantidad=models.IntegerField(default=1)
    subtotal=models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    iva=models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total=models.DecimalField(max_digits=12, decimal_places=2, default=0.00)