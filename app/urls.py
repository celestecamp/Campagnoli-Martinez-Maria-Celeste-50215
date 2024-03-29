from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name="home"),

    #____Login/Logout/Register
    path('login/', login_request, name="login"),
    path('logout/', LogoutView.as_view(template_name="app/logout.html"), name="logout"),
    path('registrar/', register_request, name="registrar"),

    #____Views
    path('producto/<int:producto_id>/', detalle_producto, name='detalle_producto'),
    path('comentar/<int:producto_id>/', comentar, name='comentar'),

    path('editar-comentario/<int:comentario_id>/<int:producto_id>/', editar_comentario, name='editar_comentario'),
    path('borrar-comentario/<int:comentario_id>/<int:producto_id>/', borrar_comentario, name='borrar_comentario'),

    path('realizar-compra/<int:producto_id>/', compra, name="compra_realizar"),
    path('finalizar-compra/', compra_fin, name='compra_fin'),

    path('lista-productos/', productos_todos, name="lista_productos"),
    path('lista-productos/<str:tipo>/', productos_filtrados_tipo, name="productos_filtrados_tipo"),
    path('productos/etiqueta/<etiqueta_tag>/', productos_filtrados_etiqueta, name='productos_filtrados_etiqueta'),
    path('lista-productos/busqueda', buscar, name="buscar"),

    path('lista-<str:tipo>/', productos_por_categoria, name="categoria"),

    #_____CRUDs
    path('nuevo-producto/', nuevo_producto, name="nuevo_producto"),
    path('editar-producto/<id_producto>/', editar_producto, name="editar_producto"),
    path('borrar-producto/<id_producto>/', borrar_producto, name="borrar_producto"),
    
    path('nueva-etiqueta/', nueva_etiqueta, name="nueva_etiqueta"),
    path('editar-etiqueta/<id_etiqueta>/', editar_etiqueta, name="editar_etiqueta"),
    path('borrar-etiqueta/<id_etiqueta>/', borrar_etiqueta, name="borrar_etiqueta"),

    #_____Perfil/Avatar
    path('editar-perfil/', EditProfileView, name="editar_perfil"),
    path('<int:pk>/password/', ChangePasswordView.as_view(), name="cambiar_clave"),
    path('agregar-avatar/', agregarAvatar, name="agregar_avatar"),

    #____Otras Opciones del Menú
    path('preguntas/', faqs, name="faqs"),
    path('acerca-de/', acerca_de, name="acerca_de"),
]

