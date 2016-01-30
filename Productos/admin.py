from django.contrib import admin

# Register your models here.
from .models import *

class ProductoAdmin(admin.ModelAdmin):
    list_display = ("categoria","nombre","descripcion","caracteristicas","marca","stock","precio","tamanio","color","estado","es_nuevo",)
    list_display_links = ("categoria","nombre","descripcion","caracteristicas","marca","stock","precio","tamanio","color","estado","es_nuevo",)

admin.site.register(Producto,ProductoAdmin)

class ImgProductoAdmin(admin.ModelAdmin):
    list_display = ("imagen","producto",)
    list_display_links = ("imagen","producto",)


admin.site.register(Img_Producto, ImgProductoAdmin)
admin.site.register(Categoria)
admin.site.register(Marca)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ("fecha","usuario","subtotal","iva","total_pedido",)
    list_display_links = ("fecha","usuario","subtotal","iva","total_pedido",)

admin.site.register(Pedido,PedidoAdmin)

class DetallePedidioAdmin(admin.ModelAdmin):
    list_display = ("pedido","producto","cantidad","subtotal","iva","total",)
    list_display_links = ("pedido","producto","cantidad","subtotal","iva","total",)

admin.site.register(DetallePedido,DetallePedidioAdmin)
