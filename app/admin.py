from django.contrib import admin
from .models import *

class productoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio")
    list_filter = ("tipo",)

class etiquetaAdmin(admin.ModelAdmin):
    ordering = ["tag"]

class comentarioAdmin(admin.ModelAdmin):
    list_display = ("autor", "producto")

admin.site.register(Etiqueta, etiquetaAdmin)
admin.site.register(Producto, productoAdmin)
admin.site.register(Avatar)
admin.site.register(Comentario, comentarioAdmin)

# Register your models here.
